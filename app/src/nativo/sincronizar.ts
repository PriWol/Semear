// Junta o que está no aparelho (família, crianças, planos) com as notificações locais (ADR 0028).
import type { Contexto } from '../ui/app';
import { LEMBRETE_PADRAO, planejarLembretes } from '../domain/lembretes';
import type { Repositorio } from '../dados/repositorio';
import {
  ponteDoAparelho,
  sincronizarLembretes,
  type Ponte,
  type ResultadoSincronia,
} from './lembretes';

/**
 * "Apagar tudo" (#25): limpa o banco e cancela os lembretes já agendados, que podem mostrar o nome da
 * criança na tela bloqueada. Sincronizar com lista vazia cancela os pendentes e não agenda nenhum. Se a
 * ponte falhar, o banco já foi limpo, o erro não derruba a tela e o resultado vira 'lembretes-nao-cancelados'. No navegador (sem ponte) nada muda.
 */
export async function apagarTudoECancelarLembretes(
  repo: Pick<Repositorio, 'apagarTudo'>,
  ponte: Ponte | null = ponteDoAparelho(window as never),
): Promise<'ok' | 'lembretes-nao-cancelados'> {
  await repo.apagarTudo();
  try {
    await sincronizarLembretes(ponte, [], { pedirPermissao: false });
    return 'ok';
  } catch {
    // o apagar do banco já valeu; quem chama avisa a pessoa de que os lembretes podem seguir agendados
    return 'lembretes-nao-cancelados';
  }
}

export const AVISO_LEMBRETES_NAO_CANCELADOS =
  'Os dados foram apagados, mas não consegui cancelar os lembretes deste aparelho. Desligue o lembrete diário nas configurações do aparelho ou desinstale o app.';

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
