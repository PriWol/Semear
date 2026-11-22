// Pendências fixas do cadastro (D12): coisas que o app pede até serem resolvidas, sem sumir como um balão.
import type { Familia } from './tipos';

/**
 * Família sem nome do educador: acontece depois de "Apagar exemplo" mantendo uma criança real, quando o
 * nome fictício é zerado (ADR 0013, adendo). Nunca mostramos "Marina" no lugar.
 */
export function familiaSemNome(familia: Pick<Familia, 'educador'>): boolean {
  return familia.educador.trim() === '';
}
