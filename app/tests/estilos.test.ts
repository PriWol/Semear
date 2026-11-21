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
