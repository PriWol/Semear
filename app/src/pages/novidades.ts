import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { NOVIDADES } from '../novidades';
import { VERSAO } from '../versao';
import { numeroCurto } from '../ui/versao';

const dataBR = (iso: string) => iso.split('-').reverse().join('/');

export const paginaNovidades: FabricaPagina = async () => ({
  titulo: 'Novidades',
  conteudo: html`<h1>Novidades</h1>
    <p class="nota">Você está usando a versão ${numeroCurto(VERSAO.numero)}.</p>
    ${NOVIDADES.map(
      (n) =>
        html`<section class="cartao" data-versao="${n.versao}">
          <h2>${numeroCurto(n.versao)} · ${n.titulo}</h2>
          <p class="nota">${dataBR(n.data)}</p>
          <ul>
            ${n.itens.map((i) => html`<li>${i}</li>`)}
          </ul>
        </section>`,
    )}`,
});
