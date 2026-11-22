// Regra de idade do sugestor de sessões (§5.6; ADR 0036, etapa 2; decisão D4 da estória #138).
// A idade é um PESO graduado, não um filtro: a mesma atividade pode servir a várias idades (decisão de
// 21/11/2026), mas o app não oferece a uma criança de 2 anos uma atividade de 4 a 5, nem a uma de 8 uma de 2 a 3.
// Funções puras: a idade chega por parâmetro, em anos (pode ser fracionada, como em `idadeEmAnos`).
import type { Atividade } from './tipos';

/** Pontos de quem está dentro da faixa da atividade (§5.6, passo 3). */
export const PONTOS_DENTRO_DA_FAIXA = 2;
/**
 * Bônus máximo de proximidade ao centro da faixa. É só desempate: menor que qualquer outro critério
 * (vertente +3, novidade +2), para não virar regra.
 */
export const BONUS_PROXIMIDADE_MAX = 0.5;

/** Criança MAIS VELHA que a faixa: perde pontos por ano até `ANOS_PENALIDADE_GRADUADA`... */
export const PENALIDADE_POR_ANO_MAIS_VELHA = 2;
export const ANOS_PENALIDADE_GRADUADA = 2;
/** ...e, passado disso, uma penalidade fixa alta: só entra quando não há alternativa. */
export const PENALIDADE_MUITO_MAIS_VELHA = 6;

/** Atividade que COMEÇA acima da criança: perde pontos por ano de diferença... */
export const PENALIDADE_POR_ANO_ACIMA = 3;
/** ...e é EXCLUÍDA quando começa este número de anos ou mais acima (D4). */
export const ANOS_EXCLUSAO_ACIMA = 2;

/** Menores desta idade nunca recebem atividade cuja faixa começa aos 3 anos ou mais (D4, ADR 0021). */
export const IDADE_MENORES_PEQUENOS = 3;

/** Até este número de anos fora da faixa a atividade entra normalmente (com a penalidade e a nota do ajuste). */
export const TOLERANCIA_FORA_DA_FAIXA = 1;

export interface AdequacaoIdade {
  pontos: number;
  /** Exclusão dura: a atividade não pode ser sugerida a esta idade, nem sem alternativa. */
  excluida: boolean;
  /** Anos além da faixa (0 = dentro); vale para os dois lados. */
  anosFora: number;
  /** `acima`: a atividade começa depois da idade da criança; `abaixo`: a criança já passou da faixa. */
  lado: 'dentro' | 'acima' | 'abaixo';
  /** A atividade traz o `ajustes` que corresponde ao lado (`dificil` para menores, `facil` para maiores). */
  temAjuste: boolean;
  motivos: string[];
  /** Avisos curtos para a tela: "versão mais simples/mais exigente" (só com `ajustes`) e "pouco comum". */
  notas: string[];
}

/** Anos de diferença entre a idade e a faixa `[min, max]` da atividade, com o lado. */
function distanciaDaFaixa(faixa: [number, number], idade: number) {
  const [min, max] = faixa;
  if (idade < min) return { lado: 'acima' as const, anos: min - idade };
  if (idade > max) return { lado: 'abaixo' as const, anos: idade - max };
  return { lado: 'dentro' as const, anos: 0 };
}

/**
 * Quão bem a atividade serve a esta idade (D4). Regras:
 * - dentro da faixa: +2 e um pequeno bônus de proximidade ao centro;
 * - criança mais velha que o máximo: -2 por ano até 2 anos; passando disso, -6;
 * - atividade que começa acima da criança: -3 por ano; excluída quando começa 2 anos ou mais acima;
 * - menores de 3 anos: excluída qualquer atividade cuja faixa começa aos 3 ou mais, mesmo sem alternativa.
 * Que "mais de 1 ano fora só entra sem alternativa dentro da faixa" depende das outras candidatas da linha:
 * isso fica em `filtrarForaDaFaixa`.
 */
export function adequacaoDeIdade(atividade: Atividade, idade: number): AdequacaoIdade {
  const [min, max] = atividade.idade;
  const { lado, anos } = distanciaDaFaixa(atividade.idade, idade);
  const motivos: string[] = [];
  const notas: string[] = [];

  if (lado === 'dentro') {
    const meia = Math.max((max - min) / 2, 0.5);
    const proximidade = 1 - Math.min(1, Math.abs(idade - (min + max) / 2) / meia);
    motivos.push('idade adequada');
    return {
      pontos: PONTOS_DENTRO_DA_FAIXA + BONUS_PROXIMIDADE_MAX * proximidade,
      excluida: false,
      anosFora: 0,
      lado,
      temAjuste: false,
      motivos,
      notas,
    };
  }

  const ajuste = lado === 'acima' ? atividade.ajustes?.dificil : atividade.ajustes?.facil;
  const versao = lado === 'acima' ? 'Versão mais simples' : 'Versão mais exigente';
  // Até 1 ano fora COM o ajuste: basta a nota da versão. Sem o ajuste, ou mais longe, avisa que é pouco comum.
  if (anos > TOLERANCIA_FORA_DA_FAIXA || !ajuste) {
    notas.push(
      lado === 'acima'
        ? `Pouco comum para esta idade: a atividade começa aos ${min} anos.`
        : `Pouco comum para esta idade: a atividade vai até os ${max} anos.`,
    );
  }
  if (ajuste) notas.push(`${versao}: ${ajuste}`);

  if (lado === 'acima') {
    const pequenaDemais = idade < IDADE_MENORES_PEQUENOS && min >= IDADE_MENORES_PEQUENOS;
    return {
      pontos: -PENALIDADE_POR_ANO_ACIMA * anos,
      excluida: pequenaDemais || anos >= ANOS_EXCLUSAO_ACIMA,
      anosFora: anos,
      lado,
      temAjuste: Boolean(ajuste),
      motivos,
      notas,
    };
  }
  const penalidade =
    anos <= ANOS_PENALIDADE_GRADUADA
      ? PENALIDADE_POR_ANO_MAIS_VELHA * anos
      : PENALIDADE_MUITO_MAIS_VELHA;
  return {
    pontos: -penalidade,
    excluida: false,
    anosFora: anos,
    lado,
    temAjuste: Boolean(ajuste),
    motivos,
    notas,
  };
}

/**
 * Entre as candidatas de uma linha, fora da faixa só entra se não houver alternativa dentro dela (D4): mais de
 * 1 ano fora, nunca havendo alternativa; até 1 ano fora, só com o `ajustes` do lado certo (regra do Curador,
 * que é o que dá o "versão mais simples/mais exigente"). Recebe só as não excluídas, devolve a lista final.
 */
export function filtrarForaDaFaixa<T extends { adequacao: AdequacaoIdade }>(candidatas: T[]): T[] {
  const temDentro = candidatas.some((c) => c.adequacao.lado === 'dentro');
  if (!temDentro) return candidatas;
  return candidatas.filter(
    (c) =>
      c.adequacao.lado === 'dentro' ||
      (c.adequacao.anosFora <= TOLERANCIA_FORA_DA_FAIXA && c.adequacao.temAjuste),
  );
}
