import { beforeEach, describe, expect, it } from 'vitest';
import { carregarConteudo } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import { criarExemplo } from '../src/domain/exemplo';
import {
  arquivoGrandeDemais,
  LIMITES_BACKUP,
  TAMANHO_MAX_BACKUP_BYTES,
} from '../src/domain/backup';
import { abrirRepositorio, validarBackup, type Repositorio } from '../src/dados/repositorio';
import type { Sessao } from '../src/domain/tipos';
import { AGORA, crianca, familia } from './fabricas';

// D23 / SEG-2: a cópia importada é dado de fora; recusa o incoerente, mas nunca uma cópia antiga legítima.
const idx = criarIndice(carregarConteudo());
const sessao = (id: string, criancaId = 'c1'): Sessao => ({
  id,
  codigo: `S-${id}`,
  criancaId,
  criadaEm: AGORA,
  duracaoMin: 30,
  foco: 'equilibrado',
  atividadeIds: [],
  livroId: null,
});
const copia = (extra: Record<string, unknown> = {}) => ({
  app: 'semear',
  versao: 1,
  exportadoEm: AGORA,
  familia: familia(),
  criancas: [crianca()],
  estados: [],
  historico: [],
  sessoes: [sessao('s1')],
  ...extra,
});

describe('tamanho do arquivo', () => {
  it('recusa acima de 10 MB e aceita exatamente 10 MB', () => {
    expect(arquivoGrandeDemais(TAMANHO_MAX_BACKUP_BYTES)).toBe(false);
    expect(arquivoGrandeDemais(TAMANHO_MAX_BACKUP_BYTES + 1)).toBe(true);
    expect(arquivoGrandeDemais(22 * 1024)).toBe(false); // a cópia real de 7 crianças e 35 sessões
  });
});

describe('validarBackup: coerência', () => {
  it('uma cópia coerente passa', () => {
    expect(() => validarBackup(copia())).not.toThrow();
  });

  it('exige a família quando há crianças, com a mensagem pedida', () => {
    expect(() => validarBackup(copia({ familia: null }))).toThrow(
      'Este arquivo tem crianças, mas não tem a família. Não foi possível restaurar.',
    );
  });

  it('sem crianças, a família pode faltar (aparelho vazio)', () => {
    expect(() => validarBackup(copia({ familia: null, criancas: [], sessoes: [] }))).not.toThrow();
  });

  it('recusa criancaId que não existe no arquivo em sessões, estados, histórico e planos', () => {
    const solto = 'outra';
    expect(() => validarBackup(copia({ sessoes: [sessao('s1', solto)] }))).toThrow(/sessões/);
    expect(() => validarBackup(copia({ estados: [{ criancaId: solto, estados: {} }] }))).toThrow(
      /estados/,
    );
    expect(() =>
      validarBackup(
        copia({
          historico: [
            {
              criancaId: solto,
              chave: 'LG.FON.01',
              registro: { estado: 'consolidado', atualizadoEm: AGORA, origem: 'manual' },
            },
          ],
        }),
      ),
    ).toThrow(/histórico/);
    const plano = {
      id: 'p1',
      criancaId: solto,
      inicio: '2026-10-12',
      criadoEm: AGORA,
      rotina: { dias: ['seg'], duracaoMin: 30 },
      dias: [],
    };
    expect(() => validarBackup(copia({ planos: [plano] }))).toThrow(/planos/);
  });

  it('recusa ids de criança repetidos', () => {
    expect(() =>
      validarBackup(copia({ criancas: [crianca(), crianca({ nome: 'Outra' })] })),
    ).toThrow(/id repetido/);
  });

  it('recusa nome acima do limite do formulário e quantidade absurda', () => {
    expect(() =>
      validarBackup(copia({ criancas: [crianca({ nome: 'x'.repeat(LIMITES_BACKUP.nome + 1) })] })),
    ).toThrow(/nome/);
    expect(() => validarBackup(copia({ familia: familia({ educador: 'x'.repeat(61) }) }))).toThrow(
      /família/,
    );
    const muitas = Array.from({ length: LIMITES_BACKUP.criancas + 1 }, (_, i) =>
      crianca({ id: `c${i}` }),
    );
    expect(() => validarBackup(copia({ criancas: muitas, sessoes: [] }))).toThrow(
      /crianças demais/,
    );
  });
});

describe('validarBackup: nascimento', () => {
  const com = (nascimento: string) => copia({ criancas: [crianca({ nascimento })] });
  it('recusa futuro (2099), ano 0001 e mais de 18 anos', () => {
    expect(() => validarBackup(com('2099-01-01'))).toThrow(/nascimento/);
    expect(() => validarBackup(com('0001-01-01'))).toThrow(/nascimento/);
    expect(() => validarBackup(com('1990-05-05'))).toThrow(/nascimento/);
  });
  it('aceita irmão fora de 2 a 8 anos', () => {
    expect(() => validarBackup(com('2016-05-05'))).not.toThrow();
  });
});

describe('cópias antigas legítimas continuam entrando', () => {
  let repo: Repositorio;
  beforeEach(async () => {
    repo = await abrirRepositorio(`limites-${Math.random()}`);
  });

  it('a família de exemplo exportada volta a entrar (com e sem planos)', async () => {
    await repo.carregarExemplo(criarExemplo(idx, new Date(AGORA)));
    const exportada = JSON.parse(JSON.stringify(await repo.exportar(AGORA))) as Record<
      string,
      unknown
    >;
    expect(() => validarBackup(exportada)).not.toThrow();
    // Cópia anterior aos planos semanais (#8): o campo nem existe.
    delete exportada.planos;
    expect(() => validarBackup(exportada)).not.toThrow();
    await repo.apagarTudo();
    validarBackup(exportada);
    await repo.importar(exportada);
    expect((await repo.criancas()).map((c) => c.nome).sort()).toEqual(['Ana', 'Theo']);
  });

  it('cópia sem nada (aparelho vazio) entra', () => {
    expect(() =>
      validarBackup({
        app: 'semear',
        versao: 1,
        exportadoEm: AGORA,
        familia: null,
        criancas: [],
        estados: [],
        historico: [],
        sessoes: [],
      }),
    ).not.toThrow();
  });
});
