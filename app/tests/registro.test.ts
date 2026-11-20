import { describe, expect, it } from 'vitest';
import {
  acharSessaoPorCodigo,
  montarRegistro,
  observacoesDaSessao,
  observacoesRegistradas,
  pareceProntoPara,
  sessaoRegistrada,
  ultimasSessoes,
} from '../src/domain/registro';
import { diaFeito, type DiaPlano } from '../src/domain/semana';
import {
  ENGAJAMENTOS,
  type EstadoMarco,
  type EstadosCrianca,
  type EventoMarco,
  type Sessao,
} from '../src/domain/tipos';
import { AGORA, atividade, conteudoBase, indiceBase } from './fabricas';
import { criarIndice } from '../src/domain/conteudo';

// Registro de sessão (#11, §5.2 e §5.7): a ficha grava a OBSERVAÇÃO e nunca muda o estado do marco.

const sessao = (extra: Partial<Sessao> = {}): Sessao => ({
  id: 's1',
  codigo: 'S-1014-A1',
  criancaId: 'c1',
  criadaEm: '2026-10-14T10:00:00.000Z',
  duracaoMin: 40,
  foco: 'equilibrado',
  atividadeIds: ['atv-fon-1', 'atv-fon-2'],
  livroId: null,
  ...extra,
});

const idx = indiceBase();

describe('observacoesDaSessao: a mesma lista que a ficha impressa mostra', () => {
  it('traz os marcos principais e os de revisão, sem repetir, na ordem das atividades', () => {
    const obs = observacoesDaSessao(sessao(), idx);
    expect(obs.map((o) => [o.chave, o.revisao])).toEqual([
      ['LG.FON.01', false],
      ['LG.FON.02', false],
    ]);
  });

  it('um marco que é principal numa atividade e revisão em outra conta como principal', () => {
    // atv-fon-2 revisa LG.FON.01, que atv-fon-1 trabalha como principal.
    const obs = observacoesDaSessao(sessao({ atividadeIds: ['atv-fon-2', 'atv-fon-1'] }), idx);
    expect(obs.find((o) => o.marcoId === 'LG.FON.01')?.revisao).toBe(false);
  });

  it('marco só de revisão aparece marcado como revisão', () => {
    const obs = observacoesDaSessao(sessao({ atividadeIds: ['atv-fon-2'] }), idx);
    expect(obs.map((o) => [o.chave, o.revisao])).toEqual([
      ['LG.FON.02', false],
      ['LG.FON.01', true],
    ]);
  });

  it('em Línguas a chave é "id@idioma", como a jornada grava', () => {
    const i = criarIndice(
      conteudoBase({
        atividades: [
          atividade('atv-voc-en', ['LI.VOC.01'], { idioma: 'en' }),
          atividade('atv-voc-fr', ['LI.VOC.01'], { idioma: 'fr' }),
          atividade('atv-fon-1', ['LG.FON.01']),
        ],
      }),
    );
    const obs = observacoesDaSessao(
      sessao({ atividadeIds: ['atv-voc-en', 'atv-voc-fr', 'atv-fon-1'] }),
      i,
    );
    expect(obs.map((o) => o.chave)).toEqual(['LI.VOC.01@en', 'LI.VOC.01@fr', 'LG.FON.01']);
    expect(obs[0]?.idioma).toBe('en');
    expect(obs[2]?.idioma).toBeUndefined();
  });

  it('atividade complementar (sem marcos) não tem o que registrar', () => {
    const i = criarIndice(
      conteudoBase({
        atividades: [atividade('atv-arte', [], { dominio: 'AR', categoria: 'Canto' })],
      }),
    );
    expect(observacoesDaSessao(sessao({ atividadeIds: ['atv-arte'] }), i)).toEqual([]);
  });

  it('ignora atividade que não existe mais no conteúdo', () => {
    expect(observacoesDaSessao(sessao({ atividadeIds: ['sumiu'] }), idx)).toEqual([]);
  });
});

