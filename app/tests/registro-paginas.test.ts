import { beforeEach, describe, expect, it } from 'vitest';
import { abrirRepositorio, type Repositorio } from '../src/dados/repositorio';
import type { Contexto } from '../src/ui/app';
import { paginaRegistrarBusca } from '../src/pages/registrar-busca';
import { paginaSessaoRegistrar } from '../src/pages/sessao-registrar';
import { paginaJornada } from '../src/pages/jornada';
import { paginaPrivacidade } from '../src/pages/privacidade';
import { montarRegistro, observacoesDaSessao } from '../src/domain/registro';
import type { Sessao } from '../src/domain/tipos';
import { AGORA, crianca, familia, indiceBase } from './fabricas';

// As telas de registro (#11) desenhadas a partir de um banco de verdade (IndexedDB simulado).
const idx = indiceBase();
let repo: Repositorio;
let n = 0;

const sessao = (id: string, dia: number, extra: Partial<Sessao> = {}): Sessao => ({
  id,
  codigo: `S-10${String(dia).padStart(2, '0')}-A1`,
  criancaId: 'c1',
  criadaEm: `2026-10-${String(dia).padStart(2, '0')}T10:00:00.000Z`,
  duracaoMin: 40,
  foco: 'equilibrado',
  atividadeIds: ['atv-fon-1', 'atv-fon-2'],
  livroId: null,
  ...extra,
});

const ctx = (): Contexto => ({
  repo,
  idx,
  agora: () => AGORA,
  ir: () => undefined,
  atualizar: async () => undefined,
  avisar: () => undefined,
});

beforeEach(async () => {
  repo = await abrirRepositorio(`paginas-${++n}`);
  await repo.salvarFamilia(familia());
  await repo.salvarCrianca(crianca({ id: 'c1', nome: 'Ana' }));
});

describe('busca de sessão para registrar', () => {
  it('traz o texto, o campo com rótulo visível e o botão', async () => {
    await repo.salvarSessao(sessao('s1', 14));
    const { conteudo } = await paginaRegistrarBusca(ctx(), {});
    const h = conteudo.valor;
    expect(h).toContain('<h1>Registrar sessão</h1>');
    expect(h).toContain('Digite o código impresso na folha da sessão, por exemplo S-1014-A1.');
    expect(h).toContain('<b>Código da sessão</b>');
    expect(h).toContain('autocapitalize="characters"');
    expect(h).toContain('autocomplete="off"');
    expect(h).toContain('spellcheck="false"');
    expect(h).toContain('Encontrar sessão');
    expect(h).toContain('Ou escolha uma das últimas sessões');
  });

  it('lista no máximo 6 sessões, a mais recente primeiro, com Feita ou Para registrar', async () => {
    for (let d = 1; d <= 8; d++) {
      await repo.salvarSessao(sessao(`s${d}`, d, d === 8 ? { registradaEm: AGORA } : {}));
    }
    const { conteudo } = await paginaRegistrarBusca(ctx(), {});
    const links = [...conteudo.valor.matchAll(/href="#\/sessao\/(s\d)\/registrar"/g)].map(
      (m) => m[1],
    );
    expect(links).toEqual(['s8', 's7', 's6', 's5', 's4', 's3']);
    expect(conteudo.valor).toContain('<span class="selo-feita">Feita ✓</span>');
    expect(conteudo.valor).toContain('Para registrar');
  });

  it('sem nenhuma sessão, convida a preparar a primeira', async () => {
    const { conteudo } = await paginaRegistrarBusca(ctx(), {});
    expect(conteudo.valor).toContain(
      'Nenhuma sessão ainda. Prepare a primeira e ela aparece aqui.',
    );
    expect(conteudo.valor).toContain('Preparar sessão');
    expect(conteudo.valor).not.toContain('id="codigo"');
  });

  it('escapa o nome da criança', async () => {
    await repo.salvarCrianca(crianca({ id: 'c1', nome: '<img src=x onerror=alert(1)>' }));
    await repo.salvarSessao(sessao('s1', 14));
    const { conteudo } = await paginaRegistrarBusca(ctx(), {});
    expect(conteudo.valor).not.toContain('<img');
    expect(conteudo.valor).toContain('&lt;img src=x');
  });
});

