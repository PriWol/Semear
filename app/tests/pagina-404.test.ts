import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

// Executa o script real do public/404.html com um endereço simulado (o vite preview usado nos e2e
// não serve o 404.html como o GitHub Pages, então testamos o script diretamente).
const html = readFileSync(new URL('../public/404.html', import.meta.url), 'utf-8');
const script = /<script>([\s\S]*?)<\/script>/.exec(html)?.[1] ?? '';

function redirecionamento(pathname: string, hash = ''): string | null {
  let destino: string | null = null;
  const location = { pathname, hash, replace: (url: string) => (destino = url) };
  new Function('location', script)(location);
  return destino;
}

describe('página 404 (endereços antigos e inexistentes)', () => {
  it('o script existe no 404.html', () => {
    expect(script).toContain('location.replace');
  });

  it('endereços do site antigo voltam para o início do app', () => {
    expect(redirecionamento('/Semear/weekly-plan')).toBe('/Semear/');
    expect(redirecionamento('/Semear/onboarding')).toBe('/Semear/');
    expect(redirecionamento('/Semear/assets/inexistente.js')).toBe('/Semear/');
  });

  it('mantém a rota por hash', () => {
    expect(redirecionamento('/Semear/x', '#/familia')).toBe('/Semear/#/familia');
  });

  it('fora de /Semear/ vai para a raiz', () => {
    expect(redirecionamento('/outra-coisa')).toBe('/');
  });

  it('não entra em loop quando a própria base deu 404 (ex.: publicação quebrada)', () => {
    expect(redirecionamento('/Semear/')).toBeNull();
    expect(redirecionamento('/')).toBeNull();
  });
});
