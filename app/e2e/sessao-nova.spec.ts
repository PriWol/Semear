import { expect, test } from '@playwright/test';

// QA2-03: "Preparar sessão" não despeja 30 linhas na tela. A lista só aparece em "Escolher linhas".

test('Preparar sessão: a lista de linhas só aparece em "Escolher linhas" e o botão fica à vista', async ({
  page,
}) => {
  await page.setViewportSize({ width: 360, height: 740 });
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await page.goto('./#/sessao/nova?crianca=exemplo-ana');
  await expect(page.getByRole('heading', { name: 'Preparar sessão' })).toBeVisible();

  // Equilibrado (padrão): nenhuma caixa de linha visível e o botão principal cabe na tela.
  await expect(page.locator('input[name=foco]:visible')).toHaveCount(0);
  const botao = page.getByRole('button', { name: 'Sugerir atividades' });
  await expect(botao).toBeVisible();
  const caixa = await botao.boundingBox();
  expect(caixa).not.toBeNull();
  expect(caixa!.y + caixa!.height).toBeLessThan(900);

  // Escolher linhas: a lista abre e a contagem acompanha as marcações.
  await page.getByRole('radio', { name: /Escolher linhas/ }).check();
  const caixas = page.locator('input[name=foco]:visible');
  expect(await caixas.count()).toBeGreaterThan(1);
  await expect(page.locator('#contagem-linhas')).toHaveText('0 linhas escolhidas');
  await caixas.first().check();
  await expect(page.locator('#contagem-linhas')).toHaveText('1 linha escolhida');

  // Voltar a Equilibrado esconde a lista de novo.
  await page.getByRole('radio', { name: /Equilibrado/ }).check();
  await expect(page.locator('input[name=foco]:visible')).toHaveCount(0);
});
