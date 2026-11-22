import { expect, test } from '@playwright/test';

// QA2-02: marcar um estado por teclado redesenha a tela, mas o foco volta ao botão que a pessoa usou.

test('jornada: depois de marcar um estado por teclado, o foco volta ao mesmo botão', async ({
  page,
}) => {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await page.goto('./#/jornada/exemplo-ana');
  await expect(page.getByRole('heading', { name: /Jornada de Ana/ })).toBeVisible();

  const botao = page
    .locator('li.marco')
    .first()
    .locator('button[data-acao=estado][data-estado=em-desenvolvimento]');
  const chave = await botao.getAttribute('data-chave');
  await botao.focus();
  await page.keyboard.press('Enter');

  // O botão marcado é um botão novo (a tela foi refeita) e está com o foco.
  await expect(botao).toHaveAttribute('aria-pressed', 'true');
  const focado = page.locator(':focus');
  await expect(focado).toHaveAttribute('data-acao', 'estado');
  await expect(focado).toHaveAttribute('data-chave', chave ?? '');
  await expect(focado).toHaveAttribute('data-estado', 'em-desenvolvimento');

  // E dá para seguir pelo teclado: Tab vai ao botão seguinte do mesmo marco, não ao começo da página.
  await page.keyboard.press('Tab');
  await expect(page.locator(':focus')).toHaveAttribute('data-chave', chave ?? '');
});
