import { expect, test, type Page } from '@playwright/test';
import { readFile } from 'node:fs/promises';
import { abrirAjustes, apagarTudoPelosAjustes, confirmarTrazerCopia } from './ajustes-ajuda';

// Tela de Ajustes (antes "Configurações"): seis grupos, cópia de segurança acessível, caixa própria
// para as ações sem volta e nada de alert()/confirm() do navegador.

async function comExemplo(page: Page) {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await abrirAjustes(page);
}

/** Junta as mensagens de alert/confirm/prompt nativos; o teste confere no fim que não houve nenhuma. */
function vigiarDialogosNativos(page: Page): string[] {
  const mensagens: string[] = [];
  page.on('dialog', (d) => {
    mensagens.push(d.message());
    void d.dismiss();
  });
  return mensagens;
}

const semRolagemHorizontal = (page: Page) =>
  page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth);

test('a tela tem o nome Ajustes, a rota antiga continua e os seis grupos vêm na ordem', async ({
  page,
}) => {
  await page.goto('./#/config');
  await expect(page.getByRole('heading', { name: 'Ajustes', level: 1 })).toBeVisible();
  await expect(page.getByRole('navigation', { name: 'Principal' })).toContainText('Ajustes');
  await expect(page.getByText('Seus dados, avisos e cópias de segurança.')).toContainText(
    'Tudo fica neste aparelho.',
  );
  await expect(page.locator('main h2')).toHaveText([
    'Família',
    'Aviso diário',
    'Cópia de segurança',
    'Material de apoio',
    'Sobre o Semear',
    'Cuidado',
  ]);
  // Sem família: o grupo diz o que fazer em vez de sumir.
  await expect(page.getByRole('link', { name: 'Cadastrar a família' })).toBeVisible();
  await expect(page.getByText('Cadastre a família para escolher o aviso diário.')).toBeVisible();
  // Sem exemplo, não há "Apagar o exemplo".
  await expect(page.getByRole('button', { name: 'Apagar o exemplo' })).toHaveCount(0);
});

