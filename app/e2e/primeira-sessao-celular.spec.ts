import { expect, test, type Locator, type Page } from '@playwright/test';

// #173: protege o caminho curto da primeira sessão no celular. Sem analytics (privacidade), este teste é a única
// proteção contra o caminho crescer sem querer. Mede toques e digitações, nunca tempo (tempo de máquina é instável).
// O orçamento está no ROADMAP; baixá-lo (meta: 5) só depois de melhorar a tela "Pronto" (estória B).
const ORCAMENTO = { toques: 7, digitacoes: 3 };

// Única chamada externa permitida hoje (CLAUDE.md, Privacidade): as fontes do Google.
const HOSTS_PERMITIDOS = new Set(['localhost:4173', 'fonts.googleapis.com', 'fonts.gstatic.com']);

test.use({ viewport: { width: 390, height: 844 } });

type Toque = { passo: string; rotulo: string };

function listar(toques: Toque[]): string {
  return toques.map((t, i) => `${i + 1}. ${t.rotulo} (${t.passo})`).join('\n');
}

function criarContadores() {
  const toques: Toque[] = [];
  let digitacoes = 0;
  return {
    toques,
    digitacoes: () => digitacoes,
    // Todo clique em botão ou link passa por aqui; estoura na hora, com a lista de cada toque.
    async tocar(passo: string, rotulo: string, alvo: Locator) {
      toques.push({ passo, rotulo });
      expect(
        toques.length,
        `Orçamento de ${ORCAMENTO.toques} toques estourado. Toques até aqui:\n${listar(toques)}`,
      ).toBeLessThanOrEqual(ORCAMENTO.toques);
      await alvo.click();
    },
    async digitar(campo: Locator, valor: string) {
      digitacoes += 1;
      await campo.fill(valor);
    },
  };
}

async function semRolagemLateral(page: Page, tela: string) {
  const excesso = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(excesso, `rolagem lateral na tela "${tela}"`).toBeLessThanOrEqual(0);
}

function nascimentoCincoAnosAtras(): string {
  // Calculado aqui (e não fixo) para a criança não sair da faixa com o passar dos anos.
  const d = new Date();
  d.setFullYear(d.getFullYear() - 5);
  d.setMonth(d.getMonth() - 1);
  return d.toISOString().slice(0, 10);
}

test('família nova chega à prévia da primeira sessão em até 7 toques e 3 digitações', async ({
  page,
}) => {
  const externos: string[] = [];
  page.on('request', (req) => {
    const url = new URL(req.url());
    if (['data:', 'blob:', 'about:'].includes(url.protocol)) return;
    if (!HOSTS_PERMITIDOS.has(url.host)) externos.push(req.url());
  });

  const c = criarContadores();

  await page.goto('./');
  // Família nova: navegador limpo, boas-vindas sem dados e sem a família de exemplo (CA4).
  await expect(page.getByRole('link', { name: 'Começar' })).toBeVisible();
  await semRolagemLateral(page, 'boas-vindas');
  await c.tocar('boas-vindas', 'link "Começar"', page.getByRole('link', { name: 'Começar' }));

  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  await c.digitar(page.locator('[name=educador]'), 'Marta Fictícia');
  await semRolagemLateral(page, 'família');
  await c.tocar('família', 'botão "Continuar"', page.getByRole('button', { name: 'Continuar' }));

  await expect(page.getByRole('heading', { name: 'Adicionar criança' })).toBeVisible();
  await c.digitar(page.locator('[name=nome]'), 'Lia');
  await c.digitar(page.locator('[name=nascimento]'), nascimentoCincoAnosAtras());
  await semRolagemLateral(page, 'criança');
  await c.tocar('criança', 'botão "Salvar"', page.getByRole('button', { name: 'Salvar' }));

  await expect(page.getByRole('heading', { name: 'Pronto, Lia está cadastrada' })).toBeVisible();
  await semRolagemLateral(page, 'pronto');
  await c.tocar(
    'pronto',
    'link "Preparar a primeira sessão"',
    page.getByRole('link', { name: 'Preparar a primeira sessão' }),
  );

  await expect(page.getByRole('button', { name: 'Sugerir atividades' })).toBeVisible();
  await semRolagemLateral(page, 'preparar sessão');
  await c.tocar(
    'preparar sessão',
    'botão "Sugerir atividades"',
    page.getByRole('button', { name: 'Sugerir atividades' }),
  );

  await expect(page.getByRole('button', { name: 'Gerar pacote' })).toBeVisible();
  await c.tocar(
    'sugestão',
    'botão "Gerar pacote"',
    page.getByRole('button', { name: 'Gerar pacote' }),
  );

  // CA1: a prévia aparece sozinha e "Imprimir / salvar PDF" está visível e ativo.
  await expect(page).toHaveURL(/#\/sessao\/(?!nova)/);
  await expect(page.locator('#previa')).toBeVisible();
  await expect(page.locator('#previa')).toHaveAttribute('sandbox', /.+/);
  await expect(page.frameLocator('#previa').locator('body')).toBeVisible();
  const imprimir = page.getByRole('button', { name: 'Imprimir / salvar PDF' });
  await expect(imprimir).toBeVisible();
  await expect(imprimir).toBeEnabled();
  await semRolagemLateral(page, 'sessão');
  // A impressão acontece num quadro isolado e não é medível aqui; só conta o toque.
  await c.tocar('sessão', 'botão "Imprimir / salvar PDF"', imprimir);

  expect(page.url()).not.toContain('exemplo');
  expect(c.toques.length, `Toques:\n${listar(c.toques)}`).toBeLessThanOrEqual(ORCAMENTO.toques);
  expect(c.digitacoes(), 'digitações').toBeLessThanOrEqual(ORCAMENTO.digitacoes);
  expect(externos, `pedidos de rede fora dos hosts permitidos:\n${externos.join('\n')}`).toEqual(
    [],
  );
});
