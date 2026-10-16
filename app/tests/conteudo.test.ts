import { describe, expect, it } from 'vitest';
import { validarConteudo } from '../src/domain/conteudo';
import { carregarConteudo } from '../src/conteudo';
import { atividade, conteudoBase, marco } from './fabricas';

describe('conteúdo real (app/content)', () => {
  // Este teste é a "porta de qualidade" do conteúdo (ADR 0005): erros quebram o CI.
  it('não tem erros de validação', () => {
    const { erros } = validarConteudo(carregarConteudo());
    expect(erros).toEqual([]);
  });
  // O motor de jornada segue só a `ordem` dentro da linha (domain/jornada.ts), então uma ordem
  // que contradiz a idade típica trava a sugestão de sessões da criança em marcos mais difíceis.
  it('mantém a idade típica sem diminuir ao longo da ordem de cada linha', () => {
    const porLinha = new Map<string, { id: string; ordem: number; idadeTipica: number }[]>();
    for (const m of carregarConteudo().marcos) {
      porLinha.set(m.linha, [...(porLinha.get(m.linha) ?? []), m]);
    }
    const fora: string[] = [];
    for (const marcos of porLinha.values()) {
      const ordenados = [...marcos].sort((a, b) => a.ordem - b.ordem);
      ordenados.slice(1).forEach((m, i) => {
        if (m.idadeTipica < (ordenados[i]?.idadeTipica ?? 0)) fora.push(m.id);
      });
    }
    expect(fora).toEqual([]);
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
