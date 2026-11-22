// Tempo do aviso flutuante (QA2-12). Função pura: a tela só liga o relógio.

/** `sucesso` some sozinho; `alerta` (algo que a pessoa precisa ler) fica até ser fechado. */
export type NivelAviso = 'sucesso' | 'alerta';

export const SEM_PRAZO = null;

const MIN_MS = 6000;
const MAX_MS = 8000;
const MS_POR_LETRA = 50;
const LETRAS_INCLUIDAS_NO_MINIMO = 60;

/** 6 s para frase curta, até 8 s para frase longa. `null` = não some sozinho. */
export function duracaoDoAviso(texto: string, nivel: NivelAviso): number | null {
  if (nivel === 'alerta') return SEM_PRAZO;
  const extra = Math.max(0, texto.length - LETRAS_INCLUIDAS_NO_MINIMO) * MS_POR_LETRA;
  return Math.min(MAX_MS, MIN_MS + extra);
}
