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
    expect(semComentarios).toMatch(/outline:\s*3px solid var\(--s-foco\)/);
    expect(semComentarios).toMatch(/outline-offset:\s*2px/);
  });

  it('os alvos de toque usam --s-alvo-toque', () => {
    expect(semComentarios).toMatch(/min-height:\s*var\(--s-alvo-toque\)/);
  });
});
