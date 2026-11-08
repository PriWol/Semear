import type { FabricaPagina } from '../ui/app';
import { html, textoRico } from '../ui/html';
import { formatarReferencia } from '../domain/orientacao';
import { carregarGuia } from '../conteudo';

/** Guia pedagógico das vertentes (#30): ajuda a escolher a principal e as inspirações. */
export const paginaGuia: FabricaPagina = async (ctx) => {
  const guia = carregarGuia();
  const emRevisao = guia.vertentes.some((v) => v.revisao?.estado === 'rascunho');
  const referencia = (id: string) => ctx.idx.referencia(id);

  return {
    titulo: 'Guia das vertentes',
    conteudo: html`
      <h1>Guia das vertentes</h1>
      <p class="nota">
        Cada vertente é um jeito de educar. Leia as cinco e escolha uma principal; as outras podem
        entrar como inspiração. <a href="#/familia">Voltar ao cadastro da família</a>
      </p>
      ${
        emRevisao
          ? html`<p class="alerta" role="note">
              Textos em revisão por educadoras de cada vertente. Use como ponto de partida.
            </p>`
          : ''
      }
      ${guia.vertentes.map(
        (s) => html`<section class="cartao" data-vertente="${s.vertente}">
          <h2>${s.vertente}</h2>
          <p><b>${textoRico(s.resumo)}</b></p>
          <h3>Princípios</h3>
          <ul>
            ${s.principios.map((p) => html`<li>${textoRico(p)}</li>`)}
          </ul>
          <h3>Como é uma sessão típica</h3>
          <p>${textoRico(s.sessaoTipica)}</p>
          <h3>Ritmo</h3>
          <p>${textoRico(s.ritmo)}</p>
          <h3>Marcos extras</h3>
          <p>${textoRico(s.marcosExtras)}</p>
          <h3>Tipo de atividade</h3>
          <p>${textoRico(s.atividades)}</p>
          ${
            s.referencias.length
              ? html`<h3>Para ler</h3>
                  <ul class="referencias">
                    ${s.referencias.map((id) => {
                      const r = referencia(id);
                      return r ? html`<li>${textoRico(formatarReferencia(r))}</li>` : '';
                    })}
                  </ul>`
              : ''
          }
        </section>`,
      )}
      <section class="cartao">
        <h2>${guia.combinar.titulo}</h2>
        <p>${textoRico(guia.combinar.texto)}</p>
        <ul>
          ${guia.combinar.exemplos.map((e) => html`<li>${textoRico(e)}</li>`)}
        </ul>
      </section>
    `,
  };
};
