import { describe, expect, it } from 'vitest';
import {
  ANOS_AINDA_CEDO,
  linhaSemRegistro,
  marcoDePartidaPelaIdade,
  posicaoDaLinha,
  posicaoParaSugestao,
} from '../src/domain/jornada';
import { adequacaoDeIdade } from '../src/domain/idade-sugestao';
import {
  candidatas,
  complementares,
  opcoesDeTroca,
  proporSessao,
  proximaAlternativa,
  type Escolha,
  type PedidoSessao,
} from '../src/domain/sessao';
import type { Pista } from '../src/domain/jornada';
import type { EstadosCrianca } from '../src/domain/tipos';
import { AGORA, ESTADOS_NEUTROS, atividade, crianca, familia, indiceBase, marco } from './fabricas';

// Sugestor v2, etapas 2 e 3 (ADR 0036, adendo; estória #146): regra de idade (D4), ponto de partida
// provisório pela idade (D6) e ajuste pela vertente (F). Fixtures pequenas, independentes do conteúdo real.

function pedido(extra: Partial<PedidoSessao> = {}): PedidoSessao {
  return {
    familia: familia(),
    crianca: crianca(),
    idade: 5,
    estados: ESTADOS_NEUTROS,
    historico: [],
    duracaoMin: 30,
    foco: ['LG.FON'],
    agora: AGORA,
    ...extra,
  };
}

const ids = (p: ReturnType<typeof proporSessao>) => p.escolhas.map((e) => e.atividade.id);
const FON: Pick<Pista, 'linha' | 'idioma'> = { linha: indiceBase().linha('LG.FON')! };

describe('adequacaoDeIdade: idade como peso graduado (D4)', () => {
  const a = (idade: [number, number], extra = {}) =>
    atividade('x', ['LG.FON.01'], { idade, ...extra });

  it('dentro da faixa: +2 e um pequeno bônus de proximidade ao centro', () => {
    const centro = adequacaoDeIdade(a([4, 6]), 5);
    const borda = adequacaoDeIdade(a([4, 6]), 4);
    expect(centro.lado).toBe('dentro');
    expect(centro.pontos).toBeGreaterThan(borda.pontos);
    expect(borda.pontos).toBeGreaterThanOrEqual(2);
    expect(centro.pontos).toBeLessThanOrEqual(2.5);
    expect(centro.motivos).toContain('idade adequada');
  });

  it('criança mais velha que o máximo: -2 por ano até 2 anos, depois -6', () => {
    expect(adequacaoDeIdade(a([4, 6]), 7).pontos).toBe(-2);
    expect(adequacaoDeIdade(a([4, 6]), 8).pontos).toBe(-4);
    expect(adequacaoDeIdade(a([4, 6]), 9).pontos).toBe(-6);
    expect(adequacaoDeIdade(a([2, 3]), 8).pontos).toBe(-6);
    expect(adequacaoDeIdade(a([4, 6]), 9).excluida).toBe(false);
  });

  it('atividade que começa acima da criança: -3 por ano', () => {
    const r = adequacaoDeIdade(a([5, 7]), 4);
    expect(r.pontos).toBe(-3);
    expect(r.excluida).toBe(false);
    expect(r.lado).toBe('acima');
  });

  it('exclusão dura quando a atividade começa 2 anos ou mais acima', () => {
    expect(adequacaoDeIdade(a([6, 8]), 4).excluida).toBe(true);
    expect(adequacaoDeIdade(a([6, 8]), 4.5).excluida).toBe(false);
    expect(adequacaoDeIdade(a([7, 8]), 4).excluida).toBe(true);
  });

  it('menores de 3 anos nunca recebem atividade cuja faixa começa aos 3 ou mais', () => {
    expect(adequacaoDeIdade(a([3, 8]), 2).excluida).toBe(true);
    expect(adequacaoDeIdade(a([3, 8]), 2.9).excluida).toBe(true);
    expect(adequacaoDeIdade(a([3, 8]), 3).excluida).toBe(false);
    expect(adequacaoDeIdade(a([2, 8]), 2).excluida).toBe(false);
  });

  it('até 1 ano fora com `ajustes`: nota "versão mais simples/mais exigente"', () => {
    const ajustes = { dificil: 'Só cante junto.', facil: 'Invente a rima.' };
    const menor = adequacaoDeIdade(a([5, 7], { ajustes }), 4.5);
    expect(menor.notas).toEqual(['Versão mais simples: Só cante junto.']);
    const maior = adequacaoDeIdade(a([3, 5], { ajustes }), 6);
    expect(maior.notas).toEqual(['Versão mais exigente: Invente a rima.']);
  });

  it('sem `ajustes` correspondente, nunca diz "versão mais simples/mais exigente"', () => {
    const r = adequacaoDeIdade(a([5, 7], { ajustes: { facil: 'x' } }), 4.5);
    expect(r.notas.join(' ')).not.toMatch(/Versão mais/);
    expect(r.temAjuste).toBe(false);
  });

  it('mais de 1 ano fora: avisa que é pouco comum', () => {
    const r = adequacaoDeIdade(a([4, 6]), 8);
    expect(r.notas[0]).toMatch(/Pouco comum para esta idade/);
  });
});

