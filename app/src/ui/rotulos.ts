import { dataBR } from '../domain/datas';
import type { Engajamento, EstadoMarco } from '../domain/tipos';

/** Engajamento (#11): o texto guardado é "baixo/ok/bom/alto"; emoji e rótulo são só da tela. */
export const NOME_ENGAJAMENTO: Record<Engajamento, string> = {
  baixo: 'Pouco',
  ok: 'Normal',
  bom: 'Animado',
  alto: 'Empolgado',
};

export const ICONE_ENGAJAMENTO: Record<Engajamento, string> = {
  baixo: '😴',
  ok: '🙂',
  bom: '😄',
  alto: '🤩',
};

/** "Feita ✓": pílula igual no início, na busca e no plano semanal. */
export const ROTULO_FEITA = 'Feita ✓';

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
