import { expect, test, type Page } from '@playwright/test';

// #139: "Abrir em tela cheia" (sessão) e "Abrir para imprimir" (semana) não abrem mais uma aba blob:
// (que herdava a CSP do app, matava o script do pacote e seria da origem do app). Abrem um painel
// sobre a tela com a mesma prévia isolada (iframe sandbox sem a origem do app, ADR 0022).

const HOSTS_PERMITIDOS = /^(localhost|fonts\.googleapis\.com|fonts\.gstatic\.com)$/;
const QUADRO = 'dialog.painel-pacote iframe';

function observar(page: Page) {
  const violacoes: string[] = [];
  const externas: string[] = [];
  page.on('console', (m) => {
    if (/Content Security Policy|Refused to/i.test(m.text())) violacoes.push(m.text());
  });
  page.on('pageerror', (e) => violacoes.push(e.message));
  page.on('request', (r) => {
    const u = new URL(r.url());
    if (u.protocol.startsWith('http') && !HOSTS_PERMITIDOS.test(u.hostname)) externas.push(r.url());
  });
  page.on('popup', (p) => violacoes.push(`abriu nova aba: ${p.url()}`));
  return { violacoes, externas };
}

async function entrarNoExemplo(page: Page) {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
}

/** Espera o script do pacote carregar dentro do iframe e troca `print` por um contador. */
async function espiarImpressao(page: Page) {
  const quadro = page.locator(QUADRO);
  await expect(quadro).toHaveAttribute('sandbox', 'allow-scripts allow-modals');
  const frame = await (await quadro.elementHandle())!.contentFrame();
  await expect
    .poll(
      () =>
        frame!.evaluate(
          () => typeof (window as unknown as { alternarTablet?: unknown }).alternarTablet,
        ),
      // Teto de 40 s (padrão do poll é 5 s): o script do pacote só roda depois que o parser termina, e o parser espera as
      // fontes do Google (rede externa). 40 s é folga para CI lento; não há medição do tempo típico registrada.
      { timeout: 40_000 },
    )
    .toBe('function');
  await frame!.evaluate(() => {
    const w = window as unknown as { __impressoes: number };
    w.__impressoes = 0;
    window.print = () => {
      w.__impressoes++;
    };
  });
  const contagem = () =>
    frame!.evaluate(() => (window as unknown as { __impressoes: number }).__impressoes);
  return { frame: frame!, contagem };
}

async function semRolagemLateral(page: Page) {
  const m = await page.evaluate(() => {
    const d = document.querySelector('dialog.painel-pacote')!.getBoundingClientRect();
    return {
      rolagem: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      direita: d.right,
      largura: window.innerWidth,
    };
  });
  expect(m.rolagem).toBeLessThanOrEqual(0);
  expect(m.direita).toBeLessThanOrEqual(m.largura);
}

