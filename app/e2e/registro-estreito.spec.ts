import { expect, test } from '@playwright/test';

// QA2-01: em celular, "Como foi a sessão?" não quebra palavra no meio, não rola para o lado e a barra
// de salvar cabe numa linha.

for (const largura of [320, 390]) {
  test(`registro em ${largura} px: rótulos inteiros, sem rolagem lateral, barra de uma linha`, async ({
    page,
  }) => {
    await page.setViewportSize({ width: largura, height: 700 });
    await page.goto('./');
    await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
    await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
    await page.goto('./#/sessao/exemplo-sessao-1/registrar');
    await expect(page.getByRole('heading', { name: 'Como foi a sessão?' })).toBeVisible();

    const medidas = await page.evaluate(() => {
      const de = document.documentElement;
      // Número de linhas do texto de cada rótulo: palavra quebrada no meio vira linha a mais.
      const linhas = [...document.querySelectorAll('.reg-rotulo')].map((el) => {
        // Só os nós de texto: o ícone ao lado ficaria numa "linha" própria e enganaria a conta.
        const topos = new Set<number>();
        const andador = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        for (let n = andador.nextNode(); n; n = andador.nextNode()) {
          if (!n.textContent?.trim()) continue;
          const r = document.createRange();
          r.selectNodeContents(n);
          [...r.getClientRects()].forEach((c) => topos.add(Math.round(c.top)));
        }
        return { texto: (el.textContent ?? '').trim(), linhas: topos.size };
      });
      const barra = document.querySelector('.reg-acoes')?.getBoundingClientRect();
      return { excesso: de.scrollWidth - de.clientWidth, linhas, alturaBarra: barra?.height ?? 0 };
    });

    expect(medidas.excesso).toBeLessThanOrEqual(0);
    expect(medidas.linhas.length).toBeGreaterThan(0);
    for (const l of medidas.linhas) {
      expect(l.linhas, `"${l.texto}" quebrou em ${l.linhas} linhas`).toBe(1);
    }
    // Uma linha: contador + Salvar (48 px do botão + respiros), nunca duas ou três.
    expect(medidas.alturaBarra).toBeLessThan(80);
  });
}
