// Tipos do domínio do Semear. O glossário (docs/GUIA_APRENDIZADO.md, §6) explica cada termo.

export const VERTENTES = [
  'Montessori',
  'Waldorf',
  'Clássico',
  'Religioso',
  'Charlotte Mason',
] as const;
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

/** Obra do catálogo de referências bibliográficas (content/referencias.json). Formato ABNT. */
export interface Referencia {
  id: string; // ex.: "montessori-mente-absorvente"
  /** já no formato ABNT: "MONTESSORI, Maria" ou "WISE, Jessie; BAUER, Susan Wise" */
  autores: string;
  titulo: string;
  ano: number;
  /** local e editora (ex.: "São Paulo: Kirion") ou o meio, quando não é livro */
  veiculo: string;
  /** só para fontes de acesso livre e oficiais; livros não levam link */
  link?: string;
}

/** O que a vertente da família acrescenta à orientação geral de um marco. */
export interface OrientacaoVertente {
  comoParticipar: string;
  /** ids do catálogo de referências */
  referencias: string[];
}

/** Texto pedagógico de um marco para os pais (§ orientação para os pais). */
export interface OrientacaoPais {
  porQueImporta: string;
  comoParticipar: string;
  sinaisDeAtencao: string;
  /** ids do catálogo de referências */
  referencias: string[];
  /** só as vertentes que têm algo a acrescentar; as demais veem apenas o texto geral */
  porVertente?: Partial<Record<Vertente, OrientacaoVertente>>;
}

export interface Marco {
  id: string; // ex.: "LG.FON.04"
  linha: string;
  ordem: number;
  titulo: string;
  descricaoPais: string;
  /** texto de apoio para os pais, lido sob demanda na jornada; ausente = ainda não escrito (aviso) */
  orientacaoPais?: OrientacaoPais;
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

/** Trecho de um volume d'O Grande Tesouro de Marina (ADR 0015) que acompanha a atividade. */
export interface MaterialImpresso {
  volume: number;
  unidade: number;
  /** primeira e última página do trecho no PDF do volume */
  paginas: [number, number];
}

export interface Atividade {
  id: string;
  titulo: string;
  /**
   * Marcos que a atividade trabalha (os "principais"). Vazio = atividade complementar (§3.0):
   * precisa de `dominio` e `categoria`, e não entra no posicionamento da criança.
   */
  marcos: string[];
  /** só nas complementares: domínio sem jornada (ex.: "AR") e categoria dele (ex.: "Escuta musical") */
  dominio?: string;
  categoria?: string;
  materialImpresso?: MaterialImpresso;
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
  autoria: {
    origem: 'ia' | 'humano';
    status: 'rascunho' | 'revisado' | 'publicado';
    revisadoEm?: string;
  };
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
  editora?: string;
  /** página onde comprar (só https); abre em outra aba, o app não faz chamada nenhuma */
  linkCompra?: string;
}

export type IdiomaAcervo = 'pt' | Idioma;

/** Obra de acesso gratuito (domínio público ou licença aberta) que o app só aponta; nada é baixado. */
export interface ItemAcervo {
  id: string;
  titulo: string;
  autor: string;
  idioma: IdiomaAcervo;
  idade: [number, number];
  fonte: string;
  licenca: string;
  url: string;
  /** "obra" abre o livro; "busca" abre a busca da fonte por este título */
  tipoLink: 'obra' | 'busca';
  sobre: string;
}

export interface Conteudo {
  dominios: Dominio[];
  marcos: Marco[];
  atividades: Atividade[];
  livros: Livro[];
  acervo: ItemAcervo[];
  referencias: Referencia[];
}

// ---------- Dados da família (ficam no aparelho) ----------

export interface Familia {
  educador: string;
  vertentePrincipal: Vertente;
  inspiracoes: Vertente[];
  idiomasEducador: Idioma[];
  criadaEm: string;
  /** família de exemplo (#39): apagada junto com o exemplo */
  exemplo?: true;
}

export interface Crianca {
  id: string;
  nome: string;
  /** AAAA-MM-DD */
  nascimento: string;
  /** null = automático (por idade e vertente) */
  letra: Letra | null;
  trilhas: Idioma[];
  /** criança do exemplo (#39): só registros marcados são apagados com o exemplo */
  exemplo?: true;
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
  exemplo?: true;
}
