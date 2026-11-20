import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import type { Contexto } from '../src/ui/app';
import { paginaPrivacidade } from '../src/pages/privacidade';
import { paginaTermos } from '../src/pages/termos';

// Estas páginas não usam o contexto (são texto fixo), então um objeto vazio basta.
const ctx = {} as Contexto;

async function texto(fabrica: typeof paginaTermos) {
  const pagina = await fabrica(ctx, {});
  return {
    pagina,
    html: pagina.conteudo.valor,
    plano: pagina.conteudo.valor.replace(/<[^>]+>/g, ' '),
  };
}

describe('termos e privacidade (#25)', () => {
  it('privacidade: h1 e aviso de versão inicial', async () => {
    const { html } = await texto(paginaPrivacidade);
    expect(html).toContain('<h1>Política de privacidade</h1>');
    expect(html).toContain('Versão inicial, ainda sem revisão jurídica');
    expect(html).toContain('somente neste aparelho');
  });

  it('termos: h1 e aviso de versão inicial', async () => {
    const { html } = await texto(paginaTermos);
    expect(html).toContain('<h1>Termos de uso</h1>');
    expect(html).toContain('Versão inicial, ainda sem revisão jurídica');
  });

  it.each([
    ['privacidade', paginaPrivacidade],
    ['termos', paginaTermos],
  ] as const)('%s: sem promessa de preço, plano ou prazo', async (_nome, fabrica) => {
    const { plano } = await texto(fabrica);
    expect(plano).not.toMatch(
      /R\$|preço|assinatura|mensalidade|\bplano (pago|gratuito|premium|mensal|anual)/i,
    );
    expect(plano).not.toMatch(/\b\d+\s*(dias|meses|semanas)\b/i);
  });

  it('termos: gratuito por ora, com aviso antes de cobrança', async () => {
    const { plano } = await texto(paginaTermos);
    expect(plano).toMatch(/cobrança, avisaremos antes/);
    expect(plano).toMatch(/Nada será cobrado\s+sem esse aviso/);
  });

  it.each([
    ['privacidade', paginaPrivacidade],
    ['termos', paginaTermos],
  ] as const)(
    '%s: não afirma conformidade legal nem traz seções adiadas',
    async (_nome, fabrica) => {
      const { plano } = await texto(fabrica);
      expect(plano).not.toMatch(/LGPD|ECA Digital|em conformidade|compatível com|conforme a lei/i);
      expect(plano).not.toMatch(/Sem garantias|Quem responde|Dúvidas/);
      expect(plano).not.toMatch(/você diz que é adulto/);
    },
  );

  it('a nota de "Apagar dados" descreve o que o app apaga de fato', () => {
    const config = readFileSync(new URL('../src/pages/config.ts', import.meta.url), 'utf8');
    expect(config).toContain('Remove tudo o que você cadastrou e registrou neste aparelho.');
  });

  it('a rota /termos está registrada ao lado de /privacidade', () => {
    const main = readFileSync(new URL('../src/main.ts', import.meta.url), 'utf8');
    expect(main).toContain("'/termos': paginaTermos");
    expect(main).toContain("'/privacidade': paginaPrivacidade");
  });
});

describe('rodapé (#25): só tokens, sem valor solto', () => {
  const css = readFileSync(new URL('../src/estilos.css', import.meta.url), 'utf8');
  const inicio = css.indexOf('.rodape {');
  const bloco = css.slice(inicio);

  it('o CSS do rodapé existe', () => {
    expect(inicio).toBeGreaterThan(-1);
  });

  it('não usa cor, px, rem ou em soltos (só var(--s-*))', () => {
    // A espessura de fio (1px solid) do filete não é medida de layout e não tem token.
    const semVar = bloco.replace(/var\(--s-[a-z0-9-]+\)/g, '').replace(/\b1px solid\b/g, '');
    expect(semVar).not.toMatch(/#[0-9a-f]{3,8}\b/i);
    expect(semVar).not.toMatch(/rgba?\(/);
    expect(semVar).not.toMatch(/\d(px|rem|em)\b/);
    expect(bloco).not.toMatch(/var\(--(?!s-)/);
  });

  it('alvo de toque, texto mínimo e ocultação na impressão', () => {
    expect(bloco).toContain('min-height: var(--s-alvo-toque)');
    expect(bloco).toContain('font-size: var(--s-texto-minimo)');
    expect(bloco).toMatch(/@media print\s*\{\s*\.rodape\s*\{\s*display: none;/);
  });

  it('os tokens de medida existem com 3rem e 1rem', () => {
    const tokens = readFileSync(new URL('../src/tokens.css', import.meta.url), 'utf8');
    expect(tokens).toMatch(/--s-alvo-toque:\s*3rem/);
    expect(tokens).toMatch(/--s-texto-minimo:\s*1rem/);
  });
});
