// Atividade para LER na tela, sem criar sessão (pedido da dona do produto; §5.7 mostra o mesmo conteúdo no pacote).
// Regra pura: decide o que aparece e em que ordem; a página só desenha.
import type { IndiceConteudo } from './conteudo';
import { marcosVisiveis, revisaVisivel } from './conteudo';
import type { Atividade, Vertente } from './tipos';

export interface MarcoLido {
  id: string;
  titulo: string;
}

export interface ToqueLido {
  vertente: Vertente;
  texto: string;
  principal: boolean;
}

export interface Leitura {
  /** cuidados vêm antes dos passos: quem lê precisa vê-los antes de começar */
  cuidados: string | null;
  marcos: MarcoLido[];
  revisao: MarcoLido[];
  toques: ToqueLido[];
}

/** Só atividades publicadas aparecem (a mesma regra da lista de Atividades). */
export function atividadePublicada(a: Atividade | undefined): a is Atividade {
  return a !== undefined && a.autoria.status === 'publicado';
}

/**
 * Marcos com título (nunca o id cru), cuidados e toques das vertentes da família. O toque da vertente
 * principal vem primeiro; vertente sem texto na atividade não aparece.
 */
export function leituraDaAtividade(
  a: Atividade,
  idx: Pick<IndiceConteudo, 'marco'>,
  vertentesDaFamilia: readonly Vertente[],
): Leitura {
  const comTitulo = (id: string): MarcoLido => ({ id, titulo: idx.marco(id)?.titulo ?? '' });
  const toques: ToqueLido[] = [];
  vertentesDaFamilia.forEach((v, i) => {
    const texto = a.toqueVertente?.[v]?.trim();
    if (texto && !toques.some((t) => t.vertente === v)) {
      toques.push({ vertente: v, texto, principal: i === 0 });
    }
  });
  return {
    cuidados: a.cuidados?.trim() || null,
    marcos: marcosVisiveis(idx, a).map(comTitulo),
    revisao: revisaVisivel(idx, a).map(comTitulo),
    toques,
  };
}
