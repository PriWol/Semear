import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { idadeEmAnos } from '../domain/datas';
import { letraDaCrianca } from '../domain/letra';
import type { Atividade } from '../domain/tipos';
import { gerarPacote, nomeArquivoPacote } from '../pacote/gerar';
import { rotuloDoMaterial } from '../domain/material';
import { enderecoDoMaterial } from '../tesouro';
import { dataCurta } from '../ui/rotulos';

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
  if (!sessao || !familia || !crianca) throw new Error('Sessão não encontrada.');

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
    livro: sessao.livroId ? (ctx.idx.livro(sessao.livroId) ?? null) : null,
    marco: (id) => ctx.idx.marco(id),
  });
  const nomeArquivo = nomeArquivoPacote(sessao, crianca);

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
      ${atividades
        .filter((a) => a.materialImpresso && enderecoDoMaterial(a.materialImpresso))
        .map(
          (a) =>
            html`<p>
              📖
              <a href="${enderecoDoMaterial(a.materialImpresso!)}" target="_blank" rel="noopener"
                >Abrir no livro</a
              >
              <span class="nota">${a.titulo} · ${rotuloDoMaterial(a.materialImpresso!)}</span>
            </p>`,
        )}
      <div class="acoes barra-pacote">
        <button class="botao primario" type="button" id="imprimir">🖨️ Imprimir / salvar PDF</button>
        <button class="botao" type="button" id="baixar">⬇️ Baixar arquivo</button>
        <button class="botao" type="button" id="abrir">↗️ Abrir em tela cheia</button>
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
      ></iframe>
    `,
    montar(raiz) {
      const iframe = raiz.querySelector<HTMLIFrameElement>('#previa');
      if (iframe) iframe.srcdoc = documento;

      // A prévia é isolada (sandbox, sem a origem do app): o app não chama print() diretamente,
      // pede por mensagem e o próprio pacote imprime.
      raiz.querySelector('#imprimir')?.addEventListener('click', () => {
        iframe?.contentWindow?.postMessage('semear:imprimir', '*');
      });
      raiz.querySelector('#baixar')?.addEventListener('click', () => {
        baixarArquivo(nomeArquivo, documento, 'text/html;charset=utf-8');
      });
      raiz.querySelector('#abrir')?.addEventListener('click', () => {
        const url = URL.createObjectURL(new Blob([documento], { type: 'text/html;charset=utf-8' }));
        window.open(url, '_blank', 'noopener');
        setTimeout(() => URL.revokeObjectURL(url), 60_000);
      });
      raiz.querySelector('#excluir')?.addEventListener('click', async () => {
        if (!confirm(`Excluir a sessão ${sessao.codigo}?`)) return;
        await ctx.repo.removerSessao(sessao.id);
        ctx.avisar('Sessão excluída.');
        ctx.ir('/');
      });
    },
  };
};
