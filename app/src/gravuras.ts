// Gravuras botânicas de domínio público das telas (ADR 0035, estória #130/#24), no padrão de origem +
// SHA-256 + falha fechada dos ADR 0019 e 0021. Os arquivos são locais (public/gravuras/); o app nunca
// chama o archive.org: os endereços abaixo só documentam de onde vieram. scripts/gravuras.py baixa,
// confere o SHA-256 do original e gera os WebP; tests/gravuras.test.ts confere os arquivos contra
// este registro. Imagem que não está aqui não aparece (ui/gravura.ts).

export interface Gravura {
  id: string;
  titulo: string;
  autor: string;
  /** Ano da edição de onde veio a prancha (a obra de Redouté saiu em fascículos, 1802 a 1816). */
  ano: number;
  livro: string;
  /** Item e página (n<N>) no Internet Archive; a digitalização é da Missouri Botanical Garden (BHL). */
  item: string;
  pagina: number;
  urlPagina: string;
  urlOrigem: string;
  licenca: string;
  /** SHA-256 do JPEG ORIGINAL baixado do Internet Archive. */
  sha256Original: string;
  /** Arquivos em app/public/gravuras/, relativos a ela, e o SHA-256 de cada um. */
  arquivoClaro: string;
  arquivoEscuro: string;
  sha256Claro: string;
  sha256Escuro: string;
  /** Tamanho em pixels (evita o salto de layout ao carregar). */
  largura: number;
  altura: number;
  /** Descrição curta; na tela a imagem é ornamento e usa alt vazio (ver ui/gravura.ts). */
  alt: string;
  credito: string;
}

const BESLER = 'Basilius Besler (1561–1629)';
const REDOUTE = 'Pierre-Joseph Redouté (1759–1840)';
const HORTUS = 'Hortus Eystettensis';
const LILIACEES = 'Les Liliacées';
const ITEM_BESLER = 'mobot31753003651095';
const ITEM_REDOUTE = 'mobot31753002806732';
const LICENCA = 'Domínio público (autor falecido há mais de 70 anos; obras de 1640 e de 1802–1816)';

type Dados = Pick<
  Gravura,
  | 'id'
  | 'titulo'
  | 'autor'
  | 'ano'
  | 'livro'
  | 'item'
  | 'pagina'
  | 'sha256Original'
  | 'sha256Claro'
  | 'sha256Escuro'
  | 'largura'
  | 'altura'
  | 'alt'
> & { obra: string };

function gravuraDe({ obra, ...d }: Dados): Gravura {
  return {
    ...d,
    urlPagina: `https://archive.org/details/${d.item}/page/n${d.pagina}`,
    urlOrigem: `https://archive.org/download/${d.item}/page/n${d.pagina}.jpg`,
    licenca: LICENCA,
    arquivoClaro: `${d.id}.webp`,
    arquivoEscuro: `${d.id}-escuro.webp`,
    credito: `${d.autor}, ${obra}, ${d.titulo}. Digitalização: Missouri Botanical Garden (Biodiversity Heritage Library), no Internet Archive. ${LICENCA}.`,
  };
}

export const GRAVURAS: Readonly<Record<string, Gravura>> = {
  girassol: gravuraDe({
    id: 'girassol',
    titulo: 'Flos Solis prolifer (girassol)',
    autor: BESLER,
    obra: `${HORTUS} (1640)`,
    ano: 1640,
    livro: HORTUS,
    item: ITEM_BESLER,
    pagina: 222,
    sha256Original: 'f02a39e3267a85dd057e53e8168064ba4700ad5bfc90c7f0abf6e4f27f726952',
    sha256Claro: 'aba355ec9c4f778eb7581b50fc3425aac8ca95bd4ad1f6ca9d8d56ca701b672d',
    sha256Escuro: 'ac30367ee49e1ed74c7239eaf4d8cd5a50e6e14aca637d425f6ec36d8edb8bc9',
    largura: 532,
    altura: 618,
    alt: 'Gravura botânica: girassol',
  }),
  gladiolo: gravuraDe({
    id: 'gladiolo',
    titulo: 'Gladiolus gracilis (gladíolo)',
    autor: REDOUTE,
    obra: `${LILIACEES} (1802–1816)`,
    ano: 1802,
    livro: LILIACEES,
    item: ITEM_REDOUTE,
    pagina: 36,
    sha256Original: '934fe988dc0f65c8a60e88a55173642e74a25c1727d3db22d6427adf26d63e04',
    sha256Claro: '49236625c7b5cd2c7659f79d9d758bb310871557b52ced441ede3b8f161a2b9e',
    sha256Escuro: '4aa45fa0e5451cb7a9bf8fca9a819054d8bc4e3b728f9ee5205889c2c8db40ff',
    largura: 312,
    altura: 952,
    alt: 'Gravura botânica: gladíolo',
  }),
  tulipas: gravuraDe({
    id: 'tulipas',
    titulo: 'Tulipa (cinco tulipas com bulbo)',
    autor: BESLER,
    obra: `${HORTUS} (1640)`,
    ano: 1640,
    livro: HORTUS,
    item: ITEM_BESLER,
    pagina: 78,
    sha256Original: '9e42bd675444ec7beef20a9153f0df423d8c8d5919085b68a2336418c9f61580',
    sha256Claro: '1afb0de215790f8594c21e61d1a879400ef4ad513614a4122a802bd26ac6f51a',
    sha256Escuro: '546b72d4db374ce7ef87ce62da4318f026be6c46db9ac93f47aa681e290aea9a',
    largura: 632,
    altura: 712,
    alt: 'Gravura botânica: tulipas',
  }),
};

/** Texto da tela "Sobre" (Ajustes). */
export const CREDITO_GRAVURAS =
  'Gravuras: Besler, Hortus Eystettensis (1640); Redouté, Les Liliacées (1802–1816), via Biodiversity Heritage Library / Missouri Botanical Garden, no Internet Archive; domínio público.';

export function gravura(id: string): Gravura | undefined {
  return Object.hasOwn(GRAVURAS, id) ? GRAVURAS[id] : undefined;
}
