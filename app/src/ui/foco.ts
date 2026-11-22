// Foco de teclado depois de redesenhar a tela (QA2-02): a tela é refeita inteira, e o foco ia para o <body>.
// O botão novo é "o equivalente" do antigo: mesmo seletor. `preventScroll` para não brigar com a rolagem restaurada.

/** Aspas e barras do valor não podem quebrar o seletor. */
const valorCss = (v: string) => `"${v.replace(/["\\]/g, '\\$&')}"`;

/** Seletor de um elemento por atributos `data-*`, ex.: `seletorPorDados('button', { acao: 'estado' })`. */
export function seletorPorDados(tag: string, dados: Record<string, string | undefined>): string {
  return (
    tag +
    Object.entries(dados)
      .filter((par): par is [string, string] => par[1] !== undefined)
      .map(([k, v]) => `[data-${k}=${valorCss(v)}]`)
      .join('')
  );
}

/** Devolve o foco ao elemento equivalente depois do redesenho. Sem ele na tela, não faz nada. */
export function restaurarFoco(seletor: string): void {
  document.querySelector<HTMLElement>(seletor)?.focus({ preventScroll: true });
}
