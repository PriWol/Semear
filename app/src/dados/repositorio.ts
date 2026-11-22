// Repositório: único ponto de acesso aos dados guardados no aparelho (ADR 0002).
import { openDB, type DBSchema, type IDBPDatabase } from 'idb';
import {
  ANOTACOES_MAX,
  DURACAO_REAL_MAX,
  ENGAJAMENTOS,
  ESTADOS,
  IDIOMAS,
  VERTENTES,
  type Crianca,
  type EstadosCrianca,
  type EventoMarco,
  type Familia,
  type RegistroMarco,
  type Sessao,
} from '../domain/tipos';
import { dataValida, MENSAGEM_NASCIMENTO, problemaDeNascimento } from '../domain/datas';
import { LIMITES_BACKUP, problemaDeCoerencia, problemaDeQuantidade } from '../domain/backup';
import { horaValida } from '../domain/lembretes';
import { ehLetra } from '../domain/letra';
import { DIAS, type PlanoSemana } from '../domain/semana';
import { EDUCADOR_EXEMPLO, type DadosExemplo } from '../domain/exemplo';

export const VERSAO_BACKUP = 1;

// O evento do histórico mora no domínio (tipos.ts); reexportado aqui para quem já importava daqui.
export type { EventoMarco };

export interface Backup {
  app: 'semear';
  versao: number;
  exportadoEm: string;
  familia: Familia | null;
  criancas: Crianca[];
  estados: { criancaId: string; estados: EstadosCrianca }[];
  historico: EventoMarco[];
  sessoes: Sessao[];
  /** planos semanais (#8); backups anteriores não têm */
  planos?: PlanoSemana[];
}

export interface Repositorio {
  familia(): Promise<Familia | null>;
  salvarFamilia(familia: Familia): Promise<void>;
  /**
   * Muda SÓ os campos informados, lendo e gravando na mesma transação (QA1-03): duas abas abertas não
   * desfazem uma à outra. Recusa se não há família (nunca cria uma incompleta).
   */
  atualizarFamilia(campos: Partial<Familia>): Promise<void>;

  criancas(): Promise<Crianca[]>;
  crianca(id: string): Promise<Crianca | null>;
  /** recusa nascimento impossível (§ D18); fora de 2 a 8 anos é permitido */
  salvarCrianca(crianca: Crianca): Promise<void>;
  /** como `atualizarFamilia`: só os campos informados; recusa se a criança foi removida em outra aba */
  atualizarCrianca(id: string, campos: Partial<Omit<Crianca, 'id'>>): Promise<void>;
  /** remove a criança e tudo o que é dela (estados, histórico, sessões) */
  removerCrianca(id: string): Promise<void>;

  estados(criancaId: string): Promise<EstadosCrianca>;
  /** aplica mudanças nos estados e grava cada uma no histórico, numa única transação */
  atualizarEstados(criancaId: string, mudancas: Record<string, RegistroMarco>): Promise<void>;
  historico(criancaId: string): Promise<EventoMarco[]>;

  sessoes(criancaId?: string): Promise<Sessao[]>;
  sessao(id: string): Promise<Sessao | null>;
  salvarSessao(sessao: Sessao): Promise<void>;
  /** remove a sessão e as observações que a ficha dela gravou no histórico (#11) */
  removerSessao(id: string): Promise<void>;
  /**
   * Registra a ficha de uma sessão (#11): grava a sessão atualizada e acrescenta os eventos ao histórico,
   * numa única transação (falhou, nada é gravado). NÃO toca em `estados`: só o pai muda o estado (§5.2).
   * Recusa sessão que não existe e evento que não pertence a esta sessão e a esta criança.
   */
  registrarSessao(sessao: Sessao, eventos: EventoMarco[]): Promise<void>;
  /**
   * "Desfazer" logo depois de registrar (D20): devolve a sessão a `anterior` e remove SÓ as observações que
   * aquele registro acrescentou (as de `registradaEm`). Recusa (devolve false) se a sessão já não está como
   * aquele registro a deixou (registrada de novo em outra aba, ou removida): nunca apaga o que é mais novo.
   * O prazo de 10 s é da tela; aqui vale só a conferência. Não toca em `estados` (ADR 0030).
   */
  desfazerRegistro(anterior: Sessao, registradaEm: string): Promise<boolean>;

