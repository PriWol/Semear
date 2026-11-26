import js from '@eslint/js';
import globals from 'globals';
import tseslint from 'typescript-eslint';

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
    // e2e espera por elemento ou condição, nunca por tempo: espera fixa é a causa clássica de teste instável
    // (docs/APRENDIZADOS.md). Os `new Promise` de e2e são pontes de evento, não de relógio, e não são barrados.
    files: ['e2e/**/*.ts'],
    rules: {
      'no-restricted-syntax': [
        'error',
        {
          selector: "CallExpression[callee.property.name='waitForTimeout']",
          message:
            'Espera fixa (waitForTimeout) deixa o e2e instável. Espere por um elemento ou condição: expect(...).toBeVisible() ou expect.poll (docs/APRENDIZADOS.md).',
        },
        {
          selector:
            "CallExpression[callee.name='setTimeout'], CallExpression[callee.property.name='setTimeout']",
          message:
            'setTimeout no e2e é espera por tempo. Espere por um elemento ou condição: expect(...).toBeVisible() ou expect.poll (docs/APRENDIZADOS.md).',
        },
        {
          selector: "Literal[value='networkidle']",
          message:
            "'networkidle' espera por tempo de rede ocioso e é frágil. Espere pelo elemento que prova que a tela carregou (docs/APRENDIZADOS.md).",
        },
      ],
    },
  },
);
