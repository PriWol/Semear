// Busca no acervo gratuito. Pura: roda inteira no aparelho, sem consultar nenhum serviço externo.
import type { IdiomaAcervo, ItemAcervo } from './tipos';

export interface FiltroAcervo {
  texto: string;
  idioma: IdiomaAcervo | '';
  /** idade da criança; mantém os itens cuja faixa a inclui */
  idade: number | null;
}

/** Minúsculas e sem acento, para "cancao" achar "Canção". */
export function normalizar(texto: string): string {
  return texto
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

export function buscarAcervo(itens: ItemAcervo[], filtro: FiltroAcervo): ItemAcervo[] {
  const termos = normalizar(filtro.texto).split(/\s+/).filter(Boolean);
  return itens.filter((i) => {
    if (filtro.idioma && i.idioma !== filtro.idioma) return false;
    if (filtro.idade !== null && (filtro.idade < i.idade[0] || filtro.idade > i.idade[1]))
      return false;
    const palheiro = normalizar(`${i.titulo} ${i.autor} ${i.fonte} ${i.sobre}`);
    return termos.every((t) => palheiro.includes(t));
  });
}
