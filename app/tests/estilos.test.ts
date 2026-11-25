import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

// Identidade visual do app (#41, ADR 0014): estilos.css só usa tokens --s-*, sem paleta antiga nem valor solto.
const lerArquivo = (caminho: string) => readFileSync(new URL(caminho, import.meta.url), 'utf8');
const tokens = lerArquivo('../src/tokens.css');
const css = lerArquivo('../src/estilos.css').replace(/\/\*[\s\S]*?\*\//g, '');
const html = lerArquivo('../index.html');

describe('estilos.css (direção A)', () => {
  it('não tem nenhuma cor solta (#hex, rgb, hsl)', () => {
    expect(css).not.toMatch(/#[0-9a-fA-F]{3,8}\b/);
    expect(css).not.toMatch(/\b(rgb|rgba|hsl|hsla)\(/);
  });

  it('só usa variáveis --s-* e todas existem em tokens.css', () => {
    const usadas = [...css.matchAll(/var\(\s*(--[a-z0-9-]+)/g)].map((m) => m[1]!);
    expect(usadas.length).toBeGreaterThan(50);
    for (const v of new Set(usadas)) {
      expect(v.startsWith('--s-'), v).toBe(true);
      expect(tokens, v).toContain(`${v}:`);
    }
    expect(css).not.toMatch(/^\s*--[a-z]/m);
  });

  it('não tem medida solta em px ou rem (exceto pontos de quebra e o 1px do rótulo oculto)', () => {
    const semExcecoes = css.replace(/@media[^{]*/g, '').replace(/\b1px\b/g, '');
    expect(semExcecoes).not.toMatch(/\d(px|rem)\b/);
  });

  it('o foco usa o token --s-foco em todo o app', () => {
    expect(css).toMatch(
      /:focus-visible\s*\{\s*outline:\s*var\(--s-foco-largura\) solid var\(--s-foco\)/,
    );
  });

  it('campos e botões têm borda de controle (3:1), nunca só --s-linha', () => {
    for (const seletor of [
      '.botao {',
      '.formulario select {',
      '#filtros select {',
      '.estado-botao {',
    ]) {
      const bloco = css.slice(css.indexOf(seletor), css.indexOf('}', css.indexOf(seletor)));
      expect(bloco, seletor).toContain('var(--s-borda-controle)');
    }
  });

  it('avisos de texto usam terracota escura, não uma cor própria', () => {
    expect(css).toMatch(/\.aviso-marco\s*\{[^}]*color:\s*var\(--s-alerta\)/);
    expect(css).toMatch(/\.link-botao\s*\{[^}]*color:\s*var\(--s-alerta\)/);
  });
});

describe('fontes (DESIGN.md: Fraunces nos títulos, Inter no texto)', () => {
  it('index.html carrega Fraunces e Inter do Google Fonts com font-display: swap, sem Nunito', () => {
    expect(html).toContain('family=Fraunces:wght@400;600');
    expect(html).toContain('family=Inter:wght@400;500;600');
    expect(html).toContain('display=swap');
    expect(html).not.toContain('Nunito');
  });

  it('o corpo usa a fonte de texto e os títulos, a de título', () => {
    expect(css).toMatch(/body\s*\{[^}]*font-family:\s*var\(--s-fonte-texto\)/);
    expect(css).toMatch(/h1,\s*h2,\s*h3\s*\{[^}]*font-family:\s*var\(--s-fonte-titulo\)/);
  });
});

describe('conforto e movimento', () => {
  it('prefers-reduced-motion desliga transições e animações', () => {
    expect(css).toMatch(/@media \(prefers-reduced-motion: reduce\)[\s\S]*transition-duration/);
  });

  it('o aviso flutuante respeita a área segura e não captura o toque', () => {
    const bloco = css.slice(
      css.indexOf('.aviso-flutuante {'),
      css.indexOf('}', css.indexOf('.aviso-flutuante {')),
    );
    expect(bloco).toContain('env(safe-area-inset-bottom)');
    expect(bloco).toContain('pointer-events: none');
  });

  it('o texto corrido é limitado a 65 caracteres e a lista de atividades não tem marcadores', () => {
    expect(css).toMatch(/\.texto-corrido :is\(p, li\)\s*\{\s*max-width: var\(--s-medida-leitura\)/);
    expect(tokens).toMatch(/--s-medida-leitura:\s*65ch/);
    expect(css).toMatch(/\.lista-atividades\s*\{[^}]*list-style: none/);
  });
});

describe('largura da página no computador (#176, DESIGN.md "Largura e medida de leitura")', () => {
  it('o teto do conteúdo vem de token (100rem) e a margem lateral é fluida, sem valor solto', () => {
    expect(tokens).toMatch(/--s-largura-app:\s*100rem/);
    expect(tokens).toMatch(/--s-margem-pagina:\s*clamp\(/);
    expect(css).toMatch(/\.conteudo-app\s*\{[^}]*max-width:\s*var\(--s-largura-app\)/);
    expect(css).toMatch(/\.conteudo-app\s*\{[^}]*padding-inline:\s*var\(--s-margem-pagina\)/);
    expect(css).toMatch(/\.topo\s*\{[^}]*padding:\s*var\(--s-espaco-2\) var\(--s-margem-pagina\)/);
  });

  it('listas longas viram grade com colunas que se adaptam à largura', () => {
    for (const seletor of ['.lista-atividades', '.lista-acervo', '.lista-sessoes']) {
      const i = css.indexOf(`${seletor} {`);
      expect(i, seletor).toBeGreaterThan(-1);
      const bloco = css.slice(i, css.indexOf('}', i));
      expect(bloco, seletor).toContain('display: grid');
      expect(bloco, seletor).toMatch(
        /grid-template-columns:\s*repeat\(auto-fill, minmax\(var\(--s-largura-cartao-min\), 1fr\)\)/,
      );
    }
  });

  it('os filtros de Atividades ficam numa grade em linha, com a busca na linha toda', () => {
    expect(css).toMatch(
      /#filtros-atividades\s*\{[^}]*repeat\(auto-fit, minmax\(var\(--s-largura-filtro-min\), 1fr\)\)/,
    );
    expect(css).toMatch(
      /#filtros-atividades label:has\(\[type='search'\]\)\s*\{\s*grid-column: 1 \/ -1/,
    );
  });

  it('formulários e a lista de progresso do Início mantêm largura de leitura em janela larga', () => {
    expect(css).toMatch(/\.formulario\s*\{[^}]*max-width:\s*var\(--s-medida-leitura\)/);
    expect(css).toMatch(/#filtros\s*\{[^}]*max-width:\s*var\(--s-medida-leitura\)/);
    expect(css).toMatch(/#filtros-atividades\s*\{\s*max-width:\s*none/);
    expect(css).toMatch(/\.progresso-dominios\s*\{[^}]*max-width:\s*var\(--s-largura-tabela\)/);
  });

  it('parágrafos de abertura e de dentro dos cartões seguem a medida de leitura', () => {
    expect(css).toMatch(
      /\.conteudo-app > p,\s*\.cartao > p\s*\{\s*max-width: var\(--s-medida-leitura\)/,
    );
  });

  it('o botão do cartão "hoje" e a tabela de conteúdo têm limite de largura por token', () => {
    expect(css).toMatch(
      /\.crianca-cartao\.hoje #preparar-hoje\s*\{[^}]*max-width:\s*var\(--s-medida-leitura\)/,
    );
    expect(css).toMatch(/\.tabela\s*\{[^}]*max-width:\s*var\(--s-largura-tabela\)/);
    expect(tokens).toContain('--s-largura-tabela:');
  });
});

describe('ícones (ADR 0034)', () => {
  it('tokens de tamanho existem e o CSS os usa', () => {
    expect(tokens).toContain('--s-icone: 1.25rem');
    expect(tokens).toContain('--s-icone-g: 2rem');
    expect(css).toMatch(/\.icone\s*\{[^}]*width:\s*var\(--s-icone\)/);
    expect(css).toMatch(/\.icone-g\s*\{[^}]*var\(--s-icone-g\)/);
    expect(css).toMatch(/\.icone\s*\{[^}]*flex-shrink:\s*0/);
  });
});
