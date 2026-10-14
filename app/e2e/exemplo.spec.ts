import { expect, test } from '@playwright/test';

// Família de exemplo (#39): demonstrar o app em 1 minuto, sem cadastrar nada, e sair sem deixar rastro.

test.beforeEach(async ({ page }) => {
  page.on('dialog', (d) => void d.accept());
});

test('explorar o exemplo, preparar uma sessão e apagar o exemplo', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();

  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  const faixa = page.locator('#faixa-exemplo');
  await expect(faixa).toBeVisible();
  const ana = page.locator('.crianca-cartao', { hasText: 'Ana' });
  await expect(ana).toContainText('5 anos');
  await expect(page.locator('.crianca-cartao', { hasText: 'Theo' })).toContainText('7 anos');
  await expect(page.locator('.lista-sessoes li')).toHaveCount(3);
  // O exemplo não dispara o lembrete de backup.
  await expect(page.locator('.alerta')).toHaveCount(0);

  // A Ana já está posicionada: dá para preparar uma sessão direto.
  await ana.getByRole('link', { name: 'Preparar sessão' }).click();
  await page.getByRole('button', { name: 'Sugerir atividades' }).click();
  await expect(page.locator('#proposta')).toContainText(/Caça às sílabas|Feira dos números/);
  await page.getByRole('button', { name: 'Gerar pacote' }).click();
  await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();
  await expect(faixa).toBeVisible();

  // Tentar cadastrar uma criança no exemplo mostra o aviso para começar de verdade.
  await page.goto('./#/crianca/nova');
  await expect(page.locator('#aviso-exemplo')).toContainText('Você está no exemplo');

  // Apagar o exemplo volta para as boas-vindas, e recarregar não traz nada de volta.
  await faixa.getByRole('button', { name: 'Apagar exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Bem-vindo ao Semear' })).toBeVisible();
  await expect(faixa).toBeHidden();
  await page.reload();
  await expect(page.getByRole('heading', { name: 'Bem-vindo ao Semear' })).toBeVisible();
});

test('"Começar com a minha família" apaga o exemplo e abre o cadastro', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();

  await page.goto('./#/familia');
  await page.getByRole('button', { name: 'Começar com a minha família' }).click();
  await expect(page.getByRole('heading', { name: 'Vamos conhecer sua família' })).toBeVisible();
  await expect(page.locator('#faixa-exemplo')).toBeHidden();
  await expect(page.getByLabel('Seu nome (educador)')).toHaveValue('');
});