test('com a família de exemplo: resumo da família, links de apoio e Cuidado por último', async ({
  page,
}) => {
  await comExemplo(page);
  await expect(page.getByText('Família Marina · 2 crianças')).toBeVisible();
  await expect(page.getByRole('link', { name: 'Dados da família e das crianças' })).toHaveAttribute(
    'href',
    '#/familia',
  );
  const sobre = page.locator('#sobre');
  for (const nome of ['Novidades', 'Privacidade', 'Termos de uso', 'Cobertura do conteúdo'])
    await expect(sobre.getByRole('link', { name: nome })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Biblioteca' }).first()).toBeVisible();
  await expect(page.getByRole('link', { name: 'Acervo gratuito' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Apagar o exemplo' })).toBeVisible();
  // O texto longo da cópia mora num bloco recolhido.
  const detalhe = page.locator('details', { hasText: 'O que tem na cópia?' });
  await expect(detalhe).not.toHaveAttribute('open', '');
  await detalhe.getByText('O que tem na cópia?').click();
  await expect(detalhe).toContainText('não é protegido por senha');
  // O grupo Cuidado é o último e explica a diferença entre os dois apagares.
  const cuidado = page.locator('section', { has: page.getByRole('heading', { name: 'Cuidado' }) });
  await expect(cuidado).toContainText('remove só a família de exemplo');
  await expect(cuidado).toContainText('inclusive o que você cadastrou');
  const ultimoGrupo = page.locator('main section.cartao').last();
  await expect(ultimoGrupo.getByRole('heading', { name: 'Cuidado' })).toBeVisible();
});

test('Aviso diário: a nota do aplicativo vem antes do formulário e a hora é de 24 h', async ({
  page,
}) => {
  await comExemplo(page);
  const nota = page.getByText('Os avisos só funcionam no aplicativo de celular');
  const form = page.locator('#form-lembrete');
  const yNota = (await nota.boundingBox())!.y;
  const yForm = (await form.boundingBox())!.y;
  expect(yNota).toBeLessThan(yForm);
  await expect(page.locator('#form-lembrete input[type="time"]')).toHaveCount(0);
  // O botão não ocupa a largura toda no desktop.
  const botao = page.getByRole('button', { name: 'Salvar aviso' });
  const larguraBotao = (await botao.boundingBox())!.width;
  const larguraForm = (await form.boundingBox())!.width;
  if ((page.viewportSize()?.width ?? 0) >= 900) expect(larguraBotao).toBeLessThan(larguraForm / 2);

  // Hora inválida: erro dentro do formulário, nada é salvo.
  await page.getByLabel('Hora', { exact: true }).fill('25');
  await page.getByLabel('Minutos').fill('00');
  await botao.click();
  await expect(page.locator('#erro-hora')).toContainText('hora de 0 a 23');
  await page.getByLabel('Hora', { exact: true }).fill('19');
  await page.getByLabel('Minutos').fill('05');
  await botao.click();
  await expect(page.locator('#erro-hora')).toBeHidden();
  await expect(page.getByText('Aviso salvo.')).toBeVisible();
  await page.reload();
  await expect(page.getByLabel('Hora', { exact: true })).toHaveValue('19');
  await expect(page.getByLabel('Minutos')).toHaveValue('05');
});

test('Apagar tudo: Cancelar e Esc mantêm os dados; só APAGAR libera o botão', async ({ page }) => {
  const nativos = vigiarDialogosNativos(page);
  await comExemplo(page);
  const abrir = page.getByRole('button', { name: 'Apagar todos os dados deste aparelho' });
  const caixa = page.getByRole('dialog', { name: 'Apagar tudo neste aparelho?' });

  await abrir.click();
  await expect(caixa).toContainText('Saem a família, as crianças, as sessões e os avisos');
  const apagar = caixa.getByRole('button', { name: 'Apagar mesmo assim' });
  await expect(caixa.getByRole('button', { name: 'Guardar uma cópia primeiro' })).toBeVisible();
  await expect(apagar).toBeDisabled();
  await caixa.getByLabel(/digite APAGAR/).fill('APAGA');
  await expect(apagar).toBeDisabled();
  await caixa.getByRole('button', { name: 'Cancelar' }).click();
  await expect(caixa).toHaveCount(0);

  // Esc cancela e o foco volta ao botão que abriu a caixa.
  await abrir.click();
  await expect(caixa.getByLabel(/digite APAGAR/)).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(caixa).toHaveCount(0);
  await expect(abrir).toBeFocused();

  await page.getByRole('link', { name: 'Início' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await abrirAjustes(page);

  // Digitando APAGAR (em qualquer caixa) o botão libera e tudo é apagado.
  await abrir.click();
  await caixa.getByLabel(/digite APAGAR/).fill('apagar');
  await expect(apagar).toBeEnabled();
  await apagar.click();
  await expect(page.getByRole('heading', { name: 'Como funciona' })).toBeVisible();
  await expect(
    page.getByRole('button', { name: 'Explorar com uma família de exemplo' }),
  ).toBeVisible();
  expect(nativos).toEqual([]);
});

test('"Guardar uma cópia primeiro" baixa o arquivo e mantém a caixa aberta', async ({ page }) => {
  await comExemplo(page);
  await page.getByRole('button', { name: 'Apagar todos os dados deste aparelho' }).click();
  const caixa = page.getByRole('dialog', { name: 'Apagar tudo neste aparelho?' });
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    caixa.getByRole('button', { name: 'Guardar uma cópia primeiro' }).click(),
  ]);
  expect(JSON.parse(await readFile((await download.path())!, 'utf-8'))).toMatchObject({
    app: 'semear',
  });
  await expect(caixa).toContainText('Cópia guardada.');
  await caixa.getByRole('button', { name: 'Cancelar' }).click();
  await expect(page.getByText(/Última cópia: hoje/)).toBeVisible();
});

test('Apagar o exemplo usa a confirmação simples, sem digitar nada', async ({ page }) => {
  const nativos = vigiarDialogosNativos(page);
  await comExemplo(page);
  await page.getByRole('button', { name: 'Apagar o exemplo' }).click();
  const caixa = page.getByRole('dialog', { name: 'Apagar o exemplo?' });
  await expect(caixa.getByRole('textbox')).toHaveCount(0);
  await caixa.getByRole('button', { name: 'Cancelar' }).click();
  await expect(page.getByText('Família Marina · 2 crianças')).toBeVisible();

  await page.getByRole('button', { name: 'Apagar o exemplo' }).click();
  await caixa.getByRole('button', { name: 'Apagar o exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Como funciona' })).toBeVisible();
  expect(nativos).toEqual([]);
});

test('Trazer uma cópia guardada: botão por teclado, arquivo válido restaura, inválido mostra erro no cartão', async ({
  page,
}) => {
  const nativos = vigiarDialogosNativos(page);
  await comExemplo(page);
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Guardar uma cópia dos meus dados' }).click(),
  ]);
  const arquivo = (await download.path())!;

  // O botão recebe foco por teclado e abre o seletor de arquivo com Enter.
  const trazer = page.getByRole('button', { name: 'Trazer uma cópia guardada' });
  await trazer.focus();
  await expect(trazer).toBeFocused();
  const [seletor] = await Promise.all([
    page.waitForEvent('filechooser'),
    page.keyboard.press('Enter'),
  ]);
  await seletor.setFiles({
    name: 'lixo.json',
    mimeType: 'application/json',
    buffer: Buffer.from('isto nao e json'),
  });
  const erro = page.locator('#erro-copia');
  await expect(erro).toBeVisible();
  await expect(erro).toContainText('não parece ser uma cópia do Semear');
  await expect(erro).toHaveAttribute('role', 'alert');
  // O erro fica dentro do cartão da cópia de segurança.
  await expect(
    page
      .locator('section', { has: page.getByRole('heading', { name: 'Cópia de segurança' }) })
      .locator('#erro-copia'),
  ).toHaveCount(1);

  // JSON de outro app: também recusado, com a mensagem da validação.
  await page.locator('#importar').setInputFiles({
    name: 'errado.json',
    mimeType: 'application/json',
    buffer: Buffer.from('{"app":"outro"}'),
  });
  await expect(erro).toContainText('Arquivo de backup inválido');

  // Arquivo válido: pede confirmação e restaura; recusar a caixa não muda nada.
  await page.locator('#importar').setInputFiles(arquivo);
  const caixa = page.getByRole('dialog', { name: 'Trazer esta cópia?' });
  await caixa.getByRole('button', { name: 'Cancelar' }).click();
  await expect(page.getByText('Família Marina · 2 crianças')).toBeVisible();
  await page.locator('#importar').setInputFiles(arquivo);
  await confirmarTrazerCopia(page);
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  expect(nativos).toEqual([]);
});

test('Apagar tudo e trazer a cópia de volta (fluxo completo pelos Ajustes)', async ({ page }) => {
  await comExemplo(page);
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Guardar uma cópia dos meus dados' }).click(),
  ]);
  const arquivo = (await download.path())!;
  await apagarTudoPelosAjustes(page);
  await expect(page.getByRole('heading', { name: 'Como funciona' })).toBeVisible();
  await abrirAjustes(page);
  await page.locator('#importar').setInputFiles(arquivo);
  await confirmarTrazerCopia(page);
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
});

