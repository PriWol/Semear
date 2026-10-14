// Repositório: único ponto de acesso aos dados guardados no aparelho (ADR 0002).
import { openDB, type DBSchema, type IDBPDatabase } from 'idb';
import {
  ESTADOS,
  IDIOMAS,
  VERTENTES,
  type Crianca,
  type EstadosCrianca,
  type Familia,
  type RegistroMarco,
  type Sessao,
} from '../domain/tipos';
import { ehLetra } from '../domain/letra';
import type { DadosExemplo } from '../domain/exemplo';

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

  /** data do último backup exportado (para o lembrete mensal) */
  ultimoBackup(): Promise<string | null>;
  marcarBackup(agora: string): Promise<void>;

  exportar(agora: string): Promise<Backup>;
  /** substitui todos os dados pelos do backup */
  importar(backup: Backup): Promise<void>;
  apagarTudo(): Promise<void>;

  /** grava a família de exemplo (#39); recusa se já existe uma família no aparelho */
  carregarExemplo(dados: DadosExemplo, agora: string): Promise<void>;
  /**
   * remove SÓ os registros marcados como exemplo: o que a pessoa cadastrou continua no aparelho.
   * Se ela cadastrou crianças, a família é mantida (sem o marcador) para elas não ficarem órfãs.
   */
  apagarExemplo(): Promise<void>;
}

interface Esquema extends DBSchema {
  config: { key: string; value: Familia | { em: string } };
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
const CHAVE_BACKUP = 'ultimoBackup';

const lerFamilia = (v: Familia | { em: string } | undefined): Familia | null =>
  v && 'educador' in v ? v : null;

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
        banco
          .createObjectStore('sessoes', { keyPath: 'id' })
          .createIndex('porCrianca', 'criancaId');
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
      return lerFamilia(await db.get('config', CHAVE_FAMILIA));
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

    async ultimoBackup() {
      const v = await db.get('config', CHAVE_BACKUP);
      return v && 'em' in v ? v.em : null;
    },
    async marcarBackup(agora) {
      await db.put('config', { em: agora }, CHAVE_BACKUP);
    },

    async exportar(agora) {
      return {
        app: 'semear',
        versao: VERSAO_BACKUP,
        exportadoEm: agora,
        familia: lerFamilia(await db.get('config', CHAVE_FAMILIA)),
        criancas: await db.getAll('criancas'),
        estados: await db.getAll('estados'),
        historico: await db.getAll('historico'),
        sessoes: await db.getAll('sessoes'),
      };
    },
    async importar(backup) {
      validarBackup(backup);
      const tx = db.transaction(LOJAS, 'readwrite');
      try {
        // Mantém a data do último backup (está em config): só a família é substituída.
        await tx.objectStore('config').delete(CHAVE_FAMILIA);
        await Promise.all(
          LOJAS.filter((l) => l !== 'config').map((l) => tx.objectStore(l).clear()),
        );
        if (backup.familia) await tx.objectStore('config').put(backup.familia, CHAVE_FAMILIA);
        for (const c of backup.criancas) await tx.objectStore('criancas').put(c);
        for (const e of backup.estados) await tx.objectStore('estados').put(e);
        for (const h of backup.historico) await tx.objectStore('historico').add(h);
        for (const s of backup.sessoes) await tx.objectStore('sessoes').put(s);
        await tx.done;
      } catch (erro) {
        // Um erro de gravação não desfaz a transação sozinho: sem isto, as lojas já limpas seriam gravadas
        // e a família perderia tudo.
        try {
          tx.abort();
        } catch {
          // a transação já terminou (abortada pelo próprio navegador)
        }
        throw erro;
      }
    },
    async apagarTudo() {
      const tx = db.transaction(LOJAS, 'readwrite');
      await Promise.all(LOJAS.map((l) => tx.objectStore(l).clear()));
      await tx.done;
    },

    async carregarExemplo(dados, agora) {
      const tx = db.transaction(LOJAS, 'readwrite');
      // A checagem fica dentro da transação: dois toques seguidos não gravam o exemplo duas vezes.
      if (lerFamilia(await tx.objectStore('config').get(CHAVE_FAMILIA))) {
        tx.done.catch(() => undefined); // o abort abaixo rejeita tx.done de propósito
        tx.abort();
        throw new Error('Já existe uma família neste aparelho: o exemplo não foi carregado.');
      }
      await tx.objectStore('config').put(dados.familia, CHAVE_FAMILIA);
      for (const c of dados.criancas) await tx.objectStore('criancas').put(c);
      for (const e of dados.estados) {
        await tx.objectStore('estados').put(e);
        for (const [chave, registro] of Object.entries(e.estados)) {
          await tx.objectStore('historico').add({ criancaId: e.criancaId, chave, registro });
        }
      }
      for (const s of dados.sessoes) await tx.objectStore('sessoes').put(s);
      // O exemplo não é dado da família: não deve disparar o lembrete de backup.
      await tx.objectStore('config').put({ em: agora }, CHAVE_BACKUP);
      await tx.done;
    },

