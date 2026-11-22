// QA3-02: o conteúdo usa **negrito** em Cuidados e Materiais; a tela e o pacote precisam transformar,
// nunca mostrar os asteriscos crus. E o escape do HTML continua valendo (CLAUDE.md, Privacidade/segurança).
import { describe, expect, it } from 'vitest';
import { paginaAtividade } from '../src/pages/atividade';
import { gerarPacote, type EntradaPacote } from '../src/pacote/gerar';
import { gerarSemana } from '../src/pacote/semana';
import { carregarConteudo } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import { materiaisDaSemana, type PlanoSemana } from '../src/domain/semana';
import type { Atividade } from '../src/domain/tipos';
import type { Contexto } from '../src/ui/app';
import { AGORA, crianca, familia } from './fabricas';

const idx = criarIndice(carregarConteudo());
const publicadas = idx.conteudo.atividades.filter((a) => a.autoria.status === 'publicado');

function ctxCom(indice: typeof idx): Contexto {
  const repo = { familia: async () => null, criancas: async () => [] };
  return { repo, idx: indice } as unknown as Contexto;
}

async function htmlDaPagina(indice: typeof idx, id: string): Promise<string> {
  const pagina = await paginaAtividade(ctxCom(indice), { id });
  return pagina.conteudo.valor;
}

function entrada(atividades: Atividade[]): EntradaPacote {
  return {
    sessao: {
      id: 's1',
      codigo: 'S-1121-A1',
      criancaId: 'c1',
      criadaEm: AGORA,
      duracaoMin: 40,
      foco: 'equilibrado',
      atividadeIds: atividades.map((a) => a.id),
      livroId: null,
    },
    familia: familia(),
    crianca: crianca(),
    idade: 5.5,
    letra: 'script',
    atividades,
    livro: null,
    marco: (id) => idx.marco(id),
  };
}

describe('asteriscos crus em Cuidados e Materiais (QA3-02)', () => {
  it('há atividades publicadas para varrer', () => {
    expect(publicadas.length).toBeGreaterThan(30);
  });

  it('nenhuma página de atividade publicada mostra "**"', async () => {
    const com: string[] = [];
    for (const a of publicadas) {
      if ((await htmlDaPagina(idx, a.id)).includes('**')) com.push(a.id);
    }
    expect(com).toEqual([]);
  });

  it('nenhum pacote de sessão de atividade publicada mostra "**"', () => {
    const com = publicadas.filter((a) => gerarPacote(entrada([a])).includes('**')).map((a) => a.id);
    expect(com).toEqual([]);
  });

  it('o pacote da semana (materiais de todas as atividades) não mostra "**"', () => {
    const plano: PlanoSemana = {
      id: 'p',
      criancaId: 'c1',
      inicio: '2026-11-09',
      criadoEm: '2026-11-09T12:00:00.000Z',
      rotina: { dias: ['seg'], duracaoMin: 40 },
      dias: [
        {
          dia: 'seg',
          data: '2026-11-09',
          duracaoMin: 40,
          atividadeIds: publicadas.map((a) => a.id),
          livroId: null,
          feito: false,
        },
      ],
    };
    const doc = gerarSemana({
      crianca: crianca({ id: 'c1' }),
      plano,
      dias: [],
      materiais: materiaisDaSemana(idx, plano),
      modo: 'roteiros',
    });
    expect(doc).toContain('Materiais da semana');
    expect(doc).not.toContain('**');
  });

  it('o negrito vira <b>, mas HTML malicioso em cuidados e materiais continua escapado', async () => {
    const base = publicadas[0]!;
    const ruim: Atividade = {
      ...base,
      cuidados: '**nunca deixe sozinha** <img src=x onerror=alert(1)><script>x()</script>',
      materiais: [{ item: '**tesoura** <b onclick="x()">', deCasa: false }],
    };
    const indice = { ...idx, atividade: () => ruim } as typeof idx;
    const pagina = await htmlDaPagina(indice, ruim.id);
    const pacote = gerarPacote(entrada([ruim]));
    for (const doc of [pagina, pacote]) {
      expect(doc).toContain('<b>nunca deixe sozinha</b>');
      expect(doc).toContain('<b>tesoura</b>');
      expect(doc).toContain('&lt;img src=x onerror=alert(1)&gt;');
      expect(doc).not.toContain('<img src=x');
      expect(doc).not.toContain('<b onclick');
    }
    expect(pagina).not.toContain('<script>x()');
  });
});
