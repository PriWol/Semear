import { describe, expect, it } from 'vitest';
import {
  FRACAO_MAXIMA_ATIVIDADE,
  FRACAO_MAXIMA_ATIVIDADE_PEQUENOS,
  TETO_CHARLOTTE_MASON,
  proporSessao,
  tetoDeDuracao,
  type PedidoSessao,
} from '../src/domain/sessao';
import { AGORA, atividade, crianca, familia, indiceBase } from './fabricas';

// Gerador de sessão v2, etapa 1 (ADR 0036, §5.6): duração por atividade e mistura de áreas.

function pedido(extra: Partial<PedidoSessao> = {}): PedidoSessao {
  return {
    familia: familia(),
    crianca: crianca(),
    idade: 5,
    estados: {},
    historico: [],
    duracaoMin: 30,
    foco: 'equilibrado',
    agora: AGORA,
    ...extra,
  };
}

const ids = (p: ReturnType<typeof proporSessao>) => p.escolhas.map((e) => e.atividade.id);

describe('teto de duração por idade (D5)', () => {
  it('segue a tabela da dona do produto', () => {
    expect(tetoDeDuracao(2, 'Montessori')).toBe(10);
    expect(tetoDeDuracao(3, 'Montessori')).toBe(12);
    expect(tetoDeDuracao(4, 'Montessori')).toBe(15);
    expect(tetoDeDuracao(5, 'Montessori')).toBe(20);
    expect(tetoDeDuracao(6, 'Montessori')).toBe(20);
    expect(tetoDeDuracao(7, 'Montessori')).toBe(25);
    expect(tetoDeDuracao(8, 'Montessori')).toBe(25);
  });

  it('usa a idade inteira: 4,9 anos ainda é teto de 4 anos', () => {
    expect(tetoDeDuracao(4.9, 'Waldorf')).toBe(15);
  });

  it('Charlotte Mason nunca passa de 20 minutos, e os pequenos seguem o teto da idade', () => {
    expect(TETO_CHARLOTTE_MASON).toBe(20);
    expect(tetoDeDuracao(8, 'Charlotte Mason')).toBe(20);
    expect(tetoDeDuracao(3, 'Charlotte Mason')).toBe(12);
  });
});

describe('a primeira atividade também precisa caber', () => {
  const longa = atividade('a-longa', ['LG.FON.01'], { duracaoMin: 35, vertentes: ['Montessori'] });
  const curta = atividade('b-curta', ['LG.FON.01'], { duracaoMin: 10, vertentes: ['Waldorf'] });

  it('prefere a curta, mesmo com menos pontos, quando a mais pontuada estoura o tempo', () => {
    const idx = indiceBase({ atividades: [longa, curta] });
    const p = proporSessao(idx, pedido({ idade: 6, foco: ['LG.FON'], duracaoMin: 20 }));
    expect(ids(p)).toEqual(['b-curta']);
    expect(p.avisos).toEqual([]);
  });

  it('troca a atividade antes de avisar "mais do que os M min"', () => {
    const a25 = atividade('a25', ['LG.FON.01'], { duracaoMin: 25 });
    const a18 = atividade('b18', ['LG.FON.01'], { duracaoMin: 18, vertentes: ['Waldorf'] });
    const idx = indiceBase({ atividades: [a25, a18] });
    const p = proporSessao(idx, pedido({ idade: 7, foco: ['LG.FON'], duracaoMin: 20 }));
    expect(ids(p)).toEqual(['b18']);
    expect(p.avisos).toEqual([]);
  });

  it('se nada cabe, entra a mais curta e o aviso de tempo aparece', () => {
    const idx = indiceBase({
      atividades: [
        atividade('a', ['LG.FON.01'], { duracaoMin: 18 }),
        atividade('b', ['LG.FON.01'], { duracaoMin: 14, vertentes: ['Waldorf'] }),
      ],
    });
    const p = proporSessao(idx, pedido({ idade: 7, foco: ['LG.FON'], duracaoMin: 10 }));
    expect(ids(p)).toEqual(['b']);
    expect(p.avisos[0]).toMatch(/14 min, mais do que os 10 min/);
  });
});

describe('a próxima é a melhor que caiba no que resta', () => {
  it('pula a mais pontuada que estouraria e pega a seguinte', () => {
    const idx = indiceBase({
      atividades: [
        atividade('fon-a', ['LG.FON.01'], { duracaoMin: 12 }),
        atividade('fon-b', ['LG.FON.01'], { duracaoMin: 12, vertentes: ['Waldorf'] }),
        atividade('sen-grande', ['MA.SEN.01'], { duracaoMin: 20 }),
        atividade('sen-pequena', ['MA.SEN.01'], { duracaoMin: 8, vertentes: ['Waldorf'] }),
      ],
    });
    // 30 min, 6 anos: LG abre com fon-a (12). Em MA, sen-grande (20) estouraria 33; entra sen-pequena (8).
    const p = proporSessao(idx, pedido({ idade: 6, duracaoMin: 30 }));
    expect(ids(p)).toContain('fon-a');
    expect(ids(p)).toContain('sen-pequena');
    expect(ids(p)).not.toContain('sen-grande');
    expect(p.minutos).toBeLessThanOrEqual(33);
  });
});

