import { expect, test, type Page } from '@playwright/test';

// Largura da página no computador (#176, opção B): o conteúdo acompanha a janela até o teto de
// --s-largura-app (100rem = 1600 px) e o texto corrido continua com ~65 caracteres por linha.
// Só no projeto "desktop": o celular tem os seus próprios testes de largura (layout-estreito*).

test.skip(({ isMobile }) => isMobile, 'regra do computador');

const TETO = 1600;
const MARGEM_MIN = 16; // --s-espaco-4: a margem lateral nunca fica abaixo disto
const MARGEM_MAX = 32; // --s-espaco-6

const TELAS: { nome: string; rota: string }[] = [
  { nome: 'Início', rota: '/' },
  { nome: 'Atividades', rota: '/atividades' },
  { nome: 'Biblioteca', rota: '/biblioteca' },
  { nome: 'Progresso', rota: '/jornada/exemplo-ana' },
  { nome: 'Nova sessão', rota: '/sessao/nova?crianca=exemplo-ana' },
  { nome: 'Ajustes', rota: '/config' },
];

async function comExemplo(page: Page, largura: number) {
  await page.setViewportSize({ width: largura, height: 900 });
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
}

/** Largura de `65ch` na fonte do elemento, medida com uma sonda invisível. */
const medidaDeLeitura = (alvo: import('@playwright/test').Locator) =>
  alvo.evaluate((el) => {
    const sonda = document.createElement('div');
    sonda.style.cssText = 'position:absolute;visibility:hidden;width:65ch';
    el.appendChild(sonda);
    const medida = sonda.getBoundingClientRect().width;
    sonda.remove();
    return { largura: el.getBoundingClientRect().width, limite: medida };
  });

test('em 1280 px o conteúdo ocupa a janela menos as margens, sem a faixa de 920 px', async ({
  page,
}) => {
  await comExemplo(page, 1280);
  const caixa = await page.locator('main').evaluate((m) => {
    const r = m.getBoundingClientRect();
    return { esquerda: r.left, direita: window.innerWidth - r.right, largura: r.width };
  });
  expect(caixa.largura).toBeGreaterThan(1280 - 2 * MARGEM_MAX - 1);
  expect(caixa.largura).toBeGreaterThan(920);
  expect(caixa.esquerda).toBeLessThanOrEqual(1);
  expect(caixa.direita).toBeLessThanOrEqual(1);
  // O menu e o conteúdo começam na mesma margem lateral.
  const alinhamento = await page.evaluate(() => {
    const marca = document.querySelector('.topo .marca')!.getBoundingClientRect().left;
    const texto = document.querySelector('main h1')!.getBoundingClientRect().left;
    return Math.abs(marca - texto);
  });
  expect(alinhamento).toBeLessThanOrEqual(1);
});

test('em 1920 px o conteúdo não passa de 100rem e fica centralizado', async ({ page }) => {
  await comExemplo(page, 1920);
  const caixa = await page.locator('main').evaluate((m) => {
    const r = m.getBoundingClientRect();
    return { esquerda: r.left, direita: window.innerWidth - r.right, largura: r.width };
  });
  expect(caixa.largura).toBeLessThanOrEqual(TETO);
  expect(caixa.largura).toBeGreaterThan(TETO - 1);
  expect(Math.abs(caixa.esquerda - caixa.direita)).toBeLessThanOrEqual(1);
  // Acima do teto o menu acompanha o conteúdo centralizado, em vez de ficar colado na borda.
  const alinhamento = await page.evaluate(() => {
    const marca = document.querySelector('.topo .marca')!.getBoundingClientRect().left;
    const texto = document.querySelector('main h1')!.getBoundingClientRect().left;
    return Math.abs(marca - texto);
  });
  expect(alinhamento).toBeLessThanOrEqual(1);
});

for (const largura of [1280, 1920]) {
  test(`em ${largura} px nenhuma tela principal rola para o lado`, async ({ page }) => {
    await comExemplo(page, largura);
    for (const { nome, rota } of TELAS) {
      await page.goto(`./#${rota}`);
      await expect(page.locator('h1').first()).toBeVisible();
      const medidas = await page.evaluate(() => ({
        rolagem: document.documentElement.scrollWidth,
        janela: document.documentElement.clientWidth,
        margem: parseFloat(getComputedStyle(document.querySelector('.conteudo-app')!).paddingLeft),
      }));
      expect(medidas.rolagem, nome).toBeLessThanOrEqual(medidas.janela);
      expect(medidas.margem, nome).toBeGreaterThanOrEqual(MARGEM_MIN);
      expect(medidas.margem, nome).toBeLessThanOrEqual(MARGEM_MAX);
    }
  });
}

test('em 1920 px o texto corrido de Termos não passa de ~65 caracteres por linha', async ({
  page,
}) => {
  await comExemplo(page, 1920);
  await page.goto('./#/termos');
  const paragrafo = page.locator('.texto-corrido p').first();
  await expect(paragrafo).toBeVisible();
  const { largura, limite } = await medidaDeLeitura(paragrafo);
  expect(largura).toBeLessThanOrEqual(limite + 1);
});

