// Modelos das folhas da criança: cada tipo de folha do conteúdo vira uma página A4.
import type { Folha, ItemFigura } from '../domain/tipos';
import { html, type HtmlSeguro } from '../ui/html';

const CORES = [
  'var(--azul)',
  'var(--pessego)',
  'var(--amarelo)',
  'var(--verde-claro)',
  'var(--lilas)',
];
const cor = (i: number) => CORES[i % CORES.length]!;

function cabecalho(): HtmlSeguro {
  return html`<div class="cabecalho-crianca">
    <span>Nome: <span class="campo"></span></span><span>🌱</span>
  </div>`;
}

function figura(item: ItemFigura, i: number): HtmlSeguro {
  return html`<div class="item" style="--cor:${cor(i)}">
    <span class="emoji">${item.emoji}</span><span class="palavra">${item.texto}</span>
  </div>`;
}

/** Repete o emoji em fileiras (de 10 ou 5), para a criança contar com organização. */
function fileiras(emoji: string, quantidade: number, porFileira: number): HtmlSeguro {
  const linhas: HtmlSeguro[] = [];
  for (let i = 0; i < quantidade; i += porFileira) {
    const n = Math.min(porFileira, quantidade - i);
    linhas.push(
      html`<div class="fila">${Array.from({ length: n }, () => html`<span>${emoji}</span>`)}</div>`,
    );
  }
  return html`${linhas}`;
}

function quadroDez(preenchidos: number): HtmlSeguro {
  return html`<div class="dez">
    ${Array.from({ length: 10 }, (_, k) => html`<i class="${k < preenchidos ? 'on' : ''}"></i>`)}
  </div>`;
}

/** Dois quadros de dez: até 20. Os preenchidos enchem o primeiro antes do segundo. */
function doisQuadros(preenchidos: number, mini = false): HtmlSeguro {
  return html`<div class="dois-dez${mini ? ' mini' : ''}">
    ${quadroDez(Math.min(preenchidos, 10))}${quadroDez(Math.max(preenchidos - 10, 0))}
  </div>`;
}

function corpo(folha: Folha): HtmlSeguro {
  switch (folha.tipo) {
    case 'ligar':
      return html`${cabecalho()}
        <h2 class="titulo-crianca">${folha.titulo}</h2>
        <div class="ligar">
          <div class="col esq">${folha.esquerda.map(figura)}</div>
          <div class="col dir">${folha.direita.map((f, i) => figura(f, i + 2))}</div>
        </div>`;

    case 'marcar':
      return html`${cabecalho()}
        <h2 class="titulo-crianca">${folha.titulo}</h2>
        ${folha.grupos.map(
          (g, gi) =>
            html`<div class="modelo">
                <span class="emoji">${g.modelo.emoji}</span
                ><span class="silabas">${g.modelo.texto}</span>
              </div>
              <div class="grade">
                ${g.itens.map(
                  (it) =>
                    html`<div class="item" style="--cor:${cor(gi + 3)}">
                      <span class="emoji">${it.emoji}</span><span class="palavra">${it.texto}</span
                      ><span class="quadrado"></span>
                    </div>`,
                )}
              </div>`,
        )}`;

    case 'cartas':
      return html`<div class="cabecalho-crianca">
          <span>✂️ ${folha.titulo}</span><span>🌱</span>
        </div>
        <div class="cartas">
          ${folha.cartas.map((c, i) => {
            if ('numero' in c) {
              return html`<div class="carta" style="--cor:var(--amarelo)">
                <span class="num-carta">${c.numero}</span>
              </div>`;
            }
            if ('quadroDez' in c) {
              return html`<div class="carta" style="--cor:var(--azul)">
                ${doisQuadros(c.quadroDez, true)}
              </div>`;
            }
            return html`<div class="carta" style="--cor:${cor(i)}">
              <span class="emoji">${c.emoji}</span><span class="palavra">${c.texto}</span>
            </div>`;
          })}
        </div>`;

    case 'desenho':
      return html`${cabecalho()}
        <h2 class="titulo-crianca">${folha.titulo}</h2>
        <div class="moldura">
          <div class="pauta"><div></div></div>
        </div>
        ${folha.legenda ? html`<p class="dica" style="margin-top:3mm">${folha.legenda}</p>` : ''}`;

    case 'contar':
      return html`${cabecalho()}
        <h2 class="titulo-crianca">${folha.titulo}</h2>
        <div class="lista-conta">
          ${folha.itens.map(
            (it, i) =>
              html`<div class="conta" style="--cor:${cor(i + 1)}">
                <div class="cesto">${fileiras(it.emoji, it.quantidade, 10)}</div>
                <div class="opcoes">
                  ${it.opcoes.map((o) => html`<span class="num">${o}</span>`)}
                </div>
              </div>`,
          )}
        </div>`;

    case 'quadro-dez':
      return html`${cabecalho()}
        <h2 class="titulo-crianca">${folha.titulo}</h2>
        ${folha.dica ? html`<p class="dica">${folha.dica}</p>` : ''}
        <div class="lista-repr">
          ${folha.numeros.map(
            (n) =>
              html`<div class="representa">
                <div class="numero-grande">${n}</div>
                ${doisQuadros(0)}
              </div>`,
          )}
        </div>`;

    case 'comparar':
      return html`${cabecalho()}
        <h2 class="titulo-crianca">${folha.titulo}</h2>
        ${folha.dica ? html`<p class="dica">${folha.dica}</p>` : ''}
        <div class="lista-pares">
          ${folha.pares.map(
            (p) =>
              html`<div class="par">
                <div class="minicesto" style="--cor:var(--pessego)">
                  ${fileiras(p.a.emoji, p.a.quantidade, 5)}
                </div>
                <span class="ou">ou</span>
                <div class="minicesto" style="--cor:var(--azul)">
                  ${fileiras(p.b.emoji, p.b.quantidade, 5)}
                </div>
                <span class="iguais"><span class="quadrado"></span> iguais</span>
              </div>`,
          )}
        </div>`;
  }
}

export function paginaDaFolha(folha: Folha, rodape: string): HtmlSeguro {
  return html`<section class="pagina crianca">
    ${corpo(folha)}
    <div class="rodape"><span>${rodape}</span><span>Semear</span></div>
  </section>`;
}
