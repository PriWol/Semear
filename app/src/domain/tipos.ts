// Tipos do domínio do Semear. Ver docs/GLOSSARIO.md para o significado de cada termo.

export const VERTENTES = ['Montessori', 'Waldorf', 'Clássico', 'Religioso', 'Charlotte Mason'] as const;
export type Vertente = (typeof VERTENTES)[number];

export const IDIOMAS = { en: 'Inglês', fr: 'Francês', la: 'Latim' } as const;
export type Idioma = keyof typeof IDIOMAS;

export const ESTADOS = ['nao-observado', 'em-desenvolvimento', 'consolidado'] as const;
export type EstadoMarco = (typeof ESTADOS)[number];

export const LETRAS = ['bastao', 'script', 'cursiva'] as const;
export type Letra = (typeof LETRAS)[number];

// ---------- Conteúdo (curado pela equipe, em app/content) ----------

export interface Linha {
  id: string; // ex.: "LG.FON"
  nome: string;
  /** null = comum a todas as vertentes; lista = linha extra só dessas vertentes */
  vertentes: Vertente[] | null;
  /** só no domínio de Línguas */
  idiomas?: Idioma[];
  idadeInicio?: number;
}

export interface Trilha {
  id: Idioma;
  nome: string;
  idadeInicio: number;
  preRequisitos?: string[];
}

export interface Dominio {
  id: string; // ex.: "LG"
  nome: string;
  icone: string;
  /** false = só atividades, sem posicionamento (decisão 20) */
  comJornada: boolean;
  linhas?: Linha[];
  trilhas?: Trilha[];
  maxTrilhasAtivas?: number;
  categorias?: string[];
}

export interface Marco {
  id: string; // ex.: "LG.FON.04"
  linha: string;
  ordem: number;
  titulo: string;
  descricaoPais: string;
  evidencias: string[];
  idadeTipica: number;
  idadeIntroducao: Partial<Record<Vertente, number>>;
  preRequisitos: string[];
  vertentes?: Vertente[] | null;
  idiomas?: Idioma[] | null;
  bncc: string[];
}

export interface ItemFigura {
  emoji: string;
  texto: string;
}

export type Folha =
  | { tipo: 'ligar'; titulo: string; esquerda: ItemFigura[]; direita: ItemFigura[] }
  | {
      tipo: 'marcar';
      titulo: string;
      grupos: { modelo: ItemFigura; itens: ItemFigura[] }[];
    }
  | {
      tipo: 'cartas';
      titulo: string;
      cartas: ({ emoji: string; texto: string } | { numero: number } | { quadroDez: number })[];
    }
  | { tipo: 'desenho'; titulo: string; legenda?: string }
  | {
      tipo: 'contar';
      titulo: string;
      itens: { emoji: string; quantidade: number; opcoes: number[] }[];
    }
  | { tipo: 'quadro-dez'; titulo: string; dica?: string; numeros: number[] }
  | {
      tipo: 'comparar';
      titulo: string;
      dica?: string;
      pares: {
        a: { emoji: string; quantidade: number };
        b: { emoji: string; quantidade: number };
      }[];
    };

export type TipoFolha = Folha['tipo'];

export interface Passo {
  titulo: string;
  minutos: number;
  texto: string;
  fala?: string;
}

export interface Atividade {
  id: string;
  titulo: string;
  /** marcos que a atividade trabalha (os "principais") */
  marcos: string[];
  /** marcos revisados (aparecem na ficha como "revisão") */
  revisa?: string[];
  vertentes: Vertente[];
  idade: [number, number];
  duracaoMin: number;
  objetivo: string;
  passos: Passo[];
  observar: { consolidado: string[]; emDesenvolvimento: string[] };
  ajustes?: { dificil?: string; facil?: string };
  materiais: { item: string; deCasa: boolean }[];
  toqueVertente?: Partial<Record<Vertente, string>>;
  evidencias: { texto: string; resposta: string }[];
  perguntaFicha?: string;
  /** só no domínio de Línguas: idioma da atividade */
  idioma?: Idioma;
  folhas: Folha[];
  autoria: { origem: 'ia' | 'humano'; status: 'rascunho' | 'revisado' | 'publicado'; revisadoEm?: string };
}

export interface Livro {
  id: string;
  titulo: string;
  autor: string;
  vertentes: Vertente[];
  marcos: string[];
  idade: [number, number];
  uso: 'leitura-em-voz-alta' | 'leitura-pela-crianca' | 'apoio-ao-educador';
  porQue: string;
}

export interface Conteudo {
  dominios: Dominio[];
  marcos: Marco[];
  atividades: Atividade[];
  livros: Livro[];
}

// ---------- Dados da família (ficam no aparelho) ----------

export interface Familia {
  educador: string;
  vertentePrincipal: Vertente;
  inspiracoes: Vertente[];
  idiomasEducador: Idioma[];
  criadaEm: string;
}

export interface Crianca {
  id: string;
  nome: string;
  /** AAAA-MM-DD */
  nascimento: string;
  /** null = automático (por idade e vertente) */
  letra: Letra | null;
  trilhas: Idioma[];
}

export interface RegistroMarco {
  estado: EstadoMarco;
  atualizadoEm: string;
  origem: 'manual' | 'posicionamento' | 'sessao' | 'sondagem';
}

/** Estados dos marcos de uma criança. Chave = id do marco, ou "id@idioma" no domínio de Línguas. */
export type EstadosCrianca = Record<string, RegistroMarco>;

export interface Sessao {
  id: string;
  codigo: string;
  criancaId: string;
  criadaEm: string;
  duracaoMin: number;
  foco: string[] | 'equilibrado';
  atividadeIds: string[];
  livroId: string | null;
}
