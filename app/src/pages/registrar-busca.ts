import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { acharSessaoPorCodigo, sessaoRegistrada, ultimasSessoes } from '../domain/registro';
import { dataCurta, ROTULO_FEITA } from '../ui/rotulos';

/** Quantas sessões recentes a busca mostra como atalho. */
const ATALHOS = 6;

/**
 * Registrar sessão (#11), passo 1: a pessoa digita o código impresso na folha (ou escolhe uma das últimas
 * sessões) e segue para a ficha de registro. O código tolera maiúsculas, espaços e hífens (domain/registro).
 */
export const paginaRegistrarBusca: FabricaPagina = async (ctx, params) => {
  const todas = await ctx.repo.sessoes();
  const criancas = await ctx.repo.criancas();
  const nomeDe = (id: string) => criancas.find((c) => c.id === id)?.nome ?? '—';
  // "Registrar sessão" no cartão de uma criança mostra só as sessões dela; o código acha qualquer sessão.
  const doFiltro = params.crianca ? todas.filter((s) => s.criancaId === params.crianca) : todas;
  const recentes = ultimasSessoes(doFiltro.length > 0 ? doFiltro : todas, ATALHOS);

  if (todas.length === 0) {
    return {
      titulo: 'Registrar sessão',
      conteudo: html`
        <h1>Registrar sessão</h1>
        <section class="cartao reg-vazio">
          <p>Nenhuma sessão ainda. Prepare a primeira e ela aparece aqui.</p>
          <p><a class="botao primario" href="#/sessao/nova">Preparar sessão</a></p>
        </section>
      `,
    };
  }

  return {
    titulo: 'Registrar sessão',
    conteudo: html`
      <h1>Registrar sessão</h1>
      <p class="nota" id="ajuda-codigo">
        Digite o código impresso na folha da sessão, por exemplo S-1014-A1. Não importa se for
        maiúscula ou minúscula, nem os espaços.
      </p>
      <form class="reg-busca" id="form-busca" novalidate>
        <label for="codigo"><b>Código da sessão</b></label>
        <input
          class="reg-campo"
          id="codigo"
          name="codigo"
          type="text"
          autocapitalize="characters"
          autocomplete="off"
          spellcheck="false"
          aria-invalid="false"
          aria-describedby="ajuda-codigo erro-codigo"
        />
        <p class="reg-erro" id="erro-codigo" role="alert" hidden></p>
        <div><button class="botao primario" type="submit">Encontrar sessão</button></div>
      </form>

      <h2>Ou escolha uma das últimas sessões</h2>
      <ul class="reg-lista-sessoes">
        ${recentes.map((s) => {
          const titulos = s.atividadeIds.map((id) => ctx.idx.atividade(id)?.titulo ?? id);
          return html`<li>
            <a href="#/sessao/${s.id}/registrar">
              <span><b>${s.codigo}</b> · ${nomeDe(s.criancaId)} · ${dataCurta(s.criadaEm)}</span>
              <span class="nota">${titulos.join(' + ')}</span>
              ${
                sessaoRegistrada(s)
                  ? html`<span class="selo-feita">${ROTULO_FEITA}</span>`
                  : html`<span class="reg-pendente">Para registrar</span>`
              }
            </a>
          </li>`;
        })}
      </ul>
    `,
    montar(raiz) {
      const form = raiz.querySelector<HTMLFormElement>('#form-busca');
      const campo = raiz.querySelector<HTMLInputElement>('#codigo');
      const erro = raiz.querySelector<HTMLElement>('#erro-codigo');
      if (!form || !campo || !erro) return;

      const mostrarErro = (texto: string) => {
        // textContent: o que a pessoa digitou aparece como texto, nunca como HTML.
        erro.textContent = texto;
        erro.hidden = false;
        campo.setAttribute('aria-invalid', 'true');
        campo.focus();
      };
      campo.addEventListener('input', () => {
        erro.hidden = true;
        campo.setAttribute('aria-invalid', 'false');
      });
      form.addEventListener('submit', (ev) => {
        ev.preventDefault();
        const digitado = campo.value.trim();
        if (digitado === '') return mostrarErro('Digite o código da sessão.');
        const achada = acharSessaoPorCodigo(digitado, todas);
        if (!achada) {
          return mostrarErro(
            `Não achamos a sessão “${digitado}”. Confira o código impresso no alto da folha ou escolha uma sessão na lista abaixo.`,
          );
        }
        ctx.ir(`/sessao/${achada.id}/registrar`);
      });
    },
  };
};
