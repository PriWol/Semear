import { describe, expect, it } from 'vitest';
import { buscarAtividades, dominioDaAtividade } from '../src/domain/busca';
import { validarConteudo } from '../src/domain/conteudo';
import { validarBackup } from '../src/dados/repositorio';
import { atividade, conteudoBase, marco } from './fabricas';

const caca = atividade('atv-caca', ['LG.FON.04'], {
  titulo: 'Caça às sílabas',
  objetivo: 'Separar figuras pela sílaba inicial.',
  palavrasChave: ['rimas', 'dinossauros'],
  idade: [4, 7],
  duracaoMin: 30,
  vertentes: ['Montessori'],
});
const feira = atividade('atv-feira', ['MA.SEN.06'], {
  titulo: 'Feira dos números',
  objetivo: 'Contar até 20 com objetos.',
  idade: [5, 7],
  duracaoMin: 35,
  vertentes: ['Waldorf'],
});
const todas = [caca, feira];
const existentes = new Set(['LG.FON.04', 'MA.SEN.06']);
const idx = { marco: (id: string) => (existentes.has(id) ? marco(id, 1) : undefined) };
const ids = (r: { atividade: { id: string } }[]) => r.map((x) => x.atividade.id);

describe('busca de atividades (#13)', () => {
  it('ignora acento e maiúsculas: "silaba" encontra "sílabas"', () => {
    expect(ids(buscarAtividades(todas, { texto: 'SILABA' }, idx))).toEqual(['atv-caca']);
  });
  it('acha pelo objetivo, pelas palavras-chave e pelo id do marco', () => {
    expect(ids(buscarAtividades(todas, { texto: 'contar' }, idx))).toEqual(['atv-feira']);
    expect(ids(buscarAtividades(todas, { texto: 'dinossauros' }, idx))).toEqual(['atv-caca']);
    expect(ids(buscarAtividades(todas, { texto: 'MA.SEN.06' }, idx))).toEqual(['atv-feira']);
  });
  it('todos os termos precisam aparecer (e); sem texto traz tudo em ordem de título', () => {
    expect(buscarAtividades(todas, { texto: 'silaba numeros' }, idx)).toEqual([]);
    expect(ids(buscarAtividades(todas, { texto: '  ' }, idx))).toEqual(['atv-caca', 'atv-feira']);
  });
  it('título pesa mais que objetivo', () => {
    const a = atividade('a', ['LG.FON.01'], { titulo: 'Rimas', objetivo: 'x' });
    const b = atividade('b', ['LG.FON.01'], { titulo: 'Outra', objetivo: 'Brincar com rimas.' });
    expect(ids(buscarAtividades([b, a], { texto: 'rimas' }, idx))).toEqual(['a', 'b']);
  });
  it('filtra por domínio, idade, vertente e duração máxima', () => {
    expect(ids(buscarAtividades(todas, { texto: '', dominio: 'MA' }, idx))).toEqual(['atv-feira']);
    expect(ids(buscarAtividades(todas, { texto: '', idade: 4 }, idx))).toEqual(['atv-caca']);
    expect(ids(buscarAtividades(todas, { texto: '', vertente: 'Waldorf' }, idx))).toEqual([
      'atv-feira',
    ]);
    expect(ids(buscarAtividades(todas, { texto: '', duracaoMax: 30 }, idx))).toEqual(['atv-caca']);
  });
  it('marco escondido não casa na busca por id nem define o domínio', () => {
    const rascunho = atividade('atv-cad', ['DI.CAD.04'], { titulo: 'Caderneta', dominio: 'AR' });
    expect(buscarAtividades([rascunho], { texto: 'DI.CAD.04' }, idx)).toEqual([]);
    expect(dominioDaAtividade(rascunho, idx)).toBe('AR');
  });
  it('o domínio vem do marco principal, ou do campo "dominio" nas complementares', () => {
    expect(dominioDaAtividade(caca, idx)).toBe('LG');
    const comp = atividade('c', [], { dominio: 'AR', categoria: 'Canto' });
    expect(dominioDaAtividade(comp, idx)).toBe('AR');
  });
});

describe('palavras-chave e sessão avulsa', () => {
  it('validação recusa palavras-chave que não são lista de textos', () => {
    const c = conteudoBase();
    const ruim = atividade('atv-x', ['LG.FON.01'], { palavrasChave: ['ok', ' '] });
    expect(
      validarConteudo({ ...c, atividades: [ruim] }).erros.some((e) => /palavrasChave/.test(e)),
    ).toBe(true);
    const boa = atividade('atv-y', ['LG.FON.01'], { palavrasChave: ['rimas'] });
    expect(validarConteudo({ ...c, atividades: [boa] }).erros).toEqual([]);
  });
  it('o backup aceita tipo "avulsa" e recusa outro valor', () => {
    const base = {
      app: 'semear',
      versao: 1,
      exportadoEm: '2026-11-08T00:00:00.000Z',
      familia: null,
      criancas: [],
      estados: [],
      historico: [],
      sessoes: [
        {
          id: 's',
          codigo: 'S-1',
          criancaId: 'c',
          criadaEm: 'x',
          duracaoMin: 30,
          foco: 'equilibrado',
          atividadeIds: ['a'],
          livroId: null,
          tipo: 'avulsa',
        },
      ],
    };
    expect(() => validarBackup(base)).not.toThrow();
    const ruim = { ...base, sessoes: [{ ...base.sessoes[0], tipo: 'outra' }] };
    expect(() => validarBackup(ruim)).toThrow();
  });
});
