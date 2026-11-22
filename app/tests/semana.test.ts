import { describe, expect, it } from 'vitest';
import {
  marcarFeito,
  materiaisDaSemana,
  planejarSemana,
  removerAtividade,
  diaPassou,
  inicioDaSemana,
  segundaDaSemana,
  semanaPadrao,
  trocarAtividade,
  type EntradaSemana,
} from '../src/domain/semana';
import { carregarConteudo } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import { posicionarAqui } from '../src/domain/jornada';
import type { EstadosCrianca } from '../src/domain/tipos';
import { crianca, familia } from './fabricas';

// O planejador é testado com o conteúdo-base (itens sem `revisao`, o conjunto que existia quando este teste
// foi escrito) para que a aprovação de conteúdo novo não mude as atividades esperadas (#8).
const conteudoAtual = carregarConteudo();
const semRevisao = <T extends { revisao?: unknown }>(itens: T[]): T[] =>
  itens.filter((i) => i.revisao === undefined);
const idx = criarIndice({
  ...conteudoAtual,
  marcos: semRevisao(conteudoAtual.marcos),
  atividades: semRevisao(conteudoAtual.atividades),
});
const AGORA = '2026-11-09T12:00:00.000Z'; // uma segunda-feira
const pista = (id: string) => ({
  linha: { id, nome: id, vertentes: null },
  dominio: idx.conteudo.dominios[0]!,
});
// "Está aqui" em LG.FON.04 e MA.SEN.06: os marcos anteriores ficam consolidados.
const estados: EstadosCrianca = {
  ...posicionarAqui(idx, pista('LG.FON'), 'LG.FON.04', {}, AGORA),
  ...posicionarAqui(idx, pista('MA.SEN'), 'MA.SEN.06', {}, AGORA),
};

function entrada(extra: Partial<EntradaSemana> = {}): EntradaSemana {
  return {
    familia: familia(),
    crianca: crianca({ id: 'c1', nome: 'Ana' }),
    idade: 5.6,
    estados,
    historico: [],
    rotina: { dias: ['seg', 'qua', 'sex'], duracaoMin: 40 },
    agora: AGORA,
    inicio: '2026-11-09',
    id: 'plano-1',
    ...extra,
  };
}

describe('segundaDaSemana', () => {
  it('devolve a segunda-feira da semana, no calendário local', () => {
    expect(segundaDaSemana(new Date(2026, 10, 9))).toBe('2026-11-09'); // segunda
    expect(segundaDaSemana(new Date(2026, 10, 11))).toBe('2026-11-09'); // quarta
    expect(segundaDaSemana(new Date(2026, 10, 15))).toBe('2026-11-09'); // domingo fecha a semana
  });
});

describe('semana seguinte (D11, #141)', () => {
  // Hora local do aparelho, como o app faz (o teste vale em qualquer fuso). 20/11/2026 é sexta.
  const em = (dia: number, h = 0, min = 0) => new Date(2026, 10, dia, h, min);

  it('padrão: a atual até sexta 11:59; a próxima de sexta 12:00 até domingo', () => {
    expect(semanaPadrao(em(16, 0, 0))).toBe('esta'); // segunda 00:00
    expect(semanaPadrao(em(19, 23, 59))).toBe('esta'); // quinta
    expect(semanaPadrao(em(20, 11, 59))).toBe('esta'); // sexta 11:59
    expect(semanaPadrao(em(20, 12, 0))).toBe('proxima'); // sexta 12:00
    expect(semanaPadrao(em(21, 9))).toBe('proxima'); // sábado
    expect(semanaPadrao(em(22, 23, 59))).toBe('proxima'); // domingo
    expect(semanaPadrao(em(23, 0, 0))).toBe('esta'); // segunda 00:00 volta à atual
  });

  it('o início da próxima semana é a segunda seguinte, também na virada de mês e de ano', () => {
    expect(inicioDaSemana(em(21), 'esta')).toBe('2026-11-16');
    expect(inicioDaSemana(em(21), 'proxima')).toBe('2026-11-23');
    expect(inicioDaSemana(new Date(2026, 11, 30), 'proxima')).toBe('2027-01-04');
  });

  it('planeja a partir do início recebido, sem dias passados num sábado', () => {
    const sabado = em(21, 10);
    const inicio = inicioDaSemana(sabado, semanaPadrao(sabado));
    const p = planejarSemana(idx, entrada({ agora: sabado.toISOString(), inicio }));
    expect(p.inicio).toBe('2026-11-23');
    expect(p.dias.map((d) => d.data)).toEqual(['2026-11-23', '2026-11-25', '2026-11-27']);
    expect(p.dias.some((d) => diaPassou(d, sabado))).toBe(false);
  });

  it('dia passado é o anterior a hoje; hoje ainda vale', () => {
    const quarta = em(18, 15);
    expect(diaPassou({ data: '2026-11-17' }, quarta)).toBe(true);
    expect(diaPassou({ data: '2026-11-18' }, quarta)).toBe(false);
    expect(diaPassou({ data: '2026-11-19' }, quarta)).toBe(false);
  });
});

