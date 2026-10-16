// Orientação para os pais: escolhe o que mostrar de acordo com a vertente da família.
// Funções puras: recebem o índice do conteúdo e a família por parâmetro.
import type { IndiceConteudo } from './conteudo';
import type { Familia, OrientacaoPais, Referencia, Vertente } from './tipos';

/** Uma vertente da família com algo a acrescentar sobre o marco. */
export interface OrientacaoDaVertente {
  vertente: Vertente;
  /** true = vertente principal; false = inspiração */
  principal: boolean;
  comoParticipar: string;
}

export interface OrientacaoDaFamilia {
  geral: Pick<OrientacaoPais, 'porQueImporta' | 'comoParticipar' | 'sinaisDeAtencao'>;
  /** principal primeiro, depois as inspirações na ordem em que a família as escolheu */
  vertentes: OrientacaoDaVertente[];
  /** referências do texto geral e das vertentes exibidas, sem repetir */
  referencias: Referencia[];
}

/** 6.5 → "6,5": as idades aparecem no formato brasileiro. */
export function formatarIdade(idade: number): string {
  return String(idade).replace('.', ',');
}

/**
 * `{idade}` no texto de uma vertente vira a idade de introdução daquela vertente no marco. Assim o texto
 * não depende do aviso de ritmo estar na tela (ele só aparece para a vertente principal e antes da idade)
 * e a idade tem uma única fonte, `idadeIntroducao`.
 */
function preencherIdade(texto: string, idade: number | undefined): string {
  return idade === undefined ? texto : texto.replace(/\{idade\}/g, formatarIdade(idade));
}

/**
 * Referência em ABNT. O título vem entre `*` (itálico) para passar por `textoRico`.
 * Ex.: `MORAIS, Artur Gomes de. *Consciência fonológica*. Belo Horizonte: Autêntica, 2019.`
 */
export function formatarReferencia(r: Referencia): string {
  const base = `${r.autores}. *${r.titulo}*. ${r.veiculo}, ${r.ano}.`;
  return r.link ? `${base} Disponível em: ${r.link}.` : base;
}

/** null = o marco não existe ou ainda não tem orientação escrita (a tela não mostra nada). */
export function orientacaoParaFamilia(
  idx: IndiceConteudo,
  marcoId: string,
  familia: Familia,
): OrientacaoDaFamilia | null {
  const marco = idx.marco(marcoId);
  const orientacao = marco?.orientacaoPais;
  if (!marco || !orientacao) return null;

  const vertentesDaFamilia = [familia.vertentePrincipal, ...familia.inspiracoes];
  const vertentes: OrientacaoDaVertente[] = [];
  const idsDeReferencia = [...orientacao.referencias];
  for (const vertente of new Set(vertentesDaFamilia)) {
    const texto = orientacao.porVertente?.[vertente];
    if (!texto) continue;
    vertentes.push({
      vertente,
      principal: vertente === familia.vertentePrincipal,
      comoParticipar: preencherIdade(texto.comoParticipar, marco.idadeIntroducao[vertente]),
    });
    idsDeReferencia.push(...texto.referencias);
  }

  const referencias = [...new Set(idsDeReferencia)]
    .map((id) => idx.referencia(id))
    .filter((r): r is Referencia => r !== undefined);

  const { porQueImporta, comoParticipar, sinaisDeAtencao } = orientacao;
  return { geral: { porQueImporta, comoParticipar, sinaisDeAtencao }, vertentes, referencias };
}
