import { describe, expect, it } from 'vitest';
import { validarConteudo } from '../src/domain/conteudo';
import { carregarConteudo } from '../src/conteudo';
import type { OrientacaoPais, Referencia } from '../src/domain/tipos';
import { atividade, conteudoBase, marco } from './fabricas';

describe('conteúdo real (app/content)', () => {
  // Este teste é a "porta de qualidade" do conteúdo (ADR 0005): erros quebram o CI.
  it('não tem erros de validação', () => {
    const { erros } = validarConteudo(carregarConteudo());
    expect(erros).toEqual([]);
  });
  it('nenhum texto aponta para o "aviso acima" (ele só aparece em certas condições)', () => {
    // O aviso de ritmo só aparece para a vertente principal e antes da idade de introdução.
    // O texto deve trazer a idade por {idade}, e não depender do aviso estar na tela.
    for (const m of carregarConteudo().marcos) {
      const textos = Object.values(m.orientacaoPais.porVertente ?? {}).map((t) => t.comoParticipar);
      for (const t of textos) expect(t, m.id).not.toMatch(/aviso acima/i);
    }
  });
  it('tem as atividades de exemplo publicadas', () => {
    const ids = carregarConteudo().atividades.map((a) => a.id);
    expect(ids).toEqual(expect.arrayContaining(['atv-caca-silabas', 'atv-feira-numeros']));
  });
});

describe('validarConteudo', () => {
  it('conteúdo de teste é válido', () => {
    expect(validarConteudo(conteudoBase()).erros).toEqual([]);
  });

  it('acusa ids repetidos', () => {
    const c = conteudoBase();
    c.marcos.push(marco('LG.FON.01', 9));
    expect(validarConteudo(c).erros).toContain('Marco com id repetido: LG.FON.01');
  });

  it('acusa ordem repetida na mesma linha', () => {
    const c = conteudoBase();
    c.marcos.push(marco('LG.FON.09', 1));
    expect(validarConteudo(c).erros.some((e) => e.includes('ordem 1 repetida'))).toBe(true);
  });

  it('acusa marco em linha inexistente', () => {
    const c = conteudoBase();
    c.marcos.push(marco('XX.YYY.01', 1));
    expect(validarConteudo(c).erros).toContain('Marco XX.YYY.01: linha XX.YYY não existe');
  });

  it('pré-requisito ainda não escrito é só aviso', () => {
    const c = conteudoBase();
    c.marcos.push(marco('LG.FON.05', 5, { preRequisitos: ['LG.LET.03'] }));
    const r = validarConteudo(c);
    expect(r.erros).toEqual([]);
    expect(r.avisos).toContain('Marco LG.FON.05: pré-requisito LG.LET.03 ainda não existe');
  });

  it('acusa atividade com marco inexistente', () => {
    const c = conteudoBase();
    c.atividades.push(atividade('atv-x', ['LG.FON.99']));
    expect(validarConteudo(c).erros).toContain('Atividade atv-x: marco LG.FON.99 não existe');
  });

  it('acusa folha de contar cuja resposta não está nas opções', () => {
    const c = conteudoBase();
    c.atividades.push(
      atividade('atv-y', ['MA.SEN.01'], {
        folhas: [
          {
            tipo: 'contar',
            titulo: 'Conte',
            itens: [{ emoji: '🍊', quantidade: 5, opcoes: [3, 4, 6] }],
          },
        ],
      }),
    );
    expect(validarConteudo(c).erros.some((e) => e.includes('não incluem a resposta 5'))).toBe(true);
  });

  it('acusa quadro de dez acima de 20', () => {
    const c = conteudoBase();
    c.atividades.push(
      atividade('atv-z', ['MA.SEN.01'], {
        folhas: [{ tipo: 'quadro-dez', titulo: 'Q', numeros: [25] }],
      }),
    );
    expect(validarConteudo(c).erros.some((e) => e.includes('de 0 a 20'))).toBe(true);
  });

  it('rascunhos geram aviso, não erro', () => {
    const c = conteudoBase();
    c.atividades.push(
      atividade('atv-r', ['MA.SEN.01'], { autoria: { origem: 'ia', status: 'rascunho' } }),
    );
    const r = validarConteudo(c);
    expect(r.erros).toEqual([]);
    expect(r.avisos.some((a) => a.includes('atv-r'))).toBe(true);
  });

  it('atividade sem marco só vale como complementar de domínio sem jornada, com categoria válida', () => {
    const ok = atividade('c-ok', [], { dominio: 'AR', categoria: 'Canto' });
    expect(validarConteudo(conteudoBase({ atividades: [ok] })).erros).toEqual([]);
    const casos = [
      atividade('c1', []),
      atividade('c2', [], { dominio: 'XX', categoria: 'Canto' }),
      atividade('c3', [], { dominio: 'LG', categoria: 'Canto' }),
      atividade('c4', [], { dominio: 'AR', categoria: 'Inexistente' }),
    ];
    for (const a of casos) {
      expect(validarConteudo(conteudoBase({ atividades: [a] })).erros, a.id).toHaveLength(1);
    }
  });

  it('acusa material impresso com páginas invertidas ou volume inválido', () => {
    const base = { dominio: 'AR', categoria: 'Canto' };
    const ruim = [
      { volume: 4, unidade: 1, paginas: [9, 6] as [number, number] },
      { volume: 0, unidade: 1, paginas: [1, 2] as [number, number] },
    ];
    const malformados = [
      { volume: 4, unidade: 1 },
      { volume: 4, unidade: 1, paginas: [1.5, 3] },
    ];
    for (const m of [...ruim, ...(malformados as unknown as (typeof ruim)[number][])]) {
      const a = atividade('m', [], { ...base, materialImpresso: m });
      expect(validarConteudo(conteudoBase({ atividades: [a] })).erros).toHaveLength(1);
    }
  });
});

