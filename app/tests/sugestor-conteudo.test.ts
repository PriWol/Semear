import { describe, expect, it } from 'vitest';
import { carregarConteudo } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import {
  chaveMarco,
  idPista,
  marcosDaPista,
  pistasDaCrianca,
  posicaoParaSugestao,
} from '../src/domain/jornada';
import {
  atividadesRecentes,
  candidatas,
  complementares,
  proporSessao,
  tetoDeDuracao,
  PISTA_COMPLEMENTAR,
  type Escolha,
} from '../src/domain/sessao';
import { VERTENTES, type EstadosCrianca, type Vertente } from '../src/domain/tipos';
import { AGORA, crianca, familia } from './fabricas';

// Teste de propriedades do sugestor com o CONTEÚDO REAL (estórias #145 e #146, ADR 0036). Não compara ids
// de atividades (mudam com o conteúdo): confere regras que valem para qualquer conteúdo.

const idx = criarIndice(carregarConteudo());
const IDADES = [2, 3, 4, 5, 6, 7, 8];
const DURACOES = [20, 30, 40, 60];
const FOLGA = 1.1;

/** Criança "posicionada": marcos de cada linha com idade típica até meio ano abaixo da idade, consolidados. */
function posicionadaPelaIdade(idade: number, vertente: Vertente): EstadosCrianca {
  const f = familia({ vertentePrincipal: vertente });
  const estados: EstadosCrianca = {};
  for (const pista of pistasDaCrianca(idx, f, crianca())) {
    for (const m of marcosDaPista(idx, pista)) {
      if (m.idadeTipica > idade - 0.5) break;
      estados[chaveMarco(m.id, pista.idioma)] = {
        estado: 'consolidado',
        atualizadoEm: AGORA,
        origem: 'manual',
      };
    }
  }
  return estados;
}

const dominioDe = (e: Escolha) =>
  e.pista === PISTA_COMPLEMENTAR ? 'complementar' : e.pista.slice(0, 2);

/** Todas as candidatas que o gerador poderia usar, com o domínio de cada uma. */
function candidatasPossiveis(idade: number, vertente: Vertente, estados: EstadosCrianca) {
  const f = familia({ vertentePrincipal: vertente });
  const recentes = atividadesRecentes([], 'c1', AGORA);
  const lista: { dominio: string; minutos: number; dentro: boolean }[] = [];
  const dentroDaFaixa = (c: Escolha) => c.foraDaFaixa !== true;
  for (const pista of pistasDaCrianca(idx, f, crianca())) {
    const pos = posicaoParaSugestao(idx, pista, estados, idade, vertente);
    for (const c of candidatas(idx, pista, pos.ativos, f, idade, recentes)) {
      lista.push({
        dominio: idPista(pista).slice(0, 2),
        minutos: c.atividade.duracaoMin,
        dentro: dentroDaFaixa(c),
      });
    }
  }
  for (const c of complementares(idx, f, idade, recentes)) {
    lista.push({
      dominio: 'complementar',
      minutos: c.atividade.duracaoMin,
      dentro: dentroDaFaixa(c),
    });
  }
  return lista;
}

/**
 * Existe um par de atividades de domínios diferentes, dentro do teto e da faixa de idade, que cabe junto em
 * 30 min? "Quando houver" conta só as que servem à idade: fora da faixa é último recurso (D4).
 */
function existeParDeDominios(idade: number, vertente: Vertente, estados: EstadosCrianca): boolean {
  const teto = tetoDeDuracao(idade, vertente);
  const dentro = candidatasPossiveis(idade, vertente, estados).filter(
    (c) => c.minutos <= teto && c.dentro,
  );
  return dentro.some((a) =>
    dentro.some((b) => a.dominio !== b.dominio && a.minutos + b.minutos <= 30 * FOLGA),
  );
}

const casos = IDADES.flatMap((idade) =>
  VERTENTES.flatMap((vertente) =>
    (['posicionada', 'sem sondagem'] as const).flatMap((modo) =>
      DURACOES.map((duracaoMin) => ({ idade, vertente, modo, duracaoMin })),
    ),
  ),
);

function proposta(c: (typeof casos)[number]) {
  const estados = c.modo === 'posicionada' ? posicionadaPelaIdade(c.idade, c.vertente) : {};
  return {
    estados,
    proposta: proporSessao(idx, {
      familia: familia({ vertentePrincipal: c.vertente }),
      crianca: crianca(),
      idade: c.idade,
      estados,
      historico: [],
      duracaoMin: c.duracaoMin,
      foco: 'equilibrado',
      agora: AGORA,
    }),
  };
}

