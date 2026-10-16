import { describe, expect, it } from 'vitest';
import { buscarAcervo, normalizar } from '../src/domain/acervo';
import { enderecoHttpsValido, validarConteudo } from '../src/domain/conteudo';
import type { ItemAcervo } from '../src/domain/tipos';
import { carregarConteudo } from '../src/conteudo';
import { conteudoBase } from './fabricas';

function item(extra: Partial<ItemAcervo> = {}): ItemAcervo {
  return {
    id: 'acervo-x',
    titulo: 'Canção de Ninar',
    autor: 'Autora',
    idioma: 'pt',
    idade: [2, 5],
    fonte: 'Fonte',
    licenca: 'Domínio público',
    url: 'https://exemplo.org/livro',
    tipoLink: 'obra',
    sobre: 'Rimas',
    ...extra,
  };
}

describe('buscarAcervo', () => {
  const itens = [
    item(),
    item({ id: 'b', titulo: 'Orbis Pictus', idioma: 'la', idade: [4, 8], autor: 'Comenius' }),
  ];
  const vazio = { texto: '', idioma: '' as const, idade: null };

  it('sem filtros devolve tudo', () => {
    expect(buscarAcervo(itens, vazio)).toHaveLength(2);
  });
  it('ignora acento e maiúsculas', () => {
    expect(normalizar('  CANÇÃO ')).toBe('cancao');
    expect(buscarAcervo(itens, { ...vazio, texto: 'cancao ninar' }).map((i) => i.id)).toEqual([
      'acervo-x',
    ]);
  });
  it('filtra por idioma e por idade', () => {
    expect(buscarAcervo(itens, { ...vazio, idioma: 'la' }).map((i) => i.id)).toEqual(['b']);
    expect(buscarAcervo(itens, { ...vazio, idade: 3 }).map((i) => i.id)).toEqual(['acervo-x']);
    expect(buscarAcervo(itens, { ...vazio, idade: 8 }).map((i) => i.id)).toEqual(['b']);
  });
  it('todos os termos precisam aparecer', () => {
    expect(buscarAcervo(itens, { ...vazio, texto: 'orbis ninar' })).toEqual([]);
  });
});

describe('validação do acervo e dos links', () => {
  it('só aceita https', () => {
    expect(enderecoHttpsValido('https://a.org/x')).toBe(true);
    expect(enderecoHttpsValido('http://a.org/x')).toBe(false);
    expect(enderecoHttpsValido('javascript:alert(1)')).toBe(false);
    expect(enderecoHttpsValido('/relativo')).toBe(false);
  });
  it('acusa url insegura, idade fora de 2–8 e id repetido no acervo', () => {
    const c = conteudoBase();
    c.acervo = [item({ url: 'http://x.org' }), item({ id: 'acervo-x', idade: [1, 5] })];
    const { erros } = validarConteudo(c);
    expect(erros).toContain('Acervo acervo-x: url precisa ser um endereço https');
    expect(erros).toContain('Acervo acervo-x: idade fora de 2 a 8 anos');
    expect(erros).toContain('Item do acervo com id repetido: acervo-x');
  });
  it('acusa linkCompra que não seja https', () => {
    const c = conteudoBase();
    c.livros[0]!.linkCompra = 'javascript:alert(1)';
    expect(validarConteudo(c).erros).toContain(
      'Livro livro-a: linkCompra precisa ser um endereço https',
    );
  });
});

describe('conteúdo real', () => {
  it('tem pelo menos 50 livros e acervo nos quatro idiomas', () => {
    const c = carregarConteudo();
    expect(c.livros.length).toBeGreaterThanOrEqual(50);
    expect(new Set(c.acervo.map((i) => i.idioma))).toEqual(new Set(['pt', 'en', 'la', 'fr']));
  });
});
