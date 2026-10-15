/// <reference types="vitest/config" />
import { readFileSync } from 'node:fs';
import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

// Versão visível no app (#38): o número vem do package.json; a data e o commit, do build.
// No CI, o GitHub informa o commit em GITHUB_SHA; localmente aparece "local".
const pacote = JSON.parse(readFileSync(new URL('./package.json', import.meta.url), 'utf-8')) as {
  version: string;
};

// base relativa: o mesmo build funciona em qualquer subcaminho (ex.: GitHub Pages /Semear/)
export default defineConfig({
  base: './',
  define: {
    __VERSAO__: JSON.stringify(pacote.version),
    __DATA_BUILD__: JSON.stringify(new Date().toISOString()),
    __COMMIT__: JSON.stringify((process.env.GITHUB_SHA ?? 'local').slice(0, 7)),
  },
  plugins: [
    VitePWA({
      // "prompt": a versão nova espera o educador tocar em "Atualizar" (#38), em vez de trocar a tela
      // no meio do uso. O registro é feito em src/main.ts (virtual:pwa-register).
      registerType: 'prompt',
      injectRegister: false,
      includeAssets: ['icone.svg'],
      manifest: {
        name: 'Semear',
        short_name: 'Semear',
        description: 'Jornada de aprendizado e materiais para imprimir, para famílias educadoras.',
        lang: 'pt-BR',
        theme_color: '#2d5016',
        background_color: '#f7f5ef',
        display: 'standalone',
        start_url: './',
        scope: './',
        icons: [{ src: 'icone.svg', sizes: 'any', type: 'image/svg+xml', purpose: 'any' }],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,json}'],
        // A faxina do site antigo e o 404 não precisam ficar no cache offline do app.
        globIgnores: ['service-worker.js', '404.html'],
        // Os PDFs do Tesouro (./tesouro/) são abertos pelo navegador, não pelo app: sem isto o
        // service worker responderia com o index.html no lugar do PDF (ADR 0015).
        navigateFallbackDenylist: [/\.pdf$/],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/fonts\.(googleapis|gstatic)\.com\/.*/,
            handler: 'StaleWhileRevalidate',
            options: { cacheName: 'fontes', expiration: { maxEntries: 30 } },
          },
        ],
      },
    }),
  ],
  test: {
    environment: 'node',
    include: ['tests/**/*.test.ts'],
    setupFiles: ['tests/setup.ts'],
    // O pacote embute o próprio CSS (?raw). Sem isto, o Vitest troca CSS por texto vazio.
    css: { include: [/pacote\.css/] },
  },
});
