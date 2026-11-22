import { expect, test, type Page } from '@playwright/test';
import { readFile } from 'node:fs/promises';

// #141 (D11, D24): semana seguinte no planejador, caixas próprias no lugar de confirm() e letra de
// imprensa aos 2 anos. O relógio do navegador é fixado em hora local (o app usa a data do aparelho).

// 2026-11-16 é segunda; 20 é sexta, 21 sábado, 22 domingo.
const em = (dia: number, h = 0, min = 0) => new Date(2026, 10, dia, h, min);

async function explorar(page: Page, quando: Date) {
  await page.clock.setFixedTime(quando);
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await page.goto('./#/semana/exemplo-ana');
}

const abas = (page: Page) => page.getByRole('navigation', { name: 'Semana a planejar' });

test('de sexta 12h a domingo a próxima semana vem escolhida; antes disso, a atual', async ({
  page,
}) => {
  const casos: [Date, string][] = [
    [em(16, 0, 0), 'Esta semana'], // segunda 00:00
    [em(20, 11, 59), 'Esta semana'], // sexta 11:59
    [em(20, 12, 0), 'Próxima semana'], // sexta 12:00
    [em(21, 10), 'Próxima semana'], // sábado
    [em(22, 23, 59), 'Próxima semana'], // domingo
    [em(23, 0, 0), 'Esta semana'], // segunda 00:00 seguinte
  ];
  await explorar(page, casos[0]![0]);
  for (const [quando, esperada] of casos) {
    // os dados do exemplo já estão no aparelho: só muda a hora e recarrega a tela
    await page.clock.setFixedTime(quando);
    await page.reload();
    await expect(abas(page).locator('[aria-current="page"]')).toHaveText(esperada);
  }
});

test('num sábado o plano sai com a próxima semana, sem dias passados', async ({ page }) => {
  await explorar(page, em(21, 10));
  await page.getByRole('button', { name: 'Planejar semana' }).click();
  const dias = page.locator('section.dia-plano');
  await expect(dias).toHaveCount(3);
  await expect(dias.nth(0)).toContainText('23/11');
  await expect(dias.nth(1)).toContainText('25/11');
  await expect(dias.nth(2)).toContainText('27/11');
  await expect(page.locator('section.dia-plano.passado')).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Marcar como feito' })).toHaveCount(3);

  // "Esta semana" continua acessível: planeja 16, 18 e 20, todos já passados, esmaecidos e sem o botão.
  await abas(page).getByRole('link', { name: 'Esta semana' }).click();
  await expect(abas(page).locator('[aria-current="page"]')).toHaveText('Esta semana');
  await page.getByRole('button', { name: 'Planejar semana' }).click();
  await expect(dias).toHaveCount(3);
  await expect(page.locator('section.dia-plano.passado')).toHaveCount(3);
  await expect(page.getByRole('button', { name: 'Marcar como feito' })).toHaveCount(0);
  await expect(dias.first()).toContainText('Este dia já passou');

  // O plano da próxima semana segue guardado, ao lado do desta.
  await abas(page).getByRole('link', { name: 'Próxima semana' }).click();
  await expect(page.locator('section.dia-plano').first()).toContainText('23/11');
});

test('numa quarta, só os dias anteriores a hoje ficam esmaecidos', async ({ page }) => {
  await explorar(page, em(18, 15)); // quarta, esta semana por padrão
  await page.getByRole('button', { name: 'Planejar semana' }).click();
  const dias = page.locator('section.dia-plano');
  await expect(dias.nth(0)).toHaveClass(/passado/); // segunda
  await expect(dias.nth(1)).not.toHaveClass(/passado/); // quarta (hoje)
  await expect(dias.nth(1).getByRole('button', { name: 'Marcar como feito' })).toBeVisible();
  await expect(dias.nth(0).getByRole('button', { name: 'Marcar como feito' })).toHaveCount(0);
});

test('planejar de novo e excluir a sessão usam caixa própria, nunca confirm() do navegador', async ({
  page,
}) => {
  const nativas: string[] = [];
  page.on('dialog', (d) => {
    nativas.push(d.message());
    void d.dismiss();
  });
  await explorar(page, em(16, 9));
  await page.getByRole('button', { name: 'Planejar semana' }).click();
  await expect(page.locator('section.dia-plano')).toHaveCount(3);

  // Cancelar mantém o plano; o botão principal é o seguro.
  await page.getByRole('button', { name: 'Planejar de novo' }).click();
  const caixa = page.getByRole('dialog', { name: 'Planejar de novo?' });
  await expect(caixa).toBeVisible();
  await expect(caixa.getByRole('button', { name: 'Manter o plano' })).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(caixa).toHaveCount(0);
  await expect(page.locator('section.dia-plano')).toHaveCount(3);

  // Confirmar apaga o plano e volta ao formulário.
  await page.getByRole('button', { name: 'Planejar de novo' }).click();
  await caixa.getByRole('button', { name: 'Apagar o plano e planejar de novo' }).click();
  await expect(page.getByRole('button', { name: 'Planejar semana' })).toBeVisible();
  await expect(page.locator('section.dia-plano')).toHaveCount(0);

  // Excluir uma sessão: cancelar mantém, confirmar exclui.
  await page.goto('./#/sessao/exemplo-sessao-1');
  await page.getByRole('button', { name: 'Excluir', exact: true }).click();
  const excluir = page.getByRole('dialog', { name: /Excluir a sessão/ });
  await expect(excluir.getByRole('button', { name: 'Manter a sessão' })).toBeFocused();
  await excluir.getByRole('button', { name: 'Manter a sessão' }).click();
  await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();
  await page.getByRole('button', { name: 'Excluir', exact: true }).click();
  await excluir.getByRole('button', { name: 'Excluir a sessão' }).click();
  await expect(page.getByText('Sessão excluída.')).toBeVisible();

  expect(nativas).toEqual([]);
});

test('criança de 2 anos recebe folha de imprensa, mesmo em Montessori; o seletor continua livre', async ({
  page,
}) => {
  await page.clock.setFixedTime(em(16, 9));
  await page.goto('./');
  await page.getByRole('link', { name: 'Começar' }).click();
  await page.getByLabel('Seu nome (educador)').fill('Maria');
  await page.getByRole('radio', { name: /Montessori/ }).check();
  await page.getByRole('button', { name: 'Continuar' }).click();
  await expect(page.getByRole('heading', { name: 'Adicionar criança' })).toBeVisible();
  await page.getByLabel('Nome').fill('Bia');
  await page.getByLabel('Data de nascimento').fill('2024-06-15'); // 2 anos em 16/11/2026
  await page.getByRole('button', { name: 'Salvar' }).click();
  await expect(page.getByRole('heading', { name: /Jornada de Bia/ })).toBeVisible();

  await page.getByRole('link', { name: 'Planejar a semana' }).click();
  await page.getByRole('button', { name: 'Planejar semana' }).click();
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: /Baixar arquivo/ }).click(),
  ]);
  const doc = await readFile((await download.path())!, 'utf-8');
  expect(doc).toContain('<body class="letra-bastao">');
  expect(doc).toContain('Letra da criança');
  expect(doc).toContain('letra-cursiva'); // a opção de mudar continua no seletor
});