describe('montarRegistro', () => {
  const obs = observacoesDaSessao(sessao(), idx);
  const AGORA2 = '2026-10-15T09:00:00.000Z';
  const entrada = (extra = {}) => ({
    estados: { 'LG.FON.01': 'consolidado', 'LG.FON.02': 'em-desenvolvimento' },
    ...extra,
  });

  it('devolve a sessão registrada e um evento por marco escolhido, sempre com origem "sessao"', () => {
    const r = montarRegistro(
      sessao(),
      obs,
      entrada({ duracaoReal: 35, engajamento: 'bom', anotacoes: 'Adorou.' }),
      AGORA2,
    );
    expect(r.sessao).toMatchObject({
      id: 's1',
      registradaEm: AGORA2,
      duracaoReal: 35,
      engajamento: 'bom',
      anotacoes: 'Adorou.',
    });
    expect(r.eventos).toEqual([
      {
        criancaId: 'c1',
        chave: 'LG.FON.01',
        sessaoId: 's1',
        registro: { estado: 'consolidado', atualizadoEm: AGORA2, origem: 'sessao' },
      },
      {
        criancaId: 'c1',
        chave: 'LG.FON.02',
        sessaoId: 's1',
        registro: { estado: 'em-desenvolvimento', atualizadoEm: AGORA2, origem: 'sessao' },
      },
    ]);
    expect(r.eventos.every((e) => e.registro.origem === 'sessao')).toBe(true);
  });

  it('os campos opcionais ausentes ficam fora da sessão', () => {
    const { sessao: s } = montarRegistro(sessao(), obs, entrada(), AGORA2);
    expect(s.duracaoReal).toBeUndefined();
    expect(s.engajamento).toBeUndefined();
    expect(s.anotacoes).toBeUndefined();
    expect('duracaoReal' in s).toBe(false);
    // anotação só com espaços também é "ausente"
    expect(
      montarRegistro(sessao(), obs, entrada({ anotacoes: '   ' }), AGORA2).sessao.anotacoes,
    ).toBeUndefined();
  });

  it('marco sem escolha na ficha não gera evento', () => {
    const r = montarRegistro(sessao(), obs, { estados: { 'LG.FON.01': 'consolidado' } }, AGORA2);
    expect(r.eventos.map((e) => e.chave)).toEqual(['LG.FON.01']);
    const nada = montarRegistro(sessao(), obs, { estados: {} }, AGORA2);
    expect(nada.eventos).toEqual([]);
    expect(sessaoRegistrada(nada.sessao)).toBe(true); // registrar sem marcar nada é permitido
  });

  it('recusa estado fora de ESTADOS', () => {
    expect(() =>
      montarRegistro(sessao(), obs, { estados: { 'LG.FON.01': 'pronto' } }, AGORA2),
    ).toThrow(/estado/i);
    expect(() =>
      montarRegistro(sessao(), obs, { estados: { 'LG.FON.01': '__proto__' } }, AGORA2),
    ).toThrow();
  });

  it('recusa marco que não está na ficha da sessão', () => {
    expect(() =>
      montarRegistro(sessao(), obs, { estados: { 'MA.SEN.01': 'consolidado' } }, AGORA2),
    ).toThrow(/ficha/);
    expect(() =>
      montarRegistro(sessao(), obs, { estados: { __proto__x: 'consolidado' } }, AGORA2),
    ).toThrow();
  });

  it('recusa engajamento fora de ENGAJAMENTOS e aceita os quatro valores', () => {
    expect(() => montarRegistro(sessao(), obs, entrada({ engajamento: 'otimo' }), AGORA2)).toThrow(
      /engajamento/i,
    );
    for (const e of ENGAJAMENTOS) {
      expect(
        montarRegistro(sessao(), obs, entrada({ engajamento: e }), AGORA2).sessao.engajamento,
      ).toBe(e);
    }
  });

  it.each([0, -5, 1000, 241, 12.5, NaN, Infinity])('recusa a duração real %s', (d) => {
    expect(() => montarRegistro(sessao(), obs, entrada({ duracaoReal: d }), AGORA2)).toThrow(
      /dura/i,
    );
  });

  it.each([1, 35, 240])('aceita a duração real %s', (d) => {
    expect(
      montarRegistro(sessao(), obs, entrada({ duracaoReal: d }), AGORA2).sessao.duracaoReal,
    ).toBe(d);
  });

  it('recusa anotação com mais de 500 caracteres e aceita exatamente 500', () => {
    expect(() =>
      montarRegistro(sessao(), obs, entrada({ anotacoes: 'a'.repeat(501) }), AGORA2),
    ).toThrow(/500/);
    expect(
      montarRegistro(sessao(), obs, entrada({ anotacoes: 'a'.repeat(500) }), AGORA2).sessao
        .anotacoes,
    ).toHaveLength(500);
  });

  it('guarda a anotação como texto literal, sem interpretar', () => {
    const r = montarRegistro(sessao(), obs, entrada({ anotacoes: '<b>x</b>' }), AGORA2);
    expect(r.sessao.anotacoes).toBe('<b>x</b>');
  });

  it('não altera a sessão recebida e nunca devolve estados', () => {
    const original = sessao();
    const copia = structuredClone(original);
    const r = montarRegistro(original, obs, entrada({ duracaoReal: 20 }), AGORA2);
    expect(original).toEqual(copia);
    expect(r.sessao).not.toBe(original);
    expect(Object.keys(r)).toEqual(['sessao', 'eventos']); // nada de "estados": só o pai muda o estado (§5.2)
  });

  it('corrigir um registro troca os campos da sessão (os que sumiram saem)', () => {
    const primeira = montarRegistro(
      sessao(),
      obs,
      entrada({ duracaoReal: 30, anotacoes: 'antes' }),
      AGORA,
    ).sessao;
    const segunda = montarRegistro(primeira, obs, entrada({ engajamento: 'ok' }), AGORA2).sessao;
    expect(segunda.registradaEm).toBe(AGORA2);
    expect(segunda.engajamento).toBe('ok');
    expect(segunda.duracaoReal).toBeUndefined();
    expect(segunda.anotacoes).toBeUndefined();
  });
});

