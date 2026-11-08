import { describe, expect, it } from 'vitest';
import { validarConteudo, criarIndice } from '../src/domain/conteudo';
import { sugerirLivro } from '../src/domain/sessao';
import { gerarPacote } from '../src/pacote/gerar';
import type { Livro } from '../src/domain/tipos';
import { AGORA, atividade, conteudoBase, crianca, familia } from './fabricas';

const base: Livro = {
  id: 'liv',
  titulo: 'Título',
  autor: 'Autor',
  vertentes: ['Montessori'],
  marcos: [],
  idade: [3, 8],
  uso: 'leitura-em-voz-alta',
  porQue: 'Porque sim.',
};
const obra = (extra: Partial<Livro> = {}): Livro => ({
  ...base,
  id: 'obra-1',
  tipo: 'obra',
  titulo: 'A noite estrelada',
  autor: 'Vincent van Gogh',
  uso: 'observar-e-conversar',
  fonte: 'Domínio público (1889); acervo do MoMA, Nova York',
  linhas: ['LG.FON'],
  ...extra,
});
const musica = (extra: Partial<Livro> = {}): Livro => ({
  ...base,
  id: 'mus-1',
  tipo: 'musica',
  titulo: 'Ciranda, cirandinha',
  autor: 'Tradicional',
  uso: 'ouvir-e-cantar',
  fonte: 'Cantiga de roda, domínio público',
  marcos: ['LG.FON.01'],
  ...extra,
});
const erros = (livros: Livro[]) => validarConteudo({ ...conteudoBase(), livros }).erros;

describe('obras e músicas na curadoria (#73)', () => {
  it('aceita livro, obra e música, com fonte nas duas últimas', () => {
    expect(erros([base, obra(), musica()])).toEqual([]);
  });
  it('recusa tipo desconhecido e obra ou música sem fonte', () => {
    expect(erros([{ ...base, tipo: 'filme' as never }]).some((e) => /tipo/.test(e))).toBe(true);
    expect(erros([obra({ fonte: ' ' })]).some((e) => /fonte/.test(e))).toBe(true);
    expect(erros([musica({ fonte: undefined })]).some((e) => /fonte/.test(e))).toBe(true);
  });
  it('recusa linha que não existe e link gratuito que não é https', () => {
    expect(erros([obra({ linhas: ['XX.YYY'] })].flat()).some((e) => /linha/.test(e))).toBe(true);
    expect(
      erros([obra({ linkGratuito: 'javascript:alert(1)' })]).some((e) => /linkGratuito/.test(e)),
    ).toBe(true);
    expect(erros([obra({ linkGratuito: 'https://exemplo.org/obra' })])).toEqual([]);
  });
});

describe('indicação da sessão (#73)', () => {
  const idx = criarIndice(
    conteudoBase({ livros: [obra()], atividades: [atividade('a', ['LG.FON.02'])] }),
  );
  it('liga a indicação pela linha dos marcos trabalhados, não só pelo marco', () => {
    expect(sugerirLivro(idx, [{ atividade: idx.atividade('a')! }], familia(), 5)?.id).toBe(
      'obra-1',
    );
  });
  it('o pacote nomeia o tipo e mostra a fonte, sem link para a criança abrir', () => {
    const doc = gerarPacote({
      sessao: {
        id: 's',
        codigo: 'S-1',
        criancaId: 'c1',
        criadaEm: AGORA,
        duracaoMin: 20,
        foco: 'equilibrado',
        atividadeIds: ['a'],
        livroId: 'obra-1',
      },
      familia: familia(),
      crianca: crianca(),
      idade: 5,
      letra: 'script',
      atividades: [idx.atividade('a')!],
      livro: idx.livro('obra-1') ?? null,
      marco: (id) => idx.marco(id),
    });
    expect(doc).toContain('Obra para apreciar');
    expect(doc).toContain('Domínio público (1889); acervo do MoMA, Nova York');
    expect(doc).not.toContain('Livro sugerido');
  });
});