describe('ficha de registro no app', () => {
  it('um fieldset por marco com 3 rádios, nenhum marcado, e a duração planejada', async () => {
    await repo.salvarSessao(sessao('s1', 14));
    const { conteudo } = await paginaSessaoRegistrar(ctx(), { id: 's1' });
    const h = conteudo.valor;
    expect(h).toContain('Como foi a sessão?');
    expect(h).toContain('S-1014-A1 · Ana ·');
    expect(h.match(/<fieldset class="reg-marco">/g)).toHaveLength(2);
    expect(h.match(/type="radio"\s+name="m\d"/g)).toHaveLength(6);
    expect(h).toContain('Não observado');
    expect(h).toContain('Em desenvolvimento');
    expect(h).toContain('Consolidado');
    expect(h).not.toMatch(/name="m\d"[^>]*checked/);
    expect(h).toContain('Planejado: 40 min');
    expect(h).toContain('0 de 2 marcos marcados');
    expect(h).toContain('aria-live="polite"');
    expect(h).toContain('Salvar registro');
    expect(h).toContain('Cancelar');
    expect(h).not.toContain('Esta sessão já foi registrada');
    expect(h).not.toContain('(revisão)'); // LG.FON.01 é principal em atv-fon-1: principal vale mais que revisão
  });

  it('os quatro engajamentos têm ícone de traço só como enfeite, o rótulo escrito e nenhum emoji', async () => {
    await repo.salvarSessao(sessao('s1', 14));
    const h = (await paginaSessaoRegistrar(ctx(), { id: 's1' })).conteudo.valor;
    for (const rotulo of ['Pouco', 'Normal', 'Animado', 'Empolgado']) expect(h).toContain(rotulo);
    const reg = h.slice(h.indexOf('reg-engajamento'));
    expect(reg.match(/<svg[^>]*aria-hidden="true"/g)).toHaveLength(4);
    expect(h).not.toMatch(/\p{Extended_Pictographic}/u);
  });

  it('as telas e os rótulos do registro não têm emoji', async () => {
    const { readFileSync } = await import('node:fs');
    const le = (f: string) => readFileSync(new URL(`../src/${f}`, import.meta.url), 'utf8');
    // Em rotulos.ts só o bloco do engajamento (os ícones de estado da jornada são outra estória).
    const rotulos = le('ui/rotulos.ts');
    const engajamento = rotulos.slice(
      rotulos.indexOf('NOME_ENGAJAMENTO'),
      rotulos.indexOf('ROTULO_FEITA'),
    );
    expect(engajamento.length).toBeGreaterThan(100);
    expect(engajamento).not.toMatch(/\p{Extended_Pictographic}/u);
    for (const f of ['pages/sessao-registrar.ts', 'pages/registrar-busca.ts']) {
      expect(le(f), f).not.toMatch(/\p{Extended_Pictographic}/u);
    }
  });

  it('avisa junto das anotações que ficam só no aparelho e entram no backup', async () => {
    await repo.salvarSessao(sessao('s1', 14));
    const h = (await paginaSessaoRegistrar(ctx(), { id: 's1' })).conteudo.valor;
    expect(h).toContain('Fica só neste aparelho e entra no backup.');
  });

  it('sessão já registrada: aviso, campos preenchidos e "Salvar alterações"', async () => {
    const s = sessao('s1', 14);
    await repo.salvarSessao(s);
    const ficha = observacoesDaSessao(s, idx);
    const r = montarRegistro(
      s,
      ficha,
      {
        estados: { 'LG.FON.01': 'consolidado' },
        duracaoReal: 33,
        engajamento: 'alto',
        anotacoes: '<b>x</b>',
      },
      '2026-10-15T09:00:00.000Z',
    );
    await repo.registrarSessao(r.sessao, r.eventos);
    const h = (await paginaSessaoRegistrar(ctx(), { id: 's1' })).conteudo.valor;
    expect(h).toMatch(/Esta sessão já foi registrada em\s+15\/10\. Você pode\s+corrigi-la\./);
    expect(h).toMatch(/value="consolidado"\s+checked/);
    expect(h).toContain('value="33"');
    expect(h).toMatch(/value="alto"\s+checked/);
    expect(h).toContain('Salvar alterações');
    expect(h).toContain('1 de 2 marcos marcados');
    // a anotação vai para o textarea como texto: o < e o > são escapados
    expect(h).toContain('&lt;b&gt;x&lt;/b&gt;');
    expect(h).not.toContain('<b>x</b>');
  });

  it('atividade complementar: sem marcos, mas ainda dá para registrar os detalhes', async () => {
    await repo.salvarSessao(sessao('s1', 14, { atividadeIds: ['sumiu'] }));
    const h = (await paginaSessaoRegistrar(ctx(), { id: 's1' })).conteudo.valor;
    expect(h).toContain('não há marcos para registrar');
    expect(h).not.toContain('class="reg-marco"');
    expect(h).toContain('Salvar registro');
  });

  it('sessão inexistente dá erro claro', async () => {
    await expect(paginaSessaoRegistrar(ctx(), { id: 'nada' })).rejects.toThrow(
      /Sessão não encontrada/,
    );
  });
});

