import { describe, expect, it } from 'vitest';
import { diasEntre, idadeEmAnos, idadeInteira } from '../src/domain/datas';
import { letraDaCrianca, letraPadrao } from '../src/domain/letra';

describe('idadeEmAnos', () => {
  const hoje = new Date(2026, 9, 14);
  it('calcula a idade com uma casa decimal', () => {
    expect(idadeEmAnos('2021-04-14', hoje)).toBe(5.5);
    expect(idadeEmAnos('2021-07-14', hoje)).toBe(5.2);
    expect(idadeInteira('2021-04-14', hoje)).toBe(5);
  });
  it('faz aniversário exatamente no dia', () => {
    expect(idadeInteira('2020-10-14', hoje)).toBe(6);
    expect(idadeInteira('2020-10-15', hoje)).toBe(5);
  });
  it('rejeita data inválida', () => {
    expect(() => idadeEmAnos('15/03/2021', hoje)).toThrow(/inválida/);
  });
});

describe('diasEntre', () => {
  it('é simétrico', () => {
    expect(diasEntre('2026-10-01T00:00:00Z', '2026-10-15T00:00:00Z')).toBe(14);
    expect(diasEntre('2026-10-15T00:00:00Z', '2026-10-01T00:00:00Z')).toBe(14);
  });
});

describe('letra padrão (§5.8)', () => {
  it('segue a idade nas vertentes sem preferência', () => {
    const f = { vertentePrincipal: 'Clássico' as const };
    expect(letraPadrao(4.9, f)).toBe('bastao');
    expect(letraPadrao(5, f)).toBe('script');
    expect(letraPadrao(6, f)).toBe('cursiva');
  });
  it('Montessori e Waldorf começam na cursiva', () => {
    expect(letraPadrao(3, { vertentePrincipal: 'Montessori' })).toBe('cursiva');
    expect(letraPadrao(3, { vertentePrincipal: 'Waldorf' })).toBe('cursiva');
  });
  it('a escolha do pai prevalece sobre o padrão', () => {
    expect(letraDaCrianca({ letra: 'bastao' }, 7, { vertentePrincipal: 'Waldorf' })).toBe('bastao');
    expect(letraDaCrianca({ letra: null }, 7, { vertentePrincipal: 'Clássico' })).toBe('cursiva');
  });
});
