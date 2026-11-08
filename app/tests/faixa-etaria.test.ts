import { describe, expect, it } from 'vitest';
import { dataValida } from '../src/domain/datas';
import { faixaEtaria, IDADE_MAXIMA, IDADE_MINIMA } from '../src/domain/faixa';
import { DURACAO_PADRAO, DURACOES } from '../src/domain/sessao';
import { validarConteudo } from '../src/domain/conteudo';
import { gerarPacote, type EntradaPacote } from '../src/pacote/gerar';
import { carregarConteudo } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import { AGORA, atividade, conteudoBase, crianca, familia } from './fabricas';

describe('faixa etária de 2 a 8 anos (#71)', () => {
  const hoje = new Date(2026, 10, 8);
  it('vai de 2 a 8 anos', () => {
    expect([IDADE_MINIMA, IDADE_MAXIMA]).toEqual([2, 8]);
  });
  it('aceita a partir do segundo aniversário, no próprio dia', () => {
    expect(faixaEtaria('2024-11-08', hoje)).toBe('dentro');
    expect(faixaEtaria('2024-11-09', hoje)).toBe('abaixo');
  });
  it('vai até o dia anterior ao 9º aniversário', () => {
    expect(faixaEtaria('2018-11-09', hoje)).toBe('dentro');
    expect(faixaEtaria('2017-11-08', hoje)).toBe('acima');
  });
  it('trata data inválida como fora da faixa, sem lançar erro', () => {
    expect(faixaEtaria('ontem', hoje)).toBe('invalida');
  });
});

describe('dataValida', () => {
  it('só aceita data real no formato AAAA-MM-DD', () => {
    expect(dataValida('2026-11-08')).toBe(true);
    expect(dataValida('2024-02-29')).toBe(true);
    expect(dataValida('2026-02-29')).toBe(false);
    expect(dataValida('2026-13-01')).toBe(false);
    expect(dataValida('08/11/2026')).toBe(false);
  });
});

describe('sessão padrão de 30 minutos', () => {
  it('oferece 30 min e começa por ele', () => {
    expect(DURACOES).toContain(30);
    expect(DURACAO_PADRAO).toBe(30);
  });
});

describe('atividades para 2 anos (validação)', () => {
  const comDois = (extra = {}) =>
    atividade('atv-2', ['LG.FON.01'], { idade: [2, 4], duracaoMin: 8, ...extra });
  const validar = (a: ReturnType<typeof atividade>) =>
    validarConteudo({ ...conteudoBase(), atividades: [a] }).erros;

  it('exige o aviso de materiais pequenos (engasgo)', () => {
    expect(validar(comDois()).some((e) => /cuidados/.test(e))).toBe(true);
    expect(
      validar(comDois({ cuidados: 'Nada que caiba na boca. Fique junto o tempo todo.' })),
    ).toEqual([]);
  });
  it('só aceita atividades curtas (até 10 min), para juntar várias na sessão', () => {
    const erros = validar(comDois({ cuidados: 'Fique junto.', duracaoMin: 20 }));
    expect(erros.some((e) => /até 10 min/.test(e))).toBe(true);
  });
  it('quem começa aos 3 anos ou mais não precisa do aviso nem da duração curta', () => {
    expect(validar(atividade('atv-3', ['LG.FON.01'], { idade: [3, 6], duracaoMin: 20 }))).toEqual(
      [],
    );
  });
});

describe('pacote: preparação à parte', () => {
  const idx = criarIndice(carregarConteudo());
  const base: Omit<EntradaPacote, 'atividades'> = {
    sessao: {
      id: 's1',
      codigo: 'S-1',
      criancaId: 'c1',
      criadaEm: AGORA,
      duracaoMin: 30,
      foco: 'equilibrado',
      atividadeIds: ['a'],
      livroId: null,
    },
    familia: familia(),
    crianca: crianca(),
    idade: 2.5,
    letra: 'bastao',
    livro: null,
    marco: (id: string) => idx.marco(id),
  };
  it('mostra a duração e a preparação em campos separados e imprime os cuidados', () => {
    const a = atividade('a', [], {
      dominio: 'AR',
      categoria: 'Escuta musical',
      idade: [2, 4],
      duracaoMin: 8,
      preparoMin: 12,
      cuidados: 'Tampas seladas pelo adulto.',
    });
    const doc = gerarPacote({ ...base, atividades: [a] });
    expect(doc).toContain('Prepare antes · 12 min');
    expect(doc).toContain('~8 min');
    expect(doc).toContain('Tampas seladas pelo adulto.');
  });
  it('sem preparoMin informado, mantém os 5 min de sempre', () => {
    const doc = gerarPacote({ ...base, atividades: [atividade('a', ['LG.FON.01'])] });
    expect(doc).toContain('Prepare antes · 5 min');
  });
});
