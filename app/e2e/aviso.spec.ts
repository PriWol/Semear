import { expect, test, type Page } from '@playwright/test';

// QA2-12: o aviso flutuante tem botão "Fechar"; sucesso some sozinho (6 a 8 s) e alerta fica até fechar.

async function abrirCriancaDoExemplo(page: Page) {
  await page.clock.install();
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await page.goto('./#/crianca/exemplo-ana');
  await expect(page.getByLabel('Data de nascimento')).toBeVisible();
}

test('aviso de sucesso: tem Fechar e some sozinho depois de 8 s, nunca antes de 6 s', async ({
  page,
}) => {
  await abrirCriancaDoExemplo(page);
  const ano = new Date().getFullYear() - 5;
  await page.getByLabel('Data de nascimento').fill(`${ano}-03-15`);
  await page.getByRole('button', { name: 'Salvar' }).click();
  const aviso = page.locator('#aviso');
  await expect(aviso).toContainText('Dados salvos.');
  await expect(aviso.getByRole('button', { name: 'Fechar' })).toBeVisible();

  await page.clock.fastForward(5500);
  await expect(aviso).toBeVisible();
  await page.clock.fastForward(2600);
  await expect(aviso).toBeHidden();
});

test('aviso de sucesso: o botão Fechar esconde na hora', async ({ page }) => {
  await abrirCriancaDoExemplo(page);
  await page.getByRole('button', { name: 'Salvar' }).click();
  const aviso = page.locator('#aviso');
  await expect(aviso).toBeVisible();
  await aviso.getByRole('button', { name: 'Fechar' }).click();
  await expect(aviso).toBeHidden();
});

test('alerta (idade fora da faixa) não some sozinho; só some ao fechar', async ({ page }) => {
  await abrirCriancaDoExemplo(page);
  await page.getByLabel('Data de nascimento').fill('2000-03-15');
  await page.getByRole('button', { name: 'Salvar' }).click();
  const aviso = page.locator('#aviso');
  await expect(aviso).toContainText('Atenção');

  await page.clock.fastForward(60_000);
  await expect(aviso).toBeVisible();
  await aviso.getByRole('button', { name: 'Fechar' }).click();
  await expect(aviso).toBeHidden();
});
