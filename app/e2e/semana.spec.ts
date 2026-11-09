import { expect, test } from '@playwright/test';
import { readFile } from 'node:fs/promises';

// #8 e #9: planejar a semana, marcar um dia como feito e baixar o documento da semana.
test('planejar a semana, marcar um dia e baixar a semana', async ({ page }) => {
  page.on('dialog', (d) => void d.accept());
  await page.goto('./');
  await page.getByRole('button', { name: /Explorar com uma família de exemplo/ }).click();
  await expect(page.getByRole('heading', { name: /Olá/ })).toBeVisible();

  await page.getByRole('link', { name: 'Planejar semana' }).nth(1).click();
  await expect(page.getByRole('heading', { name: /Semana de Ana/ })).toBeVisible();
  await page.getByRole('radio', { name: '40 min' }).check();
  await page.getByRole('button', { name: 'Planejar semana' }).click();

  // seg, qua e sex vêm marcados por padrão: três dias, sem atividade repetida
  const dias = page.locator('section.dia-plano');
  await expect(dias).toHaveCount(3);
  const titulos = await dias.locator('li').allInnerTexts();
  const nomes = titulos.map((t) =>
    t
      .split('\n')[0]!
      .replace(/\s*\d+ min.*$/, '')
      .trim(),
  );
  expect(new Set(nomes).size).toBe(nomes.length);

  // remove uma atividade de um dia e marca outro como feito
  const antes = await dias.nth(2).locator('li').count();
  if (antes > 0) {
    await dias.nth(2).getByRole('button', { name: 'Remover' }).first().click();
    await expect(page.locator('section.dia-plano').nth(2).locator('li')).toHaveCount(antes - 1);
  }
  await page
    .locator('section.dia-plano')
    .first()
    .getByRole('button', { name: 'Marcar como feito' })
    .click();
  await expect(page.locator('section.dia-plano').first()).toContainText('feito ✓');

  // a sessão do dia feito entra no histórico
  await page.getByRole('link', { name: 'Início' }).click();
  await expect(page.locator('.lista-sessoes')).toContainText('S-');
  await page.getByRole('link', { name: 'Planejar semana' }).nth(1).click();

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: /Baixar arquivo/ }).click(),
  ]);
  expect(download.suggestedFilename()).toMatch(/^semear-semana-.+-\d{4}-\d{2}-\d{2}\.html$/);
  const doc = await readFile((await download.path())!, 'utf-8');
  expect(doc).toContain('Materiais da semana');
  expect(doc).toMatch(/(Segunda|Quarta|Sexta) · Sessão S-/);
});
