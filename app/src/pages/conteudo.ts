import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { validarConteudo } from '../domain/conteudo';

/** Visão para a curadoria: cobertura do conteúdo e problemas encontrados pela validação. */
export const paginaConteudo: FabricaPagina = async (ctx) => {
  const { erros, avisos } = validarConteudo(ctx.idx.conteudo);
  const dominios = ctx.idx.conteudo.dominios.filter((d) => d.comJornada);

  return {
    titulo: 'Conteúdo',
    conteudo: html`
      <h1>Cobertura do conteúdo</h1>
      <p class="nota">
        ${ctx.idx.conteudo.marcos.length} marcos · ${ctx.idx.conteudo.atividades.length} atividades
        · ${ctx.idx.conteudo.livros.length} livros. Para adicionar conteúdo, veja
        <code>app/content/README.md</code>.
      </p>
      ${
        erros.length
          ? html`<div class="alerta erro">
              <b>Erros</b>
              <ul>
                ${erros.map((e) => html`<li>${e}</li>`)}
              </ul>
            </div>`
          : ''
      }
      ${
        avisos.length
          ? html`<details class="cartao">
              <summary>${avisos.length} aviso(s)</summary>
              <ul>
                ${avisos.map((a) => html`<li>${a}</li>`)}
              </ul>
            </details>`
          : ''
      }
      ${dominios.map(
        (d) =>
          html`<section class="cartao">
            <h2>${d.icone} ${d.nome}</h2>
            <table class="tabela">
              <tr>
                <th>Linha</th>
                <th>Marcos</th>
                <th>Marcos com atividade</th>
              </tr>
              ${(d.linhas ?? []).map((l) => {
                const marcos = ctx.idx.marcosDaLinha(l.id);
                const comAtividade = marcos.filter(
                  (m) => ctx.idx.atividadesDoMarco(m.id).length > 0,
                ).length;
                return html`<tr class="${marcos.length === 0 ? 'vazia' : ''}">
                  <td>${l.nome}</td>
                  <td>${marcos.length}</td>
                  <td>${comAtividade}</td>
                </tr>`;
              })}
            </table>
          </section>`,
      )}
    `,
  };
};
