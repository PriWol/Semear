import { expect, type Page } from '@playwright/test';

/**
 * Deixa uma atividade conhecida como primeira da proposta, trocando até ela aparecer.
 * Os testes de fluxo dependem de uma atividade específica (e dos marcos dela); com mais conteúdo aprovado,
 * o sugestor pode escolher outra primeiro, e isso não é o que esses testes verificam.
 */
export async function escolherAtividade(page: Page, titulo: string): Promise<void> {
  const primeira = page.locator('#proposta .escolhas li').first();
  await expect(primeira).toBeVisible();
  for (let i = 0; i < 40; i++) {
    // O título completo traz um subtítulo ("Caça às sílabas: começa igual!"); basta o começo coincidir.
    if ((await primeira.locator('b').innerText()).trim().startsWith(titulo)) return;
    const trocar = primeira.getByRole('button', { name: 'Trocar' });
    if ((await trocar.count()) === 0) break;
    await trocar.click();
  }
  await expect(page.locator('#proposta')).toContainText(titulo);
}
