import { expect, test, type Page } from '@playwright/test';
import { abrirAjustes } from './ajustes-ajuda';
import { irParaJornadaDepoisDeCadastrar } from './cadastro';

// Estória #140 (SEG-1 a SEG-5): dados impossíveis são recusados com mensagem clara, o nome fictício do
// exemplo não vaza e a criança padrão é a que a família está usando.

async function comExemplo(page: Page) {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
}

const cartaoDaCopia = (page: Page) =>
  page.locator('section', { has: page.getByRole('heading', { name: 'Cópia de segurança' }) });

test('cópia com crianças e sem família é recusada, dentro do cartão da cópia', async ({ page }) => {
  await comExemplo(page);
  await abrirAjustes(page);
  const copia = {
    app: 'semear',
    versao: 1,
    exportadoEm: '2026-11-01T10:00:00.000Z',
    familia: null,
    criancas: [{ id: 'c1', nome: 'Ana', nascimento: '2021-03-15', letra: null, trilhas: [] }],
    estados: [],
    historico: [],
    sessoes: [],
  };
  await page.locator('#importar').setInputFiles({
    name: 'sem-familia.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify(copia)),
  });
  const erro = cartaoDaCopia(page).locator('.alerta.erro');
  await expect(erro).toBeVisible();
  await expect(erro).toHaveText(
    'Este arquivo tem crianças, mas não tem a família. Não foi possível restaurar.',
  );
  // Nada foi substituído: a família de exemplo continua lá.
  await expect(page.getByText('Família Marina · 2 crianças')).toBeVisible();
});

test('cópia de 11 MB é recusada antes de ler', async ({ page }) => {
  await comExemplo(page);
  await abrirAjustes(page);
  await page.locator('#importar').setInputFiles({
    name: 'enorme.json',
    mimeType: 'application/json',
    buffer: Buffer.alloc(11 * 1024 * 1024, 0x20), // 11 MB de espaços
  });
  const erro = cartaoDaCopia(page).locator('.alerta.erro');
  await expect(erro).toBeVisible();
  await expect(erro).toContainText('mais de 10 MB');
  await expect(page.getByText('Família Marina · 2 crianças')).toBeVisible();
});

test('nascimento no futuro é recusado no formulário, com mensagem fixa', async ({ page }) => {
  await comExemplo(page);
  await page.goto('./#/crianca/nova');
  await page.getByLabel('Nome').fill('Bia');
  await page.getByLabel('Data de nascimento').fill('2099-01-01');
  await page.getByRole('button', { name: 'Salvar' }).click();
  const erro = page.locator('#erro-nascimento');
  await expect(erro).toBeVisible();
  await expect(erro).toContainText('não pode ser no futuro');
  await expect(page.getByRole('heading', { name: 'Adicionar criança' })).toBeVisible();
  await page.goto('./#/');
  await expect(page.locator('.crianca-cartao')).toHaveCount(2); // nada foi gravado
});

test('fora de 2 a 8 anos: aviso fixo no formulário, e ainda dá para salvar', async ({ page }) => {
  await comExemplo(page);
  await page.goto('./#/crianca/nova');
  const aviso = page.locator('#aviso-faixa');
  await expect(aviso).toBeHidden();
  await page.getByLabel('Nome').fill('Caio');
  const ano = new Date().getFullYear() - 12;
  await page.getByLabel('Data de nascimento').fill(`${ano}-03-15`);
  await expect(aviso).toBeVisible();
  await expect(aviso).toContainText('2 a 8 anos');
  await page.getByLabel('Data de nascimento').fill(`${new Date().getFullYear() - 5}-03-15`);
  await expect(aviso).toBeHidden();
  await page.getByLabel('Data de nascimento').fill(`${ano}-03-15`);
  await page.getByRole('button', { name: 'Salvar' }).click();
  await irParaJornadaDepoisDeCadastrar(page, 'Caio');
});

test('apagar o exemplo mantendo criança real deixa o nome da família pendente, sem "Marina"', async ({
  page,
}) => {
  await comExemplo(page);
  await page.goto('./#/crianca/nova'); // dentro do exemplo, "Adicionar criança" continua livre
  await page.getByLabel('Nome').fill('Lia');
  await page.getByLabel('Data de nascimento').fill(`${new Date().getFullYear() - 5}-03-15`);
  await page.getByRole('button', { name: 'Salvar' }).click();
  await irParaJornadaDepoisDeCadastrar(page, 'Lia');

  page.on('dialog', (d) => void d.accept()); // a faixa global do exemplo ainda usa o confirm()
  await page.locator('#faixa-exemplo').getByRole('button', { name: 'Apagar exemplo' }).click();

  // A tela da família abre com o nome vazio e um aviso fixo (não só o balão).
  await expect(page.getByRole('heading', { name: 'Família' })).toBeVisible();
  await expect(page.getByLabel('Seu nome (educador)')).toHaveValue('');
  await expect(page.locator('#pendencia-nome')).toContainText('Falta o seu nome');

  // O Início continua pedindo, e "Marina" não aparece em lugar nenhum.
  await page.goto('./#/');
  await expect(page.locator('#pendencia-nome')).toContainText('Complete o nome da família');
  await expect(page.locator('.crianca-cartao')).toContainText('Lia');
  await expect(page.locator('body')).not.toContainText('Marina');

  // Apagar a criança real em seguida também não traz o nome fictício de volta.
  await page.goto('./#/familia');
  await page.getByLabel('Seu nome (educador)').fill('Priscila');
  await page.getByRole('button', { name: 'Salvar' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Priscila!' })).toBeVisible();
  await expect(page.locator('#pendencia-nome')).toHaveCount(0);
});

test('a criança padrão é a da sessão mais recente (preparar sessão e atividade avulsa)', async ({
  page,
}) => {
  await comExemplo(page);
  // Theo (7) é o mais velho e abre a lista; a Ana vira a padrão ao receber a sessão mais recente.
  await page.goto('./#/sessao/nova?crianca=exemplo-ana');
  await page.getByRole('button', { name: 'Sugerir atividades' }).click();
  await page.getByRole('button', { name: 'Gerar pacote' }).click();
  await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();

  await page.goto('./#/sessao/nova');
  await expect(page.locator('select[name=crianca]')).toHaveValue('exemplo-ana');

  await page.goto('./#/atividades');
  await page.locator('a[href^="#/atividade/"]').first().click();
  await expect(page.locator('#crianca-imprimir')).toHaveValue('exemplo-ana');

  // E a outra criança, quando recebe a sessão mais nova, passa a ser a padrão.
  await page.goto('./#/sessao/nova?crianca=exemplo-theo');
  await page.getByRole('button', { name: 'Sugerir atividades' }).click();
  await page.getByRole('button', { name: 'Gerar pacote' }).click();
  await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();
  await page.goto('./#/sessao/nova');
  await expect(page.locator('select[name=crianca]')).toHaveValue('exemplo-theo');
});
