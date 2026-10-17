import { expect, test, type Page } from '@playwright/test';

// "Para os pais": texto pedagógico de cada marco, recolhido por padrão e adaptado à vertente da família.

async function cadastrarFamiliaECrianca(page: Page) {
  await page.goto('./');
  await page.getByRole('link', { name: 'Começar' }).click();
  await page.getByLabel('Seu nome (educador)').fill('Maria');
  await page.getByRole('radio', { name: /Montessori/ }).check();
  await page.locator('input[name=inspiracoes][value=Waldorf]').check();
  await page.getByRole('button', { name: 'Continuar' }).click();
  // Espera a tela renderizar: preencher antes disso perde o texto (como no helper de fluxo-principal).
  await expect(page.getByRole('heading', { name: 'Adicionar criança' })).toBeVisible();
  await page.getByLabel('Nome').fill('Ana');
  await page.getByLabel('Data de nascimento').fill('2021-03-15');
  await page.getByRole('button', { name: 'Salvar' }).click();
  await expect(page.getByRole('heading', { name: /Jornada de Ana/ })).toBeVisible();
}

function marco(page: Page, id: string) {
  return page.locator(`li.marco[data-marco="${id}"]`);
}

test('o texto para os pais fica recolhido e abre sob demanda', async ({ page }) => {
  await cadastrarFamiliaECrianca(page);
  const bloco = marco(page, 'LG.FON.04').locator('details.para-os-pais');

  await expect(bloco).not.toHaveAttribute('open', '');
  await expect(bloco.getByText('Por que importa')).toBeHidden();

  await bloco.getByText('Para os pais').click();
  await expect(bloco.getByText('Por que importa')).toBeVisible();
  await expect(bloco.getByText('Sinais de atenção')).toBeVisible();
});

test('mostra a vertente principal, as inspirações e as referências da família', async ({
  page,
}) => {
  await cadastrarFamiliaECrianca(page);
  const bloco = marco(page, 'LG.FON.04').locator('details.para-os-pais');
  await bloco.getByText('Para os pais').click();

  await expect(bloco.getByRole('heading', { name: 'Na pedagogia Montessori' })).toBeVisible();
  await expect(bloco.getByRole('heading', { name: 'Inspiração Waldorf' })).toBeVisible();
  // A idade vem do marco ({idade}), mesmo sem o aviso de ritmo (que só existe para a vertente principal).
  await expect(bloco.locator('.para-os-pais-texto')).toContainText('por volta dos 6,5 anos');
  await expect(bloco.locator('.para-os-pais-texto')).not.toContainText('aviso acima');
  // vertentes que a família não escolheu não aparecem
  await expect(bloco.getByRole('heading', { name: /Clássico/ })).toHaveCount(0);

  await expect(bloco.getByRole('heading', { name: 'Para saber mais' })).toBeVisible();
  await expect(bloco.locator('.referencias')).toContainText('MORAIS, Artur Gomes de');
  await expect(bloco.locator('.referencias')).toContainText('MONTESSORI, Maria');
  await expect(bloco.locator('.referencias')).not.toContainText('MASON');
});

test('abrir o texto não muda o estado do marco, e marcar o estado não fecha o texto', async ({
  page,
}) => {
  await cadastrarFamiliaECrianca(page);
  const m = marco(page, 'LG.FON.04');
  const naoObservado = m.getByRole('button', { name: /Não observado/ });
  await expect(naoObservado).toHaveAttribute('aria-pressed', 'true');

  await m.getByText('Para os pais').click();
  await expect(naoObservado).toHaveAttribute('aria-pressed', 'true');

  await m.getByRole('button', { name: /Em desenvolvimento/ }).click();
  await expect(m.getByRole('button', { name: /Em desenvolvimento/ })).toHaveAttribute(
    'aria-pressed',
    'true',
  );
  await expect(m.getByText('Por que importa')).toBeVisible();
});

test('Matemática também traz o texto para os pais', async ({ page }) => {
  await cadastrarFamiliaECrianca(page);
  await page.getByRole('link', { name: /Matemática/ }).click();
  const bloco = marco(page, 'MA.SEN.03').locator('details.para-os-pais');

  await expect(bloco.getByText('Por que importa')).toBeHidden();
  await bloco.getByText('Para os pais').click();
  await expect(bloco.getByRole('heading', { name: 'Na pedagogia Montessori' })).toBeVisible();
  await expect(bloco.locator('.referencias')).toContainText('KAMII, Constance');
});

test('a linha Operações aparece com texto para os pais e pré-requisito de outra linha', async ({
  page,
}) => {
  await cadastrarFamiliaECrianca(page);
  await page.getByRole('link', { name: /Matemática/ }).click();
  await expect(page.getByRole('heading', { name: 'Operações' })).toBeVisible();

  const m = marco(page, 'MA.OPE.04');
  // MA.OPE.04 depende de MA.SEN.07 e MA.OPE.02, que ainda não estão consolidados
  await expect(m).toContainText('Aguardando');
  await m.getByText('Para os pais').click();
  await expect(m.getByRole('heading', { name: 'Na pedagogia Montessori' })).toBeVisible();
  await expect(m.locator('.referencias')).toContainText('NUNES, Terezinha; BRYANT, Peter');
});

test('a linha Sistema de numeração mostra o texto e a idade de introdução da pedagogia Waldorf', async ({
  page,
}) => {
  await cadastrarFamiliaECrianca(page);
  await page.getByRole('link', { name: /Matemática/ }).click();
  await expect(page.getByRole('heading', { name: /Sistema de numeração/ })).toBeVisible();

  const m = marco(page, 'MA.SND.03');
  await m.getByText('Para os pais').click();
  await expect(m.getByRole('heading', { name: 'Na pedagogia Montessori' })).toBeVisible();
  await expect(m.getByRole('heading', { name: 'Inspiração Waldorf' })).toBeVisible();
  // A idade vem do marco ({idade}), mesmo sem o aviso de ritmo (Waldorf aqui é só inspiração).
  await expect(m.locator('.para-os-pais-texto')).toContainText('por volta dos 7 anos');
  await expect(m.locator('.para-os-pais-texto')).not.toContainText('aviso acima');
});

test('a linha Escrita mostra a idade Waldorf já preenchida, sem o marcador {idade}', async ({
  page,
}) => {
  await cadastrarFamiliaECrianca(page);
  await expect(page.getByRole('heading', { name: 'Escrita', exact: true })).toBeVisible();

  const m = marco(page, 'LG.ESC.05');
  await m.getByText('Para os pais').click();
  await expect(m.getByRole('heading', { name: 'Na pedagogia Montessori' })).toBeVisible();
  await expect(m.getByRole('heading', { name: 'Inspiração Waldorf' })).toBeVisible();
  await expect(m.locator('.para-os-pais-texto')).toContainText('por volta dos 7 anos');
  await expect(m.locator('.para-os-pais-texto')).not.toContainText('{idade}');
  await expect(m.locator('.referencias')).toContainText('FERREIRO, Emilia; TEBEROSKY, Ana');
});
