import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { CADERNOS, enderecoDoPdf, VOLUMES } from '../tesouro';
import type { CadernoTesouro, UnidadeTesouro, VolumeTesouro } from '../tesouro';

// Os cadernos trazem orientações sobre desenvolvimento ainda sem conferência profissional (ADR 0015,
// adendo; ADR 0021 e 0026): o aviso fica à vista, acima dos cartões e dentro de cada um.
const AVISO_SAUDE =
  'Os cadernos trazem orientações sobre a fase do “não”, atenção curta e desenvolvimento que ainda não foram conferidas por um profissional de saúde. Não substituem o pediatra; em caso de dúvida sobre fala, audição, comportamento ou desenvolvimento, converse com ele.';
const AVISO_INGLES =
  'Estas orientações ainda não foram conferidas por um profissional de saúde. Não substituem o pediatra; em caso de dúvida sobre fala, audição, comportamento ou desenvolvimento, converse com ele ou com uma fonoaudióloga que acompanhe crianças bilíngues.';
const AVISO_ATIVIDADES =
  'Estas orientações ainda não foram conferidas por um profissional de saúde. Não substituem o pediatra; em caso de dúvida sobre fala, audição, comportamento ou desenvolvimento, converse com ele.';

interface DadosCartao {
  titulo: string;
  arquivo: { arquivo: string };
  botao: string;
  unidades: UnidadeTesouro[];
  aviso?: string;
}

function cartao(c: DadosCartao) {
  return html`<section class="cartao">
    <h2>${c.titulo}</h2>
    ${c.aviso ? html`<p class="nota">${c.aviso}</p>` : ''}
    <p>
      <a class="botao primario" href="${enderecoDoPdf(c.arquivo)}" target="_blank" rel="noopener"
        >${c.botao}</a
      >
    </p>
    <ul>
      ${c.unidades.map(
        (u) =>
          html`<li>
            <a href="${enderecoDoPdf(c.arquivo, u.paginas[0])}" target="_blank" rel="noopener"
              >Unidade ${u.numero} · ${u.titulo}</a
            >
            <span class="nota">p. ${u.paginas[0]}–${u.paginas[1]}</span>
            ${u.volume ? html`<span class="nota"> · acompanha o Volume ${u.volume}</span>` : ''}
          </li>`,
      )}
    </ul>
  </section>`;
}

const doVolume = (v: VolumeTesouro): DadosCartao => ({
  titulo: `Volume ${v.numero} · ${v.titulo}`,
  arquivo: v,
  botao: 'Abrir o volume',
  unidades: v.unidades,
});

const doCaderno = (c: CadernoTesouro): DadosCartao => {
  const ingles = c.id === 'ingles-2-anos';
  return {
    titulo: `${ingles ? 'Caderno de inglês' : 'Caderno de atividades'} · ${c.subtitulo}`,
    arquivo: c,
    botao: 'Abrir o caderno',
    unidades: c.unidades,
    aviso: ingles ? AVISO_INGLES : AVISO_ATIVIDADES,
  };
};

/** Biblioteca: abre os volumes e cadernos d'O Grande Tesouro de Marina direto na unidade (ADR 0015). */
export const paginaBiblioteca: FabricaPagina = async () => ({
  titulo: 'Biblioteca',
  conteudo: html`<h1>Biblioteca</h1>
    <p class="nota">
      <i>O Grande Tesouro de Marina</i>: o material para imprimir ou ler na tela. Os volumes e
      cadernos abrem neste mesmo site; é preciso estar conectado à internet, a não ser que o
      arquivo já tenha sido baixado neste aparelho.
    </p>
    ${VOLUMES.map((v) => cartao(doVolume(v)))}
    <h2>Cadernos para 2 anos</h2>
    <p class="nota">${AVISO_SAUDE}</p>
    ${CADERNOS.map((c) => cartao(doCaderno(c)))}`,
});
