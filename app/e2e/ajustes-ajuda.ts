import { expect, type Page } from '@playwright/test';

/** Abre os Ajustes pelo menu (o item antes se chamava "Config."). */
export async function abrirAjustes(page: Page) {
  await page.getByRole('link', { name: 'Ajustes', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Ajustes', level: 1 })).toBeVisible();
}

/** Apaga tudo pela caixa de confirmação: digita APAGAR e escolhe "Apagar mesmo assim". */
export async function apagarTudoPelosAjustes(page: Page) {
  await page.getByRole('button', { name: 'Apagar todos os dados deste aparelho' }).click();
  const caixa = page.getByRole('dialog', { name: 'Apagar tudo neste aparelho?' });
  await caixa.getByLabel(/digite APAGAR/).fill('APAGAR');
  await caixa.getByRole('button', { name: 'Apagar mesmo assim' }).click();
}

/** Confirma a caixa de "Trazer esta cópia?". */
export async function confirmarTrazerCopia(page: Page) {
  await page
    .getByRole('dialog', { name: 'Trazer esta cópia?' })
    .getByRole('button', { name: 'Substituir os dados' })
    .click();
}