describe('sugestor com o conteúdo real: propriedades (§5.6)', () => {
  it('cobre 7 idades x 5 vertentes x 2 modos x 4 durações', () => {
    expect(casos).toHaveLength(7 * VERTENTES.length * 2 * 4);
  });

  it('a soma das durações fica em até 110% do tempo escolhido', () => {
    const falhas = casos
      .map((c) => ({ c, minutos: proposta(c).proposta.minutos }))
      .filter((x) => x.minutos > x.c.duracaoMin * FOLGA);
    expect(falhas).toEqual([]);
  });

  it('em 30 minutos há pelo menos 2 atividades e 2 domínios quando o conteúdo permite', () => {
    const falhas = casos
      .filter((c) => c.duracaoMin === 30)
      .map((c) => ({ c, ...proposta(c) }))
      .filter((x) => existeParDeDominios(x.c.idade, x.c.vertente, x.estados))
      .filter((x) => {
        const dominios = new Set(x.proposta.escolhas.map(dominioDe));
        return x.proposta.escolhas.length < 2 || dominios.size < 2;
      })
      .map((x) => x.c);
    expect(falhas).toEqual([]);
  });

  it('atividade acima do teto da idade só entra se for a única da sessão', () => {
    const falhas = casos
      .map((c) => ({ c, escolhas: proposta(c).proposta.escolhas }))
      .filter(
        (x) =>
          x.escolhas.length > 1 &&
          x.escolhas.some((e) => e.atividade.duracaoMin > tetoDeDuracao(x.c.idade, x.c.vertente)),
      )
      .map((x) => x.c);
    expect(falhas).toEqual([]);
  });

  it('a mesma entrada dá sempre a mesma saída', () => {
    for (const c of casos) {
      expect(proposta(c).proposta).toEqual(proposta(c).proposta);
    }
  });

  it('nenhuma sessão de 30 minutos tem uma única atividade de mais de 20 minutos', () => {
    const falhas = casos
      .filter((c) => c.duracaoMin === 30)
      .map((c) => ({ c, escolhas: proposta(c).proposta.escolhas }))
      .filter((x) => x.escolhas.length === 1 && x.escolhas[0]!.atividade.duracaoMin > 20)
      .map((x) => x.c);
    expect(falhas).toEqual([]);
  });

  it('Charlotte Mason nunca recebe atividade acima de 20 min junto com outras', () => {
    const falhas = casos
      .filter((c) => c.vertente === 'Charlotte Mason')
      .map((c) => ({ c, escolhas: proposta(c).proposta.escolhas }))
      .filter((x) => x.escolhas.length > 1 && x.escolhas.some((e) => e.atividade.duracaoMin > 20));
    expect(falhas).toEqual([]);
  });

  // ---- Etapas 2 e 3 (#146): regra de idade (D4), ponto de partida pela idade (D6) ----

  const comAtividades = (lista: { idade: number; escolhas: Escolha[] }[]) =>
    lista.flatMap((x) => x.escolhas.map((e) => ({ idade: x.idade, e })));
  const todasEscolhas = () =>
    comAtividades(casos.map((c) => ({ idade: c.idade, escolhas: proposta(c).proposta.escolhas })));

  it('nenhuma atividade que começa 2 anos ou mais acima da criança', () => {
    const falhas = todasEscolhas().filter((x) => x.e.atividade.idade[0] - x.idade >= 2);
    expect(falhas.map((x) => `${x.idade}: ${x.e.atividade.id}`)).toEqual([]);
  });

  it('menores de 3 anos nunca recebem atividade cuja faixa começa aos 3 ou mais', () => {
    const falhas = todasEscolhas().filter((x) => x.idade < 3 && x.e.atividade.idade[0] >= 3);
    expect(falhas.map((x) => `${x.idade}: ${x.e.atividade.id}`)).toEqual([]);
  });

  it('fora da faixa de idade em no máximo 3% das sugestões (antes: 9%)', () => {
    const todas = todasEscolhas();
    const fora = todas.filter(
      (x) => x.idade < x.e.atividade.idade[0] || x.idade > x.e.atividade.idade[1],
    );
    expect(todas.length).toBeGreaterThan(0);
    expect(fora.length / todas.length).toBeLessThanOrEqual(0.03);
  });

  it('o que entra fora da faixa traz nota e nunca passa de 1 ano fora sem estar sozinho na linha', () => {
    const falhas = todasEscolhas().filter(
      (x) =>
        (x.idade < x.e.atividade.idade[0] || x.idade > x.e.atividade.idade[1]) &&
        (x.e.foraDaFaixa !== true || (x.e.notas ?? []).length === 0),
    );
    expect(falhas.map((x) => `${x.idade}: ${x.e.atividade.id}`)).toEqual([]);
  });

  it('sem sondagem a primeira atividade segue a idade: não é a mesma em todas as idades', () => {
    for (const vertente of VERTENTES) {
      const primeiras = IDADES.map((idade) => {
        const c = {
          idade,
          vertente,
          modo: 'sem sondagem',
          duracaoMin: 30,
        } as (typeof casos)[number];
        return { idade, a: proposta(c).proposta.escolhas[0]?.atividade };
      });
      const ids = new Set(primeiras.map((p) => p.a?.id));
      expect(ids.size, vertente).toBeGreaterThanOrEqual(4);
      for (const { idade, a } of primeiras) {
        expect(a, `${vertente} ${idade}`).toBeDefined();
        // perto da idade: dentro da faixa, ou no máximo 1 ano fora dela
        expect(idade).toBeGreaterThanOrEqual(a!.idade[0] - 1);
        expect(idade).toBeLessThanOrEqual(a!.idade[1] + 1);
        // o "Poema do passeio" (3 a 6 anos) era a primeira sugestão de todas as idades
        if (idade >= 7) expect(a!.id).not.toBe('atv-fon-poema-passeio');
      }
    }
  });

  it('sem sondagem a sessão avisa que usou a idade como ponto de partida', () => {
    const c = {
      idade: 5,
      vertente: 'Montessori',
      modo: 'sem sondagem',
      duracaoMin: 30,
    } as (typeof casos)[number];
    const p = proposta(c).proposta;
    expect(p.linhasPelaIdade.length).toBeGreaterThan(0);
    expect(p.avisos.join(' ')).toMatch(/ainda não foi posicionada/);
  });

  it('com a criança posicionada, não há aviso de ponto de partida pela idade', () => {
    const c = {
      idade: 5,
      vertente: 'Montessori',
      modo: 'posicionada',
      duracaoMin: 30,
    } as (typeof casos)[number];
    expect(proposta(c).proposta.linhasPelaIdade).toEqual([]);
  });

  it('numa linha só (foco escolhido), a fatia fora da faixa também cai bem abaixo da de antes', () => {
    // Medição antes da etapa 2: 7,4% (posicionada) e 54,8% (sem sondagem). O que sobra é falta de conteúdo
    // para 7 e 8 anos (lista de trabalho do Curador, ADR 0036).
    const f = familia();
    let total = 0;
    let fora = 0;
    for (const modo of ['posicionada', 'sem sondagem'] as const) {
      for (const idade of IDADES) {
        const estados =
          modo === 'posicionada' ? posicionadaPelaIdade(idade, f.vertentePrincipal) : {};
        for (const pista of pistasDaCrianca(idx, f, crianca())) {
          const p = proporSessao(idx, {
            familia: f,
            crianca: crianca(),
            idade,
            estados,
            historico: [],
            duracaoMin: 30,
            foco: [idPista(pista)],
            agora: AGORA,
          });
          for (const e of p.escolhas) {
            total++;
            if (idade < e.atividade.idade[0] || idade > e.atividade.idade[1]) fora++;
          }
        }
      }
    }
    expect(fora / total).toBeLessThanOrEqual(0.06);
  });

  it('com linhas empatadas, a linha que abre a sessão gira de um dia para o outro', () => {
    const f = familia();
    const abre = new Set<string>();
    for (let dia = 1; dia <= 28; dia++) {
      const agora = `2026-11-${String(dia).padStart(2, '0')}T12:00:00.000Z`;
      const p = proporSessao(idx, {
        familia: f,
        crianca: crianca(),
        idade: 5,
        estados: posicionadaPelaIdade(5, f.vertentePrincipal),
        historico: [],
        duracaoMin: 30,
        foco: 'equilibrado',
        agora,
      });
      const primeira = p.escolhas[0];
      if (primeira) abre.add(dominioDe(primeira));
    }
    expect(abre.size).toBeGreaterThan(1);
  });
});