describe('observacoesRegistradas: o que já foi marcado na sessão (para corrigir)', () => {
  it('vale o último evento de cada marco naquela sessão', () => {
    const h: EventoMarco[] = [
      ev('LG.FON.01', 'em-desenvolvimento', 's1'),
      ev('LG.FON.01', 'consolidado', 's1'),
      ev('LG.FON.02', 'consolidado', 's2'),
      ev('LG.FON.02', 'consolidado', undefined, 'manual'),
    ];
    expect(observacoesRegistradas('s1', h)).toEqual({ 'LG.FON.01': 'consolidado' });
    expect(observacoesRegistradas('s2', h)).toEqual({ 'LG.FON.02': 'consolidado' });
    expect(observacoesRegistradas('s3', h)).toEqual({});
  });
});

function ev(
  chave: string,
  estado: EstadoMarco,
  sessaoId?: string,
  origem: EventoMarco['registro']['origem'] = 'sessao',
): EventoMarco {
  const e: EventoMarco = {
    criancaId: 'c1',
    chave,
    registro: { estado, atualizadoEm: AGORA, origem },
  };
  if (sessaoId) e.sessaoId = sessaoId;
  return e;
}

describe('pareceProntoPara: selo "parece pronto" (§5.2), só uma dica', () => {
  const K = 'LG.FON.04';
  const aberto: EstadosCrianca = {}; // marco sem estado = não observado
  const emDes: EstadosCrianca = {
    [K]: { estado: 'em-desenvolvimento', atualizadoEm: AGORA, origem: 'posicionamento' },
  };
  const consolidado: EstadosCrianca = {
    [K]: { estado: 'consolidado', atualizadoEm: AGORA, origem: 'manual' },
  };

  it('a mesma sessão duas vezes conta uma só', () => {
    const h = [ev(K, 'consolidado', 's1'), ev(K, 'consolidado', 's1')];
    expect(pareceProntoPara(K, emDes, h)).toBe(false);
  });

  it('duas sessões diferentes com Consolidado mostram o selo', () => {
    const h = [ev(K, 'consolidado', 's1'), ev(K, 'consolidado', 's2')];
    expect(pareceProntoPara(K, aberto, h)).toBe(true);
  });

  it('uma sessão só não basta', () => {
    expect(pareceProntoPara(K, emDes, [ev(K, 'consolidado', 's1')])).toBe(false);
  });

  it('marco Em desenvolvimento com 2 sessões Consolidado mostra', () => {
    const h = [ev(K, 'consolidado', 's1'), ev(K, 'consolidado', 's2')];
    expect(pareceProntoPara(K, emDes, h)).toBe(true);
  });

  it('marco já Consolidado não mostra', () => {
    const h = [ev(K, 'consolidado', 's1'), ev(K, 'consolidado', 's2')];
    expect(pareceProntoPara(K, consolidado, h)).toBe(false);
  });

  it('duas Consolidado e depois uma terceira Em desenvolvimento ainda mostram', () => {
    const h = [
      ev(K, 'consolidado', 's1'),
      ev(K, 'consolidado', 's2'),
      ev(K, 'em-desenvolvimento', 's3'),
    ];
    expect(pareceProntoPara(K, emDes, h)).toBe(true);
  });

  it('de cada sessão vale só o último registro do marco', () => {
    // s2 corrigiu de Consolidado para Em desenvolvimento: só s1 sobra com Consolidado
    const h = [
      ev(K, 'consolidado', 's1'),
      ev(K, 'consolidado', 's2'),
      ev(K, 'em-desenvolvimento', 's2'),
    ];
    expect(pareceProntoPara(K, emDes, h)).toBe(false);
    // e o contrário: corrigir para Consolidado passa a contar
    const h2 = [
      ev(K, 'consolidado', 's1'),
      ev(K, 'em-desenvolvimento', 's2'),
      ev(K, 'consolidado', 's2'),
    ];
    expect(pareceProntoPara(K, emDes, h2)).toBe(true);
  });

  it('sessões anteriores a um "Está aqui" não contam (pela ordem do histórico)', () => {
    const h = [
      ev(K, 'consolidado', 's1'),
      ev(K, 'consolidado', 's2'),
      ev(K, 'em-desenvolvimento', undefined, 'posicionamento'),
    ];
    expect(pareceProntoPara(K, emDes, h)).toBe(false);
    // depois do "Está aqui", duas sessões novas voltam a mostrar
    expect(
      pareceProntoPara(K, emDes, [...h, ev(K, 'consolidado', 's3'), ev(K, 'consolidado', 's4')]),
    ).toBe(true);
    // uma antes e uma depois: só a de depois conta
    expect(
      pareceProntoPara(K, emDes, [
        ev(K, 'consolidado', 's1'),
        ev(K, 'em-desenvolvimento', undefined, 'posicionamento'),
        ev(K, 'consolidado', 's2'),
      ]),
    ).toBe(false);
  });

  it('a ordem do histórico manda, não a data gravada', () => {
    const antigo = ev(K, 'em-desenvolvimento', undefined, 'posicionamento');
    antigo.registro.atualizadoEm = '2000-01-01T00:00:00.000Z'; // data "velha", mas gravado por último
    const s1 = ev(K, 'consolidado', 's1');
    s1.registro.atualizadoEm = '2030-01-01T00:00:00.000Z'; // data "futura", mas gravado antes
    const s2 = ev(K, 'consolidado', 's2');
    expect(pareceProntoPara(K, emDes, [s1, s2, antigo])).toBe(false);
    expect(pareceProntoPara(K, emDes, [antigo, s1, s2])).toBe(true);
  });

  it('eventos sem sessaoId nunca contam, nem os de outra origem', () => {
    const h = [
      ev(K, 'consolidado', undefined, 'sessao'),
      ev(K, 'consolidado', undefined, 'sessao'),
      ev(K, 'consolidado', undefined, 'manual'),
    ];
    expect(pareceProntoPara(K, emDes, h)).toBe(false);
  });

  it('só olha o marco pedido (e em Línguas, só o idioma pedido)', () => {
    const h = [
      ev('LI.VOC.01@en', 'consolidado', 's1'),
      ev('LI.VOC.01@fr', 'consolidado', 's2'),
      ev('LG.FON.01', 'consolidado', 's3'),
    ];
    expect(pareceProntoPara('LI.VOC.01@en', aberto, h)).toBe(false);
    expect(
      pareceProntoPara('LI.VOC.01@en', aberto, [...h, ev('LI.VOC.01@en', 'consolidado', 's5')]),
    ).toBe(true);
  });

  it('Não observado não conta como Consolidado e não zera o selo dos outros', () => {
    const h = [
      ev(K, 'consolidado', 's1'),
      ev(K, 'consolidado', 's2'),
      ev(K, 'nao-observado', 's3'),
    ];
    expect(pareceProntoPara(K, aberto, h)).toBe(true);
  });
});

