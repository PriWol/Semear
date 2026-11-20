import { describe, expect, it } from 'vitest';
import { criarRotas, lerHash, lista } from '../src/ui/app';
import { ROTAS } from '../src/rotas';
import { paginaRegistrarBusca } from '../src/pages/registrar-busca';
import { paginaSessaoRegistrar } from '../src/pages/sessao-registrar';
import { paginaSessao } from '../src/pages/sessao';
import { paginaSessaoNova } from '../src/pages/sessao-nova';

describe('rotas por hash (ADR 0008)', () => {
  it('separa caminho e parâmetros de busca', () => {
    expect(lerHash('#/sessao/nova?crianca=abc&x=1')).toEqual({
      caminho: '/sessao/nova',
      query: { crianca: 'abc', x: '1' },
    });
    expect(lerHash('')).toEqual({ caminho: '/', query: {} });
  });
  it('casa rotas com parâmetros nomeados, priorizando a ordem de declaração', async () => {
    const pagina = async () => ({ titulo: '', conteudo: { valor: '' } as never });
    const rotas = criarRotas({ '/sessao/nova': pagina, '/sessao/:id': pagina });
    expect(rotas[0]!.padrao.test('/sessao/nova')).toBe(true);
    const m = rotas[1]!.padrao.exec('/sessao/123');
    expect(m?.[1]).toBe('123');
    expect(rotas[1]!.nomes).toEqual(['id']);
    expect(rotas[1]!.padrao.test('/sessao/1/2')).toBe(false);
  });
  it('as rotas de registro (#11): ":id" não engole "registrar" e cada uma vai para a sua tela', () => {
    const rotas = criarRotas(ROTAS);
    const quem = (hash: string) => {
      const { caminho } = lerHash(hash);
      return rotas.find((r) => r.padrao.test(caminho))?.fabrica;
    };
    expect(quem('#/sessao/registrar')).toBe(paginaRegistrarBusca);
    expect(quem('#/sessao/registrar?crianca=c1')).toBe(paginaRegistrarBusca);
    expect(quem('#/sessao/abc-123/registrar')).toBe(paginaSessaoRegistrar);
    expect(quem('#/sessao/abc-123')).toBe(paginaSessao);
    expect(quem('#/sessao/nova')).toBe(paginaSessaoNova);
    // um id que se chama "registrar" também chega à tela de registro, não à busca
    expect(quem('#/sessao/registrar/registrar')).toBe(paginaSessaoRegistrar);
  });
  it('lista normaliza campos de formulário', () => {
    expect(lista(undefined)).toEqual([]);
    expect(lista('a')).toEqual(['a']);
    expect(lista(['a', 'b'])).toEqual(['a', 'b']);
  });
});
