import { expect, test } from '@playwright/test';

// QA2-08: "Ir para o conteúdo" é o primeiro item da página (visível só com foco) e, a cada troca de tela,
// o foco vai para o título (<h1>) da tela nova.

test('o primeiro Tab mostra "Ir para o conteúdo" e ele leva o foco ao título', async ({ page }) => {
  await page.goto('./');
  const pular = page.getByRole('link', { name: 'Ir para o conteúdo' });
  // Fora do foco, não aparece na tela.
  await expect(pular).not.toBeInViewport();
  await page.keyboard.press('Tab');
  await expect(pular).toBeFocused();
  await expect(pular).toBeInViewport();

  await page.keyboard.press('Enter');
  const foco = page.locator(':focus');
  await expect(foco).toHaveJSProperty('tagName', 'H1');
  // A rota não mudou (o link não pode tratar "#conteudo" como tela).
  expect(new URL(page.url()).hash).toBe('');
});

test('ao trocar de tela, o foco vai para o <h1> da tela nova', async ({ page }) => {
  await page.goto('./');
  await page
    .locator('nav[aria-label="Principal"]')
    .getByRole('link', { name: 'Atividades' })
    .click();
  await expect(page.getByRole('heading', { level: 1 }).first()).toBeVisible();
  const foco = page.locator(':focus');
  await expect(foco).toHaveJSProperty('tagName', 'H1');
  await expect(foco).toHaveAttribute('tabindex', '-1');
});
