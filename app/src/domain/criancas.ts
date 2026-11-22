// Criança padrão das telas que precisam de uma só criança quando o endereço não diz qual (D19).
import type { Crianca, Sessao } from './tipos';

/**
 * A criança da sessão mais recente; sem nenhuma sessão de criança existente, a primeira da lista.
 * Derivada das sessões que já existem: nada novo é gravado (privacidade e formato do backup intactos).
 * `repo.criancas()` ordena pelo nascimento, então `criancas[0]` é a mais velha, e não a que a
 * família está usando agora.
 */
export function criancaPadrao<C extends Pick<Crianca, 'id'>>(
  criancas: C[],
  sessoes: Pick<Sessao, 'criancaId' | 'criadaEm'>[],
): C | null {
  const recente = [...sessoes]
    .sort((a, b) => b.criadaEm.localeCompare(a.criadaEm))
    .find((s) => criancas.some((c) => c.id === s.criancaId));
  return criancas.find((c) => c.id === recente?.criancaId) ?? criancas[0] ?? null;
}