test.describe('alerta da última cópia', () => {
  async function gravarUltimaCopia(page: Page, diasAtras: number) {
    await page.evaluate(
      (dias) =>
        new Promise<void>((resolve, reject) => {
          const abrir = indexedDB.open('semear');
          abrir.onerror = () => reject(abrir.error);
          abrir.onsuccess = () => {
            const db = abrir.result;
            const tx = db.transaction('config', 'readwrite');
            const em = new Date(Date.now() - dias * 86_400_000).toISOString();
            tx.objectStore('config').put({ em }, 'ultimoBackup');
            tx.oncomplete = () => {
              db.close();
              resolve();
            };
            tx.onerror = () => reject(tx.error);
          };
        }),
      diasAtras,
    );
  }

  test('nunca guardou: mostra "nunca" em destaque e o aviso', async ({ page }) => {
    await comExemplo(page);
    await expect(page.getByText('Última cópia: nunca')).toBeVisible();
    await expect(page.getByText('Você ainda não guardou nenhuma cópia.')).toBeVisible();
  });

  test('há 12 dias: sem alerta; há 45 dias: alerta dentro dos Ajustes', async ({ page }) => {
    await comExemplo(page);
    await gravarUltimaCopia(page, 12);
    await page.reload();
    await expect(page.getByText('Última cópia: há 12 dias')).toBeVisible();
    await expect(page.getByText(/Faz \d+ dias que você não guarda/)).toHaveCount(0);

    await gravarUltimaCopia(page, 45);
    await page.reload();
    await expect(page.getByText('Última cópia: há 45 dias')).toBeVisible();
    await expect(page.getByText('Faz 45 dias que você não guarda uma cópia.')).toBeVisible();
    // O alerta é só da tela de Ajustes: o Início não ganhou nada novo.
    await page.getByRole('link', { name: 'Início' }).click();
    await expect(page.getByText('Faz 45 dias que você não guarda uma cópia.')).toHaveCount(0);
  });
});

test('sem rolagem horizontal em 320 e 390 px e sem chamadas externas além das fontes', async ({
  page,
}) => {
  const externas: string[] = [];
  page.on('request', (r) => {
    if (
      !/^(http:\/\/(localhost|127\.0\.0\.1)|data:|blob:)/.test(r.url()) &&
      !/^https:\/\/fonts\.(googleapis|gstatic)\.com\//.test(r.url())
    )
      externas.push(r.url());
  });
  await comExemplo(page);
  for (const largura of [320, 390]) {
    await page.setViewportSize({ width: largura, height: 700 });
    expect(await semRolagemHorizontal(page), `Ajustes em ${largura}px`).toBe(true);
    // Também com a caixa de confirmação aberta.
    await page.getByRole('button', { name: 'Apagar todos os dados deste aparelho' }).click();
    const caixa = page.getByRole('dialog', { name: 'Apagar tudo neste aparelho?' });
    await expect(caixa).toBeVisible();
    expect(await semRolagemHorizontal(page), `caixa em ${largura}px`).toBe(true);
    const caixaBox = (await caixa.boundingBox())!;
    expect(caixaBox.x).toBeGreaterThanOrEqual(0);
    expect(caixaBox.x + caixaBox.width).toBeLessThanOrEqual(largura);
    await page.keyboard.press('Escape');
  }
  expect(externas).toEqual([]);
});
