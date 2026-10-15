import { expect, test } from '@playwright/test';

// Biblioteca (ADR 0015): os volumes abrem neste mesmo site, na unidade certa, sem chamada externa.
test('Biblioteca lista o Volume 4 com links relativos para as unidades', async ({ page }) => {
  await page.goto('./#/config');
  await page.getByRole('link', { name: 'Biblioteca' }).click();
  await expect(page.getByRole('heading', { name: 'Biblioteca' })).toBeVisible();
  await expect(page.getByRole('heading', { name: /Volume 4/ })).toBeVisible();
  const vivaldi = page.getByRole('link', { name: /Unidade 5 · Vivaldi/ });
  await expect(vivaldi).toHaveAttribute('href', 'tesouro/volume4-tela.pdf#page=42');
});
