import type { FabricaPagina } from '../ui/app';
import { lerFormulario, lista, novoId } from '../ui/app';
import { html, type HtmlSeguro } from '../ui/html';
import { icone } from '../ui/icones';
import { idadeEmAnos } from '../domain/datas';
import { criancaPadrao } from '../domain/criancas';
import { marcosVisiveis } from '../domain/conteudo';
import { IDIOMAS } from '../domain/tipos';
import { idPista, pistasDaCrianca, posicaoDaLinha } from '../domain/jornada';
import {
  atividadesRecentes,
  candidatas,
  complementares,
  PISTA_COMPLEMENTAR,
  DURACAO_PADRAO,
  DURACOES,
  montarSessaoDaProposta,
  proporSessao,
  proximaAlternativa,
  sugerirLivro,
  type Escolha,
  type PropostaSessao,
} from '../domain/sessao';

const textoContagem = (n: number) => `${n} ${n === 1 ? 'linha escolhida' : 'linhas escolhidas'}`;

export const paginaSessaoNova: FabricaPagina = async (ctx, params) => {
  const familia = await ctx.repo.familia();
  const criancas = await ctx.repo.criancas();
  if (!familia || criancas.length === 0) {
    return {
      titulo: 'Preparar sessão',
      conteudo: html`<p class="cartao">
        Cadastre a família e uma criança primeiro. <a href="#/">Início</a>
      </p>`,
    };
  }
  // Sem `?crianca=`: a da sessão mais recente (D19), não a mais velha da lista.
  const crianca =
    criancas.find((c) => c.id === params.crianca) ??
    criancaPadrao(criancas, await ctx.repo.sessoes())!;
  const agora = ctx.agora();
  const idade = idadeEmAnos(crianca.nascimento, new Date(agora));
  const estados = await ctx.repo.estados(crianca.id);
  const historico = await ctx.repo.sessoes(crianca.id);
  const pistasComAtivos = pistasDaCrianca(ctx.idx, familia, crianca)
    .map((p) => ({ p, pos: posicaoDaLinha(ctx.idx, p, estados, idade, familia.vertentePrincipal) }))
    .filter((x) => x.pos.ativos.length > 0);

  // Estado local da página: a proposta pode ser ajustada antes de gerar o pacote.
  let duracao: number = DURACAO_PADRAO;
  let foco: string[] | 'equilibrado' = 'equilibrado';
  let proposta: PropostaSessao | null = null;

  const recentes = atividadesRecentes(historico, crianca.id, agora);
  const alternativas = (e: Escolha): Escolha[] => {
    if (e.pista === PISTA_COMPLEMENTAR) return complementares(ctx.idx, familia, idade, recentes);
    const pista = pistasComAtivos.find((x) => idPista(x.p) === e.pista);
    if (!pista) return [];
    return candidatas(ctx.idx, pista.p, pista.pos.ativos, familia, idade, recentes).map((c) => ({
      ...c,
      pista: e.pista,
    }));
  };

  const vistaProposta = (p: PropostaSessao): HtmlSeguro =>
    html` <section class="cartao" id="proposta">
      <h2>Sugestão para ${crianca.nome} · ~${p.minutos} min</h2>
      ${p.avisos.map((a) => html`<p class="alerta">${a}</p>`)}
      ${
        p.escolhas.length === 0
          ? html`<p>Nenhuma atividade publicada para os marcos ativos escolhidos.</p>`
          : html`<ol class="escolhas">
              ${p.escolhas.map((e, i) => {
                const alts = alternativas(e).filter(
                  (a) => !p.escolhas.some((x) => x.atividade.id === a.atividade.id),
                );
                return html`<li>
                  <div>
                    <b>${e.atividade.titulo}</b>
                    <span class="nota">${e.atividade.duracaoMin} min</span>
                    <p class="nota">
                      ${
                        marcosVisiveis(ctx.idx, e.atividade).length
                          ? marcosVisiveis(ctx.idx, e.atividade)
                              .map((m) => ctx.idx.marco(m)?.titulo ?? '')
                              .join(' · ')
                          : e.atividade.marcos.length > 0
                            ? 'Atividade de apoio'
                            : `Complementar · ${e.atividade.categoria ?? ''}`
                      }
                      — ${e.motivos.join(', ')}
                    </p>
                  </div>
                  <div class="acoes">
                    ${alts.length ? html`<button class="botao" type="button" data-acao="trocar" data-i="${i}">Trocar</button>` : ''}
                    <button class="botao" type="button" data-acao="remover" data-i="${i}">
                      Remover
                    </button>
                  </div>
                </li>`;
              })}
            </ol>`
      }
      ${
        p.lacunas.length
          ? html`<details class="nota">
              <summary>${p.lacunas.length} linha(s) sem atividade para os marcos atuais</summary>
              <ul>
                ${p.lacunas.map(
                  (l) =>
                    html`<li>
                      ${l.nomeLinha}:
                      ${l.marcos.map((m) => ctx.idx.marco(m)?.titulo ?? m).join(', ')}
                    </li>`,
                )}
              </ul>
              <p>Isso é um sinal para a curadoria de conteúdo.</p>
            </details>`
          : ''
      }
      <p>
        ${icone('books')}
        <b>Livro:</b>
        ${p.livro ? `${p.livro.titulo}, de ${p.livro.autor}` : 'nenhum livro da curadoria para estes marcos'}
      </p>
      ${
        p.escolhas.length
          ? html`<button class="botao primario grande" type="button" data-acao="gerar">
              Gerar pacote
            </button>`
          : ''
      }
    </section>`;

  const vistaFormulario = (): HtmlSeguro =>
    html` <form class="cartao formulario" id="form-sessao">
      <label>
        Criança
        <select name="crianca">
          ${criancas.map((c) => html`<option value="${c.id}" ${c.id === crianca.id ? 'selected' : ''}>${c.nome}</option>`)}
        </select>
      </label>
      <fieldset>
        <legend>Duração</legend>
        <div class="linha-opcoes">
          ${DURACOES.map(
            (d) =>
              html`<label class="opcao"
                ><input
                  type="radio"
                  name="duracao"
                  value="${d}"
                  ${d === duracao ? 'checked' : ''}
                />
                ${d} min</label
              >`,
          )}
        </div>
      </fieldset>
      <fieldset>
        <legend>Foco</legend>
        <label class="opcao">
          <input
            type="radio"
            name="modo"
            value="equilibrado"
            ${foco === 'equilibrado' ? 'checked' : ''}
          />
          <span
            ><b>Equilibrado</b>
            <span class="nota"
              >O Semear escolhe por você: prioriza as linhas menos trabalhadas nas últimas 2
              semanas</span
            ></span
          >
        </label>
        <label class="opcao">
          <input
            type="radio"
            name="modo"
            value="escolher"
            ${foco !== 'equilibrado' ? 'checked' : ''}
          />
          <span
            ><b>Escolher linhas</b>
            <span class="nota" id="contagem-linhas" aria-live="polite"
              >${textoContagem(foco === 'equilibrado' ? 0 : foco.length)}</span
            ></span
          >
        </label>
        <!-- Só aparece em "Escolher linhas": ~30 caixas sempre abertas escondiam o botão principal (QA2-03). -->
        <div class="sublista" id="lista-linhas" ${foco === 'equilibrado' ? 'hidden' : ''}>
          ${
            pistasComAtivos.length
              ? pistasComAtivos.map(
                  ({ p, pos }) =>
                    html`<label class="opcao">
                      <input
                        type="checkbox"
                        name="foco"
                        value="${idPista(p)}"
                        ${foco !== 'equilibrado' && foco.includes(idPista(p)) ? 'checked' : ''}
                      />
                      <span
                        >${icone(p.dominio.icone)}
                        ${p.linha.nome}${p.idioma ? ` · ${IDIOMAS[p.idioma]}` : ''}
                        <span class="nota"
                          >${pos.ativos.map((m) => ctx.idx.marco(m)?.titulo ?? m).join(' · ')}</span
                        ></span
                      >
                    </label>`,
                )
              : html`<p class="nota">
                  ${crianca.nome} ainda não tem marcos ativos.
                  <a href="#/jornada/${crianca.id}">Posicionar na jornada</a>
                </p>`
          }
        </div>
      </fieldset>
      <button class="botao primario" type="submit">Sugerir atividades</button>
    </form>`;

  return {
    titulo: 'Preparar sessão',
    conteudo: html`<h1>Preparar sessão</h1>
      <div id="area-form">${vistaFormulario()}</div>
      <div id="area-proposta"></div>`,
    montar(raiz) {
      const areaProposta = raiz.querySelector<HTMLElement>('#area-proposta')!;
      let gerando = false;
      const mostrarProposta = () => {
        areaProposta.innerHTML = proposta ? vistaProposta(proposta).valor : '';
      };

      raiz
        .querySelector<HTMLSelectElement>('select[name=crianca]')
        ?.addEventListener('change', (ev) => {
          ctx.ir(`/sessao/nova?crianca=${(ev.target as HTMLSelectElement).value}`);
        });

      // A lista de linhas só aparece no modo "Escolher linhas", com a contagem do que foi marcado.
      const lista30 = raiz.querySelector<HTMLElement>('#lista-linhas');
      const contagemLinhas = raiz.querySelector<HTMLElement>('#contagem-linhas');
      const atualizarLinhas = () => {
        const escolher = raiz.querySelector<HTMLInputElement>('input[name=modo][value=escolher]');
        if (lista30) lista30.hidden = !escolher?.checked;
        const n = raiz.querySelectorAll('input[name=foco]:checked').length;
        if (contagemLinhas) contagemLinhas.textContent = textoContagem(n);
      };
      raiz
        .querySelectorAll<HTMLInputElement>('input[name=modo], input[name=foco]')
        .forEach((campo) => campo.addEventListener('change', atualizarLinhas));

      raiz.querySelector<HTMLFormElement>('#form-sessao')?.addEventListener('submit', (ev) => {
        ev.preventDefault();
        const d = lerFormulario(ev.currentTarget as HTMLFormElement);
        duracao = Number(d.duracao ?? DURACAO_PADRAO);
        foco = d.modo === 'escolher' ? lista(d.foco) : 'equilibrado';
        proposta = proporSessao(ctx.idx, {
          familia,
          crianca,
          idade,
          estados,
          historico,
          duracaoMin: duracao,
          foco,
          agora,
        });
        mostrarProposta();
        areaProposta.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });

      areaProposta.addEventListener('click', async (ev) => {
        const alvo = (ev.target as HTMLElement).closest<HTMLElement>('[data-acao]');
        if (!alvo || !proposta) return;
        const i = Number(alvo.dataset.i);
        const escolhas = [...proposta.escolhas];
        if (alvo.dataset.acao === 'remover') {
          escolhas.splice(i, 1);
        } else if (alvo.dataset.acao === 'trocar') {
          const atual = escolhas[i];
          if (!atual) return;
          const ocupadas = new Set(escolhas.map((x) => x.atividade.id));
          const proxima = proximaAlternativa(alternativas(atual), atual.atividade.id, ocupadas);
          if (proxima) escolhas[i] = proxima;
        } else if (alvo.dataset.acao === 'gerar') {
          // Evita duas sessões com o mesmo código num clique duplo.
          if (gerando) return;
          gerando = true;
          (alvo as HTMLButtonElement).disabled = true;
          const criadaEm = ctx.agora(); // a hora do clique, não a de quando a tela abriu
          const existentes = (await ctx.repo.sessoes()).map((s) => s.codigo);
          const sessao = montarSessaoDaProposta({
            id: novoId(),
            crianca,
            proposta,
            foco,
            agora: criadaEm,
            codigosExistentes: existentes,
          });
          await ctx.repo.salvarSessao(sessao);
          ctx.ir(`/sessao/${sessao.id}`);
          return;
        }
        proposta = {
          ...proposta,
          escolhas,
          minutos: escolhas.reduce((t, e) => t + e.atividade.duracaoMin, 0),
          livro: sugerirLivro(ctx.idx, escolhas, familia, idade),
        };
        mostrarProposta();
      });
    },
  };
};
