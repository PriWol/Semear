import js from '@eslint/js';
import globals from 'globals';
import tseslint from 'typescript-eslint';

const MENSAGEM_ESPERA_E2E =
  'e2e espera por elemento ou estado visível (expect(...).toBeVisible()), nunca por tempo; veja docs/APRENDIZADOS.md';

export default tseslint.config(
  { ignores: ['dist', 'dev-dist', 'node_modules', 'test-results', 'playwright-report'] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    languageOptions: { globals: { ...globals.browser, ...globals.node } },
    rules: {
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      eqeqeq: ['error', 'always'],
    },
  },
  {
    // A camada de domínio é pura: não depende da interface, do armazenamento nem do navegador (ADR 0003).
    files: ['src/domain/**/*.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        { patterns: ['../ui/*', '../pages/*', '../dados/*', '../pacote/*'] },
      ],
      'no-restricted-globals': [
        'error',
        ...[
          'window',
          'document',
          'localStorage',
          'sessionStorage',
          'indexedDB',
          'location',
          'navigator',
          'fetch',
          'XMLHttpRequest',
          'self',
          'globalThis',
        ],
      ],
    },
  },
  {
    // Teste e2e espera por elemento ou estado visível, nunca por tempo: espera fixa deixa o teste lento e instável (#175).
    files: ['e2e/**/*.ts'],
    rules: {
      'no-restricted-syntax': [
        'error',
        {
          selector: "CallExpression[callee.property.name='waitForTimeout']",
          message: MENSAGEM_ESPERA_E2E,
        },
        {
          selector: 'CallExpression[callee.name=/^(setTimeout|setInterval)$/]',
          message: MENSAGEM_ESPERA_E2E,
        },
        {
          selector: 'CallExpression[callee.property.name=/^(setTimeout|setInterval)$/]',
          message: MENSAGEM_ESPERA_E2E,
        },
        {
          // Cobre `waitUntil: 'networkidle'` e `waitForLoadState('networkidle')`.
          selector: "Literal[value='networkidle']",
          message: MENSAGEM_ESPERA_E2E,
        },
      ],
    },
  },
);
