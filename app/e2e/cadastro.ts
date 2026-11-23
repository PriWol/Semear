import { expect, type Page } from '@playwright/test';

/**
 * Depois de salvar uma criança NOVA o app mostra a tela de próximo passo (D21), não a jornada.
 * Confere essa tela e segue por "Ver jornada", para os fluxos que continuam posicionando a criança.
 */
export async function irParaJornadaDepoisDeCadastrar(page: Page, nome: string): Promise<void> {
  await expect(
    page.getByRole('heading', { name: `Pronto, ${nome} está cadastrada` }),
  ).toBeVisible();
  await page.getByRole('link', { name: 'Ver jornada' }).click();
  await expect(page.getByRole('heading', { name: new RegExp(`Jornada de ${nome}`) })).toBeVisible();
}