describe('validarConteudo: orientação para os pais e referências', () => {
  const referencia = (id: string, extra: Partial<Referencia> = {}): Referencia => ({
    id,
    autores: 'AUTORA, Ana',
    titulo: 'Obra',
    ano: 2000,
    veiculo: 'São Paulo: Editora',
    ...extra,
  });
  const orientacao = (extra: Partial<OrientacaoPais> = {}): OrientacaoPais => ({
    porQueImporta: 'a',
    comoParticipar: 'b',
    sinaisDeAtencao: 'c',
    referencias: ['r1'],
    ...extra,
  });
  const comOrientacao = (o: OrientacaoPais, referencias = [referencia('r1')]) =>
    conteudoBase({
      marcos: [marco('LG.FON.01', 1, { orientacaoPais: o })],
      atividades: [], // as de conteudoBase citam marcos que este teste não declara
      referencias,
    });

  it('orientação completa e referência existente são válidas', () => {
    expect(validarConteudo(comOrientacao(orientacao())).erros).toEqual([]);
  });

  it('acusa marco sem orientação para os pais (obrigatória em todo marco)', () => {
    const c = conteudoBase({ atividades: [] });
    c.marcos = [marco('LG.FON.01', 1, { orientacaoPais: undefined })];
    expect(validarConteudo(c).erros).toContain(
      'Marco LG.FON.01: falta a orientação para os pais (obrigatória em todo marco)',
    );
  });

  it('acusa referência citada que não existe no catálogo', () => {
    const c = comOrientacao(orientacao({ referencias: ['nao-existe'] }));
    expect(validarConteudo(c).erros).toContain(
      'Marco LG.FON.01: referência "nao-existe" não existe no catálogo',
    );
  });

  it('acusa referência inexistente também dentro do texto de uma vertente', () => {
    const c = comOrientacao(
      orientacao({
        porVertente: { Waldorf: { comoParticipar: 'x', referencias: ['nao-existe'] } },
      }),
    );
    expect(validarConteudo(c).erros).toContain(
      'Marco LG.FON.01: referência "nao-existe" não existe no catálogo',
    );
  });

  it('acusa vertente desconhecida (dado de fora é validado)', () => {
    const o = orientacao({
      porVertente: { Esotérica: { comoParticipar: 'x', referencias: [] } },
    } as unknown as Partial<OrientacaoPais>);
    expect(validarConteudo(comOrientacao(o)).erros).toContain(
      'Marco LG.FON.01: vertente "Esotérica" desconhecida na orientação para os pais',
    );
  });

  it('acusa texto vazio na orientação', () => {
    const c = comOrientacao(orientacao({ comoParticipar: '  ' }));
    expect(validarConteudo(c).erros).toContain(
      'Marco LG.FON.01: orientação para os pais com "comoParticipar" vazio',
    );
  });

  it('acusa orientação sem a lista de referências (a tela quebraria)', () => {
    const o = orientacao();
    delete (o as Partial<OrientacaoPais>).referencias;
    expect(validarConteudo(comOrientacao(o)).erros).toContain(
      'Marco LG.FON.01: orientação para os pais com "referencias" que não é uma lista',
    );
  });

  it('não lança com vertente nula ou malformada: reporta erro', () => {
    const ruins = [
      { Waldorf: null },
      { Waldorf: { comoParticipar: 'x' } }, // sem a lista de referências
    ] as unknown as OrientacaoPais['porVertente'][];
    for (const porVertente of ruins) {
      const c = comOrientacao(orientacao({ porVertente }));
      expect(() => validarConteudo(c)).not.toThrow();
      expect(validarConteudo(c).erros, JSON.stringify(porVertente)).toHaveLength(1);
    }
  });

  it('recusa asterisco nos campos da referência (deformaria o itálico do ABNT)', () => {
    const r = referencia('r1', { titulo: 'Obra *especial*' });
    expect(validarConteudo(comOrientacao(orientacao(), [r])).erros).toContain(
      'Referência r1: autores, título e veículo não podem conter "*"',
    );
  });

  it('acusa {idade} num texto cuja vertente não tem idade de introdução no marco', () => {
    const c = comOrientacao(
      orientacao({
        porVertente: {
          Waldorf: { comoParticipar: 'Por volta dos {idade} anos.', referencias: [] },
        },
      }),
    );
    expect(validarConteudo(c).erros).toContain(
      'Marco LG.FON.01: texto da vertente Waldorf usa {idade}, mas o marco não tem idadeIntroducao dessa vertente',
    );
    c.marcos[0]!.idadeIntroducao = { Waldorf: 7 };
    expect(validarConteudo(c).erros).toEqual([]);
  });

  it('acusa id de referência repetido', () => {
    const c = comOrientacao(orientacao(), [referencia('r1'), referencia('r1')]);
    expect(validarConteudo(c).erros).toContain('Referência com id repetido: r1');
  });

  it('acusa referência com dados incompletos ou ano inválido', () => {
    const ruins = [
      referencia('r1', { autores: '' }),
      referencia('r1', { titulo: ' ' }),
      referencia('r1', { veiculo: '' }),
      referencia('r1', { ano: 20 }),
    ];
    for (const r of ruins) {
      expect(
        validarConteudo(comOrientacao(orientacao(), [r])).erros,
        JSON.stringify(r),
      ).toHaveLength(1);
    }
  });

  it('só aceita link https (o link vira href na tela)', () => {
    const ruins = ['javascript:alert(1)', 'http://exemplo.gov.br', 'exemplo.gov.br'];
    for (const link of ruins) {
      const c = comOrientacao(orientacao(), [referencia('r1', { link })]);
      expect(validarConteudo(c).erros, link).toHaveLength(1);
    }
    const ok = comOrientacao(orientacao(), [referencia('r1', { link: 'https://exemplo.gov.br' })]);
    expect(validarConteudo(ok).erros).toEqual([]);
  });
});
