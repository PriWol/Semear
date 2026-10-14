import { expect, test } from '@playwright/test';
import { readFileSync } from 'node:fs';

// Versão publicada e novidades (#38): saber o que está no ar, olhando o próprio app.
const { version } = JSON.parse(
  readFileSync(new URL('../package.json', import.meta.url), 'utf-8'),
) as { version: string };
const curta = `v${version.split('.').slice(0, 2).join('.')}`;

test('a versão aparece no topo e leva às novidades', async ({ page }) => {
  await page.goto('./');
  const rotulo = page.locator('#versao');
  await expect(rotulo).toHaveText(new RegExp(`^${curta.replace('.', '\\.')} · \\d{2}/\\d{2}$`));
  await rotulo.click();
  await expect(page.getByRole('heading', { name: 'Novidades' })).toBeVisible();
  await expect(page.locator(`[data-versao="${version}"]`)).toBeVisible();
});

test('Configurações mostra versão, data e código da publicação', async ({ page }) => {
  await page.goto('./#/config');
  const sobre = page.locator('#sobre');
  await expect(sobre).toContainText(`(${version})`);
  await expect(sobre).toContainText(/publicada em\s+\d{2}\/\d{2}\/\d{4}/);
  await expect(sobre.locator('code')).toHaveText(/^([0-9a-f]{7}|local)$/);
});
