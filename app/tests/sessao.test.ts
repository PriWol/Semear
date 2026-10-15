import { describe, expect, it } from 'vitest';
import {
  atividadesRecentes,
  complementares,
  gerarCodigoSessao,
  pontuar,
  proporSessao,
  proximaAlternativa,
  sugerirLivro,
  type Escolha,
  type PedidoSessao,
} from '../src/domain/sessao';
import type { EstadosCrianca, Sessao } from '../src/domain/tipos';
import { AGORA, atividade, crianca, familia, indiceBase } from './fabricas';

const idx = indiceBase();

function pedido(extra: Partial<PedidoSessao> = {}): PedidoSessao {
  return {
    familia: familia(),
    crianca: crianca(),
    idade: 5,
    estados: {},
    historico: [],
    duracaoMin: 40,
    foco: 'equilibrado',
    agora: AGORA,
    ...extra,
  };
}

function sessao(atividadeIds: string[], criadaEm = AGORA): Sessao {
  return {
    id: `s-${atividadeIds.join('-')}`,
    codigo: 'S-1',
    criancaId: 'c1',
    criadaEm,
    duracaoMin: 40,
    foco: 'equilibrado',
    atividadeIds,
    livroId: null,
  };
}

describe('pontuação da atividade (§5.6, passo 3)', () => {
  it('soma vertente principal, inspiração, idade e novidade', () => {
    const a = atividade('x', ['LG.FON.01'], {
      vertentes: ['Montessori', 'Waldorf'],
      idade: [4, 6],
    });
    const f = familia({ inspiracoes: ['Waldorf'] });
    expect(pontuar(a, f, 5, new Set()).pontos).toBe(3 + 1 + 2 + 2);
    expect(pontuar(a, f, 7, new Set(['x'])).pontos).toBe(3 + 1);
  });
});

describe('proporSessao', () => {
  it('sugere atividades para os marcos ativos, a melhor pontuada primeiro', () => {
    const p = proporSessao(idx, pedido({ foco: ['LG.FON'] }));
    // atv-fon-1 é Montessori (+3); atv-fon-1b é Waldorf e fica de fora (já há uma por pista nesta rodada e não sobra outra pista)
    expect(p.escolhas.map((e) => e.atividade.id)).toEqual(['atv-fon-1', 'atv-fon-1b']);
    expect(p.escolhas[0]!.pista).toBe('LG.FON');
  });

  it('alterna entre as pistas e respeita a duração com 10% de folga', () => {
    const p = proporSessao(idx, pedido({ duracaoMin: 40 }));
    // LG.FON (20) + MA.SEN (15) = 35; a próxima de LG.FON (20) estouraria 44 min
    expect(p.escolhas.map((e) => e.atividade.id)).toEqual(['atv-fon-1', 'atv-sen-1']);
    expect(p.minutos).toBe(35);
  });

  it('sempre sugere ao menos uma atividade, avisando se passar do tempo', () => {
    const p = proporSessao(idx, pedido({ duracaoMin: 10, foco: ['LG.FON'] }));
    expect(p.escolhas).toHaveLength(1);
    expect(p.avisos[0]).toMatch(/mais do que os 10 min/);
  });

  it('o modo equilibrado prioriza a linha menos trabalhada nas últimas 2 semanas', () => {
    const historico = [sessao(['atv-fon-1'], '2026-10-10T10:00:00.000Z')];
    const p = proporSessao(idx, pedido({ duracaoMin: 15, historico }));
    expect(p.escolhas[0]!.atividade.id).toBe('atv-sen-1');
  });

  it('sessões com mais de 14 dias não contam como recentes', () => {
    const antiga = [sessao(['atv-fon-1'], '2026-09-01T10:00:00.000Z')];
    const p = proporSessao(idx, pedido({ duracaoMin: 15, foco: ['LG.FON'], historico: antiga }));
    expect(p.escolhas[0]!.motivos).toContain('não feita nas últimas 2 semanas');
  });

  it('registra lacunas: marcos ativos sem atividade publicada', () => {
    const estados: EstadosCrianca = {
      'LG.FON.01': { estado: 'consolidado', atualizadoEm: AGORA, origem: 'manual' },
      'LG.FON.02': { estado: 'consolidado', atualizadoEm: AGORA, origem: 'manual' },
      'MA.SEN.01': { estado: 'consolidado', atualizadoEm: AGORA, origem: 'manual' },
    };
    const p = proporSessao(idx, pedido({ estados }));
    expect(p.lacunas.map((l) => l.pista)).toEqual(['LG.FON', 'MA.SEN']);
    expect(p.escolhas).toEqual([]);
  });

  it('ignora atividades que não estão publicadas', () => {
    const rascunho = indiceBase({
      atividades: [
        atividade('r', ['LG.FON.01'], { autoria: { origem: 'ia', status: 'rascunho' } }),
      ],
    });
    expect(proporSessao(rascunho, pedido({ foco: ['LG.FON'] })).escolhas).toEqual([]);
  });

  it('é determinística: o mesmo pedido gera a mesma sugestão', () => {
    expect(proporSessao(idx, pedido())).toEqual(proporSessao(idx, pedido()));
  });

  it('foco com pista inexistente avisa em vez de quebrar', () => {
    const p = proporSessao(idx, pedido({ foco: ['XX.YYY'] }));
    expect(p.escolhas).toEqual([]);
    expect(p.avisos).toContain('Escolha pelo menos uma linha de foco.');
  });
});

