import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { criarRotas, lerHash, type Contexto } from '../src/ui/app';
import { ROTAS } from '../src/rotas';
import { paginaPrivacidade } from '../src/pages/privacidade';
import { paginaTermos } from '../src/pages/termos';

// Estas páginas não usam o contexto (são texto fixo), então um objeto vazio basta.
const ctx = {} as Contexto;

// Promessa de preço, plano ou prazo: os textos não podem ter nada disso (#25). O teste de controle
// abaixo prova que a regex pega os casos ruins, para ela não passar "em branco".
const PROMESSA =
  /R\$|preço|assinatura|mensalidade|\bplano (pago|gratuito|premium|mensal|anual)|cobrar|cobraremos|custará|\bcusta\b|\bvalor\b|\b(\d+|trinta|sessenta|noventa)[\s-]*(dias|meses|semanas)\b/i;
const promete = (t: string) => PROMESSA.test(t);

async function texto(fabrica: typeof paginaTermos) {
  const pagina = await fabrica(ctx, {});
  return {
    pagina,
    html: pagina.conteudo.valor,
    plano: pagina.conteudo.valor.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' '),
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

  it('a política traz as seções principais e cita Google Fonts e GitHub Pages', async () => {
    const { plano } = await texto(paginaPrivacidade);
    for (const t of [
      'O que fica no seu aparelho',
      'O que sai do seu aparelho',
      'Backup',
      'Apagar tudo',
      'Google Fonts',
      'GitHub Pages',
    ])
      expect(plano).toContain(t);
  });

  it.each([
    ['privacidade', paginaPrivacidade],
    ['termos', paginaTermos],
  ] as const)('%s: sem promessa de preço, plano ou prazo', async (_nome, fabrica) => {
    const { plano } = await texto(fabrica);
    expect(promete(plano)).toBe(false);
  });

  it('controle: a regex de promessa pega preço e prazo', () => {
    for (const ruim of [
      'Custa R$ 10 por mês',
      'Teste 30 dias grátis',
      'Gratuito por trinta dias',
      'Depois cobraremos uma taxa',
      'O valor será avisado',
      'Isso custará pouco',
      'um teste de 30-dias',
    ]) {
      expect(promete(ruim), ruim).toBe(true);
    }
    expect(promete('Hoje o Semear é gratuito e não pede conta.')).toBe(false);
  });

  it('termos: gratuito por ora, com aviso antes de cobrança', async () => {
    const { plano } = await texto(paginaTermos);
    expect(plano).toMatch(/cobrança, avisaremos antes/);
    expect(plano).toMatch(/Nada será cobrado sem esse aviso/);
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

  it('privacidade: anotações de texto livre ficam no aparelho e em claro no backup', async () => {
    const { plano } = await texto(paginaPrivacidade);
    expect(plano).toContain('anotações de texto livre');
    expect(plano).toMatch(/não é criptografado.*as anotações que você escreveu nas sessões/);
    expect(plano).toContain('Evite escrever nas anotações dados que você não quer ver no arquivo');
  });

  it('o roteador real leva /termos e /privacidade às páginas certas', () => {
    const rotas = criarRotas(ROTAS);
    const quem = (hash: string) => {
      const { caminho } = lerHash(hash);
      return rotas.find((r) => r.padrao.test(caminho))?.fabrica;
    };
    expect(quem('#/termos')).toBe(paginaTermos);
    expect(quem('#/privacidade')).toBe(paginaPrivacidade);
  });
});

describe('rodapé (#25): só tokens, sem valor solto', () => {
  const css = readFileSync(new URL('../src/estilos.css', import.meta.url), 'utf8');
  // Só o trecho do rodapé, entre os dois marcadores do estilos.css (inclui o @media print dele).
  const inicio = css.indexOf('/* ---------- Rodapé (#25)');
  const fim = css.indexOf('/* ---------- fim do rodapé ----------');
  const bloco = css.slice(inicio, fim);

  it('o CSS do rodapé existe', () => {
    expect(inicio).toBeGreaterThan(-1);
    expect(fim).toBeGreaterThan(inicio);
    expect(bloco).toContain('.rodape {');
  });

  it('não usa cor, px, rem ou em soltos (só var(--s-*))', () => {
    const semVar = bloco.replace(/var\(--s-[a-z0-9-]+\)/g, '');
    expect(semVar).not.toMatch(/#[0-9a-f]{3,8}\b/i);
    expect(semVar).not.toMatch(/rgba?\(/);
    expect(semVar).not.toMatch(/\d(px|rem|em)\b/);
    expect(bloco).not.toMatch(/var\(--(?!s-)/);
  });

  it('alvo de toque, texto mínimo e ocultação na impressão', () => {
    expect(bloco).toContain('min-height: var(--s-alvo-toque)');
    expect(bloco).toContain('font-size: var(--s-texto-p)');
    expect(bloco).toContain('.rodape a:focus-visible');
    expect(bloco).toMatch(/@media print\s*\{\s*\.rodape\s*\{\s*display: none;/);
  });

  it('os tokens usados existem com 3rem e 1rem', () => {
    const tokens = readFileSync(new URL('../src/tokens.css', import.meta.url), 'utf8');
    expect(tokens).toMatch(/--s-alvo-toque:\s*3rem/);
    expect(tokens).toMatch(/--s-texto-p:\s*1rem/);
  });
});
