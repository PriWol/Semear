import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { enderecoDoPdf, VOLUMES } from '../tesouro';

/** Biblioteca: abre os volumes d'O Grande Tesouro de Marina direto na unidade (ADR 0015). */
export const paginaBiblioteca: FabricaPagina = async () => ({
  titulo: 'Biblioteca',
  conteudo: html`<h1>Biblioteca</h1>
    <p class="nota">
      <i>O Grande Tesouro de Marina</i>: o material para imprimir ou ler na tela. Os volumes abrem
      neste mesmo site; é preciso estar conectado à internet, a não ser que o arquivo já tenha sido
      baixado neste aparelho.
    </p>
    ${VOLUMES.map(
      (v) =>
        html`<section class="cartao">
          <h2>Volume ${v.numero} · ${v.titulo}</h2>
          <p><a class="botao primario" href="${enderecoDoPdf(v)}" target="_blank" rel="noopener">Abrir o volume</a></p>
          <ul>
            ${v.unidades.map(
              (u) =>
                html`<li>
                  <a href="${enderecoDoPdf(v, u.paginas[0])}" target="_blank" rel="noopener"
                    >Unidade ${u.numero} · ${u.titulo}</a
                  >
                  <span class="nota">p. ${u.paginas[0]}–${u.paginas[1]}</span>
                </li>`,
            )}
          </ul>
        </section>`,
    )}`,
});
