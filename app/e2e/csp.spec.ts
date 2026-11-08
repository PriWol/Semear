import { expect, test } from '@playwright/test';

// #32: a CSP do app não pode ser violada em nenhuma tela, nem na prévia do pacote (iframe sandbox).
// Violação aparece no console como "Refused to ..." e dispara o evento securitypolicyviolation.

test('o app e a prévia do pacote rodam sem violar a CSP', async ({ page }) => {
  const violacoes: string[] = [];
  page.on('console', (m) => {
    if (/Content Security Policy|Refused to/i.test(m.text())) violacoes.push(m.text());
  });
  page.on('pageerror', (e) => violacoes.push(e.message));
  page.on('dialog', (d) => void d.accept());

  await page.goto('./');
  await expect(page.locator('meta[http-equiv="Content-Security-Policy"]')).toHaveCount(1);
  await page.getByRole('link', { name: 'Começar' }).click();
  await page.getByLabel('Seu nome (educador)').fill('Maria');
  await page.getByRole('radio', { name: /Montessori/ }).check();
  await page.getByRole('button', { name: 'Continuar' }).click();
  await expect(page.getByRole('heading', { name: 'Adicionar criança' })).toBeVisible();
  await page.getByLabel('Nome').fill('Ana');
  await page.getByLabel('Data de nascimento').fill('2021-03-15');
  await page.getByRole('button', { name: 'Salvar' }).click();
  await expect(page.getByRole('heading', { name: /Jornada de Ana/ })).toBeVisible();
  await page
    .locator('li.marco[data-marco="LG.FON.04"]')
    .getByRole('button', { name: 'Está aqui' })
    .click();
  await page.getByRole('link', { name: 'Preparar sessão' }).click();
  await page.getByRole('radio', { name: /Escolher linhas/ }).check();
  await page.getByRole('checkbox', { name: /Consciência fonológica/ }).check();
  await page.getByRole('button', { name: 'Sugerir atividades' }).click();
  await page.getByRole('button', { name: 'Gerar pacote' }).click();
  await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();

  // O script do pacote precisa funcionar na prévia: o botão "Modo tablet" alterna a classe do body.
  const previa = page.frameLocator('#previa');
  await expect(previa.locator('body')).toBeVisible();
  // Espera o parser terminar (fontes lentas seguram o script) antes de clicar.
  await expect
    .poll(
      () =>
        previa
          .locator('body')
          .evaluate(
            () => typeof (window as unknown as { alternarTablet?: unknown }).alternarTablet,
          ),
      { timeout: 40_000 },
    )
    .toBe('function');
  await previa.getByRole('button', { name: /Modo tablet/ }).click();
  await expect(previa.locator('body')).toHaveClass(/tablet/);

  expect(violacoes).toEqual([]);
});
