// Selo único de conferência profissional (#147, #138 D2, ADR 0037): calmo, sem alarme, uma vez por tela.
import type { Revisao } from '../domain/tipos';
import {
  precisaAvisoDeConferencia,
  TEXTO_NAO_SUBSTITUI,
  TEXTO_SELO_CONFERENCIA,
} from '../domain/revisao';
import { html, type HtmlSeguro } from './html';
import { icone } from './icones';

/**
 * Selo com o texto da conferência quando algum item da tela está pendente; vazio quando não há
 * pendência (a conferência acontecida faz o selo sumir sozinho). Com `fixo`, sem pendência ainda
 * mantém a frase "Não substitui o pediatra", que nunca sai (ex.: "Para os pais" da Caderneta).
 * `role="note"` faz o leitor de tela anunciá-lo como nota.
 */
export function seloDeConferencia(
  itens: readonly { revisao?: Revisao }[],
  opcoes: { fixo?: boolean } = {},
): HtmlSeguro {
  const texto = precisaAvisoDeConferencia(itens)
    ? TEXTO_SELO_CONFERENCIA
    : opcoes.fixo
      ? TEXTO_NAO_SUBSTITUI
      : null;
  if (texto === null) return html``;
  return html`<p class="selo-conferencia" role="note">${icone('heart')}<span>${texto}</span></p>`;
}
