import { NaoEncontrado, type FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { icone } from '../ui/icones';
import { abrirPainelPacote } from '../ui/painel-pacote';
import { idadeEmAnos } from '../domain/datas';
import { letraDaCrianca } from '../domain/letra';
import type { Atividade } from '../domain/tipos';
import { gerarPacote, nomeArquivoPacote } from '../pacote/gerar';
import { rotuloDoMaterial } from '../domain/material';
import { observacoesDaSessao, sessaoRegistrada } from '../domain/registro';
import { CADERNOS, enderecoDoMaterial } from '../tesouro';
import { dataCurta, ICONE_ENGAJAMENTO, NOME_ENGAJAMENTO, ROTULO_FEITA } from '../ui/rotulos';

export function baixarArquivo(nome: string, conteudo: string, tipo: string) {
  const url = URL.createObjectURL(new Blob([conteudo], { type: tipo }));
  const a = document.createElement('a');
  a.href = url;
  a.download = nome;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10_000);
}

export const paginaSessao: FabricaPagina = async (ctx, params) => {
  const sessao = params.id ? await ctx.repo.sessao(params.id) : null;
  const familia = await ctx.repo.familia();
  const crianca = sessao ? await ctx.repo.crianca(sessao.criancaId) : null;
  if (!sessao || !familia || !crianca) throw new NaoEncontrado('sessão');

  // A data da sessão (não a de hoje) define idade e letra: o pacote reaberto sai igual ao original.
  const idade = idadeEmAnos(crianca.nascimento, new Date(sessao.criadaEm));
  const atividades = sessao.atividadeIds
    .map((id) => ctx.idx.atividade(id))
    .filter((a): a is Atividade => a !== undefined);
  const faltando = sessao.atividadeIds.length - atividades.length;
  const documento = gerarPacote({
    sessao,
    familia,
    crianca,
    idade,
    letra: letraDaCrianca(crianca, idade, familia),
    atividades,
    observacoes: observacoesDaSessao(sessao, ctx.idx),
    livro: sessao.livroId ? (ctx.idx.livro(sessao.livroId) ?? null) : null,
    marco: (id) => ctx.idx.marco(id),
    cadernos: CADERNOS,
  });
  const nomeArquivo = nomeArquivoPacote(sessao, crianca);
  const registrada = sessaoRegistrada(sessao);

  return {
    titulo: `Sessão ${sessao.codigo}`,
    conteudo: html`
      <h1>Sessão ${sessao.codigo}</h1>
      <p class="nota">
        ${crianca.nome} · ${dataCurta(sessao.criadaEm)} ·
        ${atividades.map((a) => a.titulo).join(' + ')}
      </p>
      ${
        faltando
          ? html`<p class="alerta">
              ${faltando} atividade(s) desta sessão não existem mais no conteúdo.
            </p>`
          : ''
      }
      ${atividades.flatMap((a) => {
        const m = a.materialImpresso;
        const endereco = m ? enderecoDoMaterial(m) : null;
        if (!m || !endereco) return [];
        return html`<p>
          ${icone('book-open')}
          <a href="${endereco}" target="_blank" rel="noopener">Abrir no livro</a>
          <span class="nota">${a.titulo} · ${rotuloDoMaterial(m, CADERNOS)}</span>
        </p>`;
      })}
      ${
        registrada
          ? html`<section class="cartao reg-resumo" aria-labelledby="titulo-registro">
              <h2 id="titulo-registro">
                Registro da sessão <span class="selo-feita">${ROTULO_FEITA}</span>
              </h2>
              <p class="nota">Registrada em ${dataCurta(sessao.registradaEm ?? sessao.criadaEm)}.</p>
              ${
                sessao.duracaoReal !== undefined
                  ? html`<p>Duração real: ${sessao.duracaoReal} min (planejado: ${sessao.duracaoMin} min)</p>`
                  : ''
              }
              ${
                sessao.engajamento
                  ? html`<p>
                      Engajamento:
                      ${ICONE_ENGAJAMENTO[sessao.engajamento]}
                      ${NOME_ENGAJAMENTO[sessao.engajamento]}
                    </p>`
                  : ''
              }
              ${
                sessao.anotacoes
                  ? html`<p><b>Anotações</b></p>
                      <p class="reg-anotacoes">${sessao.anotacoes}</p>`
                  : ''
              }
            </section>`
          : ''
      }
      <div class="acoes barra-pacote">
        <a class="botao" href="#/sessao/${sessao.id}/registrar"
          >${registrada ? 'Corrigir registro' : 'Registrar'}</a
        >
        <button class="botao primario" type="button" id="imprimir">${icone('printer')} Imprimir / salvar PDF</button>
        <button class="botao" type="button" id="baixar">${icone('download-simple')} Baixar arquivo</button>
        <button class="botao" type="button" id="abrir">${icone('arrow-square-out')} Abrir em tela cheia</button>
        <button class="botao perigo" type="button" id="excluir">Excluir</button>
      </div>
      <p class="nota">
        O arquivo baixado abre em qualquer navegador, inclusive no tablet sem internet, e tem o
        botão “Modo tablet”, que mostra só as folhas da criança.
      </p>
      <iframe
        class="previa"
        id="previa"
        title="Pré-visualização do pacote"
        sandbox="allow-scripts allow-modals"
        src="./previa.html"
      ></iframe>
    `,
    montar(raiz) {
      const iframe = raiz.querySelector<HTMLIFrameElement>('#previa');
      // A prévia é uma página própria (public/previa.html) com CSP separada; o pacote chega por
      // mensagem. srcdoc e blob herdariam a CSP do app e o script do pacote deixaria de rodar (#32).
      iframe?.addEventListener(
        'load',
        () => iframe.contentWindow?.postMessage({ tipo: 'semear:documento', html: documento }, '*'),
        { once: true },
      );

      // A prévia é isolada (sandbox, sem a origem do app): o app não chama print() diretamente,
      // pede por mensagem e o próprio pacote imprime.
      raiz.querySelector('#imprimir')?.addEventListener('click', () => {
        iframe?.contentWindow?.postMessage('semear:imprimir', '*');
      });
      raiz.querySelector('#baixar')?.addEventListener('click', () => {
        baixarArquivo(nomeArquivo, documento, 'text/html;charset=utf-8');
      });
      // Tela cheia = painel sobre o app com a mesma prévia isolada, não nova aba (#139, ADR 0022).
      raiz.querySelector<HTMLElement>('#abrir')?.addEventListener('click', (ev) => {
        abrirPainelPacote({
          titulo: `Sessão ${sessao.codigo}`,
          documento,
          abridor: ev.currentTarget as HTMLElement,
        });
      });
      raiz.querySelector('#excluir')?.addEventListener('click', async () => {
        const aviso = registrada ? ' O registro e as observações dela também serão apagados.' : '';
        if (!confirm(`Excluir a sessão ${sessao.codigo}?${aviso}`)) return;
        await ctx.repo.removerSessao(sessao.id);
        ctx.avisar('Sessão excluída.');
        ctx.ir('/');
      });
    },
  };
};