describe('candidatas: exclusão, alternativa dentro da faixa e lacuna', () => {
  const ativos = ['LG.FON.01'];
  const dentro = atividade('a-dentro', ['LG.FON.01'], { idade: [5, 7] });
  const velha = atividade('b-velha', ['LG.FON.01'], { idade: [2, 3] });

  it('mais de 1 ano fora só entra se não houver alternativa dentro da faixa', () => {
    const f = familia();
    const dentro8 = atividade('a-dentro', ['LG.FON.01'], { idade: [6, 8] });
    const com = indiceBase({ atividades: [dentro8, velha] });
    const ids8 = candidatas(com, FON, ativos, f, 8, new Set()).map((e) => e.atividade.id);
    expect(ids8).toEqual(['a-dentro']);
    const sem = indiceBase({ atividades: [velha] });
    const so = candidatas(sem, FON, ativos, f, 8, new Set());
    expect(so.map((e) => e.atividade.id)).toEqual(['b-velha']);
    expect(so[0]!.notas?.[0]).toMatch(/Pouco comum/);
    expect(so[0]!.foraDaFaixa).toBe(true);
  });

  it('até 1 ano fora: só com `ajustes` e atrás da que serve à idade', () => {
    const comAjuste = atividade('c-ajuste', ['LG.FON.01'], {
      idade: [3, 5],
      ajustes: { facil: 'Peça que invente a rima.' },
    });
    const semAjuste = atividade('d-sem', ['LG.FON.01'], { idade: [3, 5] });
    const idx = indiceBase({ atividades: [dentro, comAjuste, semAjuste] });
    const r = candidatas(idx, FON, ativos, familia(), 6, new Set());
    expect(r.map((e) => e.atividade.id)).toEqual(['a-dentro', 'c-ajuste']);
    expect(r[1]!.notas).toEqual(['Versão mais exigente: Peça que invente a rima.']);
  });

  it('atividade que começa 2 anos ou mais acima da criança nunca é candidata', () => {
    const alta = atividade('e-alta', ['LG.FON.01'], { idade: [7, 8] });
    const idx = indiceBase({ atividades: [alta] });
    expect(candidatas(idx, FON, ativos, familia(), 5, new Set())).toEqual([]);
  });

  it('criança de 2 anos: atividade de 3 anos ou mais nunca entra, e a linha vira lacuna que avisa', () => {
    const tres = atividade('f-tres', ['LG.FON.01'], { idade: [3, 8], duracaoMin: 8 });
    const idx = indiceBase({ atividades: [tres] });
    const p = proporSessao(idx, pedido({ idade: 2 }));
    expect(p.escolhas).toEqual([]);
    expect(p.lacunas).toHaveLength(1);
    expect(p.lacunas[0]!.motivo).toBe('idade');
    expect(p.avisos.join(' ')).toMatch(/Sem atividade adequada para 2 anos/);
  });

  it('linha sem atividade nenhuma continua lacuna comum (sem o motivo de idade)', () => {
    const idx = indiceBase({ atividades: [] });
    const p = proporSessao(idx, pedido());
    expect(p.lacunas[0]!.motivo).toBeUndefined();
    expect(p.avisos).toEqual([]);
  });

  it('a primeira atividade da sessão respeita a idade: 8 anos não recebe a de 2 a 3 anos', () => {
    const idx = indiceBase({
      atividades: [
        atividade('a-bebe', ['LG.FON.01'], { idade: [2, 3], duracaoMin: 8 }),
        atividade('b-grande', ['LG.FON.01'], { idade: [7, 8], duracaoMin: 15 }),
      ],
    });
    const p = proporSessao(idx, pedido({ idade: 8 }));
    expect(ids(p)).toEqual(['b-grande']);
  });

  it('fora da faixa que entra mostra a nota na escolha da proposta', () => {
    const idx = indiceBase({
      atividades: [
        atividade('g-ajuste', ['LG.FON.01'], {
          idade: [6, 8],
          ajustes: { dificil: 'Faça junto, com ajuda.' },
        }),
      ],
    });
    const p = proporSessao(idx, pedido({ idade: 5.5 }));
    expect(ids(p)).toEqual(['g-ajuste']);
    expect(p.escolhas[0]!.notas).toEqual(['Versão mais simples: Faça junto, com ajuda.']);
  });
});

