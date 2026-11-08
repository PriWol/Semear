// Busca de atividades (#13): roda inteira no aparelho. Função pura.
import { normalizar } from './acervo';
import type { Atividade, Vertente } from './tipos';

export interface FiltroAtividades {
  texto: string;
  dominio?: string;
  /** idade da criança: mantém atividades cuja faixa a inclui */
  idade?: number;
  vertente?: Vertente;
  /** duração máxima em minutos */
  duracaoMax?: number;
}

export interface ResultadoBusca {
  atividade: Atividade;
  pontos: number;
}

/** Domínio da atividade: o do marco principal (ex.: "LG.FON.04" → "LG") ou o campo das complementares. */
export function dominioDaAtividade(a: Atividade): string {
  return a.marcos[0] ? (a.marcos[0].split('.')[0] ?? '') : (a.dominio ?? '');
}

// Pesos por campo: o título vale mais que o objetivo, que vale mais que o resto.
const PESOS = { titulo: 5, palavrasChave: 4, marcos: 3, objetivo: 2 } as const;

function pontuar(a: Atividade, termos: string[]): number {
  const campos = {
    titulo: normalizar(a.titulo),
    palavrasChave: normalizar((a.palavrasChave ?? []).join(' ')),
    marcos: normalizar(a.marcos.join(' ')),
    objetivo: normalizar(a.objetivo),
  };
  let total = 0;
  for (const t of termos) {
    let achou = 0;
    for (const [campo, peso] of Object.entries(PESOS) as [keyof typeof PESOS, number][]) {
      if (campos[campo].includes(t)) achou = Math.max(achou, peso);
    }
    if (achou === 0) return 0; // todos os termos precisam aparecer
    total += achou;
  }
  return total;
}

/** Sem texto devolve tudo (já filtrado), em ordem de título; com texto, pela pontuação. */
export function buscarAtividades(todas: Atividade[], filtro: FiltroAtividades): ResultadoBusca[] {
  const termos = normalizar(filtro.texto).split(/\s+/).filter(Boolean);
  return todas
    .filter((a) => {
      if (filtro.dominio && dominioDaAtividade(a) !== filtro.dominio) return false;
      if (filtro.idade !== undefined && (filtro.idade < a.idade[0] || filtro.idade > a.idade[1]))
        return false;
      if (filtro.vertente && !a.vertentes.includes(filtro.vertente)) return false;
      if (filtro.duracaoMax !== undefined && a.duracaoMin > filtro.duracaoMax) return false;
      return true;
    })
    .map((atividade) => ({ atividade, pontos: termos.length ? pontuar(atividade, termos) : 1 }))
    .filter((r) => r.pontos > 0)
    .sort(
      (x, y) =>
        y.pontos - x.pontos || x.atividade.titulo.localeCompare(y.atividade.titulo, 'pt-BR'),
    );
}
