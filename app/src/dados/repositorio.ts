// Repositório: único ponto de acesso aos dados guardados no aparelho (ADR 0002).
import { openDB, type DBSchema, type IDBPDatabase } from 'idb';
import type { Crianca, EstadosCrianca, Familia, RegistroMarco, Sessao } from '../domain/tipos';

export const VERSAO_BACKUP = 1;

/** Linha do histórico de marcos: nada é apagado (especificação §4.2). */
export interface EventoMarco {
  criancaId: string;
  chave: string;
  registro: RegistroMarco;
}

export interface Backup {
  app: 'semear';
  versao: number;
  exportadoEm: string;
  familia: Familia | null;
  criancas: Crianca[];
  estados: { criancaId: string; estados: EstadosCrianca }[];
  historico: EventoMarco[];
  sessoes: Sessao[];
}

export interface Repositorio {
  familia(): Promise<Familia | null>;
  salvarFamilia(familia: Familia): Promise<void>;

  criancas(): Promise<Crianca[]>;
  crianca(id: string): Promise<Crianca | null>;
  salvarCrianca(crianca: Crianca): Promise<void>;
  /** remove a criança e tudo o que é dela (estados, histórico, sessões) */
  removerCrianca(id: string): Promise<void>;

  estados(criancaId: string): Promise<EstadosCrianca>;
  /** aplica mudanças nos estados e grava cada uma no histórico, numa única transação */
  atualizarEstados(criancaId: string, mudancas: Record<string, RegistroMarco>): Promise<void>;
  historico(criancaId: string): Promise<EventoMarco[]>;

  sessoes(criancaId?: string): Promise<Sessao[]>;
  sessao(id: string): Promise<Sessao | null>;
  salvarSessao(sessao: Sessao): Promise<void>;
  removerSessao(id: string): Promise<void>;

  exportar(agora: string): Promise<Backup>;
  /** substitui todos os dados pelos do backup */
  importar(backup: Backup): Promise<void>;
  apagarTudo(): Promise<void>;
}

interface Esquema extends DBSchema {
  config: { key: string; value: Familia };
  criancas: { key: string; value: Crianca };
  estados: { key: string; value: { criancaId: string; estados: EstadosCrianca } };
  historico: {
    key: number;
    value: EventoMarco;
    indexes: { porCrianca: string };
  };
  sessoes: { key: string; value: Sessao; indexes: { porCrianca: string } };
}

const LOJAS = ['config', 'criancas', 'estados', 'historico', 'sessoes'] as const;
const CHAVE_FAMILIA = 'familia';

export async function abrirRepositorio(nomeBanco = 'semear'): Promise<Repositorio> {
  const db = await openDB<Esquema>(nomeBanco, 1, {
    // Versão 1 do esquema. Toda mudança futura entra aqui como "if (antiga < N) { ... }", com teste.
    upgrade(banco, antiga) {
      if (antiga < 1) {
        banco.createObjectStore('config');
        banco.createObjectStore('criancas', { keyPath: 'id' });
        banco.createObjectStore('estados', { keyPath: 'criancaId' });
        banco
          .createObjectStore('historico', { autoIncrement: true })
          .createIndex('porCrianca', 'criancaId');
        banco.createObjectStore('sessoes', { keyPath: 'id' }).createIndex('porCrianca', 'criancaId');
      }
    },
  });
  return criarRepositorio(db);
}