describe('complementares seguem a mesma regra de idade', () => {
  const comp = (id: string, idade: [number, number]) =>
    atividade(id, [], { dominio: 'AR', categoria: 'Canto', idade });
  const idx = indiceBase({
    atividades: [comp('c-pequena', [4, 5]), comp('c-grande', [7, 8]), comp('c-dois', [2, 3])],
  });

  it('exclui a que começa 2 anos ou mais acima e a de 3+ para menor de 3', () => {
    const para2 = complementares(idx, familia(), 2, new Set()).map((e) => e.atividade.id);
    expect(para2).toEqual(['c-dois']);
  });

  it('mais de 1 ano fora só entra sem alternativa dentro da faixa', () => {
    const para8 = complementares(idx, familia(), 8, new Set()).map((e) => e.atividade.id);
    expect(para8).toEqual(['c-grande']);
  });
});

describe('"Trocar" respeita o teto de duração (proximaAlternativa)', () => {
  const e = (id: string, min: number) =>
    ({
      atividade: atividade(id, ['LG.FON.01'], { duracaoMin: min }),
      pista: 'LG.FON',
      pontos: 0,
      motivos: [],
    }) as Escolha;
  const lista = [e('a', 10), e('b', 25), e('c', 12)];

  it('pula a que passa do teto', () => {
    expect(proximaAlternativa(lista, 'a', new Set(), 12)?.atividade.id).toBe('c');
  });
  it('atual dentro do teto e só longas nas outras: devolve null', () => {
    expect(proximaAlternativa([e('a', 10), e('b', 25)], 'a', new Set(), 12)).toBeNull();
  });
  it('pista só com atividades acima do teto: o teto deixa de valer e dá para trocar entre elas', () => {
    const longas = [e('a', 24), e('b', 30)];
    expect(proximaAlternativa(longas, 'a', new Set(), 20)?.atividade.id).toBe('b');
    expect(opcoesDeTroca(longas, 'a', new Set(), 20)).toHaveLength(2);
  });
  it('atual acima do teto mas com opção dentro dele: só as que cabem no teto', () => {
    const mistas = [e('a', 24), e('b', 30), e('c', 12)];
    expect(proximaAlternativa(mistas, 'a', new Set(), 20)?.atividade.id).toBe('c');
    expect(proximaAlternativa(mistas, 'c', new Set(), 20)).toBeNull(); // c cabe; as outras não
  });
  it('sem teto, o comportamento é o de sempre', () => {
    expect(proximaAlternativa(lista, 'a', new Set())?.atividade.id).toBe('b');
  });
});

