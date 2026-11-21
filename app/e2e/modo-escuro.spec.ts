import { expect, test, type Page } from '@playwright/test';

// Modo escuro automático (#130, ADR 0033): segue o aparelho; a folha do pacote continua clara.

const brilho = (cor: string) => {
  const [r = 0, g = 0, b = 0] = (cor.match(/\d+(\.\d+)?/g) ?? []).slice(0, 3).map(Number);
  return (r + g + b) / 3;
};

async function coresDoCorpo(page: Page) {
  return page.evaluate(() => {
    const e = getComputedStyle(document.body);
    return { fundo: e.backgroundColor, texto: e.color };
  });
}

test.describe('esquema escuro', () => {
  test.use({ colorScheme: 'dark' });

  test('fundo escuro, texto claro, e a prévia do pacote continua clara', async ({ page }) => {
    await page.goto('./');
    await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
    await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
    const c = await coresDoCorpo(page);
    expect(brilho(c.fundo)).toBeLessThan(60);
    expect(brilho(c.texto)).toBeGreaterThan(190);

    await page.goto('./#/sessao/exemplo-sessao-1');
    const iframe = page.locator('#previa');
    await expect(iframe).toBeVisible();
    const quadro = page.frameLocator('#previa');
    await expect(quadro.locator('body *').first()).toBeAttached();
    const doQuadro = await quadro.locator('body').evaluate((b) => ({
      fundo: getComputedStyle(b).backgroundColor,
      texto: getComputedStyle(b).color,
      esquema: getComputedStyle(b.ownerDocument.documentElement).colorScheme,
    }));
    expect(doQuadro.esquema).not.toContain('dark');
    expect(brilho(doQuadro.texto)).toBeLessThan(120);
    // Corpo transparente deixa ver a moldura, que é a folha clara.
    const moldura = await iframe.evaluate((e) => getComputedStyle(e).backgroundColor);
    const fundoReal = doQuadro.fundo === 'rgba(0, 0, 0, 0)' ? moldura : doQuadro.fundo;
    expect(brilho(fundoReal)).toBeGreaterThan(200);
  });

  test('em 320 px não rola para o lado', async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 700 });
    await page.goto('./');
    await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
    for (const rota of ['/', '/jornada/exemplo-ana', '/atividades', '/config', '/biblioteca']) {
      await page.goto(`./#${rota}`);
      await expect(page.locator('h1').first()).toBeVisible();
      const largura = await page.evaluate(() => ({
        rola: document.documentElement.scrollWidth,
        vista: document.documentElement.clientWidth,
      }));
      expect(largura.rola, rota).toBeLessThanOrEqual(largura.vista);
    }
  });
});

test.describe('esquema claro', () => {
  test.use({ colorScheme: 'light' });

  test('continua com fundo claro e texto escuro', async ({ page }) => {
    await page.goto('./');
    await expect(page.locator('h1').first()).toBeVisible();
    const c = await coresDoCorpo(page);
    expect(brilho(c.fundo)).toBeGreaterThan(200);
    expect(brilho(c.texto)).toBeLessThan(80);
  });
});
