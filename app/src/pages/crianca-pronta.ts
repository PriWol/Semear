import { NaoEncontrado, type FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { figuraGravura } from '../ui/gravura';

/**
 * Depois de cadastrar uma criança (D21): uma tela curta com o próximo passo, em vez de cair numa jornada
 * de milhares de pixels. Os três caminhos levam a telas que já existem; nada é gravado aqui.
 */
export const paginaCriancaPronta: FabricaPagina = async (ctx, params) => {
  const crianca = params.id ? await ctx.repo.crianca(params.id) : null;
  if (!crianca) throw new NaoEncontrado('criança');

  return {
    titulo: `${crianca.nome} cadastrada`,
    conteudo: html`
      <section class="cartao proximo-passo" aria-labelledby="titulo-pronta">
        ${figuraGravura('gladiolo')}
        <h1 id="titulo-pronta">Pronto, ${crianca.nome} está cadastrada</h1>
        <p>O que você quer fazer agora?</p>
        <div class="proximo-passo-acoes">
          <a class="botao primario grande" href="#/sessao/nova?crianca=${crianca.id}"
            >Preparar a primeira sessão</a
          >
          <a class="botao" href="#/sondagem/${crianca.id}">Onde ${crianca.nome} está hoje (10 min)</a>
          <a class="botao" href="#/jornada/${crianca.id}">Ver jornada</a>
        </div>
        <p class="nota">
          A sondagem é uma conversa curta, sem pressa, para posicionar na jornada. Se preferir, você
          pode preparar a primeira sessão agora e posicionar depois.
        </p>
      </section>
    `,
  };
};
