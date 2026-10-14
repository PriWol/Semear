// Família de exemplo (#39): a faixa que aparece em todas as telas e a saída segura do exemplo.
import type { Contexto } from './app';
import { html, type HtmlSeguro } from './html';

/** Mostra a faixa só enquanto a família do aparelho for a de exemplo. */
export async function atualizarFaixaExemplo(ctx: Contexto): Promise<void> {
  const faixa = document.getElementById('faixa-exemplo');
  if (!faixa) return;
  faixa.hidden = !(await ctx.repo.familia())?.exemplo;
}

export function ligarFaixaExemplo(ctx: Contexto): void {
  document
    .getElementById('apagar-exemplo')
    ?.addEventListener('click', () => void sairDoExemplo(ctx, '/'));
}

/**
 * Apaga o exemplo depois de confirmar. Só os registros do exemplo saem (repositório): o que a pessoa
 * cadastrou enquanto explorava continua no aparelho.
 */
export async function sairDoExemplo(ctx: Contexto, destino: string): Promise<void> {
  const ok = confirm(
    'Apagar o exemplo? Saem a família de exemplo, a Ana, o Theo e as sessões deles. ' +
      'O que você cadastrou continua neste aparelho.',
  );
  if (!ok) return;
  await ctx.repo.apagarExemplo();
  ctx.avisar('Exemplo apagado.');
  ctx.ir(destino);
}

/**
 * Aviso nas telas de cadastro enquanto o exemplo existir: quem vai cadastrar os próprios filhos
 * deve sair do exemplo antes, senão mistura dados reais com fictícios.
 */
export function avisoExemplo(): HtmlSeguro {
  return html`<div class="alerta" id="aviso-exemplo">
    <p>
      <b>Você está no exemplo.</b> Para cadastrar sua família de verdade, comece por aqui: o exemplo
      é apagado e o que você cadastrar fica só seu.
    </p>
    <button class="botao primario" type="button" id="comecar-real">
      Começar com a minha família
    </button>
  </div>`;
}

export function ligarAvisoExemplo(raiz: HTMLElement, ctx: Contexto): void {
  raiz
    .querySelector('#comecar-real')
    ?.addEventListener('click', () => void sairDoExemplo(ctx, '/familia'));
}
