import { expect, test } from '@playwright/test';

// Biblioteca (ADR 0015): os volumes abrem neste mesmo site, na unidade certa, sem chamada externa.
test('Biblioteca lista os volumes 1 a 5 com links relativos para as unidades', async ({ page }) => {
  await page.goto('./#/config');
  await page.getByRole('link', { name: 'Biblioteca' }).click();
  await expect(page.getByRole('heading', { name: 'Biblioteca' })).toBeVisible();
  for (const n of [1, 2, 3, 4, 5])
    await expect(page.getByRole('heading', { name: new RegExp(`Volume ${n} `) })).toBeVisible();
  const vivaldi = page.getByRole('link', { name: /Unidade 5 · Vivaldi/ });
  await expect(vivaldi).toHaveAttribute('href', 'tesouro/volume4-tela.pdf#page=42');
  const monet = page.getByRole('link', { name: /Unidade 4 · Monet e o jardim/ });
  await expect(monet).toHaveAttribute('href', 'tesouro/volume5-tela.pdf#page=28');
});
