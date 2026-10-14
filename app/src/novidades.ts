// "Novidades" (#38): o que mudou em cada versão, em linguagem simples. Conteúdo em content/novidades.json.
import novidadesJson from '../content/novidades.json';

export interface Novidade {
  versao: string;
  /** AAAA-MM-DD */
  data: string;
  titulo: string;
  itens: string[];
}

/** Valida a forma do arquivo: um erro aqui quebra o teste, nunca a tela. */
export function validarNovidades(dado: unknown): Novidade[] {
  const lista = (dado as { versoes?: unknown } | null)?.versoes;
  if (!Array.isArray(lista) || lista.length === 0) throw new Error('novidades: lista vazia');
  for (const v of lista as Record<string, unknown>[]) {
    const ok =
      typeof v.versao === 'string' &&
      /^\d+\.\d+\.\d+$/.test(v.versao) &&
      typeof v.data === 'string' &&
      /^\d{4}-\d{2}-\d{2}$/.test(v.data) &&
      typeof v.titulo === 'string' &&
      Array.isArray(v.itens) &&
      v.itens.length > 0 &&
      v.itens.every((i) => typeof i === 'string' && i.trim() !== '');
    if (!ok) throw new Error(`novidades: versão ${String(v.versao)} incompleta`);
  }
  return lista as Novidade[];
}

export const NOVIDADES: Novidade[] = validarNovidades(novidadesJson);