describe('atividade acima do teto da idade', () => {
  it('nunca entra se há alternativa dentro do teto', () => {
    const idx = indiceBase({
      atividades: [
        atividade('longa', ['LG.FON.01'], { duracaoMin: 25 }),
        atividade('curta', ['LG.FON.01'], { duracaoMin: 12, vertentes: ['Waldorf'] }),
      ],
    });
    const p = proporSessao(idx, pedido({ idade: 4, foco: ['LG.FON'], duracaoMin: 60 }));
    expect(ids(p)).toEqual(['curta']);
  });

  it('entra sozinha, com aviso, se for a única possível', () => {
    const idx = indiceBase({
      atividades: [
        atividade('so-longa', ['LG.FON.01'], { duracaoMin: 25 }),
        atividade('outra-longa', ['LG.FON.01'], { duracaoMin: 30, vertentes: ['Waldorf'] }),
        atividade('sen-longa', ['MA.SEN.01'], { duracaoMin: 22 }),
      ],
    });
    const p = proporSessao(idx, pedido({ idade: 4, duracaoMin: 60 }));
    expect(p.escolhas).toHaveLength(1);
    expect(p.avisos.join(' ')).toMatch(/até 15 min/);
    expect(p.avisos.join(' ')).toMatch(/4 anos/);
  });

  it('Charlotte Mason: acima de 20 min só se for a única', () => {
    const idx = indiceBase({
      atividades: [
        atividade('cm-22', ['LG.FON.01'], { duracaoMin: 22, vertentes: ['Charlotte Mason'] }),
        atividade('cm-15', ['LG.FON.01'], { duracaoMin: 15, vertentes: ['Waldorf'] }),
      ],
    });
    const f = familia({ vertentePrincipal: 'Charlotte Mason' });
    const p = proporSessao(idx, pedido({ familia: f, idade: 8, foco: ['LG.FON'], duracaoMin: 60 }));
    expect(ids(p)).toEqual(['cm-15']);
  });
});

describe('mistura de áreas: rodízio por domínio', () => {
  const idx = indiceBase({
    atividades: [
      atividade('fon-1', ['LG.FON.01'], { duracaoMin: 8 }),
      atividade('fon-2', ['LG.FON.01'], { duracaoMin: 8 }),
      atividade('mem-1', ['LG.MEM.01'], { duracaoMin: 8, vertentes: ['Clássico'] }),
      atividade('sen-1', ['MA.SEN.01'], { duracaoMin: 8 }),
    ],
  });
  const classico = familia({ vertentePrincipal: 'Clássico' });

  it('na primeira rodada entra no máximo uma atividade por domínio', () => {
    const p = proporSessao(idx, pedido({ familia: classico, idade: 6, duracaoMin: 20 }));
    // 20 min = 2 atividades de 8 (24 cabe em 22? não: 16 cabe, 24 não). Duas atividades, de domínios diferentes.
    const dominios = p.escolhas.map((e) => e.pista.slice(0, 2));
    expect(p.escolhas).toHaveLength(2);
    expect(new Set(dominios).size).toBe(2);
  });

  it('numa sessão maior, a segunda rodada só começa depois de todos os domínios', () => {
    const p = proporSessao(idx, pedido({ familia: classico, idade: 6, duracaoMin: 30 }));
    const dominios = p.escolhas.slice(0, 2).map((e) => e.pista.slice(0, 2));
    expect(new Set(dominios).size).toBe(2);
    // Linguagem tem 2 linhas, mas a segunda atividade de LG só vem depois de MA ter a sua.
    expect(p.escolhas.map((e) => e.pista.slice(0, 2)).filter((d) => d === 'MA')).toHaveLength(1);
  });

  it('um domínio não consome o tempo antes de os outros terem a vez', () => {
    // 6 anos, 30 min: a parcela é 15. Em LG há 12 e 20 min (a de 20 passa da parcela); em MA há 8 min.
    const grande = indiceBase({
      atividades: [
        atividade('fon-12', ['LG.FON.01'], { duracaoMin: 12 }),
        atividade('mem-20', ['LG.MEM.01'], { duracaoMin: 20, vertentes: ['Clássico'] }),
        atividade('sen-8', ['MA.SEN.01'], { duracaoMin: 8, vertentes: ['Waldorf'] }),
      ],
    });
    const p = proporSessao(grande, pedido({ familia: classico, idade: 6, duracaoMin: 30 }));
    // Depois de 12 + 8, mem-20 não cabe; MA tem a vez antes de LG repetir.
    expect(new Set(p.escolhas.map((e) => e.pista.slice(0, 2))).size).toBe(2);
  });

  it('uma linha com foco escolhido continua podendo repetir domínio (só há um)', () => {
    const p = proporSessao(idx, pedido({ idade: 6, foco: ['LG.FON'], duracaoMin: 20 }));
    expect(ids(p)).toEqual(['fon-1', 'fon-2']);
  });
});