describe('desfazer uma escolha ao corrigir', () => {
  it('a ficha explica o caminho e não oferece um "limpar" que não existe', async () => {
    await repo.salvarSessao(sessao('s1', 14));
    const h = (await paginaSessaoRegistrar(ctx(), { id: 's1' })).conteudo.valor;
    expect(h).toContain('Para desfazer uma escolha, marque “Não observado”');
    expect(h).not.toMatch(/limpar/i);
    expect(h).not.toContain('type="reset"');
  });

  it('sem escolha não gera evento: o histórico mantém o último; “Não observado” gera', () => {
    const s = sessao('s1', 14);
    const ficha = observacoesDaSessao(s, idx);
    const a = montarRegistro(s, ficha, { estados: { 'LG.FON.01': 'consolidado' } }, AGORA);
    const anteriores = { 'LG.FON.01': 'consolidado' as const };
    const sem = montarRegistro(a.sessao, ficha, { estados: {} }, AGORA, anteriores);
    expect(sem.eventos).toEqual([]);
    const desfaz = montarRegistro(
      a.sessao,
      ficha,
      { estados: { 'LG.FON.01': 'nao-observado' } },
      AGORA,
      anteriores,
    );
    expect(desfaz.eventos.map((e) => e.registro.estado)).toEqual(['nao-observado']);
  });
});

describe('regra de ouro (§5.2) pela jornada: o selo é dica, quem muda o estado é o pai', () => {
  const K = 'LG.FON.01';
  const obs = (id: string) => ({
    criancaId: 'c1',
    chave: K,
    sessaoId: id,
    registro: { estado: 'consolidado' as const, atualizadoEm: AGORA, origem: 'sessao' as const },
  });
  const marcoNaJornada = async () => {
    const h = (await paginaJornada(ctx(), { id: 'c1' })).conteudo.valor;
    const i = h.indexOf(`data-marco="${K}"`);
    return h.slice(i, h.indexOf('</li>', i));
  };

  it('2 sessões Consolidado mostram o selo; o pai marca Consolidado e ele some; volta para Em desenvolvimento e ele reaparece', async () => {
    for (const id of ['s1', 's2']) {
      await repo.salvarSessao(sessao(id, id === 's1' ? 13 : 14));
      await repo.registrarSessao({ ...sessao(id, 14), registradaEm: AGORA }, [obs(id)]);
    }
    expect(await repo.estados('c1')).toEqual({}); // a ficha não mexeu no estado
    expect(await marcoNaJornada()).toContain('parece pronto');

    const manual = (estado: 'consolidado' | 'em-desenvolvimento') =>
      repo.atualizarEstados('c1', {
        [K]: { estado, atualizadoEm: AGORA, origem: 'manual' },
      });
    await manual('consolidado');
    expect(await marcoNaJornada()).not.toContain('parece pronto');

    await manual('em-desenvolvimento'); // só "Está aqui" zera; o pai voltando o marco não
    expect(await marcoNaJornada()).toContain('parece pronto');
  });
});

describe('privacidade', () => {
  it('diz que o backup e o aparelho guardam as anotações de texto livre', async () => {
    const { conteudo } = await paginaPrivacidade(ctx(), {});
    expect(conteudo.valor).toContain('anotações de texto livre');
    expect(conteudo.valor).toContain('as anotações que você escreveu nas sessões');
  });
});
