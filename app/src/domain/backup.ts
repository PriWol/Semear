// Lembrete de backup (decisão 49): avisa quando passam mais de 30 dias sem backup.
import { diasEntre } from './datas';
import type { Crianca } from './tipos';

export const DIAS_LEMBRETE_BACKUP = 30;

/**
 * Só crianças de verdade pedem backup: a família de exemplo (#39) é fictícia e some com um toque.
 * Assim, uma criança cadastrada durante o exemplo já conta, sem depender de nenhuma data gravada.
 */
export function precisaLembreteBackup(
  criancas: Pick<Crianca, 'exemplo'>[],
  ultimoBackup: string | null,
  agora: string,
): boolean {
  if (!criancas.some((c) => !c.exemplo)) return false;
  return !ultimoBackup || diasEntre(ultimoBackup, agora) > DIAS_LEMBRETE_BACKUP;
}

export interface ResumoUltimaCopia {
  estado: 'nunca' | 'recente' | 'antiga';
  /** dias inteiros desde a última cópia; null quando nunca houve */
  dias: number | null;
  /** a tela de Ajustes destaca quando nunca houve cópia ou quando faz 30 dias ou mais */
  alerta: boolean;
}

/**
 * Estado da cópia de segurança para a tela de Ajustes. O alerta vale a partir de 30 dias (>=) e não
 * olha as crianças: é só informação, ao contrário do lembrete do Início (`precisaLembreteBackup`).
 * Data no futuro (o relógio do aparelho mudou) conta como hoje.
 */
export function resumoUltimaCopia(ultimoBackup: string | null, agora: string): ResumoUltimaCopia {
  if (!ultimoBackup) return { estado: 'nunca', dias: null, alerta: true };
  const futuro = new Date(ultimoBackup).getTime() > new Date(agora).getTime();
  const dias = futuro ? 0 : Math.floor(diasEntre(ultimoBackup, agora));
  const antiga = dias >= DIAS_LEMBRETE_BACKUP;
  return { estado: antiga ? 'antiga' : 'recente', dias, alerta: antiga };
}

/** 10 MB (D23): uma cópia real de 7 crianças e 35 sessões tem 22 KB, então há folga de centenas de vezes. */
export const TAMANHO_MAX_BACKUP_BYTES = 10 * 1024 * 1024;

export const MENSAGEM_ARQUIVO_GRANDE =
  'Este arquivo tem mais de 10 MB, bem maior que uma cópia do Semear (poucos KB). ' +
  'Escolha o arquivo certo. Nada foi alterado.';

/** Confere o tamanho ANTES de ler o arquivo: ler 60 MB de texto na memória já seria o problema. */
export function arquivoGrandeDemais(bytes: number): boolean {
  return bytes > TAMANHO_MAX_BACKUP_BYTES;
}

/** Limites folgados: nenhuma família real chega perto, mas um arquivo adulterado não passa. */
export const LIMITES_BACKUP = {
  criancas: 50,
  sessoes: 20_000,
  historico: 200_000,
  planos: 5_000,
  estados: 50,
  nome: 40, // igual ao maxlength do formulário da criança
  educador: 60, // igual ao do formulário da família
  texto: 200, // ids, códigos e chaves de marco
  atividadesPorSessao: 200,
  marcosPorCrianca: 5_000,
} as const;

interface FormaBackup {
  familia?: { educador: string } | null;
  criancas: { id: string; nome: string }[];
  estados: { criancaId: string; estados: object }[];
  historico: { criancaId: string; chave: string }[];
  sessoes: { id: string; codigo: string; criancaId: string; atividadeIds: string[] }[];
  planos?: { id: string; criancaId: string }[];
}

/** Só as contagens: roda antes de percorrer qualquer lista. */
export function problemaDeQuantidade(b: {
  criancas: unknown[];
  estados: unknown[];
  historico: unknown[];
  sessoes: unknown[];
  planos?: unknown[];
}): string | null {
  const L = LIMITES_BACKUP;
  if (b.criancas.length > L.criancas)
    return 'Arquivo de backup inválido: crianças demais para uma cópia do Semear.';
  if (b.estados.length > L.estados)
    return 'Arquivo de backup inválido: registros de estado demais.';
  if (b.sessoes.length > L.sessoes) return 'Arquivo de backup inválido: sessões demais.';
  if (b.historico.length > L.historico)
    return 'Arquivo de backup inválido: histórico grande demais.';
  if ((b.planos?.length ?? 0) > L.planos)
    return 'Arquivo de backup inválido: planos semanais demais.';
  return null;
}

/**
 * Regras de coerência da cópia (D23, QA1-04), já com a forma validada: família quando há crianças,
 * ids de criança únicos, toda `criancaId` apontando para uma criança do arquivo e limites por campo.
 * Devolve a mensagem em português, ou null se estiver tudo certo.
 */
export function problemaDeCoerencia(b: FormaBackup): string | null {
  const L = LIMITES_BACKUP;
  if (b.criancas.length > 0 && !b.familia) {
    return 'Este arquivo tem crianças, mas não tem a família. Não foi possível restaurar.';
  }
  if (b.familia && b.familia.educador.length > L.educador)
    return 'Arquivo de backup inválido: nome da família longo demais.';
  const ids = new Set<string>();
  for (const c of b.criancas) {
    if (c.nome.length > L.nome)
      return `Arquivo de backup inválido: nome longo demais (${c.nome.slice(0, 20)}…).`;
    if (c.id.length > L.texto)
      return 'Arquivo de backup inválido: identificador de criança longo demais.';
    if (ids.has(c.id)) return 'Arquivo de backup inválido: há crianças com id repetido.';
    ids.add(c.id);
  }
  const orfa = (lista: { criancaId: string }[], onde: string) =>
    lista.some((x) => !ids.has(x.criancaId))
      ? `${onde} de uma criança que não está no arquivo`
      : null;
  const orfao =
    orfa(b.estados, 'há estados') ??
    orfa(b.historico, 'há histórico') ??
    orfa(b.sessoes, 'há sessões') ??
    orfa(b.planos ?? [], 'há planos semanais');
  if (orfao) return `Arquivo de backup inválido: ${orfao}.`;
  for (const e of b.estados) {
    if (Object.keys(e.estados).length > L.marcosPorCrianca)
      return 'Arquivo de backup inválido: marcos demais numa criança.';
  }
  for (const h of b.historico) {
    if (h.chave.length > L.texto) return 'Arquivo de backup inválido: chave de marco longa demais.';
  }
  for (const s of b.sessoes) {
    if (s.id.length > L.texto || s.codigo.length > L.texto)
      return 'Arquivo de backup inválido: identificador de sessão longo demais.';
    if (s.atividadeIds.length > L.atividadesPorSessao)
      return 'Arquivo de backup inválido: atividades demais numa sessão.';
  }
  return null;
}
