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

export function dataCurta(iso: string): string {
  const [a, m, d] = iso.slice(0, 10).split('-');
  return `${d}/${m}/${a}`;
}

export function anos(idade: number): string {
  const n = Math.floor(idade);
  return `${n} ${n === 1 ? 'ano' : 'anos'}`;
}