test('em 1920 px a lista de Atividades usa mais de uma coluna e os filtros ficam em linha', async ({
  page,
}) => {
  await comExemplo(page, 1920);
  await page.goto('./#/atividades');
  const cartoes = page.locator('.lista-atividades > li');
  await expect(cartoes.nth(2)).toBeVisible();
  const esquerdas = await cartoes.evaluateAll((els) =>
    els.map((e) => Math.round(e.getBoundingClientRect().left)),
  );
  expect(new Set(esquerdas).size).toBeGreaterThan(1);

  const buscar = page.locator('#filtros-atividades label', { hasText: 'Buscar' });
  const area = page.locator('#filtros-atividades label', { hasText: 'Área' });
  const vertente = page.locator('#filtros-atividades label', { hasText: 'Vertente' });
  const yArea = (await area.boundingBox())!.y;
  expect(Math.abs(yArea - (await vertente.boundingBox())!.y)).toBeLessThanOrEqual(1);
  expect((await buscar.boundingBox())!.y).toBeLessThan(yArea);
});

test('em 1920 px o botão "Preparar sessão de hoje" não ocupa a linha toda', async ({ page }) => {
  await comExemplo(page, 1920);
  const botao = page.locator('#preparar-hoje');
  await expect(botao).toBeVisible();
  const { largura, limite } = await medidaDeLeitura(page.locator('#preparar-hoje'));
  expect(largura).toBeLessThanOrEqual(limite + 1);
});

// Largura limitada exige decidir o que ocupa o espaço restante (DESIGN.md): painel de apoio, cartões
// lado a lado ou campos em colunas, nunca a metade do cartão vazia.
const caixa = async (alvo: import('@playwright/test').Locator) => (await alvo.boundingBox())!;

test('em 1920 px Nova sessão mostra a proposta à direita do formulário depois de "Sugerir atividades"', async ({
  page,
}) => {
  await comExemplo(page, 1920);
  await page.goto('./#/sessao/nova?crianca=exemplo-ana');
  const formulario = page.locator('#form-sessao');
  await expect(formulario).toBeVisible();
  // Antes de gerar, o painel não ocupa espaço.
  await expect(page.locator('#area-proposta')).toBeHidden();
  await page.getByRole('button', { name: 'Sugerir atividades' }).click();
  const proposta = page.locator('aside#area-proposta #proposta');
  await expect(proposta).toBeVisible();
  const f = await caixa(formulario);
  const p = await caixa(proposta);
  expect(p.x).toBeGreaterThanOrEqual(f.x + f.width);
  expect(Math.abs(p.y - f.y)).toBeLessThanOrEqual(2);
});

test('em 1920 px Família mostra o guia das vertentes ao lado do formulário', async ({ page }) => {
  await comExemplo(page, 1920);
  await page.goto('./#/familia');
  const guia = page.getByRole('complementary', { name: 'Guia das vertentes' });
  await expect(guia).toBeVisible();
  await expect(guia.getByRole('link', { name: 'Não sei qual escolher' })).toBeVisible();
  const f = await caixa(page.locator('#form-familia'));
  const g = await caixa(guia);
  expect(g.x).toBeGreaterThanOrEqual(f.x + f.width);
});

test('em 1920 px o cadastro da criança e a semana sem plano põem os campos em colunas', async ({
  page,
}) => {
  await comExemplo(page, 1920);
  await page.goto('./#/crianca/nova');
  const nome = page.getByLabel('Nome', { exact: true });
  await expect(nome).toBeVisible();
  const nascimento = page.getByLabel('Data de nascimento');
  expect((await caixa(nascimento)).x).toBeGreaterThan((await caixa(nome)).x + 100);

  await page.goto('./#/semana/exemplo-ana');
  const dias = page.getByRole('group', { name: 'Dias da semana' });
  await expect(dias).toBeVisible();
  const duracao = page.getByRole('group', { name: 'Duração de cada sessão' });
  expect((await caixa(duracao)).x).toBeGreaterThan((await caixa(dias)).x + 100);
});

test('em 1920 px Ajustes põe o material de apoio e o "Sobre" ao lado das seções principais', async ({
  page,
}) => {
  await comExemplo(page, 1920);
  await page.goto('./#/config');
  const lateral = page.getByRole('complementary', { name: 'Material de apoio e sobre o Semear' });
  await expect(lateral).toBeVisible();
  const familia = await caixa(page.locator('section[aria-labelledby="aj-familia"]'));
  expect((await caixa(lateral)).x).toBeGreaterThanOrEqual(familia.x + familia.width);
  await expect(page.locator('#exportar')).toBeVisible();
  await expect(page.locator('#apagar')).toBeAttached();
});

test('em 390 px os painéis de apoio somem, a proposta continua abaixo do formulário e não rola para o lado', async ({
  page,
}) => {
  await comExemplo(page, 390);
  await page.goto('./#/familia');
  await expect(page.locator('#form-familia')).toBeVisible();
  await expect(page.locator('.apoio-solto')).toBeHidden();

  await page.goto('./#/sessao/nova?crianca=exemplo-ana');
  await page.getByRole('button', { name: 'Sugerir atividades' }).click();
  const proposta = page.locator('aside#area-proposta #proposta');
  await expect(proposta).toBeVisible();
  const f = await caixa(page.locator('#form-sessao'));
  const p = await caixa(proposta);
  expect(p.y).toBeGreaterThanOrEqual(f.y + f.height - 1);

  for (const rota of ['/familia', '/crianca/nova', '/config', '/sessao/nova?crianca=exemplo-ana']) {
    await page.goto(`./#${rota}`);
    await expect(page.locator('h1').first()).toBeVisible();
    const sobra = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(sobra, rota).toBeLessThanOrEqual(0);
  }
});