describe('acharSessaoPorCodigo', () => {
  const lista = [
    sessao({ id: 'a', codigo: 'S-1014-A1' }),
    sessao({ id: 'b', codigo: 'S-1014-A10' }),
    sessao({ id: 'c', codigo: 'S-1015-T2' }),
  ];

  it('acha com maiúsculas, minúsculas, espaços e hífens a mais ou a menos', () => {
    for (const texto of [
      'S-1014-A1',
      's-1014-a1',
      's 1014 a1',
      '  S1014A1  ',
      's-1014 a1',
      'S - 1014 - A1',
    ]) {
      expect(acharSessaoPorCodigo(texto, lista)?.id).toBe('a');
    }
  });

  it('"A1" não casa com "A10", e "A10" acha a certa', () => {
    expect(acharSessaoPorCodigo('S-1014-A1', lista)?.id).toBe('a');
    expect(acharSessaoPorCodigo('S-1014-A10', lista)?.id).toBe('b');
    expect(acharSessaoPorCodigo('S-1014-A', lista)).toBeNull();
    expect(acharSessaoPorCodigo('S-1014', lista)).toBeNull();
  });

  it('devolve null para código inexistente, vazio ou só com espaços e hífens', () => {
    expect(acharSessaoPorCodigo('S-9999-Z9', lista)).toBeNull();
    expect(acharSessaoPorCodigo('', lista)).toBeNull();
    expect(acharSessaoPorCodigo('  - - ', lista)).toBeNull();
    expect(acharSessaoPorCodigo('S-1014-A1', [])).toBeNull();
  });

  it('texto hostil é só texto: nunca casa e nunca quebra', () => {
    for (const texto of ['<script>alert(1)</script>', '"; DROP', '__proto__', '.*', '\u0000']) {
      expect(acharSessaoPorCodigo(texto, lista)).toBeNull();
    }
  });
});

