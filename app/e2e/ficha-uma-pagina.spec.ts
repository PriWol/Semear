import { expect, test } from '@playwright/test';
import { createServer } from 'vite';
import type { EntradaPacote } from '../src/pacote/gerar';
import type { Sessao } from '../src/domain/tipos';
import { AGORA, crianca, familia } from '../tests/fabricas';

// #33: a ficha de registro cabe numa folha A4 quando a sessão tem duas atividades. O teste gera o
// PDF de verdade (Chromium, mídia de impressão) e confere que nenhuma folha vaza para uma página
// extra. O pacote é montado direto pelo código, porque hoje a tela não monta duas atividades de
// 35 min numa sessão de 60 min, mas a ficha precisa aguentar esse caso.

test.skip(({ browserName }) => browserName !== 'chromium', 'page.pdf só existe no Chromium');

function contarPaginasPdf(pdf: Buffer): number {
  // O Chromium escreve cada página como um objeto "/Type /Page" (o catálogo é "/Type /Pages").
  return (pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) ?? []).length;
}

/** Gera o HTML do pacote com o mesmo código e o mesmo conteúdo do app (o Vite resolve `?raw` e as globs). */
async function gerarHtml(atividadeIds: string[], duracaoMin: number): Promise<string> {
  const vite = await createServer({
    server: { middlewareMode: true },
    appType: 'custom',
    logLevel: 'silent',
  });
  try {
    const { gerarPacote } = (await vite.ssrLoadModule('/src/pacote/gerar.ts')) as {
      gerarPacote: (e: EntradaPacote) => string;
    };
    const { conteudo } = (await vite.ssrLoadModule('/src/conteudo.ts')) as {
      conteudo: () => import('../src/domain/conteudo').IndiceConteudo;
    };
    const idx = conteudo();
    const sessao: Sessao = {
      id: 's1',
      codigo: 'S-1014-A1',
      criancaId: 'c1',
      criadaEm: AGORA,
      duracaoMin,
      foco: 'equilibrado',
      atividadeIds,
      livroId: null,
    };
    return gerarPacote({
      sessao,
      familia: familia(),
      crianca: crianca(),
      idade: 5.5,
      letra: 'script',
      atividades: atividadeIds.map((id) => {
        const a = idx.atividade(id);
        if (!a) throw new Error(`atividade ${id} não existe`);
        return a;
      }),
      livro: null,
      marco: (id) => idx.marco(id),
    });
  } finally {
    await vite.close();
  }
}

// 297 mm em pixels CSS (96 dpi).
const ALTURA_A4_PX = (297 / 25.4) * 96;

const CASOS = [
  { nome: 'uma atividade', ids: ['atv-caca-silabas'], duracao: 40 },
  { nome: 'duas atividades', ids: ['atv-caca-silabas', 'atv-feira-numeros'], duracao: 60 },
];

for (const caso of CASOS) {
  test(`${caso.nome}: a ficha de registro ocupa exatamente uma página no PDF`, async ({
    browser,
  }) => {
    const html = await gerarHtml(caso.ids, caso.duracao);
    const pagina = await (await browser.newContext()).newPage();
    await pagina.setContent(html);
    await pagina.emulateMedia({ media: 'print' });

    // Altura de cada folha (em páginas A4) e se a última é a ficha. O roteiro pode ocupar mais de
    // uma página quando há várias atividades; a ficha não.
    const folhas = await pagina.evaluate(
      (alturaA4) =>
        [...document.querySelectorAll<HTMLElement>('section.pagina')].map((s) => ({
          ehFicha: s.querySelector('h1')?.textContent === 'Como foi a sessão?',
          paginas: Math.ceil((s.scrollHeight - 1) / alturaA4),
        })),
      ALTURA_A4_PX,
    );
    const ficha = folhas.filter((f) => f.ehFicha);
    expect(ficha).toHaveLength(1);
    expect(ficha[0]?.paginas).toBe(1);

    const esperadas = folhas.reduce((t, f) => t + (f.ehFicha ? 1 : f.paginas), 0);
    const pdf = await pagina.pdf({ preferCSSPageSize: true });
    expect(contarPaginasPdf(pdf)).toBe(esperadas);
  });
}
