import { expect, test } from '@playwright/test';

// Biblioteca (ADR 0015): os volumes abrem neste mesmo site, na unidade certa, sem chamada externa.
test('Biblioteca lista os volumes 1 a 7 com links relativos para as unidades', async ({ page }) => {
  await page.goto('./#/config');
  await page.getByRole('link', { name: 'Biblioteca' }).click();
  await expect(page.getByRole('heading', { name: 'Biblioteca' })).toBeVisible();
  for (const n of [1, 2, 3, 4, 5, 6, 7])
    await expect(page.getByRole('heading', { name: new RegExp(`Volume ${n} `) })).toBeVisible();
  const vivaldi = page.getByRole('link', { name: /Unidade 5 · Vivaldi/ });
  await expect(vivaldi).toHaveAttribute('href', 'tesouro/volume4-tela.pdf#page=42');
  const monet = page.getByRole('link', { name: /Unidade 4 · Monet e o jardim/ });
  await expect(monet).toHaveAttribute('href', 'tesouro/volume5-tela.pdf#page=28');
});

test('Biblioteca traz os cadernos para 2 anos, com aviso de saúde e sem chamada externa', async ({
  page,
}) => {
  const externas: string[] = [];
  page.on('request', (r) => {
    if (
      !r.url().startsWith('http://localhost') &&
      !r.url().startsWith('http://127.0.0.1') &&
      !r.url().startsWith('data:') &&
      // Fontes do Google: a única chamada externa permitida (CLAUDE.md, Privacidade).
      !/^https:\/\/fonts\.(googleapis|gstatic)\.com\//.test(r.url())
    )
      externas.push(r.url());
  });
  await page.goto('./#/biblioteca');
  await expect(page.getByRole('heading', { name: 'Cadernos para 2 anos' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Caderno de atividades · 2 anos' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Caderno de inglês · 2 anos' })).toBeVisible();
  await expect(
    page.getByText(/ainda não foram conferidas por um profissional de saúde/).first(),
  ).toBeVisible();
  await expect(page.getByRole('link', { name: /Unidade 6 · Animals/ })).toHaveAttribute(
    'href',
    'tesouro/caderno-ingles-tela.pdf#page=58',
  );
  await expect(page.getByRole('link', { name: /Unidade 4 · A comida/ })).toHaveAttribute(
    'href',
    'tesouro/volume7-tela.pdf#page=24',
  );
  await expect(page.getByRole('link', { name: /Unidade 5 · Os animais/ })).toHaveAttribute(
    'href',
    'tesouro/volume7-tela.pdf#page=30',
  );
  expect(externas).toEqual([]);
});

for (const largura of [320, 390]) {
  test(`Biblioteca sem rolagem horizontal em ${largura} px`, async ({ page }) => {
    await page.setViewportSize({ width: largura, height: 800 });
    await page.goto('./#/biblioteca');
    await expect(page.getByRole('heading', { name: 'Cadernos para 2 anos' })).toBeVisible();
    const sobra = await page.evaluate(
      () => document.documentElement.scrollWidth - window.innerWidth,
    );
    expect(sobra).toBeLessThanOrEqual(0);
  });
}
