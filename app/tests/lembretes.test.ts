import { describe, expect, it } from 'vitest';
import {
  horaValida,
  LEMBRETE_PADRAO,
  planejarLembretes,
  type PlanoParaLembrar,
} from '../src/domain/lembretes';
import { ponteDoAparelho, sincronizarLembretes, type Ponte } from '../src/nativo/lembretes';
import { validarBackup } from '../src/dados/repositorio';
import type { PlanoSemana } from '../src/domain/semana';

const AGORA = new Date(2026, 10, 9, 7, 0).toISOString(); // segunda, 07:00 locais
const plano = (extra: Partial<PlanoSemana> = {}): PlanoSemana => ({
  id: 'p1',
  criancaId: 'c1',
  inicio: '2026-11-09',
  criadoEm: AGORA,
  rotina: { dias: ['seg', 'qua', 'sex'], duracaoMin: 30 },
  dias: [
    {
      dia: 'seg',
      data: '2026-11-09',
      duracaoMin: 30,
      atividadeIds: ['a', 'b'],
      livroId: null,
      feito: false,
    },
    {
      dia: 'qua',
      data: '2026-11-11',
      duracaoMin: 30,
      atividadeIds: ['c'],
      livroId: null,
      feito: false,
    },
    {
      dia: 'sex',
      data: '2026-11-13',
      duracaoMin: 30,
      atividadeIds: [],
      livroId: null,
      feito: false,
    },
  ],
  ...extra,
});
const titulos: Record<string, string> = {
  a: 'Caça às sílabas',
  b: 'Feira dos números',
  c: 'Soprar a vela',
};
const item = (p: PlanoSemana, nome = 'Ana'): PlanoParaLembrar => ({
  plano: p,
  nomeDaCrianca: nome,
  tituloDaAtividade: (id) => titulos[id],
});
const pref = { ...LEMBRETE_PADRAO, ativo: true, hora: '08:00' };
const quando = (d: Date) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;

describe('lembretes do dia (#95)', () => {
  it('o padrão vem desligado, às 8h, sem o nome da criança', () => {
    expect(LEMBRETE_PADRAO).toEqual({ ativo: false, hora: '08:00', incluirNome: false });
  });
  it('desligado não gera lembrete', () => {
    expect(planejarLembretes([item(plano())], LEMBRETE_PADRAO, AGORA)).toEqual([]);
  });
  it('um lembrete por dia com atividade, no horário escolhido', () => {
    const l = planejarLembretes([item(plano())], pref, AGORA);
    expect(l.map((x) => quando(x.quando))).toEqual(['2026-11-09 08:00', '2026-11-11 08:00']);
    expect(l[0]?.texto).toBe('Caça às sílabas · Feira dos números');
  });
  it('dia sem atividade, dia feito e horário que já passou não geram lembrete', () => {
    const p = plano();
    p.dias[1] = { ...p.dias[1]!, feito: true };
    const tarde = new Date(2026, 10, 9, 9, 0).toISOString();
    expect(planejarLembretes([item(p)], pref, tarde)).toEqual([]);
  });
  it('o nome da criança só aparece se a família pedir', () => {
    expect(planejarLembretes([item(plano())], pref, AGORA)[0]?.texto).not.toContain('Ana');
    const com = planejarLembretes([item(plano())], { ...pref, incluirNome: true }, AGORA);
    expect(com[0]?.texto.startsWith('Ana: ')).toBe(true);
  });
  it('atividade que não existe mais é ignorada, e dia só com elas não notifica', () => {
    const p = plano();
    p.dias[1] = { ...p.dias[1]!, atividadeIds: ['sumiu'] };
    expect(planejarLembretes([item(p)], pref, AGORA).length).toBe(1);
  });
  it('os ids são estáveis e distintos, e o total respeita o limite de 64 do iPhone', () => {
    const a = planejarLembretes([item(plano())], pref, AGORA);
    const b = planejarLembretes([item(plano())], pref, AGORA);
    expect(a.map((x) => x.id)).toEqual(b.map((x) => x.id));
    expect(new Set(a.map((x) => x.id)).size).toBe(a.length);
    const muitos = Array.from({ length: 80 }, (_, i) =>
      item(plano({ id: `p${i}`, inicio: '2026-11-09' })),
    );
    expect(planejarLembretes(muitos, pref, AGORA).length).toBeLessThanOrEqual(64);
  });
  it('valida o horário HH:MM', () => {
    expect(['08:00', '23:59', '00:00'].every(horaValida)).toBe(true);
    expect(['8:00', '24:00', '12:60', 'abc', ''].some(horaValida)).toBe(false);
  });
});

