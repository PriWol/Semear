import { expect, test, type BrowserContext, type Page } from '@playwright/test';

// Selo único de conferência profissional (#147, #138 D2, ADR 0037). O conteúdo real ainda não traz o
// campo `conferenciaProfissional` (a migração é uma leva à parte), então estes testes marcam UM item
// como pendente NO TESTE: o script do build é reescrito em trânsito. app/content/ não muda.

const TEXTO = 'Orientação em conferência por profissional de saúde. Não substitui o pediatra.';
const ATIVIDADE_SEM_REVISAO = 'atv-caca-silabas';
const MARCO_SEM_REVISAO = 'LG.FON.04';
const ATIVIDADE_COM_MATERIAL = 'atv-cad-agua-na-bacia'; // tem revisao e materialImpresso (Biblioteca)

test.use({ serviceWorkers: 'block' });

const PENDENTE = 'conferenciaProfissional:{estado:`pendente`}';

/** Marca itens como pendentes no JavaScript do app (objetos literais do Vite: `{id:`...`,`). */
async function marcarPendentes(
  context: BrowserContext,
  itens: { id: string; temRevisao: boolean }[],
) {
  await context.route('**/assets/index-*.js', async (route) => {
    let js = await (await route.fetch()).text();
    for (const { id, temRevisao } of itens) {
      const alvo = id.replace(/\./g, '\\.');
      const antes = js;
      js = temRevisao
        ? js.replace(new RegExp(`(\\{id:\`${alvo}\`,[\\s\\S]*?revisao:\\{)`), `$1${PENDENTE},`)
        : js.replace(
            new RegExp(`\\{id:\`${alvo}\`,`),
            `{id:\`${id}\`,revisao:{estado:\`aprovado\`,por:\`Teste\`,em:\`2026-11-22\`,${PENDENTE}},`,
          );
      if (js === antes) throw new Error(`item ${id} não encontrado no bundle`);
    }
    await route.fulfill({ response: await route.fetch(), body: js });
  });
}

async function abrirExemplo(page: Page) {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
}

const selo = (page: Page) => page.getByRole('note').filter({ hasText: TEXTO });

async function semRolagemLateral(page: Page) {
  const excesso = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(excesso).toBeLessThanOrEqual(0);
}

for (const largura of [320, 390]) {
  test.describe(`largura ${largura}`, () => {
    test.use({ viewport: { width: largura, height: 800 } });

    test('atividade: o selo aparece uma vez quando há pendência', async ({ page, context }) => {
      await marcarPendentes(context, [{ id: ATIVIDADE_SEM_REVISAO, temRevisao: false }]);
      await abrirExemplo(page);
      await page.goto(`./#/atividade/${ATIVIDADE_SEM_REVISAO}`);
      await expect(selo(page)).toHaveCount(1);
      await expect(selo(page)).toBeVisible();
      await semRolagemLateral(page);
    });

    test('jornada: o selo aparece uma vez no domínio quando um marco está pendente', async ({
      page,
      context,
    }) => {
      await marcarPendentes(context, [{ id: MARCO_SEM_REVISAO, temRevisao: false }]);
      await abrirExemplo(page);
      await page.goto('./#/jornada/exemplo-ana');
      await expect(page.locator(`li.marco[data-marco="${MARCO_SEM_REVISAO}"]`)).toBeVisible();
      await expect(selo(page)).toHaveCount(1);
      await semRolagemLateral(page);
    });

    test('Biblioteca: o selo aparece quando um item do material impresso está pendente', async ({
      page,
      context,
    }) => {
      await marcarPendentes(context, [{ id: ATIVIDADE_COM_MATERIAL, temRevisao: true }]);
      await abrirExemplo(page);
      await page.goto('./#/biblioteca');
      await expect(selo(page)).toHaveCount(1);
      await semRolagemLateral(page);
    });
  });
}

test('sem pendência não há selo na atividade nem na Biblioteca (conteúdo real, sem o campo)', async ({
  page,
}) => {
  await abrirExemplo(page);
  await page.goto(`./#/atividade/${ATIVIDADE_SEM_REVISAO}`);
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  await expect(page.locator('.selo-conferencia')).toHaveCount(0);
  await page.goto('./#/biblioteca');
  await expect(page.getByRole('heading', { name: 'Biblioteca' })).toBeVisible();
  await expect(page.locator('.selo-conferencia')).toHaveCount(0);
});

test('"Para os pais" da Caderneta mantém "Não substitui o pediatra", mesmo sem pendência', async ({
  page,
}) => {
  await abrirExemplo(page);
  await page.goto('./#/jornada/exemplo-ana?d=DI');
  const bloco = page.locator('li.marco[data-marco="DI.CAD.01"] details.para-os-pais');
  await bloco.getByText('Para os pais').click();
  await expect(
    bloco.getByRole('note').filter({ hasText: 'Não substitui o pediatra.' }),
  ).toBeVisible();
  await expect(page.getByRole('note').filter({ hasText: 'em conferência' })).toHaveCount(0);
});
