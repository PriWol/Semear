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

test('editar a família de exemplo e cadastrar uma criança: apagar o exemplo não perde a criança', async ({
  page,
}) => {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();

  // A pessoa ignora o aviso: troca o nome da família e cadastra a própria criança.
  await page.goto('./#/familia');
  await page.getByLabel('Seu nome (educador)').fill('Priscila');
  await page.getByRole('button', { name: 'Salvar' }).click();
  // Espera a gravação terminar (o app volta ao início) antes de seguir: senão o próprio app,
  // ao terminar de salvar, leva a pessoa de volta ao início por cima da tela seguinte.
  await expect(page.getByRole('heading', { name: 'Olá, Priscila!' })).toBeVisible();
  await page.goto('./#/crianca/nova');
  await page.getByLabel('Nome').fill('Lia');
  await page.getByLabel('Data de nascimento').fill('2021-03-15');
  await page.getByRole('button', { name: 'Salvar' }).click();
  await expect(page.getByRole('heading', { name: /Jornada de Lia/ })).toBeVisible();

  await page.locator('#faixa-exemplo').getByRole('button', { name: 'Apagar exemplo' }).click();

  // Ana e Theo saem; a família fica (a Lia precisa dela) e a pessoa é levada a conferir os dados dela.
  await expect(page.getByRole('heading', { name: 'Família' })).toBeVisible();
  await expect(page.getByLabel('Seu nome (educador)')).toHaveValue('Priscila');
  await page.goto('./#/');
  await expect(page.getByRole('heading', { name: 'Olá, Priscila!' })).toBeVisible();
  await expect(page.locator('.crianca-cartao')).toHaveCount(1);
  await expect(page.locator('.crianca-cartao')).toContainText('Lia');
  await expect(page.locator('#faixa-exemplo')).toBeHidden();
});
