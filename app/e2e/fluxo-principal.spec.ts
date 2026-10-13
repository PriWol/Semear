import { expect, test, type Page } from '@playwright/test';
import { readFile } from 'node:fs/promises';

// Fluxo principal da v1: cadastrar família e criança, posicionar na jornada, gerar e baixar o pacote.

async function cadastrarFamiliaECrianca(page: Page) {
  await page.goto('./');
  await page.getByRole('link', { name: 'Começar' }).click();

  await page.getByLabel('Seu nome (educador)').fill('Maria');
  await page.getByRole('radio', { name: /Montessori/ }).check();
  await page.locator('input[name=inspiracoes][value=Waldorf]').check();
  await page.getByRole('button', { name: 'Continuar' }).click();

  await expect(page.getByRole('heading', { name: 'Adicionar criança' })).toBeVisible();
  await page.getByLabel('Nome').fill('Ana');
  await page.getByLabel('Data de nascimento').fill('2021-03-15');
  await page.getByRole('button', { name: 'Salvar' }).click();
  await expect(page.getByRole('heading', { name: /Jornada de Ana/ })).toBeVisible();
}

/** Localiza um marco na jornada pelo id (o título também pode aparecer em "Aguardando: …"). */
function marco(page: Page, id: string) {
  return page.locator(`li.marco[data-marco="${id}"]`);
}

test.beforeEach(async ({ page }) => {
  page.on('dialog', (d) => void d.accept());
});

test('primeiro acesso até baixar o pacote da sessão', async ({ page }) => {
  await cadastrarFamiliaECrianca(page);

  // Posiciona em Linguagem e confere o marco ativo
  await marco(page, 'LG.FON.04').getByRole('button', { name: 'Está aqui' }).click();
  await expect(marco(page, 'LG.FON.04')).toContainText('trabalhando agora');
  await expect(
    marco(page, 'LG.FON.03').getByRole('button', { name: /Consolidado/ }),
  ).toHaveAttribute('aria-pressed', 'true');

  // Posiciona em Matemática
  await page.getByRole('link', { name: /Matemática/ }).click();
  await marco(page, 'MA.SEN.06').getByRole('button', { name: 'Está aqui' }).click();
  await expect(marco(page, 'MA.SEN.06')).toContainText('trabalhando agora');

  // Prepara a sessão focada em Consciência fonológica
  await page.getByRole('link', { name: 'Preparar sessão' }).click();
  await page.getByRole('radio', { name: /Escolher linhas/ }).check();
  await page.getByRole('checkbox', { name: /Consciência fonológica/ }).check();
  await page.getByRole('button', { name: 'Sugerir atividades' }).click();
  await expect(page.locator('#proposta')).toContainText('Caça às sílabas');
  await expect(page.locator('#proposta')).toContainText('Ou Isto ou Aquilo');
  await page.getByRole('button', { name: 'Gerar pacote' }).click();

  // Página da sessão: prévia e download
  await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();
  const previa = page.frameLocator('#previa');
  await expect(previa.getByText('Ligue as figuras que começam igual')).toBeVisible();
  await expect(previa.locator('body')).toHaveClass(/letra-cursiva/); // Montessori começa na cursiva

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: /Baixar arquivo/ }).click(),
  ]);
  expect(download.suggestedFilename()).toMatch(/^semear-s-\d{4}-a1-ana\.html$/);
  const html = await readFile((await download.path())!, 'utf-8');
  expect(html).toContain('Caça às sílabas');
  expect(html).toContain('Ficha de registro rápido');

  // A sessão aparece no início
  await page.getByRole('link', { name: 'Início' }).click();
  await expect(page.locator('.lista-sessoes')).toContainText('Ana');
});

test('os dados continuam no aparelho depois de recarregar', async ({ page }) => {
  await cadastrarFamiliaECrianca(page);
  await page.reload();
  await expect(page.getByRole('heading', { name: /Jornada de Ana/ })).toBeVisible();
  await page.getByRole('link', { name: 'Início' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Maria!' })).toBeVisible();
  await expect(page.locator('.alerta')).toContainText('ainda não fez nenhum backup');
});

test('backup: baixar, apagar tudo e restaurar', async ({ page }) => {
  await cadastrarFamiliaECrianca(page);
  await page.getByRole('link', { name: 'Config.' }).click();

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Baixar backup' }).click(),
  ]);
  const arquivo = (await download.path())!;
  await expect(page.getByText(/Último backup: \d{2}\/\d{2}\/\d{4}/)).toBeVisible();

  await page.getByRole('button', { name: 'Apagar tudo' }).click();
  await expect(page.getByRole('heading', { name: 'Bem-vindo ao Semear' })).toBeVisible();

  await page.getByRole('link', { name: 'Config.' }).click();
  await page.locator('#importar').setInputFiles(arquivo);
  await expect(page.getByRole('heading', { name: 'Olá, Maria!' })).toBeVisible();
  await expect(page.locator('.crianca-cartao')).toContainText('Ana');
});

test('arquivo de backup inválido não apaga os dados', async ({ page }) => {
  await cadastrarFamiliaECrianca(page);
  await page.getByRole('link', { name: 'Config.' }).click();
  await page.locator('#importar').setInputFiles({
    name: 'errado.json',
    mimeType: 'application/json',
    buffer: Buffer.from('{"app":"outro"}'),
  });
  await page.getByRole('link', { name: 'Início' }).click();
  await expect(page.locator('.crianca-cartao')).toContainText('Ana');
});
