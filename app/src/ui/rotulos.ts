import { dataBR } from '../domain/datas';
import type { Engajamento, EstadoMarco } from '../domain/tipos';
import { confiavel, type HtmlSeguro } from './html';

/** Engajamento (#11): o texto guardado é "baixo/ok/bom/alto"; ícone e rótulo são só da tela. */
export const NOME_ENGAJAMENTO: Record<Engajamento, string> = {
  baixo: 'Pouco',
  ok: 'Normal',
  bom: 'Animado',
  alto: 'Empolgado',
};

const icone = (tracos: string) =>
  confiavel(
    `<svg class="icone-broto" viewBox="0 0 24 24" aria-hidden="true" focusable="false">${tracos}</svg>`,
  );

/** Ícones de traço (sem emoji, DESIGN.md): um broto que cresce com o engajamento. Constantes do próprio código. */
export const ICONE_ENGAJAMENTO: Record<Engajamento, HtmlSeguro> = {
  baixo: icone('<path d="M12 21v-5" /><path d="M12 16c0-2.5 1.5-4 4-4 0 2.5-1.5 4-4 4z" />'),
  ok: icone('<path d="M12 21v-9" /><path d="M12 12c0-4 3-6 7-6 0 4-3 6-7 6z" />'),
  bom: icone(
    '<path d="M12 21v-9" /><path d="M12 12c0-4 3-6 7-6 0 4-3 6-7 6z" /><path d="M12 15c0-3-2-5-6-5 0 3 2 5 6 5z" />',
  ),
  alto: icone(
    '<path d="M12 21V8" /><path d="M12 8c0-3 1-5 3-6 1 3 0 5-3 6z" /><path d="M12 13c0-4 3-6 7-6 0 4-3 6-7 6z" /><path d="M12 16c0-3-2-5-6-5 0 3 2 5 6 5z" />',
  ),
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
