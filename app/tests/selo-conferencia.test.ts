// Selo único de conferência profissional (#147, #138 D2, ADR 0037): o estado é um dado do registro de
// revisão; a tela mostra UM selo calmo quando algum item está pendente e o aviso some quando conferida.
import { describe, expect, it } from 'vitest';
import {
  precisaAvisoDeConferencia,
  TEXTO_NAO_SUBSTITUI,
  TEXTO_SELO_CONFERENCIA,
  validarRevisao,
} from '../src/domain/revisao';
import { criarIndice, validarConteudo } from '../src/domain/conteudo';
import { seloDeConferencia } from '../src/ui/selo';
import { paginaAtividade } from '../src/pages/atividade';
import { paginaBiblioteca } from '../src/pages/biblioteca';
import { gerarPacote, type EntradaPacote } from '../src/pacote/gerar';
import type { Revisao } from '../src/domain/tipos';
import type { Contexto } from '../src/ui/app';
import { AGORA, atividade, conteudoBase, crianca, familia, marco } from './fabricas';

const base = { estado: 'aprovado', por: 'Priscila', em: '2026-11-08' } as const;
const pendente: Revisao = { ...base, conferenciaProfissional: { estado: 'pendente' } };
const conferida: Revisao = {
  ...base,
  conferenciaProfissional: { estado: 'conferida', por: 'Dra. Ana', em: '2026-12-01' },
};

function erros(revisao: unknown): string[] {
  const lista: string[] = [];
  validarRevisao(revisao, 'Marco X', lista);
  return lista;
}

describe('validação de conferenciaProfissional', () => {
  it('aceita pendente (sem por/em) e conferida com quem e quando', () => {
    expect(erros(pendente)).toEqual([]);
    expect(erros(conferida)).toEqual([]);
  });
  it('é opcional: sem o campo, nada muda', () => {
    expect(erros(base)).toEqual([]);
  });
  it('vale também para rascunho', () => {
    expect(
      erros({ estado: 'rascunho', conferenciaProfissional: { estado: 'talvez' } }),
    ).toHaveLength(1);
    expect(erros({ estado: 'rascunho', conferenciaProfissional: { estado: 'pendente' } })).toEqual(
      [],
    );
  });
  it('recusa estado fora do conjunto, valor que não é objeto e lista', () => {
    expect(erros({ ...base, conferenciaProfissional: { estado: 'talvez' } })).toHaveLength(1);
    expect(erros({ ...base, conferenciaProfissional: {} })).toHaveLength(1);
    expect(erros({ ...base, conferenciaProfissional: 'pendente' })).toHaveLength(1);
    expect(erros({ ...base, conferenciaProfissional: null })).toHaveLength(1);
    expect(erros({ ...base, conferenciaProfissional: [] })).toHaveLength(1);
  });
  it('conferida exige por e em (AAAA-MM-DD)', () => {
    expect(erros({ ...base, conferenciaProfissional: { estado: 'conferida' } })).toHaveLength(2);
    expect(
      erros({
        ...base,
        conferenciaProfissional: { estado: 'conferida', por: ' ', em: '2026-12-01' },
      }),
    ).toHaveLength(1);
    expect(
      erros({
        ...base,
        conferenciaProfissional: { estado: 'conferida', por: 'A', em: '01/12/2026' },
      }),
    ).toHaveLength(1);
  });
  it('a validação do conteúdo acusa o item com o campo inválido', () => {
    const c = conteudoBase({
      marcos: [
        marco('LG.FON.01', 1, {
          revisao: { ...base, conferenciaProfissional: { estado: 'x' } } as never,
        }),
      ],
    });
    expect(validarConteudo(c).erros.some((e) => e.includes('conferência'))).toBe(true);
  });
});

describe('precisaAvisoDeConferencia', () => {
  it('é verdadeiro se algum item tem conferência pendente', () => {
    expect(precisaAvisoDeConferencia([{}, { revisao: pendente }])).toBe(true);
  });
  it('é falso sem itens, sem o campo ou com tudo conferido', () => {
    expect(precisaAvisoDeConferencia([])).toBe(false);
    expect(precisaAvisoDeConferencia([{}, { revisao: base }])).toBe(false);
    expect(precisaAvisoDeConferencia([{ revisao: conferida }])).toBe(false);
  });
});