  /** planos semanais da criança, do mais recente para o mais antigo */
  planos(criancaId: string): Promise<PlanoSemana[]>;
  salvarPlano(plano: PlanoSemana): Promise<void>;
  removerPlano(id: string): Promise<void>;

  /** data do último backup exportado (para o lembrete mensal) */
  ultimoBackup(): Promise<string | null>;
  marcarBackup(agora: string): Promise<void>;

  exportar(agora: string): Promise<Backup>;
  /** substitui todos os dados pelos do backup */
  importar(backup: Backup): Promise<void>;
  apagarTudo(): Promise<void>;

  /** grava a família de exemplo (#39); recusa se já existe uma família no aparelho */
  carregarExemplo(dados: DadosExemplo): Promise<void>;
  /**
   * remove SÓ os registros marcados como exemplo: o que a pessoa cadastrou continua no aparelho.
   * Se ela cadastrou crianças, a família é mantida (sem o marcador) para elas não ficarem órfãs.
   */
  apagarExemplo(): Promise<{ familiaMantida: boolean }>;
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
  planos: { key: string; value: PlanoSemana; indexes: { porCrianca: string } };
}

const LOJAS = ['config', 'criancas', 'estados', 'historico', 'sessoes', 'planos'] as const;
const CHAVE_FAMILIA = 'familia';
const CHAVE_BACKUP = 'ultimoBackup';

function exigirNascimentoPlausivel(nascimento: string, hoje: Date): void {
  const problema = problemaDeNascimento(nascimento, hoje);
  if (problema) throw new Error(MENSAGEM_NASCIMENTO[problema]);
}

const lerFamilia = (v: Familia | { em: string } | undefined): Familia | null =>
  v && 'educador' in v ? v : null;

export async function abrirRepositorio(
  nomeBanco = 'semear',
  /** relógio injetável: a validação do nascimento precisa do "hoje" (o domínio não lê o relógio) */
  agora: () => Date = () => new Date(),
): Promise<Repositorio> {
  const db = await openDB<Esquema>(nomeBanco, 2, {
    // Toda mudança de esquema entra aqui como "if (antiga < N) { ... }", com teste. v2: planos semanais (#8).
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
      if (antiga < 2) {
        banco.createObjectStore('planos', { keyPath: 'id' }).createIndex('porCrianca', 'criancaId');
      }
    },
  });
  return criarRepositorio(db, agora);
}

