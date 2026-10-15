// Texto curto do material impresso (O Grande Tesouro de Marina) para a ficha e o roteiro.
import type { MaterialImpresso } from './tipos';

/** Ex.: "Tesouro de Marina · Vol. 4, Unidade 5 (p. 42–47)". */
export function rotuloDoMaterial(m: MaterialImpresso): string {
  return `Tesouro de Marina · Vol. ${m.volume}, Unidade ${m.unidade} (p. ${m.paginas[0]}–${m.paginas[1]})`;
}
