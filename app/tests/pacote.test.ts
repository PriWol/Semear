import { describe, expect, it } from 'vitest';
import { gerarPacote, nomeArquivoPacote, type EntradaPacote } from '../src/pacote/gerar';
import { carregarConteudo } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import { observacoesDaSessao } from '../src/domain/registro';
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

  it('a ficha não parte uma linha de tabela entre duas páginas (#33)', () => {
    expect(doc).toMatch(/\.registro tr \{[^}]*break-inside: avoid/);
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

  it('a ficha imprime a lista de observacoesDaSessao, na mesma ordem (#11)', () => {
    const obs = observacoesDaSessao(sessao, idx);
    const ficha = gerarPacote(entrada({ observacoes: obs }));
    const aposFicha = ficha.slice(ficha.indexOf('Ficha de registro rápido'));
    const ids = [...aposFicha.matchAll(/<td>\s*<b>([A-Z]{2}\.[A-Z]{3}\.\d{2})<\/b>/g)].map(
      (m) => m[1],
    );
    expect(ids).toEqual(obs.map((o) => o.marcoId));
    // O que a tela de registro mostra é o que a ficha imprime: se a lista mudar, a ficha acompanha.
    const so = gerarPacote(entrada({ observacoes: obs.slice(0, 1) }));
    expect(so.slice(so.indexOf('Ficha de registro rápido'))).not.toContain(
      `<b>${obs[1]!.marcoId}</b>`,
    );
  });

  it('em Línguas, a ficha diz o idioma de cada linha', () => {
    const d = gerarPacote(
      entrada({
        observacoes: [
          { chave: 'LI.VOC.01@en', marcoId: 'LI.VOC.01', idioma: 'en', revisao: false },
        ],
      }),
    );
    expect(d).toContain('LI.VOC.01</b> · Inglês');
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
    expect(gerarPacote(entrada({ livro: null }))).toContain('Ainda não há indicação da curadoria');
  });
});

describe('nome do arquivo', () => {
  it('é seguro para qualquer sistema de arquivos', () => {
    expect(nomeArquivoPacote(sessao, crianca({ nome: 'João Pedro / 2' }))).toBe(
      'semear-s-1014-a1-joao-pedro-2.html',
    );
  });
});

describe('segurança do pacote (revisão de segurança, achados 1 e 3)', () => {
  it('uma letra adulterada (ex.: vinda de backup) não injeta HTML e cai no padrão', () => {
    const doc = gerarPacote(entrada({ letra: 'x"><img src=x onerror=alert(1)>' as never }));
    expect(doc).not.toContain('onerror=alert(1)>');
    expect(doc).toContain('<body class="letra-bastao">');
  });

  it('tem política de segurança (CSP) que corta conexões e imagens externas', () => {
    const doc = gerarPacote(entrada());
    expect(doc).toMatch(
      /<meta http-equiv="Content-Security-Policy" content="[^"]*default-src 'none'/,
    );
    expect(doc).toContain("connect-src 'none'");
  });

  it('imprime quando o app pede por mensagem (prévia isolada em sandbox)', () => {
    expect(gerarPacote(entrada())).toContain("e.data==='semear:imprimir'");
  });
});
