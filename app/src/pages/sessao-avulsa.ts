// Criação da sessão avulsa de uma atividade (#13), usada pela lista e pela página da atividade.
import type { Contexto } from '../ui/app';
import { novoId } from '../ui/app';
import { gerarCodigoSessao } from '../domain/sessao';
import type { Atividade, Crianca, Sessao } from '../domain/tipos';

/** Salva a sessão avulsa (entra no histórico) e abre a prévia do pacote. */
export async function imprimirAtividadeAvulsa(
  ctx: Contexto,
  atividade: Atividade,
  crianca: Crianca,
): Promise<void> {
  const criadaEm = ctx.agora();
  const existentes = (await ctx.repo.sessoes()).map((s) => s.codigo);
  const sessao: Sessao = {
    id: novoId(),
    codigo: gerarCodigoSessao(crianca.nome, new Date(criadaEm), existentes),
    criancaId: crianca.id,
    criadaEm,
    duracaoMin: atividade.duracaoMin,
    foco: 'equilibrado',
    atividadeIds: [atividade.id],
    livroId: null,
    tipo: 'avulsa',
  };
  await ctx.repo.salvarSessao(sessao);
  ctx.ir(`/sessao/${sessao.id}`);
}
