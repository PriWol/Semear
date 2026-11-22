// Painel em tela cheia que mostra um pacote (sessão ou semana) para imprimir ou usar no tablet (#139).
// Substitui o "abrir em nova aba": uma aba blob: herda a CSP do app (o script do pacote é bloqueado)
// e seria da origem do app, com acesso ao IndexedDB da família. Aqui o pacote fica no mesmo iframe
// isolado da prévia (public/previa.html, sandbox sem `allow-same-origin`), regra do ADR 0022:
// o pacote nunca roda na origem do app. O app só fala com ele por postMessage.
import { html } from './html';
import { icone } from './icones';

export interface OpcoesPainelPacote {
  /** nome acessível do painel e título da barra, ex.: "Sessão LUA-0301" */
  titulo: string;
  /** documento HTML completo do pacote, já gerado por `pacote/` */
  documento: string;
  /** botão que abriu o painel: recebe o foco de volta ao fechar */
  abridor?: HTMLElement | null;
}

/** Abre o painel e o remove do DOM ao fechar (Esc ou botão "Fechar"). Estilos em estilos.css. */
export function abrirPainelPacote(op: OpcoesPainelPacote): void {
  const dlg = document.createElement('dialog');
  dlg.className = 'painel-pacote';
  dlg.setAttribute('aria-label', op.titulo);
  dlg.innerHTML = html`<div class="painel-pacote-barra">
      <strong class="painel-pacote-titulo">${op.titulo}</strong>
      <button type="button" class="botao primario" data-acao="imprimir">
        ${icone('printer')} Imprimir
      </button>
      <button type="button" class="botao" data-acao="fechar">Fechar</button>
    </div>
    <iframe
      class="painel-pacote-quadro"
      title="${op.titulo}"
      sandbox="allow-scripts allow-modals"
      src="./previa.html"
    ></iframe>`.valor;

  const quadro = dlg.querySelector<HTMLIFrameElement>('iframe');
  // A página de prévia só aceita um documento, uma vez, vindo da janela-mãe.
  quadro?.addEventListener(
    'load',
    () => quadro.contentWindow?.postMessage({ tipo: 'semear:documento', html: op.documento }, '*'),
    { once: true },
  );
  // O app não chama print() no iframe (outra origem): pede por mensagem e o próprio pacote imprime.
  dlg.querySelector('[data-acao=imprimir]')?.addEventListener('click', () => {
    quadro?.contentWindow?.postMessage('semear:imprimir', '*');
  });
  dlg.querySelector('[data-acao=fechar]')?.addEventListener('click', () => dlg.close());
  // Com o foco dentro do iframe o Esc não chega ao <dialog>: o pacote avisa por mensagem.
  const aoReceber = (ev: MessageEvent) => {
    if (ev.source === quadro?.contentWindow && ev.data === 'semear:fechar') dlg.close();
  };
  window.addEventListener('message', aoReceber);
  dlg.addEventListener('close', () => {
    window.removeEventListener('message', aoReceber);
    dlg.remove();
    op.abridor?.focus({ preventScroll: true });
  });

  document.body.append(dlg);
  dlg.showModal();
  // Foco na barra (não no iframe): Esc e Tab funcionam logo que o painel abre.
  dlg.querySelector<HTMLElement>('[data-acao=imprimir]')?.focus();
}
