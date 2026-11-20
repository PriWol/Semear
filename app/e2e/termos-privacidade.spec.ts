import { expect, test } from '@playwright/test';

// #25: Termos e Privacidade a um toque, no rodapé e na boas-vindas.
test('o rodapé leva aos Termos e à Privacidade, sem rolagem horizontal', async ({ page }) => {
  await page.goto('./');
  const rodape = page.locator('footer.rodape');
  await expect(rodape).toBeVisible();
  await expect(rodape).toContainText('Seus dados ficam só neste aparelho.');

  await rodape.getByRole('link', { name: 'Termos', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Termos de uso', level: 1 })).toBeVisible();
  await expect(page.getByText('ainda sem revisão jurídica')).toBeVisible();
  await expect(rodape).toBeVisible();

  await rodape.getByRole('link', { name: 'Privacidade', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Política de privacidade' })).toBeVisible();

  for (const largura of [320, 390]) {
    await page.setViewportSize({ width: largura, height: 700 });
    const estoura = await page.evaluate(
      () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
    );
    expect(estoura).toBe(false);
  }
});

test('o alvo de toque dos links do rodapé tem pelo menos 48 px', async ({ page }) => {
  await page.goto('./');
  for (const nome of ['Termos', 'Privacidade']) {
    const caixa = await page
      .locator('footer.rodape')
      .getByRole('link', { name: nome, exact: true })
      .boundingBox();
    expect(caixa?.height ?? 0).toBeGreaterThanOrEqual(47.5);
  }
});

test('a boas-vindas tem os links de política de privacidade e de termos de uso', async ({
  page,
}) => {
  await page.goto('./');
  await page.getByRole('link', { name: 'Termos de uso' }).click();
  await expect(page.getByRole('heading', { name: 'Termos de uso', level: 1 })).toBeVisible();
  await page.goBack();
  await page.getByRole('link', { name: /política de privacidade/ }).click();
  await expect(page.getByRole('heading', { name: 'Política de privacidade' })).toBeVisible();
});
