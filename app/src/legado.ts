// Transição do site antigo para o app novo (ADR 0009).

/**
 * Prefixo dos caches do service worker do site antigo (`semear-v1.0.1`…).
 * O mesmo prefixo está em `public/service-worker.js`, que não pode importar módulos: mude os dois juntos.
 */
export const PREFIXO_CACHE_SITE_ANTIGO = 'semear-v';

/** Só caches do site antigo. Os do app novo (`workbox-precache-*`, `fontes`) nunca entram. */
export function ehCacheDoSiteAntigo(nome: string): boolean {
  return nome.startsWith(PREFIXO_CACHE_SITE_ANTIGO);
}

/**
 * Apaga os caches do site antigo. Roda a cada abertura do app: depois da primeira vez não acha nada,
 * e o custo (listar os nomes dos caches) é desprezível perto de guardar e manter um marcador.
 * Nunca lança erro (ex.: navegação privada pode recusar o acesso ao Cache Storage).
 * Devolve quantos caches apagou.
 */
export async function limparCachesAntigos(
  armazenamento: Pick<CacheStorage, 'keys' | 'delete'> | undefined,
): Promise<number> {
  if (!armazenamento) return 0;
  try {
    const antigos = (await armazenamento.keys()).filter(ehCacheDoSiteAntigo);
    // allSettled: se um cache falhar, os outros continuam sendo apagados (o que falhou fica para a próxima vez).
    const resultados = await Promise.allSettled(antigos.map((nome) => armazenamento.delete(nome)));
    return resultados.filter((r) => r.status === 'fulfilled' && r.value).length;
  } catch {
    return 0;
  }
}
