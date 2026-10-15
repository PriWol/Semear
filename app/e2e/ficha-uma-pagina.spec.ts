import { expect, test } from '@playwright/test';

// #33: a ficha de registro cabe numa folha A4 com até 2 atividades. Gera o PDF de verdade (Chromium)
// e conta as páginas só da ficha, isolando-a do resto do pacote.

test.skip(
  ({ isMobile }) => isMobile,
  'page.pdf só roda no Chromium desktop; o layout A4 é o mesmo.',
);

async function paginasDaFicha(
  page: import('@playwright/test').Page,
  duracao: string,
): Promise<number> {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await page
    .locator('.crianca-cartao', { hasText: 'Ana' })
    .getByRole('link', { name: 'Preparar sessão' })
    .click();
  await page.locator(`input[name="duracao"][value="${duracao}"]`).check({ force: true });
  await page.getByRole('button', { name: 'Sugerir atividades' }).click();
  await page.getByRole('button', { name: 'Gerar pacote' }).click();
  await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();

  const documento = await page.locator('#previa').getAttribute('srcdoc');
  expect(documento).toContain('Ficha de registro rápido');

  const folha = await page.context().newPage();
  await folha.setContent(documento ?? '');
  // Isola a ficha (última seção): as outras páginas não interessam para a contagem.
  await folha.evaluate(() => {
    const secoes = [...document.querySelectorAll('.pagina')];
    secoes.slice(0, -1).forEach((s) => s.remove());
  });
  await folha.emulateMedia({ media: 'print' });
  const pdf = await folha.pdf({ preferCSSPageSize: true });
  await folha.close();
  return (pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) ?? []).length;
}

for (const duracao of ['20', '40', '60']) {
  test(`a ficha de uma sessão de ${duracao} min ocupa uma página`, async ({ page }) => {
    expect(await paginasDaFicha(page, duracao)).toBe(1);
  });
}
