// Faxina do site antigo (ADR 0009). O Semear antigo registrava este arquivo como service worker e
// guardava páginas em caches "semear-v*". Quem já tinha visitado o site recebe esta versão, que apaga
// esses caches. O service worker do app novo é o sw.js, gerado no build.
// O prefixo "semear-v" também está em src/legado.ts (PREFIXO_CACHE_SITE_ANTIGO): mude os dois juntos.
// Sem unregister() de propósito: se o app novo já tiver registrado o sw.js no mesmo escopo, o
// unregister() desfaria o registro do app novo (ver ADR 0009).
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((nomes) =>
        Promise.all(nomes.filter((n) => n.startsWith('semear-v')).map((n) => caches.delete(n))),
      )
      .then(() => self.clients.claim()),
  );
});
