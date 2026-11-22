import { expect, test } from '@playwright/test';

// #13: buscar uma atividade (sem acento) e imprimir só ela, para uma criança escolhida.
test('buscar → imprimir uma atividade avulsa', async ({ page }) => {
  page.on('dialog', (d) => void d.accept());
  await page.goto('./');
  await page.getByRole('button', { name: /Explorar com uma família de exemplo/ }).click();
  await expect(page.getByRole('heading', { name: /Olá/ })).toBeVisible();

  await page.getByRole('link', { name: 'Atividades', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Atividades' })).toBeVisible();

  // sem acento e sem diferenciar maiúsculas
  await page.getByRole('searchbox').fill('SILABA');
  await expect(page.locator('[data-atividade="atv-caca-silabas"]')).toBeVisible();
  await expect(page.locator('[data-atividade="atv-feira-numeros"]')).toHaveCount(0);

  // o cartão mostra o título do marco, nunca o código cru; o código fica só no title (hover)
  const cartao = page.locator('[data-atividade="atv-caca-silabas"]');
  await expect(cartao.locator('.marco-cartao')).not.toHaveText(/\b[A-Z]{2}\.[A-Z]{3}\.\d{2}\b/);
  await expect(cartao.locator('.marco-cartao')).toHaveAttribute(
    'title',
    /[A-Z]{2}\.[A-Z]{3}\.\d{2}/,
  );

  // filtro por área
  // (a área Matemática tem mais de 20 atividades: a busca "feira" mantém a atividade na primeira página)
  await page.getByRole('searchbox').fill('feira');
  await page.getByLabel('Área').selectOption('MA');
  await expect(page.locator('[data-atividade="atv-feira-numeros"]')).toBeVisible();
  await expect(page.locator('[data-atividade="atv-caca-silabas"]')).toHaveCount(0);

  // imprime: gera a sessão avulsa e abre o pacote
  await page
    .locator('[data-atividade="atv-feira-numeros"]')
    .getByRole('button', { name: /Imprimir esta atividade/ })
    .click();
  await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();
  await page.getByRole('link', { name: 'Início' }).click();
  await expect(page.locator('.lista-sessoes')).toContainText('S-');
});

// Marco em rascunho citado por atividade aprovada é ignorado no código (testes unitários); aqui, só a lista abre.
test('a lista de atividades abre com as atividades aprovadas', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('button', { name: /Explorar com uma família de exemplo/ }).click();
  await page.getByRole('link', { name: 'Atividades', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Atividades' })).toBeVisible();
  await expect(page.locator('#resultado-atividades')).not.toBeEmpty();
});

// A busca filtra por idade: uma atividade de 2 a 4 anos aparece aos 3 e some aos 7 (a idade não precisa ser a de uma criança).
test('buscar por idade', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('button', { name: /Explorar com uma família de exemplo/ }).click();
  await page.getByRole('link', { name: 'Atividades', exact: true }).click();
  await page.getByLabel('Buscar').fill('pintar com o dedo');
  const atividade = page.locator('[data-atividade="atv-cad-pintar-com-o-dedo"]');
  await expect(atividade).toBeVisible();
  await page.getByLabel('Idade').selectOption('3');
  await expect(atividade).toBeVisible();
  await page.getByLabel('Idade').selectOption('7');
  await expect(atividade).toHaveCount(0);
  await page.getByLabel('Idade').selectOption('');
  await expect(atividade).toBeVisible();
});

// Ver a atividade na tela não cria sessão; só "Imprimir esta atividade" cria.
test('abrir uma atividade para ler, sem criar sessão, e depois imprimir', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('button', { name: /Explorar com uma família de exemplo/ }).click();
  await page.getByRole('link', { name: 'Atividades', exact: true }).click();
  await page.getByRole('searchbox').fill('pintar com o dedo');
  await page
    .locator('[data-atividade="atv-cad-pintar-com-o-dedo"]')
    .getByRole('link', { name: 'Pintar com o dedo' })
    .click();

  await expect(page).toHaveURL(/#\/atividade\/atv-cad-pintar-com-o-dedo/);
  await expect(page.getByRole('heading', { name: 'Pintar com o dedo', level: 1 })).toBeVisible();
  await expect(page.getByRole('heading', { name: /Passo a passo/ })).toBeVisible();
  await expect(page.getByRole('heading', { name: /Materiais/ })).toBeVisible();
  await expect(page.locator('.passos-leitura li').first()).toBeVisible();
  await expect(page.locator('.cuidados')).toContainText('Tinta atóxica');
  // marco por título, nunca o id cru
  await expect(page.locator('.atividade-leitura')).not.toContainText('AR.PIN.01');
  await expect(page.getByText(/Caderno de atividades · 2 anos/)).toBeVisible();
  await expect(page.getByRole('link', { name: 'Abrir o PDF' })).toHaveAttribute(
    'href',
    /^tesouro\//,
  );

  // nenhuma sessão foi criada só por ler
  await page.getByRole('link', { name: 'Início' }).click();
  // (a família de exemplo já tem sessões: a atividade lida não pode aparecer no histórico)
  await expect(page.locator('.lista-sessoes')).toContainText('S-');
  await expect(page.locator('.lista-sessoes')).not.toContainText('Pintar com o dedo');

  // voltando à atividade, imprimir cria a sessão e abre a prévia
  await page.goBack();
  await page.getByRole('button', { name: /Imprimir esta atividade/ }).click();
  await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();
  await page.getByRole('link', { name: 'Início' }).click();
  await expect(page.locator('.lista-sessoes')).toContainText('Pintar com o dedo');
});

test('voltar da atividade mantém a busca da lista', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('button', { name: /Explorar com uma família de exemplo/ }).click();
  await page.getByRole('link', { name: 'Atividades', exact: true }).click();
  await page.getByRole('searchbox').fill('feira');
  await page.locator('[data-atividade="atv-feira-numeros"]').getByRole('link').click();
  await page
    .getByRole('link', { name: /Voltar às atividades/ })
    .first()
    .click();
  await expect(page.getByRole('searchbox')).toHaveValue('feira');
  await expect(page.locator('[data-atividade="atv-caca-silabas"]')).toHaveCount(0);
});

test('atividade inexistente mostra a mensagem', async ({ page }) => {
  await page.goto('./#/atividade/nao-existe');
  await expect(page.getByRole('heading', { name: 'Atividade não encontrada' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Voltar às atividades' })).toBeVisible();
});

for (const largura of [320, 390]) {
  test(`página da atividade sem rolagem horizontal em ${largura}px e sem rede externa`, async ({
    page,
  }) => {
    const externas: string[] = [];
    page.on('request', (r) => {
      const u = new URL(r.url());
      const permitido = /^(localhost|127\.0\.0\.1)(:|$)|^fonts\.(googleapis|gstatic)\.com$/;
      if (u.protocol.startsWith('http') && !permitido.test(u.host)) externas.push(r.url());
    });
    await page.setViewportSize({ width: largura, height: 800 });
    await page.goto('./');
    await page.getByRole('button', { name: /Explorar com uma família de exemplo/ }).click();
    await expect(page.getByRole('heading', { name: /Olá/ })).toBeVisible();
    await page.evaluate(() => (location.hash = '#/atividade/atv-cad-pintar-com-o-dedo'));
    await expect(page.getByRole('heading', { name: 'Pintar com o dedo', level: 1 })).toBeVisible();
    const rolagem = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(rolagem).toBeLessThanOrEqual(0);
    expect(externas).toEqual([]);
  });
}

// #130: 20 por vez, "Ver mais 20", contagem para leitor de tela e "Limpar filtros".
test('lista paginada de 20 em 20, com contagem e limpar filtros', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('button', { name: /Explorar com uma família de exemplo/ }).click();
  await page.getByRole('link', { name: 'Atividades', exact: true }).click();

  const cartoes = page.locator('[data-atividade]');
  const contagem = page.locator('#contagem-atividades');
  await expect(cartoes).toHaveCount(20);
  await expect(contagem).toHaveAttribute('aria-live', 'polite');
  await expect(contagem).toHaveText(/^Mostrando 20 de \d+ atividades$/);
  await expect(page.getByRole('button', { name: 'Limpar filtros' })).toBeHidden();

  await page.getByRole('button', { name: 'Ver mais 20' }).click();
  await expect(cartoes).toHaveCount(40);
  await expect(contagem).toHaveText(/^Mostrando 40 de \d+ atividades$/);

  // qualquer filtro volta aos primeiros 20 e oferece "Limpar filtros"
  await page.getByLabel('Duração').selectOption('60');
  await expect(page.getByRole('button', { name: 'Limpar filtros' })).toBeVisible();
  await expect(cartoes.first()).toBeVisible();
  expect(await cartoes.count()).toBeLessThanOrEqual(20);

  // sem resultado: mensagem e a mesma saída
  await page.getByRole('searchbox').fill('zzzzqqqq');
  await expect(page.getByText('Nenhuma atividade encontrada. Tente')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Limpar filtros' })).toBeVisible();

  await page.getByRole('button', { name: 'Limpar filtros' }).click();
  await expect(page.getByRole('searchbox')).toHaveValue('');
  await expect(page.getByLabel('Duração')).toHaveValue('');
  await expect(cartoes).toHaveCount(20);
  await expect(contagem).toHaveText(/^Mostrando 20 de \d+ atividades$/);
  await expect(page.getByRole('button', { name: 'Limpar filtros' })).toBeHidden();
});

for (const largura of [320, 390]) {
  test(`lista de atividades sem rolagem horizontal em ${largura}px`, async ({ page }) => {
    await page.setViewportSize({ width: largura, height: 800 });
    await page.goto('./');
    await page.getByRole('button', { name: /Explorar com uma família de exemplo/ }).click();
    await page.getByRole('link', { name: 'Atividades', exact: true }).click();
    await page.getByRole('searchbox').fill('a');
    await expect(page.getByRole('button', { name: 'Limpar filtros' })).toBeVisible();
    const rolagem = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(rolagem).toBeLessThanOrEqual(0);
  });
}