describe('planejarSemana (#8)', () => {
  it('cria um dia para cada dia escolhido, em ordem, com as datas da semana', () => {
    const p = planejarSemana(idx, entrada({ rotina: { dias: ['sex', 'seg'], duracaoMin: 40 } }));
    expect(p.dias.map((d) => [d.dia, d.data])).toEqual([
      ['seg', '2026-11-09'],
      ['sex', '2026-11-13'],
    ]);
    expect(p.dias.every((d) => d.duracaoMin === 40 && !d.feito)).toBe(true);
  });
  it('não repete atividade na semana e alterna as linhas', () => {
    const p = planejarSemana(idx, entrada());
    const todas = p.dias.flatMap((d) => d.atividadeIds);
    expect(new Set(todas).size).toBe(todas.length);
    // Alterna as linhas: Linguagem e Matemática ocupam dias diferentes. Qual vem primeiro gira com a
    // data (semente do dia, §5.6), então o teste não fixa a ordem.
    const diaDe = (id: string) => p.dias.findIndex((d) => d.atividadeIds.includes(id));
    expect(diaDe('atv-caca-silabas')).toBeGreaterThanOrEqual(0);
    expect(diaDe('atv-feira-numeros')).toBeGreaterThanOrEqual(0);
    expect(diaDe('atv-caca-silabas')).not.toBe(diaDe('atv-feira-numeros'));
  });
  it('é determinístico', () => {
    expect(planejarSemana(idx, entrada())).toEqual(planejarSemana(idx, entrada()));
  });
  it('não conta sessões antigas (mais de 14 dias) como repetição', () => {
    const velha = {
      id: 's',
      codigo: 'S-1',
      criancaId: 'c1',
      criadaEm: '2026-10-01T12:00:00.000Z',
      duracaoMin: 40,
      foco: 'equilibrado' as const,
      atividadeIds: ['atv-caca-silabas'],
      livroId: null,
    };
    const p = planejarSemana(idx, entrada({ historico: [velha] }));
    expect(p.dias.flatMap((d) => d.atividadeIds)).toContain('atv-caca-silabas');
  });
});

describe('editar o plano', () => {
  it('remove uma atividade de um dia, sem mexer nos outros', () => {
    const p = planejarSemana(idx, entrada());
    const alvo = p.dias[0]!.atividadeIds[0]!;
    const q = removerAtividade(p, 'seg', alvo);
    expect(q.dias[0]!.atividadeIds).not.toContain(alvo);
    expect(q.dias[1]).toEqual(p.dias[1]);
    expect(p.dias[0]!.atividadeIds).toContain(alvo); // imutável
  });
  it('marca e desmarca o dia como feito, guardando a sessão registrada', () => {
    const p = planejarSemana(idx, entrada());
    const feito = marcarFeito(p, 'qua', true, 's-9');
    expect(feito.dias[1]).toMatchObject({ feito: true, sessaoId: 's-9' });
    expect(marcarFeito(feito, 'qua', false).dias[1]?.feito).toBe(false);
  });
  it('trocar escolhe outra atividade da mesma linha que ainda não está na semana', () => {
    const p = planejarSemana(idx, entrada());
    const r = trocarAtividade(idx, entrada(), p, 'seg', 'atv-caca-silabas');
    // com o conteúdo atual só há uma atividade nessa linha: não há troca possível
    expect(r).toBeNull();
  });
});

describe('materiaisDaSemana (#9)', () => {
  it('consolida os materiais sem repetir, com os dias em que cada um é usado', () => {
    const p = planejarSemana(idx, entrada());
    const lista = materiaisDaSemana(idx, p);
    const itens = lista.map((m) => m.item);
    expect(new Set(itens).size).toBe(itens.length);
    const feijao = lista.find((m) => /feij/i.test(m.item));
    const diaDaFeira = p.dias.find((d) => d.atividadeIds.includes('atv-feira-numeros'))?.dia;
    expect(feijao?.dias).toEqual([diaDaFeira]);
    expect(lista.every((m) => m.dias.length > 0)).toBe(true);
  });
});