describe('adaptador do aparelho', () => {
  const fabricaPonte = (permissao = 'granted') => {
    const chamadas: string[] = [];
    let agendadas: number[] = [];
    const ponte: Ponte = {
      checkPermissions: async () => ({ display: permissao }),
      requestPermissions: async () => ({ display: permissao }),
      getPending: async () => ({ notifications: [{ id: 1 }, { id: 2 }] }),
      cancel: async (o) =>
        void chamadas.push(`cancel:${o.notifications.map((n) => n.id).join(',')}`),
      schedule: async (o) => {
        agendadas = o.notifications.map((n) => n.id);
        chamadas.push('schedule');
      },
    };
    return { ponte, chamadas, agendadas: () => agendadas };
  };
  const lembretes = planejarLembretes([item(plano())], pref, AGORA);

  it('no navegador (sem ponte) não faz nada', async () => {
    expect(ponteDoAparelho({})).toBeNull();
    expect(await sincronizarLembretes(null, lembretes, { pedirPermissao: true })).toBe(
      'indisponivel',
    );
  });
  it('cancela os antigos e agenda os novos', async () => {
    const f = fabricaPonte();
    expect(await sincronizarLembretes(f.ponte, lembretes, { pedirPermissao: false })).toBe('ok');
    expect(f.chamadas).toEqual(['cancel:1,2', 'schedule']);
    expect(f.agendadas().length).toBe(lembretes.length);
  });
  it('sem permissão não agenda; só pede permissão quando a família acabou de ligar', async () => {
    const f = fabricaPonte('denied');
    expect(await sincronizarLembretes(f.ponte, lembretes, { pedirPermissao: false })).toBe(
      'sem-permissao',
    );
    expect(f.chamadas).toEqual(['cancel:1,2']);
  });
  it('reconhece a ponte do Capacitor só dentro do aplicativo', () => {
    const plugin = fabricaPonte().ponte;
    const janela = {
      Capacitor: { isNativePlatform: () => true, Plugins: { LocalNotifications: plugin } },
    };
    expect(ponteDoAparelho(janela)).toBe(plugin);
    expect(
      ponteDoAparelho({
        Capacitor: { isNativePlatform: () => false, Plugins: { LocalNotifications: plugin } },
      }),
    ).toBeNull();
  });
});

describe('backup com a preferência de lembrete', () => {
  const base = (lembrete: unknown) => ({
    app: 'semear',
    versao: 1,
    exportadoEm: AGORA,
    familia: {
      educador: 'M',
      vertentePrincipal: 'Montessori',
      inspiracoes: [],
      idiomasEducador: [],
      criadaEm: AGORA,
      lembrete,
    },
    criancas: [],
    estados: [],
    historico: [],
    sessoes: [],
  });
  it('aceita lembrete válido ou ausente e recusa o inválido', () => {
    expect(() => validarBackup(base(undefined))).not.toThrow();
    expect(() =>
      validarBackup(base({ ativo: true, hora: '08:30', incluirNome: false })),
    ).not.toThrow();
    expect(() => validarBackup(base({ ativo: true, hora: '25:00', incluirNome: false }))).toThrow();
    expect(() =>
      validarBackup(base({ ativo: 'sim', hora: '08:00', incluirNome: false })),
    ).toThrow();
  });
});
