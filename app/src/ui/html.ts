// Montagem de HTML com escape automático: protege contra injeção de HTML (XSS).
// Todo texto vindo do usuário ou do conteúdo passa por aqui.

export class HtmlSeguro {
  constructor(readonly valor: string) {}
  toString(): string {
    return this.valor;
  }
}

const ESCAPES: Record<string, string> = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
};

export function escapar(texto: string): string {
  return texto.replace(/[&<>"']/g, (c) => ESCAPES[c]!);
}

type Valor = HtmlSeguro | string | number | boolean | null | undefined | Valor[];

function converter(v: Valor): string {
  if (v === null || v === undefined || v === false) return '';
  if (Array.isArray(v)) return v.map(converter).join('');
  if (v instanceof HtmlSeguro) return v.valor;
  return escapar(String(v));
}

/** Template de HTML: interpolações são escapadas, exceto as que já são HtmlSeguro. */
export function html(partes: TemplateStringsArray, ...valores: Valor[]): HtmlSeguro {
  let saida = partes[0]!;
  valores.forEach((v, i) => {
    saida += converter(v) + partes[i + 1]!;
  });
  return new HtmlSeguro(saida);
}

/** Marca um texto como HTML confiável. Use só com texto gerado pelo próprio código, nunca do usuário. */
export function confiavel(htmlPronto: string): HtmlSeguro {
  return new HtmlSeguro(htmlPronto);
}

/**
 * Formatação mínima para textos do conteúdo: **negrito** e *itálico*.
 * O texto é escapado antes, então o conteúdo não consegue injetar HTML.
 */
export function textoRico(texto: string): HtmlSeguro {
  const seguro = escapar(texto)
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\*(.+?)\*/g, '<i>$1</i>');
  return new HtmlSeguro(seguro);
}
