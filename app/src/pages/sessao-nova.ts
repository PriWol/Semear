import type { FabricaPagina } from '../ui/app';
import { lerFormulario, lista, novoId } from '../ui/app';
import { html, type HtmlSeguro } from '../ui/html';
import { idadeEmAnos } from '../domain/datas';
import { IDIOMAS, type Sessao } from '../domain/tipos';
import { idPista, pistasDaCrianca, posicaoDaLinha } from '../domain/jornada';
import {
  atividadesRecentes,
  candidatas,
  DURACOES,
  gerarCodigoSessao,
  proporSessao,
  proximaAlternativa,
  sugerirLivro,
  type Escolha,
  type PropostaSessao,
} from '../domain/sessao';

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
  const crianca = criancas.find((c) => c.id === params.crianca) ?? criancas[0]!;
  const agora = ctx.agora();
  const idade = idadeEmAnos(crianca.nascimento, new Date(agora));
  const estados = await ctx.repo.estados(crianca.id);
  const historico = await ctx.repo.sessoes(crianca.id);
  const pistasComAtivos = pistasDaCrianca(ctx.idx, familia, crianca)
    .map((p) => ({ p, pos: posicaoDaLinha(ctx.idx, p, estados, idade, familia.vertentePrincipal) }))
    .filter((x) => x.pos.ativos.length > 0);

  // Estado local da página: a proposta pode ser ajustada antes de gerar o pacote.
  let duracao: number = 40;
  let foco: string[] | 'equilibrado' = 'equilibrado';
  let proposta: PropostaSessao | null = null;

  const recentes = atividadesRecentes(historico, crianca.id, agora);
  const alternativas = (e: Escolha): Escolha[] => {
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
                      ${e.atividade.marcos.map((m) => ctx.idx.marco(m)?.titulo ?? m).join(' · ')} —
                      ${e.motivos.join(', ')}
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
        📚
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
              >prioriza as linhas menos trabalhadas nas últimas 2 semanas</span
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
          <span><b>Escolher linhas</b></span>
        </label>
        <div class="sublista">
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
                        >${p.dominio.icone}
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

      // Marcar uma linha já escolhe o modo "Escolher linhas" (senão a escolha seria ignorada).
      raiz.querySelectorAll<HTMLInputElement>('input[name=foco]').forEach((caixa) =>
        caixa.addEventListener('change', () => {
          const escolher = raiz.querySelector<HTMLInputElement>('input[name=modo][value=escolher]');
          if (caixa.checked && escolher) escolher.checked = true;
        }),
      );

      raiz.querySelector<HTMLFormElement>('#form-sessao')?.addEventListener('submit', (ev) => {
        ev.preventDefault();
        const d = lerFormulario(ev.currentTarget as HTMLFormElement);
        duracao = Number(d.duracao ?? 40);
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
          const sessao: Sessao = {
            id: novoId(),
            codigo: gerarCodigoSessao(crianca.nome, new Date(criadaEm), existentes),
            criancaId: crianca.id,
            criadaEm,
            duracaoMin: proposta.minutos, // a duração real das atividades escolhidas
            foco,
            atividadeIds: proposta.escolhas.map((e) => e.atividade.id),
            livroId: proposta.livro?.id ?? null,
          };
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
