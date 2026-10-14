import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { ehCacheDoSiteAntigo, limparCachesAntigos, PREFIXO_CACHE_SITE_ANTIGO } from '../src/legado';

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

  it('se apagar um cache falhar, apaga os outros e conta só os apagados', async () => {
    const caches = cachesFalsos(['semear-v1', 'semear-v2', 'fontes']);
    const comFalha = {
      keys: caches.keys,
      delete: async (nome: string) => {
        if (nome === 'semear-v1') throw new Error('falhou');
        return caches.delete(nome);
      },
    };
    expect(await limparCachesAntigos(comFalha)).toBe(1);
    expect([...caches.restantes]).toEqual(['semear-v1', 'fontes']);
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

describe('faxina do service worker antigo (public/service-worker.js)', () => {
  // O arquivo não pode importar módulos: este teste impede que o prefixo divirja de legado.ts.
  it('usa o mesmo prefixo de cache que o app', () => {
    const sw = readFileSync(new URL('../public/service-worker.js', import.meta.url), 'utf-8');
    expect(sw).toContain(`startsWith('${PREFIXO_CACHE_SITE_ANTIGO}')`);
  });

  // Executa o script real com um "self" simulado e dispara install e activate, como o navegador.
  it('ao ativar, apaga só os caches antigos e assume as páginas abertas', async () => {
    const sw = readFileSync(new URL('../public/service-worker.js', import.meta.url), 'utf-8');
    const ouvintes: Record<string, (ev: { waitUntil: (p: Promise<unknown>) => void }) => void> = {};
    const nomes = ['semear-v1.0.1', 'semear-v2', 'fontes', 'workbox-precache-v2-x'];
    const apagados: string[] = [];
    let esperas: Promise<unknown>[] = [];
    const chamadas = { skipWaiting: 0, claim: 0 };
    const self = {
      addEventListener: (tipo: string, f: (typeof ouvintes)[string]) => (ouvintes[tipo] = f),
      skipWaiting: () => chamadas.skipWaiting++,
      clients: { claim: async () => chamadas.claim++ },
    };
    const caches = {
      keys: async () => nomes,
      delete: async (n: string) => (apagados.push(n), true),
    };
    new Function('self', 'caches', sw)(self, caches);
    const evento = { waitUntil: (p: Promise<unknown>) => esperas.push(p) };

    ouvintes.install?.(evento);
    expect(chamadas.skipWaiting).toBe(1);

    esperas = [];
    ouvintes.activate?.(evento);
    await Promise.all(esperas);
    expect(esperas).toHaveLength(1);
    expect(apagados).toEqual(['semear-v1.0.1', 'semear-v2']);
    expect(chamadas.claim).toBe(1);
  });
});
