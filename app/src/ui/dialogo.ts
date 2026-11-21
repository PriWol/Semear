// Caixa de confirmação própria (<dialog> modal), no lugar de confirm()/alert() do navegador, que em cada
// celular aparece de um jeito e não oferece "guardar uma cópia primeiro". O navegador cuida do foco preso
// dentro da caixa, de devolver o foco a quem abriu e de fechar com Esc. Estilos em pages/ajustes.css.
import { html, type HtmlSeguro } from './html';

export interface BotaoDialogo {
  /** valor devolvido quando a pessoa escolhe este botão */
  valor: string;
  rotulo: string;
  tipo: 'primario' | 'perigo' | 'neutro';
  /** executa `aoEscolher` e deixa a caixa aberta (ex.: guardar uma cópia antes de apagar) */
  mantemAberto?: boolean;
  /** só habilita depois de a palavra de confirmação ser digitada */
  soComPalavra?: boolean;
}

export interface OpcoesDialogo {
  titulo: string;
  texto: HtmlSeguro;
  botoes: BotaoDialogo[];
  /** campo para digitar uma palavra (ex.: APAGAR) antes de liberar os botões `soComPalavra` */
  palavra?: { rotulo: string; valida: (digitado: string) => boolean };
  /** roda nos botões `mantemAberto`; o texto devolvido aparece na caixa */
  aoEscolher?: (valor: string) => Promise<string | void>;
}

export const DIALOGO_CANCELADO = 'cancelar';

let contador = 0;

/** Abre a caixa e devolve o `valor` do botão escolhido, ou `DIALOGO_CANCELADO` (Esc ou botão Cancelar). */
export function abrirDialogo(op: OpcoesDialogo): Promise<string> {
  const id = `dialogo-${++contador}`;
  const dlg = document.createElement('dialog');
  dlg.className = 'dialogo-aj';
  dlg.setAttribute('aria-labelledby', `${id}-titulo`);
  dlg.setAttribute('aria-describedby', `${id}-texto`);
  dlg.innerHTML = html`<div class="dialogo-aj-corpo">
    <h2 id="${id}-titulo">${op.titulo}</h2>
    <div id="${id}-texto" class="dialogo-aj-texto">${op.texto}</div>
    ${
      op.palavra
        ? html`<label class="dialogo-aj-campo" for="${id}-palavra"
          >${op.palavra.rotulo}
          <input
            id="${id}-palavra"
            type="text"
            autocomplete="off"
            autocapitalize="characters"
            spellcheck="false"
          />
        </label>`
        : ''
    }
    <p class="dialogo-aj-status nota" role="status"></p>
    <div class="dialogo-aj-acoes">
      ${op.botoes.map(
        (b) =>
          html`<button
            type="button"
            class="botao ${b.tipo === 'neutro' ? '' : b.tipo}"
            data-valor="${b.valor}"
            ${b.soComPalavra ? 'disabled' : ''}
          >
            ${b.rotulo}
          </button>`,
      )}
    </div>
  </div>`.valor;

  return new Promise<string>((resolver) => {
    const status = dlg.querySelector<HTMLElement>('.dialogo-aj-status');
    const campo = dlg.querySelector<HTMLInputElement>('input');
    const botoes = [...dlg.querySelectorAll<HTMLButtonElement>('button[data-valor]')];
    let resultado = DIALOGO_CANCELADO;

    const liberar = () => {
      const ok = !op.palavra || op.palavra.valida(campo?.value ?? '');
      op.botoes.forEach((b, i) => {
        if (b.soComPalavra && botoes[i]) botoes[i].disabled = !ok;
      });
    };
    campo?.addEventListener('input', liberar);

    op.botoes.forEach((b, i) => {
      botoes[i]?.addEventListener('click', async () => {
        if (!b.mantemAberto) {
          resultado = b.valor;
          dlg.close();
          return;
        }
        botoes[i]!.disabled = true;
        try {
          const msg = await op.aoEscolher?.(b.valor);
          if (status) status.textContent = msg ?? '';
        } finally {
          botoes[i]!.disabled = false;
        }
      });
    });

    dlg.addEventListener('close', () => {
      dlg.remove();
      resolver(resultado);
    });
    document.body.append(dlg);
    dlg.showModal();
    // Com campo de palavra o foco vai para ele; sem campo, para o primeiro botão.
    (campo ?? botoes[0])?.focus();
  });
}

/** Parágrafo simples (o html`` escapa o texto), para as caixas que só têm um parágrafo. */
export const paragrafo = (texto: string): HtmlSeguro => html`<p>${texto}</p>`;
