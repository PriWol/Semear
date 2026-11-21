import { expect, test } from '@playwright/test';

// Identidade visual (#41): em 320 px nenhuma tela rola para o lado e tudo que se toca tem ao menos 44 px.

const ROTAS = [
  '/',
  '/familia',
  '/crianca/exemplo-ana',
  '/sondagem/exemplo-ana',
  '/jornada/exemplo-ana',
  '/sessao/nova?crianca=exemplo-ana',
  '/sessao/exemplo-sessao-1',
  '/sessao/exemplo-sessao-1/registrar',
  '/atividades',
  '/biblioteca',
  '/acervo',
  '/guia',
  '/semana/exemplo-ana',
  '/config',
  '/termos',
  '/privacidade',
  '/novidades',
  '/conteudo',
];

test.use({ viewport: { width: 320, height: 700 } });

test('em 320 px nenhuma tela rola para o lado e os alvos de toque têm 44 px', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();

  for (const rota of ROTAS) {
    await page.goto(`./#${rota}`);
    await expect(page.locator('h1').first()).toBeVisible();
    const medidas = await page.evaluate(() => {
      const de = document.documentElement;
      const pequenos = [...document.querySelectorAll('nav a, button, .botao, select, summary')]
        .filter((e) => {
          const r = e.getBoundingClientRect();
          return r.width > 0 && r.height > 0 && !e.closest('.rotulo-estado') && r.height < 44;
        })
        .map((e) => `${e.tagName}:${(e.textContent ?? '').trim().slice(0, 20)}`);
      return { excesso: de.scrollWidth - de.clientWidth, pequenos };
    });
    expect(medidas.excesso, `rolagem lateral em ${rota}`).toBeLessThanOrEqual(0);
    expect(medidas.pequenos, `alvo pequeno em ${rota}`).toEqual([]);
  }
});

test('o item ativo do menu do topo é marcado com aria-current', async ({ page }) => {
  await page.goto('./#/atividades');
  const ativo = page.locator('nav[aria-label="Principal"] a[aria-current="page"]');
  await expect(ativo).toHaveCount(1);
  await expect(ativo).toHaveText('Atividades');
});
