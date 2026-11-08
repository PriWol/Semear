import { expect, test } from '@playwright/test';

// #17: a sondagem tem etapa base e etapa de ajuste, e grava a posição na jornada.
test('sondagem: etapa base, ajuste só na linha indefinida e posição gravada', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('link', { name: 'Começar' }).click();
  await page.getByLabel('Seu nome (educador)').fill('Maria');
  await page.getByRole('radio', { name: /Montessori/ }).check();
  await page.getByRole('button', { name: 'Continuar' }).click();
  await expect(page.getByRole('heading', { name: 'Adicionar criança' })).toBeVisible();
  await page.getByLabel('Nome').fill('Ana');
  await page.getByLabel('Data de nascimento').fill('2021-03-15');
  await page.getByRole('button', { name: 'Salvar' }).click();
  await expect(page.getByRole('heading', { name: /Jornada de Ana/ })).toBeVisible();

  await page.getByRole('link', { name: 'Faça a sondagem' }).click();
  await expect(page.getByRole('heading', { name: 'Etapa 1: base' })).toBeVisible();
  const marcar = (marco: string, estado: string) =>
    page.locator(`input[name$="|${marco}"][value="${estado}"]`).check();

  // Fonologia: acha a fronteira na etapa base (04 e 05 consolidados, 06 ainda aprendendo).
  await marcar('LG.FON.04', 'consolidado');
  await marcar('LG.FON.05', 'consolidado');
  await marcar('LG.FON.06', 'em-desenvolvimento');
  // Senso numérico: tudo consolidado, então falta ver o próximo marco.
  await marcar('MA.SEN.05', 'consolidado');
  await marcar('MA.SEN.06', 'consolidado');
  await marcar('MA.SEN.07', 'consolidado');
  await page.getByRole('button', { name: 'Lançar resultados' }).click();

  // O ajuste traz um item novo só para a linha indefinida.
  await expect(page.getByRole('heading', { name: 'Etapa 2: ajuste' })).toBeVisible();
  await expect(page.locator('input[name$="|MA.SEN.08"]').first()).toBeVisible();
  await expect(page.locator('input[name$="|LG.FON.06"]')).toHaveCount(0);
  await marcar('MA.SEN.08', 'em-desenvolvimento');
  await page.getByRole('button', { name: 'Lançar resultados' }).click();

  await expect(page.getByRole('heading', { name: /Jornada de Ana/ })).toBeVisible();
  await expect(page.locator('li.marco[data-marco="LG.FON.06"]')).toContainText('trabalhando agora');
  await expect(
    page.locator('li.marco[data-marco="LG.FON.05"]').getByRole('button', { name: /Consolidado/ }),
  ).toHaveAttribute('aria-pressed', 'true');
});