describe('seloDeConferencia (componente)', () => {
  it('com pendência: nota anunciável com o texto exato e ícone', () => {
    const h = seloDeConferencia([{ revisao: pendente }]).valor;
    expect(h).toContain('role="note"');
    expect(h).toContain(TEXTO_SELO_CONFERENCIA);
    expect(TEXTO_SELO_CONFERENCIA).toBe(
      'Orientação em conferência por profissional de saúde. Não substitui o pediatra.',
    );
    expect(h).toContain('<svg');
  });
  it('sem pendência: nada, a não ser no modo fixo, que mantém só "Não substitui o pediatra"', () => {
    expect(seloDeConferencia([{ revisao: conferida }]).valor).toBe('');
    const fixo = seloDeConferencia([{ revisao: conferida }], { fixo: true }).valor;
    expect(fixo).toContain(TEXTO_NAO_SUBSTITUI);
    expect(fixo).not.toContain('conferência');
  });
  it('com pendência, o modo fixo mostra o texto completo (uma vez)', () => {
    const h = seloDeConferencia([{ revisao: pendente }], { fixo: true }).valor;
    expect(h.split(TEXTO_SELO_CONFERENCIA)).toHaveLength(2);
  });
});

function ctxCom(c: ReturnType<typeof conteudoBase>): Contexto {
  const repo = { familia: async () => null, criancas: async () => [], sessoes: async () => [] };
  return { repo, idx: criarIndice(c) } as unknown as Contexto;
}

describe('tela da atividade', () => {
  const conteudo = (revisao?: Revisao, cuidados?: string) =>
    conteudoBase({
      marcos: [marco('LG.FON.01', 1)],
      atividades: [
        atividade('a1', ['LG.FON.01'], {
          ...(revisao ? { revisao } : {}),
          ...(cuidados ? { cuidados } : {}),
        }),
      ],
    });
  const pagina = async (c: ReturnType<typeof conteudoBase>) =>
    (await paginaAtividade(ctxCom(c), { id: 'a1' })).conteudo.valor;

  it('mostra o selo uma vez quando a atividade está pendente', async () => {
    const h = await pagina(conteudo(pendente));
    expect(h.split(TEXTO_SELO_CONFERENCIA)).toHaveLength(2);
    expect(h).toContain('role="note"');
  });
  it('não mostra o selo sem pendência nem depois de conferida', async () => {
    expect(await pagina(conteudo())).not.toContain('conferência por profissional');
    expect(await pagina(conteudo(conferida))).not.toContain('conferência por profissional');
  });
  it('os cuidados concretos continuam mesmo sem selo, e o texto segue escapado', async () => {
    const h = await pagina(conteudo(conferida, 'Fique junto. <img src=x onerror=alert(1)>'));
    expect(h).toContain('Cuidados:');
    expect(h).not.toContain('<img');
  });
});

describe('Biblioteca', () => {
  const c = (revisao?: Revisao) =>
    conteudoBase({
      marcos: [marco('LG.FON.01', 1)],
      atividades: [
        atividade('a1', ['LG.FON.01'], {
          materialImpresso: { volume: 1, unidade: 1, paginas: [1, 2] },
          ...(revisao ? { revisao } : {}),
        }),
      ],
    });
  it('mostra o selo quando um item do material impresso está pendente', async () => {
    const h = (await paginaBiblioteca(ctxCom(c(pendente)), {})).conteudo.valor;
    expect(h.split(TEXTO_SELO_CONFERENCIA)).toHaveLength(2);
  });
  it('não mostra sem pendência', async () => {
    const h = (await paginaBiblioteca(ctxCom(c(conferida)), {})).conteudo.valor;
    expect(h).not.toContain(TEXTO_SELO_CONFERENCIA);
  });
});

describe('pacote impresso', () => {
  const entrada = (ativs: ReturnType<typeof atividade>[]): EntradaPacote => ({
    sessao: {
      id: 's1',
      codigo: 'S-1121-A1',
      criancaId: 'c1',
      criadaEm: AGORA,
      duracaoMin: 40,
      foco: 'equilibrado',
      atividadeIds: ativs.map((a) => a.id),
      livroId: null,
    },
    familia: familia(),
    crianca: crianca(),
    idade: 5,
    letra: 'script',
    atividades: ativs,
    livro: null,
    marco: (id) => marco(id, 1),
  });
  const quantas = (h: string) => h.split(TEXTO_SELO_CONFERENCIA).length - 1;

  it('mostra o aviso uma vez no roteiro, mesmo com duas atividades pendentes', () => {
    const duas = [
      atividade('a1', ['LG.FON.01'], { revisao: pendente }),
      atividade('a2', ['LG.FON.01'], { revisao: pendente }),
    ];
    expect(quantas(gerarPacote(entrada(duas)))).toBe(1);
  });
  it('não mostra sem pendência', () => {
    const uma = [atividade('a1', ['LG.FON.01'], { revisao: conferida })];
    expect(quantas(gerarPacote(entrada(uma)))).toBe(0);
  });
});
