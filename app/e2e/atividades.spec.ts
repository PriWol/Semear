import { expect, test } from '@playwright/test';

// #13: buscar uma atividade (sem acento) e imprimir só ela, para uma criança escolhida.
test('buscar → imprimir uma atividade avulsa', async ({ page }) => {
  page.on('dialog', (d) => void d.accept());
  await page.goto('./');
  await page.getByRole('button', { name: /Explorar com uma família de exemplo/ }).click();
  await expect(page.getByRole('heading', { name: /Olá/ })).toBeVisible();

  await page.getByRole('link', { name: 'Atividades', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Atividades' })).toBeVisible();

  // sem acento e sem diferenciar maiúsculas
  await page.getByRole('searchbox').fill('SILABA');
  await expect(page.locator('[data-atividade="atv-caca-silabas"]')).toBeVisible();
  await expect(page.locator('[data-atividade="atv-feira-numeros"]')).toHaveCount(0);

  // filtro por área
  await page.getByRole('searchbox').fill('');
  await page.getByLabel('Área').selectOption('MA');
  await expect(page.locator('[data-atividade="atv-feira-numeros"]')).toBeVisible();
  await expect(page.locator('[data-atividade="atv-caca-silabas"]')).toHaveCount(0);

  // imprime: gera a sessão avulsa e abre o pacote
  await page
    .locator('[data-atividade="atv-feira-numeros"]')
    .getByRole('button', { name: /Imprimir esta atividade/ })
    .click();
  await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();
  await page.getByRole('link', { name: 'Início' }).click();
  await expect(page.locator('.lista-sessoes')).toContainText('S-');
});
