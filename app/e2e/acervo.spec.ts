import { expect, test } from '@playwright/test';

// Acervo gratuito (ADR 0016): a busca roda no aparelho e os links abrem em outra aba.
test('Acervo filtra por idioma e por texto', async ({ page }) => {
  await page.goto('./#/acervo');
  await expect(page.getByRole('heading', { name: 'Acervo gratuito' })).toBeVisible();
  await page.getByLabel('Idioma').selectOption('la');
  await expect(page.getByRole('heading', { name: 'Orbis Pictus', exact: true })).toBeVisible();
  await page.getByLabel('Idioma').selectOption('');
  await page.getByLabel('Buscar').fill('esquilo nutkin');
  await expect(page.getByText('Nenhuma obra encontrada')).toBeVisible();
  await page.getByLabel('Buscar').fill('peter rabbit');
  const link = page.getByRole('link', { name: 'Buscar nesta fonte' }).first();
  await expect(link).toHaveAttribute('rel', /noopener/);
  await expect(link).toHaveAttribute('href', /^https:\/\//);
});
