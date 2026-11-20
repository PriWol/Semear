import { expect, test } from '@playwright/test';

// Biblioteca (ADR 0015): os volumes abrem neste mesmo site, na unidade certa, sem chamada externa.
test('Biblioteca lista os volumes 1 a 7 com links relativos para as unidades', async ({ page }) => {
  await page.goto('./#/config');
  await page.getByRole('link', { name: 'Biblioteca' }).click();
  await expect(page.getByRole('heading', { name: 'Biblioteca' })).toBeVisible();
  for (const n of [1, 2, 3, 4, 5, 6, 7])
    await expect(page.getByRole('heading', { name: new RegExp(`Volume ${n} `) })).toBeVisible();
  const vivaldi = page.getByRole('link', { name: /Unidade 5 · Vivaldi/ });
  await expect(vivaldi).toHaveAttribute('href', 'tesouro/volume4-tela.pdf#page=42');
  const monet = page.getByRole('link', { name: /Unidade 4 · Monet e o jardim/ });
  await expect(monet).toHaveAttribute('href', 'tesouro/volume5-tela.pdf#page=28');
});

test('Biblioteca traz os cadernos para 2 anos, com aviso de saúde e sem chamada externa', async ({
  page,
}) => {
  const externas: string[] = [];
  page.on('request', (r) => {
    if (
      !r.url().startsWith('http://localhost') &&
      !r.url().startsWith('http://127.0.0.1') &&
      !r.url().startsWith('data:') &&
      // Fontes do Google: a única chamada externa permitida (CLAUDE.md, Privacidade).
      !/^https:\/\/fonts\.(googleapis|gstatic)\.com\//.test(r.url())
    )
      externas.push(r.url());
  });
  await page.goto('./#/biblioteca');
  await expect(page.getByRole('heading', { name: 'Cadernos para 2 anos' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Caderno de atividades · 2 anos' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Caderno de inglês · 2 anos' })).toBeVisible();
  // Aviso de saúde: 1 na seção (destacado, role note) + 1 em cada um dos 2 cartões.
  const aviso = /ainda não foram conferidas por um profissional de saúde/;
  await expect(page.getByText(aviso)).toHaveCount(3);
  await expect(page.locator('div.alerta[role="note"]').getByText(aviso)).toBeVisible();
  for (const nome of ['Caderno de atividades · 2 anos', 'Caderno de inglês · 2 anos'])
    await expect(
      page
        .locator('section.cartao', { has: page.getByRole('heading', { name: nome }) })
        .getByText(aviso),
    ).toHaveCount(1);
  // Hierarquia: seção em h2, cartões dos cadernos em h3; volumes continuam h2.
  await expect(
    page.getByRole('heading', { name: 'Caderno de inglês · 2 anos', level: 3 }),
  ).toBeVisible();
  await expect(page.getByRole('heading', { name: /^Volume 6 /, level: 2 })).toBeVisible();
  // Botões de abrir com o endereço certo.
  const arquivos: Record<string, string> = {
    'Volume 1 ': 'volume1',
    'Volume 2 ': 'volume2',
    'Volume 3 ': 'volume3',
    'Volume 4 ': 'volume4',
    'Volume 5 ': 'volume5',
    'Volume 6 ': 'volume6',
    'Volume 7 ': 'volume7',
  };
  for (const [titulo, base] of Object.entries(arquivos))
    await expect(
      page
        .locator('section.cartao', {
          has: page.getByRole('heading', { name: new RegExp(`^${titulo}`) }),
        })
        .getByRole('link', { name: 'Abrir o volume' }),
    ).toHaveAttribute('href', `tesouro/${base}-tela.pdf#page=1`);
  const cadernos: Record<string, string> = {
    'Caderno de atividades · 2 anos': 'caderno-tela',
    'Caderno de inglês · 2 anos': 'caderno-ingles-tela',
  };
  for (const [titulo, base] of Object.entries(cadernos))
    await expect(
      page
        .locator('section.cartao', { has: page.getByRole('heading', { name: titulo }) })
        .getByRole('link', { name: 'Abrir o caderno' }),
    ).toHaveAttribute('href', `tesouro/${base}.pdf#page=1`);
  // O caderno de atividades diz qual volume cada unidade acompanha.
  const atividades = page.locator('section.cartao', {
    has: page.getByRole('heading', { name: 'Caderno de atividades · 2 anos' }),
  });
  for (let n = 1; n <= 7; n++)
    await expect(atividades.getByText(`acompanha o Volume ${n}`, { exact: false })).toHaveCount(1);
  // O Volume 8 é planejado e ainda não está no app: a unidade 8 avisa.
  await expect(
    atividades.getByText('acompanha o Volume 8 (ainda não disponível no app)', { exact: false }),
  ).toHaveCount(1);
  await expect(page.getByText('acompanha o Volume')).toHaveCount(8);
  await expect(page.getByRole('link', { name: /Unidade 6 · Animals/ })).toHaveAttribute(
    'href',
    'tesouro/caderno-ingles-tela.pdf#page=58',
  );
  await expect(page.getByRole('link', { name: /Unidade 4 · A comida/ })).toHaveAttribute(
    'href',
    'tesouro/volume7-tela.pdf#page=24',
  );
  await expect(page.getByRole('link', { name: /Unidade 5 · Os animais/ })).toHaveAttribute(
    'href',
    'tesouro/volume7-tela.pdf#page=30',
  );
  expect(externas).toEqual([]);
});

for (const largura of [320, 390]) {
  test(`Biblioteca sem rolagem horizontal em ${largura} px`, async ({ page }) => {
    await page.setViewportSize({ width: largura, height: 800 });
    await page.goto('./#/biblioteca');
    await expect(page.getByRole('heading', { name: 'Cadernos para 2 anos' })).toBeVisible();
    const sobra = await page.evaluate(
      () => document.documentElement.scrollWidth - window.innerWidth,
    );
    expect(sobra).toBeLessThanOrEqual(0);
  });
}
