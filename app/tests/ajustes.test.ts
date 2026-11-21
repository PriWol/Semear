import { describe, expect, it } from 'vitest';
import { horaDe24h } from '../src/domain/lembretes';
import { resumoUltimaCopia } from '../src/domain/backup';
import { confirmacaoApagarTudo } from '../src/domain/confirmacao';

const AGORA = '2026-11-21T12:00:00.000Z';
const diasAntes = (n: number) => new Date(new Date(AGORA).getTime() - n * 86_400_000).toISOString();

describe('hora do aviso em 24 h (campos de hora e minuto)', () => {
  it('junta hora e minuto em HH:MM, com zero à esquerda', () => {
    expect(horaDe24h('8', '0')).toBe('08:00');
    expect(horaDe24h('07', '30')).toBe('07:30');
    expect(horaDe24h(' 23 ', '59')).toBe('23:59');
    expect(horaDe24h('0', '5')).toBe('00:05');
  });
  it('recusa hora e minuto fora do relógio de 24 h', () => {
    expect(horaDe24h('24', '00')).toBeNull();
    expect(horaDe24h('-1', '00')).toBeNull();
    expect(horaDe24h('12', '60')).toBeNull();
    expect(horaDe24h('12', '-5')).toBeNull();
  });
  it('recusa vazio, texto, decimal e notação científica', () => {
    expect(horaDe24h('', '00')).toBeNull();
    expect(horaDe24h('08', '')).toBeNull();
    expect(horaDe24h('oito', '00')).toBeNull();
    expect(horaDe24h('8.5', '00')).toBeNull();
    expect(horaDe24h('1e1', '00')).toBeNull();
    expect(horaDe24h('123', '00')).toBeNull();
  });
});

describe('resumo da última cópia de segurança', () => {
  it('nunca: pede a primeira cópia, com alerta', () => {
    expect(resumoUltimaCopia(null, AGORA)).toEqual({ estado: 'nunca', dias: null, alerta: true });
  });
  it('menos de 30 dias: sem alerta', () => {
    expect(resumoUltimaCopia(diasAntes(0), AGORA)).toMatchObject({
      estado: 'recente',
      dias: 0,
      alerta: false,
    });
    expect(resumoUltimaCopia(diasAntes(12.4), AGORA)).toMatchObject({ dias: 12, alerta: false });
    expect(resumoUltimaCopia(diasAntes(29.9), AGORA)).toMatchObject({ dias: 29, alerta: false });
  });
  it('30 dias ou mais: alerta', () => {
    expect(resumoUltimaCopia(diasAntes(30), AGORA)).toMatchObject({
      estado: 'antiga',
      dias: 30,
      alerta: true,
    });
    expect(resumoUltimaCopia(diasAntes(95), AGORA)).toMatchObject({ dias: 95, alerta: true });
  });
  it('data no futuro (relógio mudou) não vira alerta nem dias negativos', () => {
    expect(resumoUltimaCopia(diasAntes(-3), AGORA)).toMatchObject({ dias: 0, alerta: false });
  });
});

describe('confirmação digitada para apagar tudo', () => {
  it('aceita APAGAR, sem diferença de caixa nem espaços nas pontas', () => {
    expect(confirmacaoApagarTudo('APAGAR')).toBe(true);
    expect(confirmacaoApagarTudo(' apagar ')).toBe(true);
  });
  it('recusa qualquer outra coisa', () => {
    expect(confirmacaoApagarTudo('')).toBe(false);
    expect(confirmacaoApagarTudo('APAGA')).toBe(false);
    expect(confirmacaoApagarTudo('APAGAR TUDO')).toBe(false);
    expect(confirmacaoApagarTudo('A P A G A R')).toBe(false);
  });
});
