import { defineConfig, devices } from '@playwright/test';

// Testes ponta a ponta: sobem o app (build de produção) e simulam um educador usando-o.
export default defineConfig({
  testDir: 'e2e',
  fullyParallel: true,
  retries: process.env.CI ? 1 : 0,
  // Em CI o JSON alimenta o resumo de testes instáveis (.github/scripts, ADR 0039); o caminho é relativo a app/.
  reporter: process.env.CI
    ? [['github'], ['json', { outputFile: 'playwright-report/resultados.json' }]]
    : 'list',
  use: {
    baseURL: 'http://localhost:4173',
    // Em CI grava o trace na repetição, que é o que mostra por que o teste instável falhou (ADR 0039).
    trace: process.env.CI ? 'on-first-retry' : 'retain-on-failure',
  },
  webServer: {
    command: 'npm run build && npm run preview -- --port 4173 --strictPort',
    url: 'http://localhost:4173',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'celular', use: { ...devices['Pixel 7'] } },
  ],
});
