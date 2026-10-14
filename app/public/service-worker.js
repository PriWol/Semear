// Faxina do site antigo (ADR 0009). O Semear antigo registrava este arquivo como service worker e
// guardava páginas em caches "semear-v*". Quem já tinha visitado o site recebe esta versão, que apaga
// esses caches e sai do caminho. O service worker do app novo é o sw.js, gerado no build.
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
