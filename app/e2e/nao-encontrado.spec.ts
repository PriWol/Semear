import { expect, test } from '@playwright/test';

// QA1-09: endereço de criança ou sessão que não existe mostra "Não encontramos…", sem "Algo deu errado"
// e sem erro no console.

const CASOS = [
  { rota: '/jornada/xxxx', titulo: 'Não encontramos essa criança' },
  { rota: '/sondagem/xxxx', titulo: 'Não encontramos essa criança' },
  { rota: '/semana/xxxx', titulo: 'Não encontramos essa criança' },
  { rota: '/sessao/xxxx', titulo: 'Não encontramos essa sessão' },
  { rota: '/sessao/xxxx/registrar', titulo: 'Não encontramos essa sessão' },
];

for (const { rota, titulo } of CASOS) {
  test(`${rota} mostra "${titulo}" com volta ao início e sem erro no console`, async ({ page }) => {
    const erros: string[] = [];
    page.on('console', (m) => {
      if (m.type() === 'error') erros.push(m.text());
    });
    page.on('pageerror', (e) => erros.push(e.message));

    await page.goto('./');
    await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
    await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
    await page.goto(`./#${rota}`);

    await expect(page.getByRole('heading', { name: titulo })).toBeVisible();
    await expect(page.getByText('Algo deu errado')).toHaveCount(0);
    await page.getByRole('link', { name: 'Voltar ao início' }).click();
    await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
    expect(erros).toEqual([]);
  });
}
