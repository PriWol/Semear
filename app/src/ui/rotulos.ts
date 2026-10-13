import { dataBR } from '../domain/datas';
import type { EstadoMarco } from '../domain/tipos';

export const NOME_ESTADO: Record<EstadoMarco, string> = {
  'nao-observado': 'Não observado',
  'em-desenvolvimento': 'Em desenvolvimento',
  consolidado: 'Consolidado',
};

export const ICONE_ESTADO: Record<EstadoMarco, string> = {
  'nao-observado': '○',
  'em-desenvolvimento': '🌱',
  consolidado: '✅',
};

/** DD/MM/AAAA no fuso do aparelho. */
export const dataCurta = dataBR;

export function anos(idade: number): string {
  const n = Math.floor(idade);
  return `${n} ${n === 1 ? 'ano' : 'anos'}`;
}