describe('ponto de partida provisório pela idade (D6, §5.4)', () => {
  const m = (ordem: number, idadeTipica: number) =>
    marco(`LG.FON.0${ordem}`, ordem, { idadeTipica });
  const marcos = [m(1, 3), m(2, 4), m(3, 5), m(4, 6.5)];

  it('prefere o último marco com idade típica até 6 meses abaixo da idade', () => {
    expect(marcoDePartidaPelaIdade(marcos, 5.3)?.id).toBe('LG.FON.03');
    expect(marcoDePartidaPelaIdade(marcos, 4.5)?.id).toBe('LG.FON.02');
  });

  it('sem marco nessa janela, vale o mais próximo; no empate, o mais fácil', () => {
    expect(marcoDePartidaPelaIdade(marcos, 5.7)?.id).toBe('LG.FON.03');
    expect(marcoDePartidaPelaIdade(marcos, 2)?.id).toBe('LG.FON.01');
    expect(marcoDePartidaPelaIdade(marcos, 8)?.id).toBe('LG.FON.04');
    expect(marcoDePartidaPelaIdade([m(1, 3), m(2, 5)], 4)?.id).toBe('LG.FON.01');
  });

  it('linha sem marcos não tem ponto de partida', () => {
    expect(marcoDePartidaPelaIdade([], 5)).toBeNull();
  });

  const idx = indiceBase();
  const registro = (chave: string): EstadosCrianca => ({
    [chave]: { estado: 'nao-observado', atualizadoEm: AGORA, origem: 'manual' },
  });

  it('só vale para linha SEM registro (até um "não observado" marcado conta como registro)', () => {
    expect(linhaSemRegistro(idx, FON, {})).toBe(true);
    expect(linhaSemRegistro(idx, FON, registro('LG.FON.03'))).toBe(false);
  });

  it('a posição da sugestão parte da idade, é provisória e não grava nada', () => {
    const estados: EstadosCrianca = {};
    const pos = posicaoParaSugestao(idx, FON, estados, 6, 'Montessori');
    expect(pos.provisoria).toBe(true);
    expect(pos.ativos).toEqual(['LG.FON.04']);
    expect(estados).toEqual({}); // nada foi gravado nem alterado
    // a posição "de verdade" (jornada) continua no primeiro marco
    expect(posicaoDaLinha(idx, FON, estados, 6, 'Montessori').ativos).toEqual(['LG.FON.01']);
  });

  it('com registro na linha, é a posição de sempre e não é provisória', () => {
    const estados = registro('LG.FON.01');
    const pos = posicaoParaSugestao(idx, FON, estados, 6, 'Montessori');
    expect(pos.provisoria).toBeUndefined();
    expect(pos.ativos).toEqual(['LG.FON.01']);
  });

  it('a sugestão usa o marco da idade e avisa "ainda não posicionada: usamos a idade"', () => {
    const doIdx = indiceBase({
      atividades: [
        atividade('atv-inicio', ['LG.FON.01']),
        atividade('atv-da-idade', ['LG.FON.04']),
      ],
    });
    const p = proporSessao(doIdx, pedido({ idade: 6, estados: {} }));
    expect(ids(p)).toEqual(['atv-da-idade']);
    expect(p.linhasPelaIdade).toEqual(['Fonológica']);
    expect(p.avisos.join(' ')).toMatch(
      /ainda não foi posicionada em Fonológica: usamos a idade \(6 anos\)/,
    );
  });

  it('criança posicionada na linha não recebe o aviso', () => {
    const p = proporSessao(idx, pedido({ idade: 6 }));
    expect(p.linhasPelaIdade).toEqual([]);
    expect(p.avisos.join(' ')).not.toMatch(/ainda não foi posicionada/);
  });
});