function criarRepositorio(db: IDBPDatabase<Esquema>): Repositorio {
  const ordenarSessoes = (lista: Sessao[]) =>
    lista.sort((a, b) => b.criadaEm.localeCompare(a.criadaEm));

  return {
    async familia() {
      return (await db.get('config', CHAVE_FAMILIA)) ?? null;
    },
    async salvarFamilia(familia) {
      await db.put('config', familia, CHAVE_FAMILIA);
    },

    async criancas() {
      const lista = await db.getAll('criancas');
      return lista.sort((a, b) => a.nascimento.localeCompare(b.nascimento));
    },
    async crianca(id) {
      return (await db.get('criancas', id)) ?? null;
    },
    async salvarCrianca(crianca) {
      await db.put('criancas', crianca);
    },
    async removerCrianca(id) {
      const tx = db.transaction(['criancas', 'estados', 'historico', 'sessoes'], 'readwrite');
      await tx.objectStore('criancas').delete(id);
      await tx.objectStore('estados').delete(id);
      for (const loja of ['historico', 'sessoes'] as const) {
        let cursor = await tx.objectStore(loja).index('porCrianca').openCursor(id);
        while (cursor) {
          await cursor.delete();
          cursor = await cursor.continue();
        }
      }
      await tx.done;
    },

    async estados(criancaId) {
      return (await db.get('estados', criancaId))?.estados ?? {};
    },
    async atualizarEstados(criancaId, mudancas) {
      const tx = db.transaction(['estados', 'historico'], 'readwrite');
      const atual = (await tx.objectStore('estados').get(criancaId))?.estados ?? {};
      await tx.objectStore('estados').put({ criancaId, estados: { ...atual, ...mudancas } });
      for (const [chave, registro] of Object.entries(mudancas)) {
        await tx.objectStore('historico').add({ criancaId, chave, registro });
      }
      await tx.done;
    },
    async historico(criancaId) {
      return db.getAllFromIndex('historico', 'porCrianca', criancaId);
    },

    async sessoes(criancaId) {
      const lista = criancaId
        ? await db.getAllFromIndex('sessoes', 'porCrianca', criancaId)
        : await db.getAll('sessoes');
      return ordenarSessoes(lista);
    },
    async sessao(id) {
      return (await db.get('sessoes', id)) ?? null;
    },
    async salvarSessao(sessao) {
      await db.put('sessoes', sessao);
    },
    async removerSessao(id) {
      await db.delete('sessoes', id);
    },

    async exportar(agora) {
      return {
        app: 'semear',
        versao: VERSAO_BACKUP,
        exportadoEm: agora,
        familia: (await db.get('config', CHAVE_FAMILIA)) ?? null,
        criancas: await db.getAll('criancas'),
        estados: await db.getAll('estados'),
        historico: await db.getAll('historico'),
        sessoes: await db.getAll('sessoes'),
      };
    },
    async importar(backup) {
      validarBackup(backup);
      const tx = db.transaction(LOJAS, 'readwrite');
      await Promise.all(LOJAS.map((l) => tx.objectStore(l).clear()));
      if (backup.familia) await tx.objectStore('config').put(backup.familia, CHAVE_FAMILIA);
      for (const c of backup.criancas) await tx.objectStore('criancas').put(c);
      for (const e of backup.estados) await tx.objectStore('estados').put(e);
      for (const h of backup.historico) await tx.objectStore('historico').add(h);
      for (const s of backup.sessoes) await tx.objectStore('sessoes').put(s);
      await tx.done;
    },
    async apagarTudo() {
      const tx = db.transaction(LOJAS, 'readwrite');
      await Promise.all(LOJAS.map((l) => tx.objectStore(l).clear()));
      await tx.done;
    },
  };
}

/** Confere a forma do backup antes de apagar qualquer dado (um arquivo errado não pode zerar o app). */
export function validarBackup(dado: unknown): asserts dado is Backup {
  const b = dado as Partial<Backup> | null;
  const falha = (motivo: string): never => {
    throw new Error(`Arquivo de backup inválido: ${motivo}`);
  };
  if (!b || typeof b !== 'object') falha('não é um objeto');
  if (b!.app !== 'semear') falha('não é um backup do Semear');
  if (typeof b!.versao !== 'number' || b!.versao > VERSAO_BACKUP) {
    falha('versão desconhecida (atualize o app)');
  }
  for (const campo of ['criancas', 'estados', 'historico', 'sessoes'] as const) {
    if (!Array.isArray(b![campo])) falha(`campo "${campo}" ausente`);
  }
  for (const c of b!.criancas!) {
    if (typeof c?.id !== 'string' || typeof c?.nome !== 'string') falha('criança sem id ou nome');
  }
}