    async apagarExemplo() {
      const tx = db.transaction(LOJAS, 'readwrite');
      // Nunca clear(): uma criança real cadastrada durante o exemplo não tem o marcador e fica.
      const doExemplo = (await tx.objectStore('criancas').getAll()).filter((c) => c.exemplo);
      for (const c of doExemplo) {
        await tx.objectStore('criancas').delete(c.id);
        await tx.objectStore('estados').delete(c.id);
        for (const loja of ['historico', 'sessoes'] as const) {
          let cursor = await tx.objectStore(loja).index('porCrianca').openCursor(c.id);
          while (cursor) {
            await cursor.delete();
            cursor = await cursor.continue();
          }
        }
      }
      let cursor = await tx.objectStore('sessoes').openCursor();
      while (cursor) {
        if (cursor.value.exemplo) await cursor.delete();
        cursor = await cursor.continue();
      }
      const familia = lerFamilia(await tx.objectStore('config').get(CHAVE_FAMILIA));
      if (familia?.exemplo) {
        // Sobrou criança que a pessoa cadastrou? Então a família passa a ser dela: apagar a família
        // deixaria essas crianças órfãs (invisíveis na tela). Ela fica, sem o marcador.
        const restaram = (await tx.objectStore('criancas').count()) > 0;
        if (restaram) {
          const real: Familia = { ...familia };
          delete real.exemplo;
          await tx.objectStore('config').put(real, CHAVE_FAMILIA);
        } else {
          await tx.objectStore('config').delete(CHAVE_FAMILIA);
        }
        // O backup "de mentira" do exemplo sai nos dois casos: o lembrete de backup volta a valer.
        await tx.objectStore('config').delete(CHAVE_BACKUP);
      }
      await tx.done;
    },
  };
}

/**
 * Confere a forma completa do backup ANTES de apagar qualquer dado: um arquivo errado (ou adulterado)
 * não pode zerar o app nem levar valores inesperados para as telas e o pacote.
 */
export function validarBackup(dado: unknown): asserts dado is Backup {
  const falha = (motivo: string): never => {
    throw new Error(`Arquivo de backup inválido: ${motivo}`);
  };
  const ehObjeto = (v: unknown): v is Record<string, unknown> =>
    typeof v === 'object' && v !== null && !Array.isArray(v);
  const ehTexto = (v: unknown): v is string => typeof v === 'string';
  const listaDe = (v: unknown, valido: (x: unknown) => boolean) =>
    Array.isArray(v) && v.every(valido);
  const ehVertente = (v: unknown) => (VERTENTES as readonly unknown[]).includes(v);
  const ehIdioma = (v: unknown) => ehTexto(v) && Object.hasOwn(IDIOMAS, v);
  const ehData = (v: unknown) => ehTexto(v) && /^\d{4}-\d{2}-\d{2}$/.test(v);
  // O marcador do exemplo só pode faltar ou ser true (#39).
  const marcadorOk = (v: Record<string, unknown>) => v.exemplo === undefined || v.exemplo === true;
  const ehRegistro = (v: unknown) =>
    ehObjeto(v) &&
    (ESTADOS as readonly unknown[]).includes(v.estado) &&
    ehTexto(v.atualizadoEm) &&
    ['manual', 'posicionamento', 'sessao', 'sondagem'].includes(v.origem as string);

  if (!ehObjeto(dado)) return falha('não é um objeto');
  const b = dado;
  if (b.app !== 'semear') falha('não é um backup do Semear');
  if (typeof b.versao !== 'number' || b.versao > VERSAO_BACKUP)
    falha('versão desconhecida (atualize o app)');
  for (const campo of ['criancas', 'estados', 'historico', 'sessoes']) {
    if (!Array.isArray(b[campo])) falha(`campo "${campo}" ausente`);
  }

  const f = b.familia;
  if (f !== null && f !== undefined) {
    if (
      !ehObjeto(f) ||
      !ehTexto(f.educador) ||
      !ehVertente(f.vertentePrincipal) ||
      !listaDe(f.inspiracoes, ehVertente) ||
      !listaDe(f.idiomasEducador, ehIdioma) ||
      !ehTexto(f.criadaEm) ||
      !marcadorOk(f)
    ) {
      falha('dados da família incompletos ou desconhecidos');
    }
  }
  for (const c of b.criancas as unknown[]) {
    if (!ehObjeto(c) || !ehTexto(c.id) || !ehTexto(c.nome)) falha('criança sem id ou nome');
    const cr = c as Record<string, unknown>;
    if (!ehData(cr.nascimento)) falha(`data de nascimento inválida (${String(cr.nome)})`);
    if (cr.letra !== null && !ehLetra(cr.letra)) falha(`letra desconhecida (${String(cr.nome)})`);
    if (!listaDe(cr.trilhas, ehIdioma)) falha(`línguas desconhecidas (${String(cr.nome)})`);
    if (!marcadorOk(cr)) falha(`marcador de exemplo inválido (${String(cr.nome)})`);
  }
  for (const e of b.estados as unknown[]) {
    if (!ehObjeto(e) || !ehTexto(e.criancaId) || !ehObjeto(e.estados)) falha('estado sem criança');
    if (!Object.values((e as { estados: object }).estados).every(ehRegistro)) {
      falha('estado de marco desconhecido');
    }
  }
  for (const h of b.historico as unknown[]) {
    if (!ehObjeto(h) || !ehTexto(h.criancaId) || !ehTexto(h.chave) || !ehRegistro(h.registro)) {
      falha('histórico inválido');
    }
  }
  for (const s of b.sessoes as unknown[]) {
    if (
      !ehObjeto(s) ||
      !ehTexto(s.id) ||
      !ehTexto(s.codigo) ||
      !ehTexto(s.criancaId) ||
      !ehTexto(s.criadaEm) ||
      typeof s.duracaoMin !== 'number' ||
      !(s.foco === 'equilibrado' || listaDe(s.foco, ehTexto)) ||
      !listaDe(s.atividadeIds, ehTexto) ||
      !(s.livroId === null || ehTexto(s.livroId)) ||
      !marcadorOk(s)
    ) {
      falha('sessão inválida');
    }
  }
}
