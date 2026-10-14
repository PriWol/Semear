import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { numeroCurto, rotuloVersao } from '../src/ui/versao';
import { NOVIDADES, validarNovidades } from '../src/novidades';
import { VERSAO } from '../src/versao';

const pacote = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf-8')) as {
  version: string;
};

describe('versão publicada (#38)', () => {
  it('mostra a versão curta, e a correção inteira quando houver', () => {
    expect(numeroCurto('0.2.0')).toBe('v0.2');
    expect(numeroCurto('1.0.0')).toBe('v1.0');
    expect(numeroCurto('0.2.1')).toBe('v0.2.1');
  });

  it('rótulo do topo: versão e dia/mês da publicação', () => {
    const data = new Date(2026, 9, 14, 15).toISOString(); // 14/10, horário local
    expect(rotuloVersao({ numero: '0.2.0', data })).toBe('v0.2 · 14/10');
  });

  it('a versão do app vem do package.json, embutida no build', () => {
    expect(VERSAO.numero).toBe(pacote.version);
    expect(Number.isNaN(Date.parse(VERSAO.data))).toBe(false);
    expect(VERSAO.commit).toMatch(/^([0-9a-f]{7}|local)$/);
  });
});

describe('novidades', () => {
  // Quem sobe a versão no package.json precisa contar o que mudou: senão este teste falha.
  it('a versão mais recente das novidades é a versão do app', () => {
    expect(NOVIDADES[0]?.versao).toBe(pacote.version);
  });

  it('as versões estão da mais nova para a mais antiga, sem repetir', () => {
    // numeric: "0.10.0" vem depois de "0.2.0", como nas versões.
    const versoes = NOVIDADES.map((n) => n.versao);
    const ordenadas = [...versoes].sort((a, b) => b.localeCompare(a, 'en', { numeric: true }));
    expect(versoes).toEqual(ordenadas);
    expect(new Set(versoes).size).toBe(versoes.length);
  });

  it('recusa um arquivo de novidades malformado', () => {
    expect(() => validarNovidades({ versoes: [] })).toThrow(/lista vazia/);
    expect(() =>
      validarNovidades({
        versoes: [{ versao: '1.0', data: '2026-10-14', titulo: 'x', itens: ['a'] }],
      }),
    ).toThrow(/incompleta/);
    expect(() =>
      validarNovidades({
        versoes: [{ versao: '1.0.0', data: '2026-10-14', titulo: 'x', itens: [] }],
      }),
    ).toThrow(/incompleta/);
  });
});
