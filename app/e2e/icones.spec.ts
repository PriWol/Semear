import { expect, test } from '@playwright/test';

// #130, ADR 0034: ícones de linha fina (Phosphor) no lugar dos emojis da interface.
const EMOJI = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B50}\u{23E9}-\u{23FF}\u{2197}\u{2B07}]/u;

async function abrirExemplo(page: import('@playwright/test').Page) {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
}

test('boas-vindas e topo mostram ícone SVG (e nenhum emoji)', async ({ page }) => {
  await page.goto('./');
  await expect(page.locator('.boas-vindas .selo svg.icone')).toBeVisible();
  await expect(page.locator('.topo .marca svg.icone')).toBeVisible();
  const texto = await page.locator('body').innerText();
  expect(texto).not.toMatch(EMOJI);
});

test('telas principais trocam o emoji por svg.icone, com nome acessível pelo texto', async ({
  page,
}) => {
  const externas: string[] = [];
  page.on('request', (r) => {
    const u = new URL(r.url());
    if (
      u.protocol.startsWith('http') &&
      !/localhost|127\.0\.0\.1|fonts\.(googleapis|gstatic)\.com/.test(u.host)
    )
      externas.push(r.url());
  });
  await abrirExemplo(page);

  // Início: domínios, Biblioteca, Acervo, Guia.
  await expect(page.locator('.progresso-dominios svg.icone').first()).toBeVisible();
  for (const nome of ['Biblioteca', 'Acervo gratuito', 'Guia das vertentes']) {
    const link = page.getByRole('link', { name: nome, exact: true });
    await expect(link).toBeVisible();
    await expect(link.locator('svg.icone')).toHaveAttribute('aria-hidden', 'true');
  }

  // Jornada: abas de domínio, estados, "Para os pais".
  await page.goto('./#/jornada/exemplo-ana');
  await expect(page.locator('nav a svg.icone').first()).toBeVisible();
  await expect(page.locator('.estado-botao svg.icone').first()).toBeVisible();
  await expect(page.locator('.para-os-pais summary svg.icone').first()).toBeVisible();

  // Atividades: botão por nome, sem o emoji.
  await page.goto('./#/atividades');
  const imprimir = page.getByRole('button', { name: 'Imprimir esta atividade' }).first();
  await expect(imprimir).toBeVisible();
  await expect(imprimir.locator('svg.icone')).toBeVisible();

  // Página de uma atividade: títulos de seção com ícone.
  await page.locator('.lista-atividades a').first().click();
  await expect(page.getByRole('heading', { name: /Objetivo/ })).toBeVisible();
  await expect(page.locator('h2 svg.icone').first()).toBeVisible();

  // Sessão: botões de saída.
  await page.goto('./#/sessao/exemplo-sessao-1');
  for (const nome of ['Imprimir / salvar PDF', 'Baixar arquivo', 'Abrir em tela cheia']) {
    const b = page.getByRole('button', { name: nome });
    await expect(b).toBeVisible();
    await expect(b.locator('svg.icone')).toBeVisible();
  }

  // Ajustes e Biblioteca: sem emoji.
  for (const rota of ['/config', '/biblioteca', '/acervo', '/guia', '/semana/exemplo-ana']) {
    await page.goto(`./#${rota}`);
    await expect(page.locator('h1').first()).toBeVisible();
    expect(await page.locator('main').innerText(), rota).not.toMatch(EMOJI);
  }
  expect(externas).toEqual([]);
});

test('o ícone tem o tamanho do token e o alvo de toque do botão não encolhe', async ({ page }) => {
  await abrirExemplo(page);
  await page.goto('./#/atividades');
  const botao = page.getByRole('button', { name: 'Imprimir esta atividade' }).first();
  const caixa = await botao.boundingBox();
  expect(caixa!.height).toBeGreaterThanOrEqual(44);
  const lado = await botao.locator('svg.icone').evaluate((e) => {
    const r = e.getBoundingClientRect();
    const rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
    return { l: r.width / rem, a: r.height / rem };
  });
  expect(lado.l).toBeCloseTo(1.25, 1);
  expect(lado.a).toBeCloseTo(1.25, 1);
});

for (const largura of [320, 390]) {
  test(`sem rolagem lateral em ${largura}px com os ícones`, async ({ page }) => {
    await page.setViewportSize({ width: largura, height: 800 });
    await abrirExemplo(page);
    for (const rota of ['/', '/jornada/exemplo-ana', '/atividades', '/config', '/biblioteca']) {
      await page.goto(`./#${rota}`);
      await expect(page.locator('h1').first()).toBeVisible();
      const excesso = await page.evaluate(
        () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
      );
      expect(excesso, `${rota} a ${largura}px`).toBeLessThanOrEqual(0);
    }
  });
}
