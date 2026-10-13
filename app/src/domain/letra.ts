import type { Crianca, Familia, Letra } from './tipos';

/**
 * Letra padrão da criança (decisão 37 / §5.8 da especificação):
 * Montessori e Waldorf começam pela cursiva; nas demais, bastão → script → cursiva conforme a idade.
 */
export function letraPadrao(idade: number, familia: Pick<Familia, 'vertentePrincipal'>): Letra {
  if (familia.vertentePrincipal === 'Montessori' || familia.vertentePrincipal === 'Waldorf') {
    return 'cursiva';
  }
  if (idade < 5) return 'bastao';
  if (idade < 6) return 'script';
  return 'cursiva';
}

export function letraDaCrianca(
  crianca: Pick<Crianca, 'letra'>,
  idade: number,
  familia: Pick<Familia, 'vertentePrincipal'>,
): Letra {
  return crianca.letra ?? letraPadrao(idade, familia);
}

export const NOME_LETRA: Record<Letra, string> = {
  bastao: 'BASTÃO (caixa alta)',
  script: 'script minúsculo',
  cursiva: 'cursiva',
};
