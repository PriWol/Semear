// Comparação de campos para gravar só o que mudou (QA1-03, ADR 0002): duas abas abertas não se desfazem.

/** Os campos de `depois` cujo valor difere do de `antes` (comparação por conteúdo, serve para listas). */
export function camposAlterados<T extends object>(antes: T, depois: T): Partial<T> {
  const mudados: Partial<T> = {};
  for (const chave of Object.keys(depois) as (keyof T)[]) {
    if (JSON.stringify(antes[chave]) !== JSON.stringify(depois[chave])) {
      mudados[chave] = depois[chave];
    }
  }
  return mudados;
}
