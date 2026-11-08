// Faixa etária do produto (#71, decisão de 16/10/2026): de 2 a 8 anos, de creche ao 2º ano.
import { dataValida, idadeInteira } from './datas';

export const IDADE_MINIMA = 2;
export const IDADE_MAXIMA = 8;

export type Faixa = 'abaixo' | 'dentro' | 'acima' | 'invalida';

/**
 * Onde a criança está em relação à faixa do Semear. Só informa: o cadastro não bloqueia, para o
 * educador poder usar o app com um irmão mais novo ou mais velho, e o backup nunca recusa por idade.
 */
export function faixaEtaria(nascimento: string, hoje: Date): Faixa {
  if (!dataValida(nascimento)) return 'invalida';
  const idade = idadeInteira(nascimento, hoje);
  if (idade < IDADE_MINIMA) return 'abaixo';
  return idade > IDADE_MAXIMA ? 'acima' : 'dentro';
}
