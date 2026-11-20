import { expect, test, type Page } from '@playwright/test';

// #25: Termos e Privacidade a um toque, no rodapé e na boas-vindas.
const semRolagemHorizontal = (page: Page) =>
  page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth);

test.beforeEach(async ({ page }) => {
  page.on('dialog', (d) => void d.accept());
});

test('o rodapé leva aos Termos e à Privacidade', async ({ page }) => {
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
});

test('sem rolagem horizontal em 320 e 390 px, nas páginas novas e em outras telas', async ({
  page,
}) => {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();

  const ana = page.locator('.crianca-cartao', { hasText: /\bAna\b/ });
  const hrefJornada = await ana.getByRole('link', { name: 'Ver jornada' }).getAttribute('href');
  const hrefSessao = await page.locator('.lista-sessoes li a').first().getAttribute('href');
  const rotas = ['#/', '#/termos', '#/privacidade', '#/config', hrefJornada, hrefSessao];

  for (const largura of [320, 390]) {
    await page.setViewportSize({ width: largura, height: 700 });
    for (const rota of rotas) {
      await page.evaluate((r) => (location.hash = r ?? '#/'), rota);
      await expect(page.locator('footer.rodape')).toBeVisible();
      expect(await semRolagemHorizontal(page), `${rota} em ${largura}px`).toBe(true);
    }
  }
});

test('o rodapé some na impressão', async ({ page }) => {
  await page.goto('./#/termos');
  await expect(page.locator('footer.rodape')).toBeVisible();
  await page.emulateMedia({ media: 'print' });
  await expect(page.locator('footer.rodape')).toBeHidden();
});

test('o alvo de toque dos links do rodapé tem pelo menos 48 px (celular e desktop)', async ({
  page,
}) => {
  for (const tamanho of [
    { width: 390, height: 800 },
    { width: 1280, height: 800 },
  ]) {
    await page.setViewportSize(tamanho);
    await page.goto('./');
    for (const nome of ['Termos', 'Privacidade']) {
      const caixa = await page
        .locator('footer.rodape')
        .getByRole('link', { name: nome, exact: true })
        .boundingBox();
      expect(caixa?.height ?? 0, `${nome} em ${tamanho.width}px`).toBeGreaterThanOrEqual(47.5);
    }
  }
});

test('o rodapé aparece também numa rota não encontrada', async ({ page }) => {
  await page.goto('./#/rota-que-nao-existe');
  await expect(page.getByRole('heading', { name: 'Página não encontrada' })).toBeVisible();
  await expect(page.locator('footer.rodape')).toBeVisible();
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
