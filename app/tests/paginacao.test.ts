import { describe, expect, it } from 'vitest';
import {
  TAMANHO_PAGINA,
  fatiarPagina,
  restantes,
  textoContagem,
  proximoLote,
  mostrarLimparFiltros,
} from '../src/domain/paginacao';

const itens = Array.from({ length: 134 }, (_, i) => i);

describe('paginação da lista de atividades (#130)', () => {
  it('mostra 20 por vez', () => {
    expect(TAMANHO_PAGINA).toBe(20);
    expect(fatiarPagina(itens, 20)).toHaveLength(20);
    expect(fatiarPagina(itens, 40)).toHaveLength(40);
    expect(fatiarPagina(itens, 40)[39]).toBe(39);
  });

  it('não passa do total nem aceita quantidade inválida', () => {
    expect(fatiarPagina([1, 2, 3], 20)).toEqual([1, 2, 3]);
    expect(fatiarPagina(itens, -5)).toEqual([]);
    expect(fatiarPagina(itens, Number.NaN)).toEqual([]);
  });

  it('calcula os restantes', () => {
    expect(restantes(134, 20)).toBe(114);
    expect(restantes(134, 140)).toBe(0);
    expect(restantes(0, 20)).toBe(0);
  });

  it('o próximo lote é de até 20, nunca mais que o que falta', () => {
    expect(proximoLote(134, 20)).toBe(20);
    expect(proximoLote(134, 120)).toBe(14);
    expect(proximoLote(134, 134)).toBe(0);
  });

  it('texto da contagem', () => {
    expect(textoContagem(134, 20)).toBe('Mostrando 20 de 134 atividades');
    expect(textoContagem(134, 200)).toBe('Mostrando 134 de 134 atividades');
    expect(textoContagem(1, 20)).toBe('Mostrando 1 de 1 atividade');
    expect(textoContagem(0, 20)).toBe('Nenhuma atividade encontrada');
  });

  it('"Limpar filtros" só aparece com texto ou filtro ativo', () => {
    const vazio = { texto: '', dominio: '', vertente: '', duracao: '', idade: '' };
    expect(mostrarLimparFiltros(vazio)).toBe(false);
    expect(mostrarLimparFiltros({ texto: '   ' })).toBe(false);
    expect(mostrarLimparFiltros({ ...vazio, texto: 'feira' })).toBe(true);
    expect(mostrarLimparFiltros({ ...vazio, dominio: 'MA' })).toBe(true);
    expect(mostrarLimparFiltros({ ...vazio, vertente: 'Waldorf' })).toBe(true);
    expect(mostrarLimparFiltros({ ...vazio, duracao: '20' })).toBe(true);
    expect(mostrarLimparFiltros({ ...vazio, idade: 'crianca' })).toBe(true);
  });
});
