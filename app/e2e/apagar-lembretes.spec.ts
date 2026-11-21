import { expect, test, type Page } from '@playwright/test';
import { abrirAjustes, apagarTudoPelosAjustes } from './ajustes-ajuda';

// #25: o botão "Apagar tudo" também cancela os lembretes já agendados no aparelho (podem mostrar o nome
// da criança na tela bloqueada). Simulamos o aplicativo de celular com um Capacitor falso que registra as
// chamadas; no navegador comum a ponte não existe e nada disso roda.
async function prepararPonte(page: Page, cancelaFalha: boolean) {
  await page.addInitScript((falha: boolean) => {
    const chamadas: { metodo: string; args: unknown }[] = [];
    const w = window as unknown as Record<string, unknown>;
    w.__chamadas = chamadas;
    const registra = (metodo: string, retorno: unknown) => async (args?: unknown) => {
      chamadas.push({ metodo, args });
      return retorno;
    };
    w.Capacitor = {
      isNativePlatform: () => true,
      Plugins: {
        LocalNotifications: {
          checkPermissions: registra('checkPermissions', { display: 'granted' }),
          requestPermissions: registra('requestPermissions', { display: 'granted' }),
          getPending: registra('getPending', { notifications: [{ id: 11 }, { id: 12 }] }),
          cancel: async (args?: unknown) => {
            chamadas.push({ metodo: 'cancel', args });
            if (falha) throw new Error('plugin quebrou');
          },
          schedule: registra('schedule', {}),
        },
      },
    };
  }, cancelaFalha);
  page.on('dialog', (d) => void d.accept());
}

async function abrirConfigComExemplo(page: Page) {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await abrirAjustes(page);
  await expect(
    page.getByRole('button', { name: 'Apagar todos os dados deste aparelho' }),
  ).toBeVisible();
}

test('Apagar tudo limpa o banco, cancela os lembretes pendentes e não agenda nenhum', async ({
  page,
}) => {
  await prepararPonte(page, false);
  await abrirConfigComExemplo(page);

  // Só interessa o que acontece depois do clique (a abertura do app também sincroniza).
  await page.evaluate(() => ((window as never as { __chamadas: unknown[] }).__chamadas.length = 0));
  await apagarTudoPelosAjustes(page);

  // (d) volta às boas-vindas
  await expect(page.getByRole('heading', { name: 'Como funciona' })).toBeVisible();

  // (a) banco vazio, loja por loja
  const contagens = await page.evaluate(
    () =>
      new Promise<number[]>((resolve, reject) => {
        const abrir = indexedDB.open('semear');
        abrir.onerror = () => reject(abrir.error);
        abrir.onsuccess = () => {
          const db = abrir.result;
          const lojas = [...db.objectStoreNames];
          const tx = db.transaction(lojas, 'readonly');
          const contar = lojas.map(
            (l) =>
              new Promise<number>((ok) => {
                const c = tx.objectStore(l).count();
                c.onsuccess = () => ok(c.result);
              }),
          );
          void Promise.all(contar).then((n) => {
            db.close();
            resolve(n);
          });
        };
      }),
  );
  expect(contagens.length).toBeGreaterThan(0);
  expect(contagens.every((n) => n === 0)).toBe(true);

  // (b) cancel com os ids pendentes e (c) schedule nunca chamado
  const chamadas = await page.evaluate(
    () => (window as never as { __chamadas: { metodo: string; args: unknown }[] }).__chamadas,
  );
  const cancelamentos = chamadas.filter((c) => c.metodo === 'cancel');
  expect(cancelamentos.length).toBeGreaterThan(0);
  expect(cancelamentos[0]?.args).toEqual({ notifications: [{ id: 11 }, { id: 12 }] });
  expect(chamadas.some((c) => c.metodo === 'schedule')).toBe(false);
  // deu certo: nenhum aviso de falha
  await expect(page.locator('#aviso')).toBeHidden();
});

test('se o cancelamento falhar, o banco é apagado e a pessoa é avisada', async ({ page }) => {
  await prepararPonte(page, true);
  await abrirConfigComExemplo(page);
  await apagarTudoPelosAjustes(page);

  await expect(page.getByRole('heading', { name: 'Como funciona' })).toBeVisible();
  await expect(page.locator('#aviso')).toContainText(
    'Os dados foram apagados, mas não consegui cancelar os lembretes deste aparelho.',
  );
  await expect(page.locator('#aviso')).toContainText('Desligue o lembrete diário');
  // o banco foi limpo mesmo assim: a boas-vindas sem família é a prova
  await expect(
    page.getByRole('button', { name: 'Explorar com uma família de exemplo' }),
  ).toBeVisible();
});
