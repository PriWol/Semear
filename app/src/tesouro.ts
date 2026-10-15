// Catálogo d'O Grande Tesouro de Marina (ADR 0015). Os PDFs não ficam no Git: o deploy do site
// os baixa da Release e os coloca em ./tesouro/, na mesma origem do app.
import catalogoJson from '../content/tesouro.json';

import type { MaterialImpresso } from './domain/tipos';

export interface UnidadeTesouro {
  numero: number;
  titulo: string;
  paginas: [number, number];
}

export interface VolumeTesouro {
  numero: number;
  titulo: string;
  /** caminho relativo à raiz do app */
  arquivo: string;
  paginas: number;
  unidades: UnidadeTesouro[];
}

export const VOLUMES: VolumeTesouro[] = (catalogoJson as { volumes: VolumeTesouro[] }).volumes;

/** Endereço do trecho de uma atividade (primeira página da unidade), ou null se o volume não está no catálogo. */
export function enderecoDoMaterial(m: MaterialImpresso): string | null {
  const v = VOLUMES.find((x) => x.numero === m.volume);
  return v ? enderecoDoPdf(v, m.paginas[0]) : null;
}

/** Endereço do PDF, abrindo na página pedida. Só caminho relativo: nenhuma chamada externa. */
export function enderecoDoPdf(volume: VolumeTesouro, pagina = 1): string {
  return `${volume.arquivo}#page=${pagina}`;
}
