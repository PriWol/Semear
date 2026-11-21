// Paginação da lista de Atividades (#130): funções puras, sem DOM. A tela só decide quando chamar.

/** Quantas atividades aparecem de cada vez; o catálogo não é escondido, "Ver mais" chega a todas. */
export const TAMANHO_PAGINA = 20;

/** Primeiros `mostrando` itens; quantidade inválida vira lista vazia. */
export function fatiarPagina<T>(itens: readonly T[], mostrando: number): T[] {
  if (!Number.isFinite(mostrando) || mostrando <= 0) return [];
  return itens.slice(0, Math.floor(mostrando));
}

export function restantes(total: number, mostrando: number): number {
  return Math.max(0, total - Math.max(0, mostrando));
}

/** Quantas entram no próximo "Ver mais": até uma página, nunca mais que o que falta. */
export function proximoLote(total: number, mostrando: number): number {
  return Math.min(TAMANHO_PAGINA, restantes(total, mostrando));
}

/** Frase para leitor de tela e vista: "Mostrando 20 de 134 atividades". */
export function textoContagem(total: number, mostrando: number): string {
  if (total === 0) return 'Nenhuma atividade encontrada';
  const n = Math.min(total, Math.max(0, mostrando));
  return `Mostrando ${n} de ${total} ${total === 1 ? 'atividade' : 'atividades'}`;
}

/** "Limpar filtros" só faz sentido quando há texto (não só espaços) ou algum filtro escolhido. */
export function mostrarLimparFiltros(valores: Record<string, string | undefined>): boolean {
  return Object.entries(valores).some(([nome, v]) =>
    nome === 'texto' ? (v ?? '').trim() !== '' : (v ?? '') !== '',
  );
}
