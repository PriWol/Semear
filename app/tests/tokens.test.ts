import { readFileSync } from 'node:fs';
import { beforeEach, describe, expect, it } from 'vitest';

// Garante o contraste AA (WCAG 2.1) prometido em docs/DESIGN.md para cada par texto/fundo.
const claro = readFileSync(new URL('../src/tokens.css', import.meta.url), 'utf8');
const escuro = readFileSync(new URL('../src/tokens-escuro.css', import.meta.url), 'utf8');
// Fonte em uso na conferência; o tema escuro redefine os mesmos nomes e herda do claro o que não redefine.
let css = claro;

function token(nome: string): string {
  return resolver(nome);
}

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

const pares: [string, string][] = [
  ['tinta', 'fundo'],
  ['tinta', 'papel'],
  ['suave', 'fundo'],
  ['suave', 'papel'],
  ['principal', 'fundo'],
  ['principal', 'principal-claro'],
  ['papel', 'principal'],
  ['destaque-texto', 'destaque-claro'],
  ['destaque-texto', 'papel'],
  ['alerta', 'alerta-claro'],
  ['alerta', 'papel'],
  // pares usados pelo app (#41): marco consolidado, nota sobre ele, aviso flutuante, topo
  ['tinta', 'principal-claro'],
  ['suave', 'principal-claro'],
  ['alerta', 'principal-claro'],
  ['tinta', 'alerta-claro'],
  ['principal', 'papel'],
  ['papel', 'tinta'],
  // barra do topo: texto, aba ativa e selo da versão
  ['topo-texto', 'topo'],
  ['topo-ativo-texto', 'topo-ativo'],
  ['topo-ativo', 'topo'],
];

// Componentes sem texto (WCAG 1.4.11): borda de campo e anel de foco precisam de 3:1 sobre o fundo.
const naoTexto: [string, string][] = [
  ['borda-controle', 'papel'],
  ['borda-controle', 'fundo'],
  ['foco', 'papel'],
  ['foco', 'fundo'],
  ['foco', 'principal-claro'],
  ['papel', 'principal'], // anel de foco claro sobre o topo verde
];

// --s-foco e --s-borda-controle são aliases (var(--s-…)): resolve até chegar a um #hex.
function resolver(nome: string): string {
  const m = new RegExp(`--s-${nome}:\\s*(#[0-9a-f]{6}|var\\(--s-([a-z-]+)\\))`, 'i').exec(css);
  if (!m) throw new Error(`token --s-${nome} não encontrado`);
  return m[2] ? resolver(m[2]) : m[1]!;
}

describe.each([
  ['claro', claro],
  ['escuro', `${escuro}\n${claro}`],
])('tokens visuais (direção A, tema %s)', (_tema, fonte) => {
  beforeEach(() => {
    css = fonte;
  });

  it.each(pares)('texto --s-%s sobre --s-%s tem contraste AA (≥ 4,5:1)', (texto, fundo) => {
    expect(contraste(token(texto), token(fundo))).toBeGreaterThanOrEqual(4.5);
  });

  it.each(naoTexto)('--s-%s sobre --s-%s tem contraste de 3:1 (WCAG 1.4.11)', (a, b) => {
    expect(contraste(resolver(a), resolver(b))).toBeGreaterThanOrEqual(3);
  });
});

describe('tema escuro: regras de forma', () => {
  it('redefine só tokens existentes, só sob prefers-color-scheme: dark e sem preto/branco puro', () => {
    expect(escuro).toMatch(/@media screen and \(prefers-color-scheme: dark\)/);
    for (const [, nome] of escuro.matchAll(/^\s*(--s-[a-z-]+):/gm)) {
      expect(claro).toContain(`${nome}:`);
    }
    expect(escuro).not.toMatch(/#(000000|ffffff)\b/i);
  });

  it('o fundo é escuro e o texto é claro', () => {
    css = `${escuro}\n${claro}`;
    expect(luminancia(token('fundo'))).toBeLessThan(0.05);
    expect(luminancia(token('tinta'))).toBeGreaterThan(0.6);
  });
});
