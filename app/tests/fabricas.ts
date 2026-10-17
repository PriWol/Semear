// Dados de teste pequenos e independentes do conteúdo real: mudar app/content não quebra estes testes.
import type { Atividade, Conteudo, Crianca, Familia, Marco } from '../src/domain/tipos';
import { criarIndice } from '../src/domain/conteudo';

export function marco(id: string, ordem: number, extra: Partial<Marco> = {}): Marco {
  return {
    id,
    linha: id.split('.').slice(0, 2).join('.'),
    ordem,
    titulo: `Marco ${id}`,
    descricaoPais: '',
    evidencias: [],
    idadeTipica: 4 + ordem / 2,
    idadeIntroducao: {},
    preRequisitos: [],
    bncc: [],
    // Todo marco precisa de orientação para os pais; os testes usam uma mínima e válida.
    orientacaoPais: {
      porQueImporta: 'Porque sim.',
      comoParticipar: 'Brinquem juntos.',
      sinaisDeAtencao: 'Converse com a escola.',
      referencias: [],
    },
    ...extra,
  };
}

export function atividade(id: string, marcos: string[], extra: Partial<Atividade> = {}): Atividade {
  return {
    id,
    titulo: `Atividade ${id}`,
    marcos,
    vertentes: ['Montessori'],
    idade: [3, 8],
    duracaoMin: 20,
    objetivo: 'Objetivo',
    passos: [{ titulo: 'Passo', minutos: 5, texto: 'Texto' }],
    observar: { consolidado: ['c'], emDesenvolvimento: ['d'] },
    materiais: [{ item: 'Lápis', deCasa: false }],
    evidencias: [],
    folhas: [{ tipo: 'desenho', titulo: 'Desenhe' }],
    autoria: { origem: 'humano', status: 'publicado' },
    ...extra,
  };
}

export function conteudoBase(extra: Partial<Conteudo> = {}): Conteudo {
  return {
    dominios: [
      {
        id: 'LG',
        nome: 'Linguagem',
        icone: '🗣️',
        comJornada: true,
        linhas: [
          { id: 'LG.FON', nome: 'Fonológica', vertentes: null },
          { id: 'LG.MEM', nome: 'Memorização', vertentes: ['Clássico'] },
        ],
      },
      {
        id: 'MA',
        nome: 'Matemática',
        icone: '🔢',
        comJornada: true,
        linhas: [{ id: 'MA.SEN', nome: 'Senso numérico', vertentes: null }],
      },
      {
        id: 'LI',
        nome: 'Línguas',
        icone: '🌍',
        comJornada: true,
        maxTrilhasAtivas: 2,
        trilhas: [
          { id: 'en', nome: 'Inglês', idadeInicio: 3 },
          { id: 'fr', nome: 'Francês', idadeInicio: 3 },
          { id: 'la', nome: 'Latim', idadeInicio: 6, preRequisitos: ['LG.FON.01'] },
        ],
        linhas: [
          { id: 'LI.VOC', nome: 'Vocabulário', vertentes: null, idiomas: ['en', 'fr', 'la'] },
        ],
      },
      {
        id: 'AR',
        nome: 'Artes',
        icone: '🎨',
        comJornada: false,
        categorias: ['Escuta musical', 'Canto'],
      },
    ],
    marcos: [
      marco('LG.FON.01', 1),
      marco('LG.FON.02', 2),
      marco('LG.FON.03', 3, { preRequisitos: ['MA.SEN.01'], idadeIntroducao: { Waldorf: 7 } }),
      marco('LG.FON.04', 4, { preRequisitos: ['LG.FON.03'] }), // pré-requisito na mesma linha
      marco('LG.MEM.01', 1),
      marco('MA.SEN.01', 1),
      marco('MA.SEN.02', 2),
      marco('LI.VOC.01', 1),
      marco('LI.VOC.02', 2, { preRequisitos: ['LI.VOC.01'] }),
    ],
    atividades: [
      atividade('atv-fon-1', ['LG.FON.01']),
      atividade('atv-fon-1b', ['LG.FON.01'], { vertentes: ['Waldorf'] }),
      atividade('atv-fon-2', ['LG.FON.02'], { revisa: ['LG.FON.01'] }),
      atividade('atv-sen-1', ['MA.SEN.01'], { duracaoMin: 15 }),
    ],
    referencias: [],
    livros: [
      {
        id: 'livro-a',
        titulo: 'Livro A',
        autor: 'Autora',
        vertentes: ['Montessori'],
        marcos: ['LG.FON.01'],
        idade: [3, 8],
        uso: 'leitura-em-voz-alta',
        porQue: 'Porque sim',
      },
    ],
    acervo: [],
    ...extra,
  };
}

export const indiceBase = (extra: Partial<Conteudo> = {}) => criarIndice(conteudoBase(extra));

export function familia(extra: Partial<Familia> = {}): Familia {
  return {
    educador: 'Maria',
    vertentePrincipal: 'Montessori',
    inspiracoes: [],
    idiomasEducador: ['en'],
    criadaEm: '2026-10-01T10:00:00.000Z',
    ...extra,
  };
}

export function crianca(extra: Partial<Crianca> = {}): Crianca {
  return { id: 'c1', nome: 'Ana', nascimento: '2021-03-15', letra: null, trilhas: [], ...extra };
}

export const AGORA = '2026-10-14T12:00:00.000Z';
