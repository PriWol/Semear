/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

// base relativa: o mesmo build funciona em qualquer subcaminho (ex.: GitHub Pages /Semear/)
export default defineConfig({
  base: './',
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
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
