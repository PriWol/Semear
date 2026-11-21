// Texto curto do material impresso (O Grande Tesouro de Marina) para a ficha e o roteiro.
import type { MaterialImpresso } from './tipos';

/** O que o rótulo precisa saber de um caderno; o catálogo chega por parâmetro (domain/ é puro). */
export interface IdentidadeCaderno {
  id: string;
  titulo: string;
  subtitulo: string;
}

/**
 * Ex.: "Tesouro de Marina · Vol. 4, Unidade 5 (p. 42–47)" ou, para caderno,
 * "Caderno de atividades · 2 anos, Unidade 8 (p. 30–35)" (título e subtítulo vêm do catálogo).
 */
export function rotuloDoMaterial(
  m: MaterialImpresso,
  cadernos: readonly IdentidadeCaderno[] = [],
): string {
  const trecho = `Unidade ${m.unidade} (p. ${m.paginas[0]}–${m.paginas[1]})`;
  if (m.caderno === undefined) return `Tesouro de Marina · Vol. ${m.volume}, ${trecho}`;
  const c = cadernos.find((x) => x.id === m.caderno);
  return c ? `${c.titulo} · ${c.subtitulo}, ${trecho}` : `Caderno do Tesouro · ${trecho}`;
}
