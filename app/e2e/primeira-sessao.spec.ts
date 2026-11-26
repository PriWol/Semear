import { expect, test, type Page } from '@playwright/test';

// Estória #173 (A): protege o caminho curto da primeira sessão no celular. Família nova (sem o exemplo),
// do "Começar" até a prévia com "Imprimir / salvar PDF". O orçamento conta botões e links tocados;
// digitar não conta. Se uma tela nova entrar no caminho, o teste falha e mostra cada toque.

const ORCAMENTO_DE_TOQUES = 7;
// O 7º toque do orçamento é o próprio "Imprimir / salvar PDF": o teste só confere que ele está à vista e
// habilitado (imprimir abre o diálogo do sistema), mas o orçamento o reserva.
const TOQUE_DE_IMPRIMIR = 1;
const HOSTS_PERMITIDOS = ['fonts.googleapis.com', 'fonts.gstatic.com'];

// Largura fixa: o projeto "celular" (Pixel 7) tem 412 px, e o orçamento vale para o celular mais estreito comum.
test.use({ viewport: { width: 390, height: 844 } });

/** Registra só toques de verdade (isTrusted) em botão, link ou role=button, guardando o texto do alvo. */
async function contarToques(page: Page): Promise<void> {
  await page.addInitScript(() => {
    const w = window as unknown as { __toques: string[] };
    w.__toques = [];
    document.addEventListener(
      'click',
      (event) => {
        if (!event.isTrusted || !(event.target instanceof Element)) return;
        const alvo = event.target.closest('button, a, [role=button]');
        if (!alvo) return;
        const texto = (alvo.textContent ?? '').replace(/\s+/g, ' ').trim();
        w.__toques.push(texto || alvo.getAttribute('aria-label') || alvo.tagName.toLowerCase());
      },
      true,
    );
  });
}

const toques = (page: Page) =>
  page.evaluate(() => (window as unknown as { __toques: string[] }).__toques);

const semRolagemHorizontal = (page: Page) =>
  page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth);

test('primeira sessão de uma família nova em até 7 toques, sem rolagem lateral nem rede externa', async ({
  page,
}) => {
  const externas: string[] = [];
  page.on('request', (r) => {
    const url = new URL(r.url());
    const local =
      ['localhost', '127.0.0.1'].includes(url.hostname) || /^(data|blob):$/.test(url.protocol);
    if (!local && !HOSTS_PERMITIDOS.includes(url.hostname)) externas.push(r.url());
  });
  await contarToques(page);

  /** Confere, em cada tela do caminho, a largura e que nada é dado de exemplo. */
  const conferirTela = async (nome: string) => {
    expect(await semRolagemHorizontal(page), `rolagem lateral em "${nome}"`).toBe(true);
    // A faixa existe no HTML, oculta (hidden) fora do exemplo; "visível" é o que o educador veria.
    await expect(page.getByText('Você está vendo um exemplo')).toBeHidden();
  };

  await page.goto('./');
  await expect(page.getByRole('link', { name: 'Começar' })).toBeVisible();
  await conferirTela('Boas-vindas');
  await page.getByRole('link', { name: 'Começar' }).click();

  await page.getByLabel('Seu nome (educador)').fill('Maria');
  await conferirTela('Família');
  await page.getByRole('button', { name: 'Continuar' }).click();

  await expect(page.getByRole('heading', { name: 'Adicionar criança' })).toBeVisible();
  await page.getByLabel('Nome').fill('Ana');
  // Nascimento relativo a hoje: sempre 5 anos, sem depender da data da execução.
  const nascimento = new Date();
  nascimento.setFullYear(nascimento.getFullYear() - 5);
  nascimento.setMonth(nascimento.getMonth() - 1);
  await page.getByLabel('Data de nascimento').fill(nascimento.toISOString().slice(0, 10));
  await conferirTela('Criança');
  await page.getByRole('button', { name: 'Salvar' }).click();

  await expect(page.getByRole('heading', { name: 'Pronto, Ana está cadastrada' })).toBeVisible();
  await conferirTela('Pronto');
  await page.getByRole('link', { name: 'Preparar a primeira sessão' }).click();

  await expect(page.getByRole('button', { name: 'Sugerir atividades' })).toBeVisible();
  await conferirTela('Preparar sessão');
  await page.getByRole('button', { name: 'Sugerir atividades' }).click();

  await expect(page.locator('#proposta .escolhas li').first()).toBeVisible();
  await page.getByRole('button', { name: 'Gerar pacote' }).click();

  await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();
  await expect(page.locator('#previa')).toBeVisible();
  const imprimir = page.getByRole('button', { name: 'Imprimir / salvar PDF' });
  await expect(imprimir).toBeVisible();
  await expect(imprimir).toBeEnabled();
  await conferirTela('Sessão');

  const feitos = await toques(page);
  const lista = [...feitos, 'Imprimir / salvar PDF (reservado, não tocado)']
    .map((texto, i) => `  ${i + 1}. ${texto}`)
    .join('\n');
  const total = feitos.length + TOQUE_DE_IMPRIMIR;
  expect(
    total,
    `Orçamento de ${ORCAMENTO_DE_TOQUES} toques estourado: ${total} toques.\n${lista}`,
  ).toBeLessThanOrEqual(ORCAMENTO_DE_TOQUES);
  expect(externas, 'pedidos de rede fora do app e das fontes do Google').toEqual([]);
});