describe('empate de linhas gira de forma determinística', () => {
  const idx = indiceBase({
    atividades: [
      atividade('fon-1', ['LG.FON.01'], { duracaoMin: 12 }),
      atividade('sen-1', ['MA.SEN.01'], { duracaoMin: 12 }),
    ],
  });

  it('LG.FON não abre todas as sessões de uma criança sem histórico', () => {
    const primeiras = new Set<string>();
    for (let dia = 1; dia <= 28; dia++) {
      const agora = `2026-10-${String(dia).padStart(2, '0')}T12:00:00.000Z`;
      const p = proporSessao(idx, pedido({ agora, duracaoMin: 15 }));
      primeiras.add(p.escolhas[0]!.pista);
    }
    expect(primeiras).toEqual(new Set(['LG.FON', 'MA.SEN']));
  });

  it('o mesmo dia e a mesma entrada dão sempre a mesma sessão', () => {
    expect(proporSessao(idx, pedido())).toEqual(proporSessao(idx, pedido()));
    const outraHora = pedido({ agora: '2026-10-14T20:30:00.000Z' });
    expect(ids(proporSessao(idx, outraHora))).toEqual(ids(proporSessao(idx, pedido())));
  });

  it('o histórico continua mandando: a linha menos trabalhada abre a sessão', () => {
    const historico = [
      {
        id: 's',
        codigo: 'S-1',
        criancaId: 'c1',
        criadaEm: '2026-10-10T10:00:00.000Z',
        duracaoMin: 30,
        foco: 'equilibrado' as const,
        atividadeIds: ['fon-1'],
        livroId: null,
      },
    ];
    const p = proporSessao(idx, pedido({ historico, duracaoMin: 15 }));
    expect(p.escolhas[0]!.pista).toBe('MA.SEN');
  });
});

describe('blocos curtos para 2 e 3 anos', () => {
  it('prefere blocos curtos: 30 min viram vários blocos, não duas atividades grandes', () => {
    expect(FRACAO_MAXIMA_ATIVIDADE).toBe(0.5);
    expect(FRACAO_MAXIMA_ATIVIDADE_PEQUENOS).toBeLessThan(FRACAO_MAXIMA_ATIVIDADE);
    const idx = indiceBase({
      atividades: [
        atividade('fon-10', ['LG.FON.01'], { duracaoMin: 10, idade: [2, 4] }),
        atividade('fon-6', ['LG.FON.01'], { duracaoMin: 6, idade: [2, 4], vertentes: ['Waldorf'] }),
        atividade('mem-6', ['LG.MEM.01'], { duracaoMin: 6, idade: [2, 4] }),
        atividade('sen-10', ['MA.SEN.01'], { duracaoMin: 10, idade: [2, 4] }),
        atividade('sen-5', ['MA.SEN.01'], { duracaoMin: 5, idade: [2, 4], vertentes: ['Waldorf'] }),
      ],
    });
    const f = familia({ vertentePrincipal: 'Clássico' });
    const p = proporSessao(idx, pedido({ familia: f, idade: 2, duracaoMin: 30 }));
    expect(p.escolhas.length).toBeGreaterThanOrEqual(3);
    expect(Math.max(...p.escolhas.map((e) => e.atividade.duracaoMin))).toBeLessThanOrEqual(10);
    expect(p.minutos).toBeLessThanOrEqual(33);
  });
});

describe('metade do tempo numa única atividade, no máximo', () => {
  it('com alternativas mais curtas, uma atividade de 20 min não ocupa sozinha 30 min', () => {
    const idx = indiceBase({
      atividades: [
        atividade('fon-20', ['LG.FON.01'], { duracaoMin: 20 }),
        atividade('fon-12', ['LG.FON.01'], { duracaoMin: 12, vertentes: ['Waldorf'] }),
        atividade('sen-12', ['MA.SEN.01'], { duracaoMin: 12 }),
      ],
    });
    const p = proporSessao(idx, pedido({ idade: 6, duracaoMin: 30 }));
    expect(ids(p).sort()).toEqual(['fon-12', 'sen-12']);
  });
});
