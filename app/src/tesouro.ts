// Catálogo d'O Grande Tesouro de Marina (ADR 0015). Os PDFs não ficam no Git: o deploy do site
// os baixa da Release e os coloca em ./tesouro/, na mesma origem do app.
import catalogoJson from '../content/tesouro.json';

import type { MaterialImpresso } from './domain/tipos';

export interface UnidadeTesouro {
  numero: number;
  titulo: string;
  paginas: [number, number];
  /** só no caderno de atividades: o volume da coleção que a unidade acompanha (1 a 8) */
  volume?: number;
}

export interface VolumeTesouro {
  numero: number;
  titulo: string;
  /** caminho relativo à raiz do app */
  arquivo: string;
  paginas: number;
  unidades: UnidadeTesouro[];
}

/** Caderno para 2 anos: material à parte, não é volume da coleção (ADR 0015, adendo). */
export interface CadernoTesouro {
  id: string;
  titulo: string;
  subtitulo: string;
  /** aviso de saúde mostrado no cartão (orientações ainda sem conferência profissional) */
  aviso: string;
  arquivo: string;
  paginas: number;
  unidades: UnidadeTesouro[];
}

const catalogo = catalogoJson as { volumes: VolumeTesouro[]; cadernos: CadernoTesouro[] };
export const VOLUMES: VolumeTesouro[] = catalogo.volumes;
export const CADERNOS: CadernoTesouro[] = catalogo.cadernos;

/** Endereço do trecho de uma atividade (primeira página da unidade), ou null se o volume não está no catálogo. */
export function enderecoDoMaterial(m: MaterialImpresso): string | null {
  const v = VOLUMES.find((x) => x.numero === m.volume);
  return v ? enderecoDoPdf(v, m.paginas[0]) : null;
}

/** Endereço do PDF, abrindo na página pedida. Só caminho relativo: nenhuma chamada externa. */
export function enderecoDoPdf(volume: { arquivo: string }, pagina = 1): string {
  return `${volume.arquivo}#page=${pagina}`;
}
