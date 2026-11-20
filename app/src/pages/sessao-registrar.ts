import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import {
  montarRegistro,
  observacoesDaSessao,
  observacoesRegistradas,
  sessaoRegistrada,
  type EntradaRegistro,
} from '../domain/registro';
import { ANOTACOES_MAX, DURACAO_REAL_MAX, ENGAJAMENTOS, ESTADOS, IDIOMAS } from '../domain/tipos';
import { dataCurta, ICONE_ENGAJAMENTO, NOME_ENGAJAMENTO, NOME_ESTADO } from '../ui/rotulos';

const ERRO_AO_SALVAR = 'Não foi possível salvar. Seus dados continuam na tela. Tente de novo.';

/**
 * Registrar sessão (#11), passo 2: a ficha de registro no app. Grava a OBSERVAÇÃO de cada marco e os
 * detalhes da sessão; NÃO muda o estado do marco (§5.2): só o pai muda o estado, no mapa da jornada.
 */
export const paginaSessaoRegistrar: FabricaPagina = async (ctx, params) => {
  const sessao = params.id ? await ctx.repo.sessao(params.id) : null;
  const crianca = sessao ? await ctx.repo.crianca(sessao.criancaId) : null;
  if (!sessao || !crianca) throw new Error('Sessão não encontrada.');

  const ficha = observacoesDaSessao(sessao, ctx.idx);
  const anteriores = observacoesRegistradas(sessao.id, await ctx.repo.historico(crianca.id));
  const jaRegistrada = sessaoRegistrada(sessao);
  const titulos = sessao.atividadeIds.map((id) => ctx.idx.atividade(id)?.titulo ?? id);
  const plural = (n: number) => (n === 1 ? 'marco marcado' : 'marcos marcados');
  const contagem = (n: number) => `${n} de ${ficha.length} ${plural(ficha.length)}`;
  const marcados = ficha.filter((o) => anteriores[o.chave] !== undefined).length;

  return {
    titulo: `Registrar ${sessao.codigo}`,
    conteudo: html`
      <div class="reg-pagina">
        <div>
          <h1>Como foi a sessão?</h1>
          <p class="reg-contexto">
            ${sessao.codigo} · ${crianca.nome} · ${dataCurta(sessao.criadaEm)} ·
            ${titulos.join(' + ')}
          </p>
        </div>
        ${
          jaRegistrada
            ? html`<p class="reg-aviso" role="note">
                Esta sessão já foi registrada em
                ${dataCurta(sessao.registradaEm ?? sessao.criadaEm).slice(0, 5)}. Você pode
                corrigi-la.
              </p>`
            : ''
        }
        <form class="reg-form" id="form-registro" novalidate>
          ${
            ficha.length === 0
              ? html`<p class="nota">
                  Atividade complementar: não há marcos para registrar. Você ainda pode anotar como
                  foi.
                </p>`
              : ficha.map(
                  (o, i) => html`<fieldset class="reg-marco">
                    <legend>
                      <b>${o.marcoId}</b>${o.idioma ? ` · ${IDIOMAS[o.idioma]}` : ''}${o.revisao ? ' (revisão)' : ''}
                      <span class="reg-titulo">${ctx.idx.marco(o.marcoId)?.titulo ?? ''}</span>
                    </legend>
                    <div class="reg-opcoes">
                      ${ESTADOS.map(
                        (e) => html`<label class="reg-opcao">
                          <input
                            type="radio"
                            name="m${i}"
                            value="${e}"
                            ${anteriores[o.chave] === e ? 'checked' : ''}
                          />
                          <span class="reg-rotulo">${NOME_ESTADO[e]}</span>
                        </label>`,
                      )}
                    </div>
                  </fieldset>`,
                )
          }

          <section class="reg-detalhes" aria-labelledby="titulo-detalhes">
            <h2 id="titulo-detalhes">Detalhes (opcional)</h2>
            <div class="reg-campo-bloco">
              <label for="duracao">Duração real (minutos)</label>
              <input
                class="reg-campo"
                id="duracao"
                name="duracao"
                type="text"
                inputmode="numeric"
                autocomplete="off"
                maxlength="3"
                aria-describedby="ajuda-duracao"
                value="${sessao.duracaoReal ?? ''}"
              />
              <p class="reg-ajuda" id="ajuda-duracao">
                Planejado: ${sessao.duracaoMin} min. De 1 a ${DURACAO_REAL_MAX}.
              </p>
            </div>
            <fieldset class="reg-engajamento">
              <legend>Engajamento</legend>
              <div class="reg-opcoes">
                ${ENGAJAMENTOS.map(
                  (e) => html`<label class="reg-opcao">
                    <input
                      type="radio"
                      name="engajamento"
                      value="${e}"
                      ${sessao.engajamento === e ? 'checked' : ''}
                    />
                    <span class="reg-rotulo"
                      ><span aria-hidden="true">${ICONE_ENGAJAMENTO[e]}</span>
                      ${NOME_ENGAJAMENTO[e]}</span
                    >
                  </label>`,
                )}
              </div>
            </fieldset>
            <div class="reg-campo-bloco">
              <label for="anotacoes">Anotações (opcional)</label>
              <textarea
                class="reg-campo"
                id="anotacoes"
                name="anotacoes"
                rows="4"
                maxlength="${ANOTACOES_MAX}"
                aria-describedby="contador-anotacoes"
              >${sessao.anotacoes ?? ''}</textarea>
              <p class="reg-ajuda" id="contador-anotacoes">
                <span id="contagem-anotacoes">${(sessao.anotacoes ?? '').length}</span> de
                ${ANOTACOES_MAX}
              </p>
            </div>
          </section>

          <p class="reg-erro" id="erro-registro" role="alert" hidden></p>

          <div class="reg-acoes">
            ${
              ficha.length > 0
                ? html`<p class="reg-contador" id="contador-marcos" aria-live="polite">
                    ${contagem(marcados)}
                  </p>`
                : ''
            }
            <button class="botao primario" type="submit" id="salvar">
              ${jaRegistrada ? 'Salvar alterações' : 'Salvar registro'}
            </button>
            <a class="botao" href="#/">Cancelar</a>
          </div>
        </form>
      </div>
    `,
    montar(raiz) {
      const form = raiz.querySelector<HTMLFormElement>('#form-registro');
      const botao = raiz.querySelector<HTMLButtonElement>('#salvar');
      const erro = raiz.querySelector<HTMLElement>('#erro-registro');
      const contador = raiz.querySelector<HTMLElement>('#contador-marcos');
      const contagemAnotacoes = raiz.querySelector<HTMLElement>('#contagem-anotacoes');
      if (!form || !botao || !erro) return;
      const rotuloBotao = botao.textContent ?? '';
      let salvando = false;

      const mostrarErro = (texto: string) => {
        erro.textContent = texto;
        erro.hidden = false;
      };

      form.addEventListener('change', () => {
        erro.hidden = true;
        if (!contador) return;
        const n = ficha.filter((_, i) => form.querySelector(`input[name="m${i}"]:checked`)).length;
        contador.textContent = contagem(n);
      });
      form.addEventListener('input', (ev) => {
        if ((ev.target as HTMLElement).id === 'anotacoes' && contagemAnotacoes) {
          contagemAnotacoes.textContent = String((ev.target as HTMLTextAreaElement).value.length);
        }
      });

      form.addEventListener('submit', async (ev) => {
        ev.preventDefault();
        if (salvando) return; // um toque duplo não grava duas vezes
        const dados = new FormData(form);
        const entrada: EntradaRegistro = { estados: {} };
        ficha.forEach((o, i) => {
          const valor = dados.get(`m${i}`);
          if (typeof valor === 'string') entrada.estados[o.chave] = valor;
        });
        const duracao = String(dados.get('duracao') ?? '').trim();
        // Texto que não é só dígitos vira NaN, que o domínio recusa com a mensagem certa.
        if (duracao !== '') entrada.duracaoReal = /^\d+$/.test(duracao) ? Number(duracao) : NaN;
        const engajamento = dados.get('engajamento');
        if (typeof engajamento === 'string') entrada.engajamento = engajamento;
        entrada.anotacoes = String(dados.get('anotacoes') ?? '');

        let registro;
        try {
          registro = montarRegistro(sessao, ficha, entrada, ctx.agora(), anteriores);
        } catch (e) {
          mostrarErro(e instanceof Error ? e.message : ERRO_AO_SALVAR);
          return;
        }

        salvando = true;
        erro.hidden = true;
        botao.disabled = true;
        botao.setAttribute('aria-busy', 'true');
        botao.textContent = 'Salvando…';
        try {
          await ctx.repo.registrarSessao(registro.sessao, registro.eventos);
        } catch (e) {
          console.error(e);
          salvando = false;
          botao.disabled = false;
          botao.removeAttribute('aria-busy');
          botao.textContent = rotuloBotao;
          mostrarErro(ERRO_AO_SALVAR); // a tela fica como está: nada do que foi marcado se perde
          return;
        }
        ctx.avisar(`Sessão ${sessao.codigo} registrada.`);
        ctx.ir('/');
      });
    },
  };
};
