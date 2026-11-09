// Junta o que está no aparelho (família, crianças, planos) com as notificações locais (ADR 0027).
import type { Contexto } from '../ui/app';
import { LEMBRETE_PADRAO, planejarLembretes } from '../domain/lembretes';
import { ponteDoAparelho, sincronizarLembretes, type ResultadoSincronia } from './lembretes';

/**
 * Reagenda os lembretes de hoje em diante. Roda na abertura do app e depois de mudar o plano ou a
 * preferência. Nunca lança erro: lembrete é um extra e não pode atrapalhar o uso do app.
 */
export async function sincronizarComOAparelho(
  ctx: Pick<Contexto, 'repo' | 'idx' | 'agora'>,
  opcoes: { pedirPermissao: boolean },
): Promise<ResultadoSincronia> {
  try {
    const ponte = ponteDoAparelho(window as never);
    if (!ponte) return 'indisponivel';
    const familia = await ctx.repo.familia();
    const preferencia = familia?.lembrete ?? LEMBRETE_PADRAO;
    const criancas = await ctx.repo.criancas();
    const itens = (
      await Promise.all(
        criancas.map(async (c) =>
          (await ctx.repo.planos(c.id)).map((plano) => ({
            plano,
            nomeDaCrianca: c.nome,
            tituloDaAtividade: (id: string) => ctx.idx.atividade(id)?.titulo,
          })),
        ),
      )
    ).flat();
    const lembretes = planejarLembretes(itens, preferencia, ctx.agora());
    return await sincronizarLembretes(ponte, lembretes, opcoes);
  } catch {
    return 'indisponivel';
  }
}
