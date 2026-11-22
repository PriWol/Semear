import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { figuraGravura } from '../ui/gravura';
import { CADERNOS, enderecoDoPdf, VOLUMES } from '../tesouro';
import type { CadernoTesouro, UnidadeTesouro, VolumeTesouro } from '../tesouro';

// Os cadernos trazem orientações sobre desenvolvimento ainda sem conferência profissional (ADR 0015,
// adendo; ADR 0021 e 0026): o aviso fica à vista, acima dos cartões e dentro de cada um.
const AVISO_SAUDE =
  'Os cadernos trazem orientações sobre a fase do “não”, atenção curta e desenvolvimento que ainda não foram conferidas por um profissional de saúde. Não substituem o pediatra; em caso de dúvida sobre fala, audição, comportamento ou desenvolvimento, converse com ele.';

interface DadosCartao {
  titulo: string;
  arquivo: { arquivo: string };
  botao: string;
  unidades: UnidadeTesouro[];
  aviso?: string;
  /** nível do título: cartões de volume são h2; os de caderno ficam sob o h2 da seção */
  nivel: 2 | 3;
}

/** Texto de "acompanha o Volume N"; só avisa "ainda não disponível" para um volume que não está no catálogo (ADR 0015, adendo). */
export function rotuloAcompanha(volume: number, existentes: readonly number[]): string {
  // Número que não é um volume possível (0, negativo, fracionário): sem rótulo, em vez de texto estranho.
  if (!Number.isInteger(volume) || volume < 1) return '';
  return existentes.includes(volume)
    ? `acompanha o Volume ${volume}`
    : `acompanha o Volume ${volume} (ainda não disponível no app)`;
}

function rotuloDoVolume(u: UnidadeTesouro) {
  const rotulo =
    u.volume === undefined
      ? ''
      : rotuloAcompanha(
          u.volume,
          VOLUMES.map((v) => v.numero),
        );
  return rotulo ? html`<span class="nota"> · ${rotulo}</span>` : '';
}

function cartao(c: DadosCartao) {
  return html`<section class="cartao">
    ${c.nivel === 2 ? html`<h2>${c.titulo}</h2>` : html`<h3>${c.titulo}</h3>`}
    ${c.aviso ? html`<p class="nota">${c.aviso}</p>` : ''}
    <p>
      <a class="botao primario" href="${enderecoDoPdf(c.arquivo)}" target="_blank" rel="noopener"
        >${c.botao}</a
      >
    </p>
    ${
      c.unidades.length === 0
        ? ''
        : html`<ul class="lista-unidades">
      ${c.unidades.map(
        (u) =>
          html`<li>
            <a href="${enderecoDoPdf(c.arquivo, u.paginas[0])}" target="_blank" rel="noopener"
              >Unidade ${u.numero} · ${u.titulo}</a
            >
            <span class="nota">p. ${u.paginas[0]}–${u.paginas[1]}</span>
            ${rotuloDoVolume(u)}
          </li>`,
      )}
    </ul>`
    }
  </section>`;
}

const doVolume = (v: VolumeTesouro): DadosCartao => ({
  titulo: `Volume ${v.numero} · ${v.titulo}`,
  arquivo: v,
  botao: 'Abrir o volume',
  unidades: v.unidades,
  nivel: 2,
});

/** Cartão de um caderno: título e aviso saem do próprio catálogo, sem tratar ids à parte. */
export function cartaoDoCaderno(c: CadernoTesouro) {
  return cartao({
    titulo: `${c.titulo} · ${c.subtitulo}`,
    arquivo: c,
    botao: 'Abrir o caderno',
    unidades: c.unidades,
    nivel: 3,
    aviso: c.aviso,
  });
}

/** Biblioteca: abre os volumes e cadernos d'O Grande Tesouro de Marina direto na unidade (ADR 0015). */
export const paginaBiblioteca: FabricaPagina = async () => ({
  titulo: 'Biblioteca',
  conteudo: html`<div class="topo-gravura">
      <h1>Biblioteca</h1>
      ${figuraGravura('tulipas')}
    </div>
    <p class="nota">
      <i>O Grande Tesouro de Marina</i>: o material para imprimir ou ler na tela. Os volumes e
      cadernos abrem neste mesmo site; é preciso estar conectado à internet, a não ser que o
      arquivo já tenha sido baixado neste aparelho.
    </p>
    ${VOLUMES.map((v) => cartao(doVolume(v)))}
    <h2>Cadernos para 2 anos</h2>
    <div class="alerta" role="note"><p>${AVISO_SAUDE}</p></div>
    ${CADERNOS.map(cartaoDoCaderno)}`,
});
