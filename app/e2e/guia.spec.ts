import { expect, test } from '@playwright/test';

// #30: o cadastro da família leva ao guia, que explica as cinco vertentes.
test('o cadastro leva ao guia com as cinco vertentes e como combiná-las', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('link', { name: 'Começar' }).click();
  await expect(page.getByRole('heading', { name: /família/i })).toBeVisible();
  await page.getByRole('link', { name: 'Não sei qual escolher' }).click();

  await expect(page.getByRole('heading', { name: 'Guia das vertentes' })).toBeVisible();
  for (const v of ['Montessori', 'Waldorf', 'Clássico', 'Religioso', 'Charlotte Mason']) {
    await expect(page.getByRole('heading', { name: v, level: 2 })).toBeVisible();
  }
  await expect(
    page.getByRole('heading', { name: /combinar uma vertente principal/ }),
  ).toBeVisible();
  await expect(page.getByText('Textos em revisão')).toBeVisible();
});

test('a tela de boas-vindas explica o passo a passo e leva à privacidade', async ({ page }) => {
  await page.goto('./');
  await expect(page.getByRole('heading', { name: 'Como funciona' })).toBeVisible();
  await page.getByRole('link', { name: /política de privacidade/ }).click();
  await expect(page.getByRole('heading', { name: 'Política de privacidade' })).toBeVisible();
  await expect(page.getByText('somente neste aparelho')).toBeVisible();
});
