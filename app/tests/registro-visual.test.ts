import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

// Visual do registro de sessão (#11): só tokens --s-*, alvos de toque e foco (docs/DESIGN.md, ADR 0014).
const tokens = readFileSync(new URL('../src/tokens.css', import.meta.url), 'utf8');
const registro = readFileSync(new URL('../src/registro.css', import.meta.url), 'utf8');

describe('tokens novos', () => {
  it('o alvo de toque é de 3rem (48 px) e o foco usa a cor da tinta', () => {
    expect(tokens).toMatch(/--s-alvo-toque:\s*3rem/);
    expect(tokens).toMatch(/--s-foco:\s*var\(--s-tinta\)/);
  });
});

describe('registro.css (bloco separado do CSS do registro)', () => {
  const semComentarios = registro.replace(/\/\*[\s\S]*?\*\//g, '');

  it('não tem nenhuma cor solta (#hex, rgb, hsl)', () => {
    expect(semComentarios).not.toMatch(/#[0-9a-fA-F]{3,8}\b/);
    expect(semComentarios).not.toMatch(/\b(rgb|rgba|hsl|hsla)\(/);
  });

  it('só usa variáveis --s-*', () => {
    const usadas = [...semComentarios.matchAll(/var\(\s*(--[a-z0-9-]+)/g)].map((m) => m[1]!);
    expect(usadas.length).toBeGreaterThan(0);
    for (const v of usadas) expect(v.startsWith('--s-'), v).toBe(true);
    // e todas existem em tokens.css
    for (const v of new Set(usadas)) expect(tokens, v).toContain(`${v}:`);
  });

  it('não define variáveis próprias nem usa as variáveis antigas', () => {
    expect(semComentarios).not.toMatch(/^\s*--[a-z]/m);
    expect(semComentarios).not.toMatch(/var\(\s*--(mata|terra|fundo|cartao|texto|suave|linha)\b/);
  });

  it('o foco aparece em todo controle do registro (anel de 3 px, recuo de 2 px)', () => {
    expect(semComentarios).toMatch(/:focus-visible/);
    expect(semComentarios).toMatch(/outline:\s*var\(--s-foco-largura\) solid var\(--s-foco\)/);
    expect(semComentarios).toMatch(/outline-offset:\s*var\(--s-foco-recuo\)/);
  });

  it('espessuras de borda e de foco vêm de tokens: nenhum "Npx" solto', () => {
    expect(semComentarios).not.toMatch(/\b\d+px\b/);
    expect(tokens).toMatch(/--s-foco-largura:\s*3px/);
    expect(tokens).toMatch(/--s-foco-recuo:\s*2px/);
    expect(tokens).toMatch(/--s-borda-marcada:\s*3px/);
  });

  it('a barra sticky não esconde o que ganha foco (scroll-margin-bottom)', () => {
    expect(semComentarios).toMatch(/scroll-margin-bottom:/);
  });

  it('os alvos de toque usam --s-alvo-toque', () => {
    expect(semComentarios).toMatch(/min-height:\s*var\(--s-alvo-toque\)/);
  });

  it('o texto usa tokens de tamanho: nenhum font-size solto e nada abaixo de 14 px', () => {
    const tamanhos = [...semComentarios.matchAll(/font-size:\s*([^;]+);/g)].map((m) =>
      m[1]!.trim(),
    );
    expect(tamanhos.length).toBeGreaterThan(0);
    for (const t of tamanhos) expect(t, t).toMatch(/^var\(--s-texto-(p|selo)\)$/);
    const rem = (nome: string) =>
      Number(new RegExp(`--s-${nome}:\\s*([\\d.]+)rem`).exec(tokens)?.[1]);
    expect(rem('texto-p')).toBeGreaterThanOrEqual(1);
    expect(rem('texto-selo')).toBeGreaterThanOrEqual(0.875);
  });

  it('a borda dos controles usa --s-borda-controle, nunca --s-linha', () => {
    for (const seletor of ['.reg-rotulo', '.reg-campo']) {
      const bloco =
        new RegExp(`${seletor.replace('.', '\\.')} \\{[^}]*\\}`).exec(semComentarios)?.[0] ?? '';
      expect(bloco, seletor).toMatch(/border:[^;]*var\(--s-borda-controle\)/);
      expect(bloco, seletor).not.toContain('--s-linha');
    }
  });

  it('a borda de controle tem contraste de pelo menos 3:1 sobre o papel (WCAG 1.4.11)', () => {
    const hex = (n: string) => new RegExp(`--s-${n}:\\s*(#[0-9a-f]{6})`, 'i').exec(tokens)![1]!;
    expect(tokens).toMatch(/--s-borda-controle:\s*var\(--s-suave\)/);
    expect(contraste(hex('suave'), hex('papel'))).toBeGreaterThanOrEqual(3);
    expect(contraste(hex('principal'), hex('principal-claro'))).toBeGreaterThanOrEqual(3);
  });

  it('o grid de 3 colunas não deixa o conteúdo alargar a coluna', () => {
    expect(semComentarios).toMatch(/repeat\(3, minmax\(0, 1fr\)\)/);
  });
});

function luminancia(hex: string): number {
  const [r = 0, g = 0, b = 0] = [1, 3, 5].map((i) => {
    const c = parseInt(hex.slice(i, i + 2), 16) / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
function contraste(a: string, b: string): number {
  const [claro, escuro] = [luminancia(a), luminancia(b)].sort((x, y) => y - x);
  return ((claro ?? 0) + 0.05) / ((escuro ?? 0) + 0.05);
}
