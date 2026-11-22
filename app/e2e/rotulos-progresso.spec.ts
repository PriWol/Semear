import { expect, test, type Page } from '@playwright/test';

// QA2-11 (links repetidos com o nome da criança) e QA2-05 (progresso com unidade e legenda dos ícones).

async function abrirExemplo(page: Page) {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
}

test('Início: links e botões repetidos por criança dizem de quem são, sem mudar o texto visível', async ({
  page,
}) => {
  await abrirExemplo(page);
  const cartao = page
    .locator('.crianca-cartao')
    .filter({ has: page.getByRole('heading', { name: 'Ana', exact: true }) });
  const editar = cartao.getByRole('link', { name: 'Editar Ana', exact: true });
  await expect(editar).toBeVisible();
  await expect(editar).toHaveText('editar');
  await expect(
    cartao.getByRole('link', { name: 'Preparar sessão de Ana', exact: true }),
  ).toHaveText('Preparar sessão');
  await expect(
    cartao.getByRole('link', { name: 'Registrar sessão de Ana', exact: true }),
  ).toHaveText('Registrar sessão');
  await expect(
    cartao.getByRole('link', { name: 'Planejar semana de Ana', exact: true }),
  ).toHaveText('Planejar semana');
  await expect(
    cartao.getByRole('link', { name: /^(Ver jornada|Posicionar) de Ana$/ }),
  ).toBeVisible();
});

test('Início: o progresso diz "N de M marcos consolidados" e a barra tem nome', async ({
  page,
}) => {
  await abrirExemplo(page);
  const item = page.locator('.progresso-dominios li').first();
  await expect(item.locator('.nota')).toHaveText(/^\d+ de \d+ marcos consolidados$/);
  await expect(item.locator('progress')).toHaveAttribute(
    'aria-label',
    /^.+: \d+ de \d+ marcos consolidados$/,
  );
});

test('Jornada: progresso por extenso e legenda dos três ícones de estado', async ({ page }) => {
  await abrirExemplo(page);
  await page.goto('./#/jornada/exemplo-ana');
  await expect(page.getByRole('heading', { name: /Jornada de Ana/ })).toBeVisible();

  await expect(page.locator('.linha header .nota').first()).toHaveText(
    /^\d+ de \d+ marcos consolidados$/,
  );
  const legenda = page.getByRole('list', { name: 'Legenda dos estados' });
  await expect(legenda).toBeVisible();
  await expect(legenda.getByRole('listitem')).toHaveText([
    /Não observado/,
    /Em desenvolvimento/,
    /Consolidado/,
  ]);
});
