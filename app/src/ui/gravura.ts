import { gravura } from '../gravuras';
import { html, type HtmlSeguro } from './html';

interface Opcoes {
  /** Só a que fica abaixo da dobra carrega sob demanda; a de cima carrega logo (evita o piscar). */
  abaixoDaDobra?: boolean;
}

/**
 * Gravura botânica como ornamento (docs/DESIGN.md, ADR 0035). Falha fechada: id sem registro em
 * src/gravuras.ts não mostra nada. Usa `alt=""` de propósito: a imagem é só respiro visual, o sentido
 * da tela está no título ao lado, e um leitor de tela não ganha nada ao ouvi-la. O crédito completo fica
 * em Ajustes, em "Sobre o Semear". A variante escura (tinta clara) segue o aparelho pelo mesmo gatilho
 * do tema (prefers-color-scheme, ADR 0033). Os arquivos são locais: nenhuma chamada externa.
 */
export function figuraGravura(id: string, opcoes: Opcoes = {}): HtmlSeguro {
  const g = gravura(id);
  if (!g) return html``;
  return html`<picture class="gravura gravura-${g.id}">
    <source media="(prefers-color-scheme: dark)" srcset="gravuras/${g.arquivoEscuro}" />
    <img
      src="gravuras/${g.arquivoClaro}"
      alt=""
      width="${g.largura}"
      height="${g.altura}"
      decoding="async"
      ${opcoes.abaixoDaDobra ? html`loading="lazy"` : ''}
      data-gravura="${g.id}"
    />
  </picture>`;
}
