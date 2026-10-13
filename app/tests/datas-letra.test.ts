import { describe, expect, it } from 'vitest';
import { dataBR, dataLocalISO, diasEntre, idadeEmAnos, idadeInteira } from '../src/domain/datas';
import { ehLetra, letraDaCrianca, letraPadrao } from '../src/domain/letra';

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

describe('datas no fuso do aparelho', () => {
  // Uma sessão criada às 22h do dia 13 (horário local) é do dia 13, mesmo que em UTC já seja dia 14.
  const noiteDo13 = new Date(2026, 9, 13, 22, 30);
  it('dataBR formata no dia local', () => {
    expect(dataBR(noiteDo13.toISOString())).toBe('13/10/2026');
  });
  it('dataLocalISO devolve AAAA-MM-DD local', () => {
    expect(dataLocalISO(noiteDo13)).toBe('2026-10-13');
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
  it('valor desconhecido (ex.: backup adulterado) cai no padrão', () => {
    expect(ehLetra('cursiva')).toBe(true);
    expect(ehLetra('"><img>')).toBe(false);
    expect(
      letraDaCrianca({ letra: '"><img>' as never }, 7, { vertentePrincipal: 'Clássico' }),
    ).toBe('cursiva');
  });
  it('a escolha do pai prevalece sobre o padrão', () => {
    expect(letraDaCrianca({ letra: 'bastao' }, 7, { vertentePrincipal: 'Waldorf' })).toBe('bastao');
    expect(letraDaCrianca({ letra: null }, 7, { vertentePrincipal: 'Clássico' })).toBe('cursiva');
  });
});
