import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

// Garante o contraste AA (WCAG 2.1) prometido em docs/DESIGN.md para cada par texto/fundo.
const css = readFileSync(new URL('../src/tokens.css', import.meta.url), 'utf8');

function token(nome: string): string {
  const m = new RegExp(`--s-${nome}:\\s*(#[0-9a-f]{6})`, 'i').exec(css);
  if (!m?.[1]) throw new Error(`token --s-${nome} não encontrado`);
  return m[1];
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
];

describe('tokens visuais (direção A)', () => {
  it.each(pares)('texto --s-%s sobre --s-%s tem contraste AA (≥ 4,5:1)', (texto, fundo) => {
    expect(contraste(token(texto), token(fundo))).toBeGreaterThanOrEqual(4.5);
  });
});