describe('sugerirLivro', () => {
  it('escolhe um livro ligado aos marcos da sessão', () => {
    const escolhas = [{ atividade: idx.atividade('atv-fon-2')! }];
    // atv-fon-2 revisa LG.FON.01, que está no livro-a
    expect(sugerirLivro(idx, escolhas, familia(), 5)?.id).toBe('livro-a');
    expect(
      sugerirLivro(idx, [{ atividade: idx.atividade('atv-sen-1')! }], familia(), 5),
    ).toBeNull();
  });
});

describe('código da sessão', () => {
  const data = new Date(2026, 9, 14);
  it('usa mês/dia, inicial sem acento e número sequencial', () => {
    expect(gerarCodigoSessao('Ágata', data, [])).toBe('S-1014-A1');
    expect(gerarCodigoSessao('Ana', data, ['S-1014-A1', 'S-1014-A2'])).toBe('S-1014-A3');
  });
  it('não quebra com nome sem letras', () => {
    expect(gerarCodigoSessao('123', data, [])).toBe('S-1014-X1');
  });
});

describe('proximaAlternativa (botão Trocar)', () => {
  const e = (id: string) =>
    ({
      atividade: atividade(id, ['LG.FON.01']),
      pista: 'LG.FON',
      pontos: 0,
      motivos: [],
    }) as Escolha;
  const candidatas = [e('a'), e('b'), e('c')];
  it('percorre todas as candidatas em ciclo', () => {
    expect(proximaAlternativa(candidatas, 'a', new Set())?.atividade.id).toBe('b');
    expect(proximaAlternativa(candidatas, 'b', new Set())?.atividade.id).toBe('c');
    expect(proximaAlternativa(candidatas, 'c', new Set())?.atividade.id).toBe('a');
  });
  it('pula atividades já escolhidas em outra posição da sessão', () => {
    expect(proximaAlternativa(candidatas, 'a', new Set(['b']))?.atividade.id).toBe('c');
  });
  it('sem outra opção, devolve null', () => {
    expect(proximaAlternativa([e('a')], 'a', new Set())).toBeNull();
  });
});

describe('atividadesRecentes', () => {
  it('considera só as sessões da criança nas últimas 2 semanas', () => {
    const historico = [
      sessao(['nova'], '2026-10-10T10:00:00.000Z'),
      sessao(['velha'], '2026-09-01T10:00:00.000Z'),
      { ...sessao(['outra-crianca'], AGORA), criancaId: 'c2' },
    ];
    expect([...atividadesRecentes(historico, 'c1', AGORA)]).toEqual(['nova']);
  });
});

describe('atividades complementares (§3.0)', () => {
  const comp = (id: string, extra = {}) =>
    atividade(id, [], { dominio: 'AR', categoria: 'Escuta musical', duracaoMin: 10, ...extra });

  it('entra no máximo uma complementar, depois das atividades da jornada', () => {
    const i = indiceBase({
      atividades: [atividade('atv-fon-1', ['LG.FON.01']), comp('c1'), comp('c2')],
    });
    const p = proporSessao(i, pedido());
    expect(p.escolhas.map((e) => e.atividade.id)).toEqual(['atv-fon-1', 'c1']);
    expect(p.escolhas[1]?.pista).toBe('complementar');
  });

  it('não entra se estoura a duração, e ignora rascunho e idade fora da faixa', () => {
    const i = indiceBase({
      atividades: [
        atividade('atv-fon-1', ['LG.FON.01'], { duracaoMin: 20 }),
        comp('grande', { duracaoMin: 30 }),
        comp('rascunho', { autoria: { origem: 'ia', status: 'rascunho' } }),
        comp('velha', { idade: [7, 8] }),
      ],
    });
    const p = proporSessao(i, pedido({ duracaoMin: 20 }));
    expect(p.escolhas.map((e) => e.atividade.id)).toEqual(['atv-fon-1']);
  });

  it('atividade de idioma não vira complementar', () => {
    const i = indiceBase({ atividades: [comp('en', { idioma: 'en' }), comp('pt')] });
    const alts = complementares(i, familia(), 5, new Set());
    expect(alts.map((e) => e.atividade.id)).toEqual(['pt']);
  });

  it('sem atividades da jornada, a sessão pode ser só a complementar (educadora no controle)', () => {
    const i = indiceBase({ atividades: [comp('so')] });
    const p = proporSessao(i, pedido({ duracaoMin: 20 }));
    expect(p.escolhas.map((e) => e.atividade.id)).toEqual(['so']);
  });

  it('prefere a que não foi feita nas últimas 2 semanas', () => {
    const i = indiceBase({ atividades: [comp('a'), comp('b')] });
    const p = proporSessao(i, pedido({ historico: [sessao(['a'])], duracaoMin: 20 }));
    expect(p.escolhas.map((e) => e.atividade.id)).toEqual(['b']);
  });

  it('o Trocar percorre as outras complementares', () => {
    const i = indiceBase({ atividades: [comp('a'), comp('b')] });
    const alts = complementares(i, familia(), 5, new Set());
    expect(alts.map((e) => e.atividade.id).sort()).toEqual(['a', 'b']);
    expect(alts.every((e) => e.pista === 'complementar')).toBe(true);
  });
});

describe('complementar e foco escolhido', () => {
  it('com linhas de foco escolhidas à mão, não acrescenta complementar', () => {
    const i = indiceBase({
      atividades: [
        atividade('atv-fon-1', ['LG.FON.01']),
        atividade('c1', [], { dominio: 'AR', categoria: 'Canto', duracaoMin: 10 }),
      ],
    });
    const p = proporSessao(i, pedido({ foco: ['LG.FON'] }));
    expect(p.escolhas.map((e) => e.atividade.id)).toEqual(['atv-fon-1']);
  });
});
