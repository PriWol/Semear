import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { idadeEmAnos } from '../domain/datas';
import { ESTADOS, IDIOMAS, type EstadoMarco } from '../domain/tipos';
import {
  avisosTrilhas,
  idPista,
  pistasDaCrianca,
  posicaoDaLinha,
  posicionarAqui,
  type Pista,
} from '../domain/jornada';
import { anos, ICONE_ESTADO, NOME_ESTADO } from '../ui/rotulos';

export const paginaJornada: FabricaPagina = async (ctx, params) => {
  const familia = await ctx.repo.familia();
  const crianca = params.id ? await ctx.repo.crianca(params.id) : null;
  if (!familia || !crianca) throw new Error('Criança não encontrada.');
  const idade = idadeEmAnos(crianca.nascimento, new Date(ctx.agora()));
  const estados = await ctx.repo.estados(crianca.id);
  const pistas = pistasDaCrianca(ctx.idx, familia, crianca);
  const dominios = ctx.idx.conteudo.dominios.filter((d) => d.comJornada);
  const dominioAtual = dominios.find((d) => d.id === params.d) ?? dominios[0];
  const pistasDoDominio = pistas.filter((p) => p.dominio.id === dominioAtual?.id);
  const avisos = avisosTrilhas(ctx.idx, crianca, idade, estados);
  const porId = new Map(pistas.map((p) => [idPista(p), p]));

  const cartaoPista = (pista: Pista) => {
    const pos = posicaoDaLinha(ctx.idx, pista, estados, idade, familia.vertentePrincipal);
    const nome = pista.idioma ? `${pista.linha.nome} · ${IDIOMAS[pista.idioma]}` : pista.linha.nome;
    return html`<section class="cartao linha" id="linha-${idPista(pista)}">
      <header>
        <h2>${nome}</h2>
        ${pista.linha.vertentes ? html`<span class="etiqueta">extra ${pista.linha.vertentes.join('/')}</span>` : ''}
        ${pos.total ? html`<span class="nota">${pos.consolidados}/${pos.total} consolidados</span>` : ''}
      </header>
      ${
        pos.total === 0
          ? html`<p class="nota">📝 Conteúdo desta linha em breve.</p>`
          : html`<ol class="marcos">
              ${pos.marcos.map(
                (s) =>
                  html`<li
                    class="marco estado-${s.estado} ${s.fronteira ? 'fronteira' : ''}"
                    data-marco="${s.chave}"
                  >
                    <div class="marco-texto">
                      <b>${s.marco.titulo}</b>
                      ${s.ativo ? html`<span class="selo-ativo">trabalhando agora</span>` : ''}
                      <p class="nota">${s.marco.descricaoPais}</p>
                      ${
                        s.aguardando.length
                          ? html`<p class="aviso-marco">
                              ⏳ Aguardando:
                              ${s.aguardando
                                .map((id) => ctx.idx.marco(id)?.titulo ?? id)
                                .join(', ')}
                            </p>`
                          : ''
                      }
                      ${
                        s.avisoRitmo
                          ? html`<p class="aviso-marco">
                              🕰️ Na pedagogia ${familia.vertentePrincipal}, este marco costuma vir
                              por volta dos ${s.avisoRitmo} anos.
                            </p>`
                          : ''
                      }
                    </div>
                    <div class="estado" role="group" aria-label="Estado de ${s.marco.titulo}">
                      ${ESTADOS.map(
                        (e) =>
                          html`<button
                            type="button"
                            class="estado-botao ${s.estado === e ? 'marcado' : ''}"
                            aria-pressed="${s.estado === e}"
                            data-acao="estado"
                            data-chave="${s.chave}"
                            data-estado="${e}"
                            title="${NOME_ESTADO[e]}"
                          >
                            ${ICONE_ESTADO[e]}<span class="rotulo-estado">${NOME_ESTADO[e]}</span>
                          </button>`,
                      )}
                      <button
                        type="button"
                        class="link-discreto"
                        data-acao="posicionar"
                        data-pista="${idPista(pista)}"
                        data-marco="${s.marco.id}"
                      >
                        Está aqui
                      </button>
                    </div>
                  </li>`,
              )}
            </ol>`
      }
    </section>`;
  };

  return {
    titulo: `Jornada de ${crianca.nome}`,
    conteudo: html`
      <h1>Jornada de ${crianca.nome} <span class="nota">${anos(idade)}</span></h1>
      <p class="nota">
        Em cada linha, toque em <b>“Está aqui”</b> no marco em que ${crianca.nome} está: os
        anteriores viram consolidados. Depois ajuste marco a marco quando precisar.
      </p>
      <nav class="abas" aria-label="Domínios">
        ${dominios.map(
          (d) =>
            html`<a
              href="#/jornada/${crianca.id}?d=${d.id}"
              class="${d.id === dominioAtual?.id ? 'ativo' : ''}"
              aria-current="${d.id === dominioAtual?.id ? 'page' : 'false'}"
              >${d.icone} ${d.nome}</a
            >`,
        )}
      </nav>
      ${
        dominioAtual?.trilhas && avisos.length
          ? html`<div class="alerta">${avisos.map((a) => html`<p>${a}</p>`)}</div>`
          : ''
      }
      ${
        dominioAtual?.trilhas && crianca.trilhas.length === 0
          ? html`<p class="cartao nota">
              Nenhuma língua escolhida para ${crianca.nome}.
              <a href="#/crianca/${crianca.id}">Escolher línguas</a>
            </p>`
          : ''
      }
      ${pistasDoDominio.map(cartaoPista)}
      <p>
        <a class="botao primario" href="#/sessao/nova?crianca=${crianca.id}">Preparar sessão</a>
      </p>
    `,
    montar(raiz) {
      raiz.addEventListener('click', async (ev) => {
        const alvo = (ev.target as HTMLElement).closest<HTMLElement>('[data-acao]');
        if (!alvo) return;
        const agora = ctx.agora();
        if (alvo.dataset.acao === 'estado') {
          const chave = alvo.dataset.chave;
          if (!chave) return;
          await ctx.repo.atualizarEstados(crianca.id, {
            [chave]: {
              estado: alvo.dataset.estado as EstadoMarco,
              atualizadoEm: agora,
              origem: 'manual',
            },
          });
        } else if (alvo.dataset.acao === 'posicionar') {
          const pista = porId.get(alvo.dataset.pista ?? '');
          const marcoId = alvo.dataset.marco;
          if (!pista || !marcoId) return;
          await ctx.repo.atualizarEstados(
            crianca.id,
            posicionarAqui(ctx.idx, pista, marcoId, agora),
          );
          ctx.avisar('Posição atualizada.');
        }
        const y = window.scrollY;
        await ctx.atualizar();
        window.scrollTo(0, y);
      });
    },
  };
};