test('sessão: o painel abre, imprime, fica isolado do app e fecha por Esc e pelo botão', async ({
  page,
}) => {
  const { violacoes, externas } = observar(page);
  await entrarNoExemplo(page);
  await page.goto('./#/sessao/exemplo-sessao-1');
  const abrir = page.getByRole('button', { name: /Abrir em tela cheia/ });
  await abrir.click();

  const painel = page.getByRole('dialog', { name: /Sessão/ });
  await expect(painel).toBeVisible();
  const { frame, contagem } = await espiarImpressao(page);

  // "Imprimir" da barra do painel pede a impressão ao pacote (por mensagem) e o próprio pacote imprime.
  await painel.getByRole('button', { name: 'Imprimir', exact: true }).click();
  await expect.poll(contagem).toBe(1);
  // O botão do próprio pacote também responde dentro do sandbox, e o "Modo tablet" também.
  const dentro = page.frameLocator(QUADRO);
  await dentro.getByRole('button', { name: /Imprimir \/ salvar PDF/ }).click();
  await expect.poll(contagem).toBe(2);
  await dentro.getByRole('button', { name: /Modo tablet/ }).click();
  await expect(dentro.locator('body')).toHaveClass(/tablet/);

  // Isolamento: outra origem, sem IndexedDB nem armazenamento do app.
  const isolamento = await frame.evaluate(async () => {
    const erro = async (f: () => unknown) => {
      try {
        await f();
        return 'ok';
      } catch (e) {
        return (e as Error).name;
      }
    };
    return {
      origem: window.origin,
      idb: await erro(() => indexedDB.open('semear')),
      storage: await erro(() => localStorage.getItem('x')),
    };
  });
  expect(isolamento.origem).toBe('null');
  expect(isolamento.idb).toBe('SecurityError');
  expect(isolamento.storage).toBe('SecurityError');

  // Barra: alvos de toque de pelo menos 44 px.
  for (const nome of ['Imprimir', 'Fechar']) {
    const caixa = await painel.getByRole('button', { name: nome, exact: true }).boundingBox();
    expect(caixa!.height).toBeGreaterThanOrEqual(44);
    expect(caixa!.width).toBeGreaterThanOrEqual(44);
  }

  // Esc fecha e o foco volta ao botão que abriu.
  await page.keyboard.press('Escape');
  await expect(page.locator('dialog.painel-pacote')).toHaveCount(0);
  await expect(abrir).toBeFocused();

  // Reabre e fecha pelo botão "Fechar".
  await abrir.click();
  await expect(page.getByRole('dialog', { name: /Sessão/ })).toBeVisible();
  await page
    .locator('dialog.painel-pacote')
    .getByRole('button', { name: 'Fechar', exact: true })
    .click();
  await expect(page.locator('dialog.painel-pacote')).toHaveCount(0);
  await expect(abrir).toBeFocused();

  expect(violacoes).toEqual([]);
  expect(externas).toEqual([]);
});

test('semana: "Abrir para imprimir" abre o mesmo painel, sem nova aba', async ({ page }) => {
  const { violacoes, externas } = observar(page);
  await entrarNoExemplo(page);
  await page.goto('./#/semana/exemplo-ana');
  await page.getByRole('button', { name: 'Planejar semana' }).click();
  const abrir = page.getByRole('button', { name: /Abrir para imprimir/ });
  await abrir.click();

  const painel = page.getByRole('dialog', { name: /Semana/ });
  await expect(painel).toBeVisible();
  const { contagem } = await espiarImpressao(page);
  await painel.getByRole('button', { name: 'Imprimir', exact: true }).click();
  await expect.poll(contagem).toBe(1);

  await page.keyboard.press('Escape');
  await expect(page.locator('dialog.painel-pacote')).toHaveCount(0);
  await expect(abrir).toBeFocused();

  expect(violacoes).toEqual([]);
  expect(externas).toEqual([]);
});

test('a CSP do index.html continua estrita (o painel não a afrouxa)', async ({ page }) => {
  await page.goto('./');
  const csp = await page
    .locator('meta[http-equiv="Content-Security-Policy"]')
    .getAttribute('content');
  const script = csp!
    .split(';')
    .map((d) => d.trim())
    .find((d) => d.startsWith('script-src'));
  expect(script).toBe("script-src 'self'");
  expect(csp).not.toMatch(/unsafe-eval|nonce-|sha256-/);
});

for (const largura of [320, 390]) {
  test(`o painel não rola para o lado em ${largura} px`, async ({ page }) => {
    await page.setViewportSize({ width: largura, height: 700 });
    await entrarNoExemplo(page);
    await page.goto('./#/sessao/exemplo-sessao-1');
    await page.getByRole('button', { name: /Abrir em tela cheia/ }).click();
    const painel = page.getByRole('dialog', { name: /Sessão/ });
    await expect(painel).toBeVisible();
    await semRolagemLateral(page);
    for (const nome of ['Imprimir', 'Fechar']) {
      const caixa = await painel.getByRole('button', { name: nome, exact: true }).boundingBox();
      expect(caixa!.height).toBeGreaterThanOrEqual(44);
    }
  });
}
