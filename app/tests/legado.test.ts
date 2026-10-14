import { describe, expect, it } from 'vitest';
import { ehCacheDoSiteAntigo, limparCachesAntigos } from '../src/legado';

/** Cache Storage falso, só com o que a limpeza usa. */
function cachesFalsos(nomes: string[]) {
  const restantes = new Set(nomes);
  return {
    restantes,
    keys: async () => [...restantes],
    delete: async (nome: string) => restantes.delete(nome),
  };
}

describe('limpeza dos caches do site antigo (ADR 0009)', () => {
  it('reconhece só os caches do site antigo', () => {
    expect(ehCacheDoSiteAntigo('semear-v1.0.1')).toBe(true);
    expect(ehCacheDoSiteAntigo('fontes')).toBe(false);
    expect(ehCacheDoSiteAntigo('workbox-precache-v2-https://priwol.github.io/Semear/')).toBe(false);
  });

  it('apaga os antigos e preserva os do app novo (o modo offline continua funcionando)', async () => {
    const caches = cachesFalsos([
      'semear-v1.0.1',
      'semear-v0.9',
      'fontes',
      'workbox-precache-v2-x',
    ]);
    expect(await limparCachesAntigos(caches)).toBe(2);
    expect([...caches.restantes]).toEqual(['fontes', 'workbox-precache-v2-x']);
  });

  it('não faz nada quando o navegador não tem Cache Storage', async () => {
    expect(await limparCachesAntigos(undefined)).toBe(0);
  });

  it('não lança erro quando o navegador recusa o acesso (ex.: navegação privada)', async () => {
    const recusa = {
      keys: async () => {
        throw new DOMException('negado', 'SecurityError');
      },
      delete: async () => false,
    };
    await expect(limparCachesAntigos(recusa)).resolves.toBe(0);
  });
});