describe('"ainda cedo para esta linha" na jornada (D6)', () => {
  const idx = indiceBase();

  it('marco ativo com idade típica mais de 1,5 ano acima da idade da criança', () => {
    expect(ANOS_AINDA_CEDO).toBe(1.5);
    // LG.FON.01 tem idade típica 4,5
    const cedo = posicaoDaLinha(idx, FON, {}, 2, 'Montessori');
    expect(cedo.marcos.find((s) => s.marco.id === 'LG.FON.01')!.aindaCedo).toBe(true);
    const limite = posicaoDaLinha(idx, FON, {}, 3, 'Montessori'); // 4,5 = 3 + 1,5: ainda não passa
    expect(limite.marcos[0]!.aindaCedo).toBe(false);
  });

  it('só o marco ativo recebe o aviso, e nada é bloqueado', () => {
    const pos = posicaoDaLinha(idx, FON, {}, 2, 'Montessori');
    expect(pos.marcos.filter((s) => s.aindaCedo)).toHaveLength(1);
    expect(pos.ativos).toEqual(['LG.FON.01']);
  });
});

describe('ajuste pela vertente (F, §5.3)', () => {
  const marcos = [
    marco('LG.FON.01', 1),
    marco('LG.FON.02', 2, { idadeIntroducao: { Waldorf: 7 } }),
    marco('MA.SEN.01', 1),
    marco('LG.MEM.01', 1),
    marco('LI.VOC.01', 1),
  ];
  const estados: EstadosCrianca = {
    ...ESTADOS_NEUTROS,
    'LG.FON.01': { estado: 'em-desenvolvimento', atualizadoEm: AGORA, origem: 'manual' },
  };
  const idx = indiceBase({
    marcos,
    atividades: [
      atividade('a-intro', ['LG.FON.02'], { vertentes: ['Waldorf'] }),
      atividade('b-livre', ['LG.FON.01'], { vertentes: ['Waldorf'] }),
      atividade('c-ambos', ['LG.FON.01', 'LG.FON.02'], { vertentes: ['Waldorf'] }),
    ],
  });
  const waldorf = familia({ vertentePrincipal: 'Waldorf' });
  const ativos = ['LG.FON.01', 'LG.FON.02'];

  it('marco antes da idade de introdução perde pontos e traz a nota', () => {
    const r = candidatas(idx, FON, ativos, waldorf, 5, new Set());
    const intro = r.find((e) => e.atividade.id === 'a-intro')!;
    const livre = r.find((e) => e.atividade.id === 'b-livre')!;
    expect(intro.pontos).toBeLessThan(livre.pontos);
    expect(intro.notas?.join(' ')).toMatch(
      /Na pedagogia Waldorf, este marco costuma ser introduzido por volta dos 7 anos/,
    );
    expect(livre.notas ?? []).toEqual([]);
  });

  it('atividade ligada também a um marco que a vertente já aceita não é penalizada', () => {
    const r = candidatas(idx, FON, ativos, waldorf, 5, new Set());
    expect(r.find((e) => e.atividade.id === 'c-ambos')!.notas ?? []).toEqual([]);
  });

  it('a partir da idade de introdução, não há penalidade nem nota', () => {
    const r = candidatas(idx, FON, ativos, waldorf, 7, new Set());
    const intro = r.find((e) => e.atividade.id === 'a-intro')!;
    expect(intro.notas ?? []).toEqual([]);
  });

  it('outras vertentes não são afetadas', () => {
    const r = candidatas(idx, FON, ativos, familia(), 5, new Set());
    expect(r.every((e) => (e.notas ?? []).length === 0)).toBe(true);
  });

  it('a proposta da sessão mostra o aviso na escolha', () => {
    const so = indiceBase({
      marcos,
      atividades: [atividade('a-intro', ['LG.FON.02'], { vertentes: ['Waldorf'] })],
    });
    const p = proporSessao(so, pedido({ familia: waldorf, estados }));
    expect(ids(p)).toEqual(['a-intro']);
    expect(p.escolhas[0]!.notas?.[0]).toMatch(/Waldorf/);
  });
});
