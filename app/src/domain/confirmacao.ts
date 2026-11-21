// Confirmação digitada das ações sem volta (tela de Ajustes): só "Apagar todos os dados" pede a palavra.

export const PALAVRA_APAGAR = 'APAGAR';

/** Aceita a palavra sem diferença de maiúscula e sem espaços nas pontas; qualquer outra coisa não vale. */
export function confirmacaoApagarTudo(digitado: string): boolean {
  return digitado.trim().toLocaleUpperCase('pt-BR') === PALAVRA_APAGAR;
}