function criarRepositorio(db: IDBPDatabase<Esquema>, agora: () => Date): Repositorio {
  const ordenarSessoes = (lista: Sessao[]) =>
    lista.sort((a, b) => b.criadaEm.localeCompare(a.criadaEm));

  return {
    async familia() {
      return lerFamilia(await db.get('config', CHAVE_FAMILIA));
    },
    async salvarFamilia(familia) {
      await db.put('config', familia, CHAVE_FAMILIA);
    },
    async atualizarFamilia(campos) {
      const tx = db.transaction('config', 'readwrite');
      const atual = lerFamilia(await tx.store.get(CHAVE_FAMILIA));
      if (!atual) {
        tx.done.catch(() => undefined);
        tx.abort();
        throw new Error('Não há família neste aparelho: nada foi alterado.');
      }
      await tx.store.put({ ...atual, ...campos }, CHAVE_FAMILIA);
      await tx.done;
    },

    async criancas() {
      const lista = await db.getAll('criancas');
      return lista.sort((a, b) => a.nascimento.localeCompare(b.nascimento));
    },
    async crianca(id) {
      return (await db.get('criancas', id)) ?? null;
    },
    async salvarCrianca(crianca) {
      exigirNascimentoPlausivel(crianca.nascimento, agora());
      await db.put('criancas', crianca);
    },
    async atualizarCrianca(id, campos) {
      if (campos.nascimento !== undefined) exigirNascimentoPlausivel(campos.nascimento, agora());
      const tx = db.transaction('criancas', 'readwrite');
      const atual = await tx.store.get(id);
      if (!atual) {
        tx.done.catch(() => undefined);
        tx.abort();
        throw new Error('Esta criança foi removida em outra aba: nada foi alterado.');
      }
      await tx.store.put({ ...atual, ...campos, id });
      await tx.done;
    },
    async removerCrianca(id) {
      const tx = db.transaction(
        ['criancas', 'estados', 'historico', 'sessoes', 'planos'],
        'readwrite',
      );
      await tx.objectStore('criancas').delete(id);
      await tx.objectStore('estados').delete(id);
      for (const loja of ['historico', 'sessoes', 'planos'] as const) {
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
      const tx = db.transaction(['sessoes', 'historico'], 'readwrite');
      await tx.objectStore('sessoes').delete(id);
      // Sem isto, o backup exportado depois teria eventos apontando para uma sessão que não existe.
      let cursor = await tx.objectStore('historico').openCursor();
      while (cursor) {
        if (cursor.value.sessaoId === id) await cursor.delete();
        cursor = await cursor.continue();
      }
      await tx.done;
    },
    async registrarSessao(sessao, eventos) {
      const tx = db.transaction(['sessoes', 'historico'], 'readwrite');
      try {
        if (!(await tx.objectStore('sessoes').get(sessao.id))) {
          throw new Error('Sessão não encontrada: o registro não foi salvo.');
        }
        if (eventos.some((e) => e.sessaoId !== sessao.id || e.criancaId !== sessao.criancaId)) {
          throw new Error('Há um evento que não pertence a esta sessão: o registro não foi salvo.');
        }
        await tx.objectStore('sessoes').put(sessao);
        for (const e of eventos) await tx.objectStore('historico').add(e);
        await tx.done;
      } catch (erro) {
        // Como em importar: um erro dentro da transação não a desfaz sozinho; sem o abort, a sessão já
        // gravada ficaria sem as observações.
        tx.done.catch(() => undefined); // o abort rejeita tx.done de propósito
        try {
          tx.abort();
        } catch {
          // a transação já terminou (abortada pelo próprio navegador)
        }
        throw erro;
      }
    },

    async desfazerRegistro(anterior, registradaEm) {
      const tx = db.transaction(['sessoes', 'historico'], 'readwrite');
      const atual = await tx.objectStore('sessoes').get(anterior.id);
      if (!atual || atual.registradaEm !== registradaEm) {
        await tx.done;
        return false;
      }
      await tx.objectStore('sessoes').put(anterior);
      let cursor = await tx.objectStore('historico').openCursor();
      while (cursor) {
        const e = cursor.value;
        if (
          e.sessaoId === anterior.id &&
          e.registro.origem === 'sessao' &&
          e.registro.atualizadoEm === registradaEm
        ) {
          await cursor.delete();
        }
        cursor = await cursor.continue();
      }
      await tx.done;
      return true;
    },

    async planos(criancaId) {
      const lista = await db.getAllFromIndex('planos', 'porCrianca', criancaId);
      return lista.sort((a, b) => b.inicio.localeCompare(a.inicio));
    },
    async salvarPlano(plano) {
      await db.put('planos', plano);
    },
    async removerPlano(id) {
      await db.delete('planos', id);
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
        planos: await db.getAll('planos'),
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
        for (const p of backup.planos ?? []) await tx.objectStore('planos').put(p);
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

    async carregarExemplo(dados) {
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
      // Depois dos eventos do posicionamento: a ordem do histórico é o que o selo "parece pronto" lê.
      for (const h of dados.historico) await tx.objectStore('historico').add(h);
      await tx.done;
    },

    async apagarExemplo() {
      let familiaMantida = false;
      const tx = db.transaction(LOJAS, 'readwrite');
      // Nunca clear(): uma criança real cadastrada durante o exemplo não tem o marcador e fica.
      const doExemplo = (await tx.objectStore('criancas').getAll()).filter((c) => c.exemplo);
      for (const c of doExemplo) {
        await tx.objectStore('criancas').delete(c.id);
        await tx.objectStore('estados').delete(c.id);
        for (const loja of ['historico', 'sessoes', 'planos'] as const) {
          let cursor = await tx.objectStore(loja).index('porCrianca').openCursor(c.id);
          while (cursor) {
            await cursor.delete();
            cursor = await cursor.continue();
          }
        }
      }
      const sessoesDoExemplo = new Set<string>();
      let cursor = await tx.objectStore('sessoes').openCursor();
      while (cursor) {
        if (cursor.value.exemplo) {
          sessoesDoExemplo.add(cursor.value.id);
          await cursor.delete();
        }
        cursor = await cursor.continue();
      }
      // As observações das sessões do exemplo saem junto (#11), nunca as de sessões reais.
      let evento = await tx.objectStore('historico').openCursor();
      while (evento) {
        const sessaoId = evento.value.sessaoId;
        if (sessaoId !== undefined && sessoesDoExemplo.has(sessaoId)) await evento.delete();
        evento = await evento.continue();
      }
      const familia = lerFamilia(await tx.objectStore('config').get(CHAVE_FAMILIA));
      if (familia?.exemplo) {
        // Sobrou criança que a pessoa cadastrou? Então a família passa a ser dela: apagar a família
        // deixaria essas crianças órfãs (invisíveis na tela). Ela fica, sem o marcador.
        const restaram = (await tx.objectStore('criancas').count()) > 0;
        if (restaram) {
          const real: Familia = { ...familia };
          delete real.exemplo;
          // D12 (ADR 0013, adendo): o nome fictício não passa a ser o da família de verdade. Se a pessoa já
          // trocou o nome durante o exemplo, ele fica; só o "Marina" de fábrica é zerado.
          if (real.educador === EDUCADOR_EXEMPLO) real.educador = '';
          await tx.objectStore('config').put(real, CHAVE_FAMILIA);
          familiaMantida = true;
        } else {
          await tx.objectStore('config').delete(CHAVE_FAMILIA);
        }
      }
      await tx.done;
      return { familiaMantida };
    },
  };
}

/**
 * Confere a forma completa do backup ANTES de apagar qualquer dado: um arquivo errado (ou adulterado)
 * não pode zerar o app nem levar valores inesperados para as telas e o pacote.
 */
export function validarBackup(dado: unknown, hoje: Date = new Date()): asserts dado is Backup {
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
  const ehData = (v: unknown) => ehTexto(v) && dataValida(v);
  // O marcador do exemplo só pode faltar ou ser true (#39).
  const marcadorOk = (v: Record<string, unknown>) => v.exemplo === undefined || v.exemplo === true;
  const ehLembrete = (v: unknown) =>
    ehObjeto(v) &&
    typeof v.ativo === 'boolean' &&
    typeof v.incluirNome === 'boolean' &&
    ehTexto(v.hora) &&
    horaValida(v.hora);
  const ehDia = (v: unknown) => (DIAS as readonly unknown[]).includes(v);
  const ehRotina = (v: unknown) =>
    ehObjeto(v) &&
    listaDe(v.dias, ehDia) &&
    typeof v.duracaoMin === 'number' &&
    v.duracaoMin > 0 &&
    v.duracaoMin <= 240;
  const ehDiaPlano = (v: unknown) =>
    ehObjeto(v) &&
    ehDia(v.dia) &&
    ehData(v.data) &&
    typeof v.duracaoMin === 'number' &&
    listaDe(v.atividadeIds, ehTexto) &&
    (v.livroId === null || ehTexto(v.livroId)) &&
    typeof v.feito === 'boolean' &&
    (v.sessaoId === undefined || ehTexto(v.sessaoId));
  const ehPlano = (v: unknown) =>
    ehObjeto(v) &&
    ehTexto(v.id) &&
    ehTexto(v.criancaId) &&
    ehData(v.inicio) &&
    ehTexto(v.criadoEm) &&
    ehRotina(v.rotina) &&
    Array.isArray(v.dias) &&
    v.dias.every(ehDiaPlano);
  // Instante ISO (com hora): a data do registro vem do `toISOString()` do app, nunca de texto livre.
  const ehInstante = (v: unknown) =>
    ehTexto(v) &&
    /^\d{4}-\d{2}-\d{2}T/.test(v) &&
    dataValida(v.slice(0, 10)) && // o Date aceita 31/02 e vira março: o dia precisa existir de verdade
    !Number.isNaN(Date.parse(v));
  const ehDuracaoReal = (v: unknown) =>
    typeof v === 'number' && Number.isInteger(v) && v >= 1 && v <= DURACAO_REAL_MAX;
  // Chaves que mexem no protótipo dos objetos: nenhum marco legítimo se chama assim.
  const chaveProibida = (c: string) => ['__proto__', 'constructor', 'prototype'].includes(c);
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
  if (b.planos !== undefined && !Array.isArray(b.planos)) falha('plano semanal inválido');
  // Só as contagens, antes de percorrer qualquer lista (D23).
  const demais = problemaDeQuantidade(b as Parameters<typeof problemaDeQuantidade>[0]);
  if (demais) falha(demais);

  const f = b.familia;
  if (f !== null && f !== undefined) {
    if (
      !ehObjeto(f) ||
      !ehTexto(f.educador) ||
      !ehVertente(f.vertentePrincipal) ||
      !listaDe(f.inspiracoes, ehVertente) ||
      !listaDe(f.idiomasEducador, ehIdioma) ||
      !ehTexto(f.criadaEm) ||
      !(f.lembrete === undefined || ehLembrete(f.lembrete)) ||
      !marcadorOk(f)
    ) {
      falha('dados da família incompletos ou desconhecidos');
    }
  }
  // Registros de exemplo só fazem sentido junto da família de exemplo: sem ela, a faixa "Apagar exemplo"
  // não aparece e Ana e Theo ficariam misturados aos dados reais, sem como apagá-los em bloco.
  const familiaDeExemplo = ehObjeto(f) && f.exemplo === true;
  const temExemplo = [...(b.criancas as unknown[]), ...(b.sessoes as unknown[])].some(
    (r) => ehObjeto(r) && r.exemplo === true,
  );
  if (temExemplo && !familiaDeExemplo) falha('registros de exemplo sem a família de exemplo');
  for (const c of b.criancas as unknown[]) {
    if (!ehObjeto(c) || !ehTexto(c.id) || !ehTexto(c.nome)) falha('criança sem id ou nome');
    const cr = c as Record<string, unknown>;
    const problemaNasc = ehTexto(cr.nascimento)
      ? problemaDeNascimento(cr.nascimento, hoje)
      : 'formato';
    if (problemaNasc) {
      falha(
        `data de nascimento inválida (${String(cr.nome).slice(0, LIMITES_BACKUP.nome)}): ${MENSAGEM_NASCIMENTO[problemaNasc]}`,
      );
    }
    if (cr.letra !== null && !ehLetra(cr.letra)) falha(`letra desconhecida (${String(cr.nome)})`);
    if (!listaDe(cr.trilhas, ehIdioma)) falha(`línguas desconhecidas (${String(cr.nome)})`);
    if (!marcadorOk(cr)) falha(`marcador de exemplo inválido (${String(cr.nome)})`);
    if (cr.rotina !== undefined && !ehRotina(cr.rotina))
      falha(`rotina inválida (${String(cr.nome)})`);
  }
  for (const e of b.estados as unknown[]) {
    if (!ehObjeto(e) || !ehTexto(e.criancaId) || !ehObjeto(e.estados)) falha('estado sem criança');
    if (!Object.values((e as { estados: object }).estados).every(ehRegistro)) {
      falha('estado de marco desconhecido');
    }
    if (Object.keys((e as { estados: object }).estados).some(chaveProibida))
      falha('chave de marco não permitida');
  }
  for (const h of b.historico as unknown[]) {
    if (!ehObjeto(h) || !ehTexto(h.criancaId) || !ehTexto(h.chave) || !ehRegistro(h.registro)) {
      falha('histórico inválido');
    }
    if (chaveProibida((h as { chave: string }).chave)) falha('chave de marco não permitida');
    if (
      (h as { sessaoId?: unknown }).sessaoId !== undefined &&
      !ehTexto((h as { sessaoId?: unknown }).sessaoId)
    ) {
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
      !(s.tipo === undefined || s.tipo === 'avulsa') ||
      !marcadorOk(s) ||
      // Campos do registro (#11): opcionais, então backups anteriores continuam valendo.
      !(s.registradaEm === undefined || ehInstante(s.registradaEm)) ||
      !(s.duracaoReal === undefined || ehDuracaoReal(s.duracaoReal)) ||
      !(
        s.engajamento === undefined || (ENGAJAMENTOS as readonly unknown[]).includes(s.engajamento)
      ) ||
      !(s.anotacoes === undefined || (ehTexto(s.anotacoes) && s.anotacoes.length <= ANOTACOES_MAX))
    ) {
      falha('sessão inválida');
    }
  }
  const ids = (b.sessoes as Record<string, unknown>[]).map((s) => s.id);
  if (new Set(ids).size !== ids.length) {
    // Ao importar, a segunda sessão com o mesmo id sobrescreveria a primeira em silêncio.
    falha('há sessões com id repetido');
  }
  // Observação de sessão (#11): o evento precisa apontar para uma sessão do próprio backup, da mesma
  // criança, e só a origem "sessao" leva sessaoId. Evento órfão deixaria o selo contando sessões fantasmas.
  const criancaDaSessao = new Map(
    (b.sessoes as Record<string, unknown>[]).map((s) => [s.id as string, s.criancaId]),
  );
  for (const h of b.historico as Record<string, unknown>[]) {
    // Observação de sessão sem sessaoId nunca conta para o selo: não faz sentido guardá-la assim.
    if ((h.registro as Record<string, unknown>).origem === 'sessao' && h.sessaoId === undefined) {
      falha('observação de sessão sem sessaoId');
    }
    if (h.sessaoId === undefined) continue;
    const registro = h.registro as Record<string, unknown>;
    if (registro.origem !== 'sessao')
      falha('observação de sessão com origem diferente de "sessao"');
    if (!criancaDaSessao.has(h.sessaoId as string))
      falha('observação de uma sessão que não existe');
    if (criancaDaSessao.get(h.sessaoId as string) !== h.criancaId) {
      falha('observação ligada a uma sessão de outra criança');
    }
  }
  // Planos semanais (#8): ausentes nos backups anteriores; quando existem, valem a forma inteira.
  if (b.planos !== undefined && !listaDe(b.planos, ehPlano)) falha('plano semanal inválido');
  // Por último, com a forma já garantida: família, vínculos entre registros e limites por campo (D23).
  const incoerente = problemaDeCoerencia(b as unknown as Parameters<typeof problemaDeCoerencia>[0]);
  if (incoerente) throw new Error(incoerente);
}
