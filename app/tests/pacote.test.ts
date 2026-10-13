import { describe, expect, it } from 'vitest';
import { gerarPacote, nomeArquivoPacote, type EntradaPacote } from '../src/pacote/gerar';
import { carregarConteudo } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import type { Sessao } from '../src/domain/tipos';
import { AGORA, crianca, familia } from './fabricas';

const idx = criarIndice(carregarConteudo());
const sessao: Sessao = {
  id: 's1',
  codigo: 'S-1014-A1',
  criancaId: 'c1',
  criadaEm: AGORA,
  duracaoMin: 40,
  foco: 'equilibrado',
  atividadeIds: ['atv-caca-silabas', 'atv-feira-numeros'],
  livroId: 'livro-ou-isto-ou-aquilo',
};

function entrada(extra: Partial<EntradaPacote> = {}): EntradaPacote {
  return {
    sessao,
    familia: familia({ inspiracoes: ['Waldorf'] }),
    crianca: crianca(),
    idade: 5.5,
    letra: 'script',
    atividades: sessao.atividadeIds.map((id) => idx.atividade(id)!),
    livro: idx.livro('livro-ou-isto-ou-aquilo') ?? null,
    marco: (id) => idx.marco(id),
    ...extra,
  };
}

const contar = (doc: string, trecho: string) => doc.split(trecho).length - 1;

describe('gerarPacote (§5.7)', () => {
  const doc = gerarPacote(entrada());

  it('é um documento HTML completo com CSS e script embutidos (funciona offline)', () => {
    expect(doc.startsWith('<!doctype html>')).toBe(true);
    expect(doc).toMatch(/<style>[^<]*\.pagina \{/); // o CSS do pacote está embutido de verdade
    expect(doc).toContain('@page');
    expect(doc).toContain('function alternarTablet');
  });

  it('tem roteiro, materiais, uma página por folha e a ficha', () => {
    const folhas = entrada().atividades.reduce((t, a) => t + a.folhas.length, 0);
    expect(contar(doc, 'class="pagina crianca"')).toBe(folhas);
    expect(contar(doc, 'class="pagina educador"')).toBe(3);
    expect(doc).toContain('Roteiro do educador');
    expect(doc).toContain('Ficha de registro rápido');
  });

  it('aplica a letra da criança e marca a opção no seletor', () => {
    expect(doc).toContain('<body class="letra-script">');
    expect(doc).toContain('<option value="script" selected>');
  });

  it('lista na ficha os marcos principais e os de revisão', () => {
    expect(doc).toContain('LG.FON.04');
    expect(doc).toContain('LG.FON.03</b> (revisão)');
    expect(doc).toContain('MA.SEN.05</b> (revisão)');
  });

  it('mostra só os toques das vertentes que a família usa', () => {
    expect(doc).toContain('Waldorf (inspiração):');
    expect(doc).not.toContain('<b>Clássico');
  });

  it('escapa o nome da criança', () => {
    const malicioso = gerarPacote(entrada({ crianca: crianca({ nome: '<script>x</script>' }) }));
    expect(malicioso).not.toContain('<script>x</script>');
    expect(malicioso).toContain('&lt;script&gt;x&lt;/script&gt;');
  });

  it('sem livro, mostra um aviso no lugar', () => {
    expect(gerarPacote(entrada({ livro: null }))).toContain('Ainda não há livro da curadoria');
  });
});

describe('nome do arquivo', () => {
  it('é seguro para qualquer sistema de arquivos', () => {
    expect(nomeArquivoPacote(sessao, crianca({ nome: 'João Pedro / 2' }))).toBe(
      'semear-s-1014-a1-joao-pedro-2.html',
    );
  });
});
