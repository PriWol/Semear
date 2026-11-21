import { expect, test, type Page } from '@playwright/test';

// Gravuras botânicas de domínio público (ADR 0035, estória #130/#24): boas-vindas, início sem criança
// e topo da Biblioteca. Arquivos locais, variante escura pelo aparelho, nada de rede externa.

async function criarFamiliaSemCrianca(page: Page) {
  await page.goto('./');
  await page.getByRole('link', { name: 'Começar' }).click();
  await page.getByLabel('Seu nome (educador)').fill('Maria');
  await page.getByRole('radio', { name: /Montessori/ }).check();
  await page.getByRole('button', { name: 'Continuar' }).click();
  await expect(page.getByRole('heading', { name: 'Adicionar criança' })).toBeVisible();
  await page.goto('./#/');
}

const imagem = (page: Page, id: string) => page.locator(`img[data-gravura="${id}"]`);

async function carregou(page: Page, id: string) {
  await expect(imagem(page, id)).toBeVisible();
  await expect
    .poll(() => imagem(page, id).evaluate((el: HTMLImageElement) => el.complete && el.naturalWidth))
    .toBeGreaterThan(0);
}

const semRolagemLateral = (page: Page) =>
  page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);

test('boas-vindas mostra o girassol de Besler', async ({ page }) => {
  await page.goto('./');
  await carregou(page, 'girassol');
  await expect(imagem(page, 'girassol')).toHaveAttribute('src', 'gravuras/girassol.webp');
  // ornamento: alt vazio, o sentido está no título (ui/gravura.ts)
  await expect(imagem(page, 'girassol')).toHaveAttribute('alt', '');
  await expect(page.getByRole('heading', { name: 'Bem-vindo ao Semear' })).toBeVisible();
});

test('início sem criança mostra o gladíolo de Redouté', async ({ page }) => {
  await criarFamiliaSemCrianca(page);
  await carregou(page, 'gladiolo');
  await expect(imagem(page, 'gladiolo')).toHaveAttribute('src', 'gravuras/gladiolo.webp');
  await expect(page.getByRole('heading', { name: 'Ainda não há crianças por aqui' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Adicionar a primeira criança' })).toBeVisible();
});

test('com criança cadastrada o gladíolo não aparece', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await expect(imagem(page, 'gladiolo')).toHaveCount(0);
});

test('a Biblioteca mostra as tulipas de Besler no topo', async ({ page }) => {
  await page.goto('./#/biblioteca');
  await carregou(page, 'tulipas');
  await expect(imagem(page, 'tulipas')).toHaveAttribute('src', 'gravuras/tulipas.webp');
  await expect(page.getByRole('heading', { name: 'Biblioteca', level: 1 })).toBeVisible();
});

test.describe('tema do aparelho', () => {
  test.describe('claro', () => {
    test.use({ colorScheme: 'light' });
    test('usa a variante de tinta escura sobre papel claro', async ({ page }) => {
      await page.goto('./');
      await carregou(page, 'girassol');
      const atual = await imagem(page, 'girassol').evaluate(
        (el: HTMLImageElement) => el.currentSrc,
      );
      expect(atual).toMatch(/\/gravuras\/girassol\.webp$/);
    });
  });

  test.describe('escuro', () => {
    test.use({ colorScheme: 'dark' });
    test('escolhe a variante de tinta clara', async ({ page }) => {
      await page.goto('./');
      await carregou(page, 'girassol');
      const atual = await imagem(page, 'girassol').evaluate(
        (el: HTMLImageElement) => el.currentSrc,
      );
      expect(atual).toMatch(/\/gravuras\/girassol-escuro\.webp$/);
      await page.goto('./#/biblioteca');
      await carregou(page, 'tulipas');
      const tulipas = await imagem(page, 'tulipas').evaluate(
        (el: HTMLImageElement) => el.currentSrc,
      );
      expect(tulipas).toMatch(/\/gravuras\/tulipas-escuro\.webp$/);
    });
  });
});

for (const largura of [320, 390]) {
  test.describe(`em ${largura} px`, () => {
    test.use({ viewport: { width: largura, height: 740 } });

    test('as três telas não rolam para o lado', async ({ page }) => {
      await page.goto('./');
      await carregou(page, 'girassol');
      expect(await semRolagemLateral(page)).toBeLessThanOrEqual(0);
      await criarFamiliaSemCrianca(page);
      await carregou(page, 'gladiolo');
      expect(await semRolagemLateral(page)).toBeLessThanOrEqual(0);
      await page.goto('./#/biblioteca');
      await carregou(page, 'tulipas');
      expect(await semRolagemLateral(page)).toBeLessThanOrEqual(0);
    });

    test('a gravura não empurra o botão principal para fora da primeira tela', async ({ page }) => {
      await page.goto('./');
      await carregou(page, 'girassol');
      const caixa = await page.getByRole('link', { name: 'Começar' }).boundingBox();
      expect(caixa).not.toBeNull();
      expect((caixa?.y ?? 9999) + (caixa?.height ?? 0)).toBeLessThanOrEqual(740);
    });
  });
}

test('o crédito das gravuras está em Ajustes, no grupo "Sobre o Semear"', async ({ page }) => {
  await page.goto('./#/config');
  const sobre = page.locator('#sobre');
  await sobre.getByText('Créditos das gravuras').click();
  const texto = sobre.locator('#creditos-gravuras');
  await expect(texto).toContainText('Besler, Hortus Eystettensis (1640)');
  await expect(texto).toContainText('Redouté, Les Liliacées (1802–1816)');
  await expect(texto).toContainText('Internet Archive');
  await expect(texto).toContainText('domínio público');
});

test('as gravuras vêm do próprio site: nenhuma requisição ao archive.org', async ({
  page,
  baseURL,
}) => {
  const externas: string[] = [];
  const origem = new URL(baseURL ?? 'http://localhost:4173').origin;
  page.on('request', (r) => {
    const url = new URL(r.url());
    if (url.protocol === 'data:' || url.protocol === 'blob:') return;
    // as fontes do Google são a única chamada externa permitida (CLAUDE.md)
    if (url.origin !== origem && !/(^|\.)(googleapis|gstatic)\.com$/.test(url.hostname)) {
      externas.push(r.url());
    }
  });
  await page.goto('./');
  await carregou(page, 'girassol');
  await page.goto('./#/biblioteca');
  await carregou(page, 'tulipas');
  await criarFamiliaSemCrianca(page);
  await carregou(page, 'gladiolo');
  expect(externas).toEqual([]);
});