describe('ultimasSessoes e sessaoRegistrada', () => {
  it('ordena da mais recente para a mais antiga e limita', () => {
    const l = [1, 2, 3, 4, 5, 6, 7, 8].map((n) =>
      sessao({ id: `s${n}`, criadaEm: `2026-10-0${n}T10:00:00.000Z` }),
    );
    const r = ultimasSessoes(l, 6);
    expect(r.map((s) => s.id)).toEqual(['s8', 's7', 's6', 's5', 's4', 's3']);
    expect(l[0]?.id).toBe('s1'); // não mexe na lista original
    expect(ultimasSessoes([], 6)).toEqual([]);
  });

  it('só está registrada a sessão com registradaEm', () => {
    expect(sessaoRegistrada(sessao())).toBe(false);
    expect(sessaoRegistrada(sessao({ registradaEm: AGORA }))).toBe(true);
  });
});

describe('diaFeito (plano semanal): feito à mão OU sessão registrada', () => {
  const dia = (extra: Partial<DiaPlano> = {}): DiaPlano => ({
    dia: 'seg',
    data: '2026-10-12',
    duracaoMin: 30,
    atividadeIds: [],
    livroId: null,
    feito: false,
    ...extra,
  });

  it('feito à mão conta', () => {
    expect(diaFeito(dia({ feito: true }), [])).toBe(true);
  });
  it('sessão registrada conta, mesmo sem marcar à mão', () => {
    expect(diaFeito(dia({ sessaoId: 's1' }), [sessao({ registradaEm: AGORA })])).toBe(true);
  });
  it('sessão ainda não registrada, ou de outro dia, não conta', () => {
    expect(diaFeito(dia({ sessaoId: 's1' }), [sessao()])).toBe(false);
    expect(diaFeito(dia({ sessaoId: 's9' }), [sessao({ registradaEm: AGORA })])).toBe(false);
    expect(diaFeito(dia(), [sessao({ registradaEm: AGORA })])).toBe(false);
  });
});
