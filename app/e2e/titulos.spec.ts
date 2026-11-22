import { expect, test } from '@playwright/test';

// QA2-16: os títulos não pulam nível (h1 -> h3 confunde quem navega por títulos).
// QA2-14: nenhuma frase interna da equipe aparece para a família.

for (const rota of ['/acervo', '/atividades']) {
  test(`${rota}: níveis de título em sequência, sem pular`, async ({ page }) => {
    await page.goto(`./#${rota}`);
    await expect(page.locator('main h1')).toBeVisible();
    await expect(page.locator('main h2').first()).toBeVisible();
    const niveis = await page.evaluate(() =>
      [...document.querySelectorAll('main h1, main h2, main h3, main h4')].map((h) =>
        Number(h.tagName[1]),
      ),
    );
    expect(niveis[0]).toBe(1);
    niveis.forEach((n, i) => {
      if (i > 0) expect(n - niveis[i - 1]!, `salto antes do título ${i}`).toBeLessThanOrEqual(1);
    });
  });
}

test('Família: o texto das línguas não vaza "decisão do produto"', async ({ page }) => {
  await page.goto('./#/familia');
  await expect(page.getByRole('heading', { name: /família/i }).first()).toBeVisible();
  await expect(page.getByText('Mostramos só as línguas que você marcar.')).toBeVisible();
  await expect(page.getByText(/decisão do produto/i)).toHaveCount(0);
});
