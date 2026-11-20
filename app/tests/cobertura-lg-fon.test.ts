import { describe, expect, it } from 'vitest';
import { carregarConteudo, carregarConteudoBruto, carregarSondagem } from '../src/conteudo';
import type { Atividade, Conteudo, Marco } from '../src/domain/tipos';
import type { Sondagem } from '../src/domain/sondagem';

// Cobertura mínima da linha LG.FON (estória #22). Os critérios da estória só passavam porque o
// conteúdo estava certo; aqui cada um vira uma regra que falha, dizendo QUAL marco ou atividade
// está errado. Usa o conteúdo BRUTO (com rascunhos), para valer já na revisão do conteúdo.
//
// Atividade "principal" de um marco = marco em `marcos`. Quem só o revisa (`revisa`) é
// complemento e NÃO conta para o mínimo de atividades nem para a variedade de vertentes.
// Variedade de vertentes (versão forte, cabe no conteúdo real): as principais do marco cobrem
// pelo menos 2 vertentes na união e não têm todas exatamente o mesmo conjunto de vertentes.
// Regra 10 (idade): ao menos uma principal do marco tem faixa `idade` que contém a `idadeTipica`.
// `idadeIntroducao` é POR VERTENTE (só para o aviso de ritmo), então não entra nesta regra.
// Regra 7: `cuidados` é obrigatório (não vazio) em TODA atividade da linha, de qualquer idade
// inicial. O texto em si é revisado pela dona do produto; não se compara texto entre atividades
// (seria frágil).
const LINHA = 'LG.FON';
// Regressão (PR #107): os ids dos 7 marcos antigos não mudam e os 3 novos são 08 a 10; nenhuma
// família é afetada. Mude esta lista só junto com uma migração.
const IDS_ESPERADOS = Array.from(
  { length: 10 },
  (_, i) => `${LINHA}.${String(i + 1).padStart(2, '0')}`,
);
const MIN_MARCOS = 8;
const MAX_MARCOS = 12;
const MIN_ATIVIDADES = 2;
// Formato dos ids de marco (ex.: LG.FON.04, MA.OPE.02): domínio.linha.número de 2 dígitos.
const ID_MARCO = /^[A-Z]{2}\.[A-Z]{3}\.\d{2}$/;

/** Regressão dos ids: a linha tem exatamente `esperados`, nem mais, nem menos. */
function verificarIds(c: Conteudo, esperados: string[]): string[] {
  const erros: string[] = [];
  const ids = new Set(c.marcos.filter((m) => m.linha === LINHA).map((m) => m.id));
  for (const id of esperados.filter((x) => !ids.has(x))) {
    erros.push(
      `O marco ${id} sumiu da linha ${LINHA} (os ids esperados são ${esperados[0]} a ${esperados[esperados.length - 1]}).`,
    );
  }
  for (const id of [...ids].filter((x) => !esperados.includes(x))) {
    erros.push(`O marco ${id} sobrou na linha ${LINHA}: não está entre os ids esperados.`);
  }
  return erros;
}

/** Devolve uma mensagem em português por problema encontrado; lista vazia = tudo certo. */
function verificarCobertura(c: Conteudo, sondagem: Sondagem): string[] {
  const erros: string[] = [];
  const marcos = c.marcos.filter((m) => m.linha === LINHA).sort((a, b) => a.ordem - b.ordem);
  const atividades = c.atividades.filter((a) =>
    [...a.marcos, ...(a.revisa ?? [])].some((id) => id.startsWith(`${LINHA}.`)),
  );
  const idsDaLinha = new Set(marcos.map((m) => m.id));

  if (marcos.length < MIN_MARCOS || marcos.length > MAX_MARCOS) {
    erros.push(
      `${LINHA} tem ${marcos.length} marcos; o esperado é de ${MIN_MARCOS} a ${MAX_MARCOS}.`,
    );
  }

  for (const a of atividades) {
    for (const id of [...a.marcos, ...(a.revisa ?? [])]) {
      if (id.startsWith(`${LINHA}.`) && !idsDaLinha.has(id)) {
        erros.push(`Atividade ${a.id} cita o marco ${id}, que não existe.`);
      }
    }
  }

  marcos.forEach((m, i) => {
    if (!m.bncc.some((codigo) => codigo.trim() !== '')) {
      erros.push(`Marco ${m.id} está sem código BNCC.`);
    }
    const dele = atividades.filter((a) => a.marcos.includes(m.id));
    if (dele.length < MIN_ATIVIDADES) {
      erros.push(
        `Marco ${m.id} tem ${dele.length} atividade(s) principal(is); precisa de pelo menos ${MIN_ATIVIDADES} (atividade que só revisa o marco não conta).`,
      );
    }
    const conjuntos = dele.map((a) => [...new Set(a.vertentes)].sort().join('|'));
    const uniao = new Set(dele.flatMap((a) => a.vertentes));
    if (dele.length >= 2 && (uniao.size < 2 || new Set(conjuntos).size < 2)) {
      erros.push(
        `Marco ${m.id}: as atividades principais não variam de vertente (união: ${[...uniao].join(', ') || 'nenhuma'}); precisa de pelo menos 2 vertentes e conjuntos diferentes entre elas.`,
      );
    }
    if (!sondagem.itens.some((s) => s.marco === m.id)) {
      erros.push(`Marco ${m.id} está sem item de sondagem.`);
    }
    if (m.ordem !== i + 1) {
      erros.push(
        `Ordem da linha ${LINHA} quebrada em ${m.id}: tem ordem ${m.ordem}, mas deveria ser ${i + 1} (única e contínua de 1 a N).`,
      );
    }
    if (
      dele.length > 0 &&
      !dele.some((a) => a.idade[0] <= m.idadeTipica && m.idadeTipica <= a.idade[1])
    ) {
      erros.push(
        `Marco ${m.id} tem idade típica ${m.idadeTipica}, mas nenhuma atividade principal cobre essa idade (faixas: ${dele.map((a) => `${a.id} [${a.idade[0]}, ${a.idade[1]}]`).join('; ')}).`,
      );
    }
    // Pré-requisito em OUTRA linha (ex.: LG.LET.03, que ainda não existe) é aviso conhecido da
    // estória #22 e não falha por não existir; só o formato do id é conferido.
    for (const pre of m.preRequisitos) {
      if (!ID_MARCO.test(pre)) {
        erros.push(
          `Marco ${m.id} exige "${pre}", que não tem formato de id de marco (ex.: LG.LET.03).`,
        );
      }
      if (pre.startsWith(`${LINHA}.`) && !idsDaLinha.has(pre)) {
        erros.push(`Marco ${m.id} exige ${pre}, que não existe na linha ${LINHA}.`);
      }
      const alvo = marcos.find((x) => x.id === pre);
      if (alvo && alvo.ordem >= m.ordem) {
        erros.push(
          `Marco ${m.id} exige ${pre}, que tem ordem ${alvo.ordem} (não é menor que ${m.ordem}).`,
        );
      }
    }
  });

  for (const a of atividades) {
    const [de, ate] = a.idade;
    if (de > ate || de < 2 || ate > 8) {
      erros.push(
        `Atividade ${a.id} tem idade [${de}, ${ate}]; precisa de 2 <= início <= fim <= 8.`,
      );
    }
    if (!(a.cuidados ?? '').trim()) {
      erros.push(
        `Atividade ${a.id} está sem \`cuidados\` (obrigatório em toda atividade de ${LINHA}).`,
      );
    }
  }
  return erros;
}

describe(`cobertura da linha ${LINHA} (conteúdo real)`, () => {
  it('cumpre os critérios de aceite da estória #22', () => {
    expect(verificarCobertura(carregarConteudoBruto(), carregarSondagem())).toEqual([]);
  });
  it('mantém exatamente os marcos LG.FON.01 a LG.FON.10 (ids estáveis)', () => {
    expect(verificarIds(carregarConteudoBruto(), IDS_ESPERADOS)).toEqual([]);
  });
  // Só informa (sem asserção): o critério "sem lacunas para o que as famílias veem" fica SEM teste
  // até a dona do produto aprovar o lote (portão 2); então a meta abaixo é só `it.todo`.
  // Este bloco imprime a contagem atual para o portão 2 ter um número verificável.
  {
    const visivel = carregarConteudo();
    const poucos = visivel.marcos
      .filter((m) => m.linha === LINHA)
      .map((m) => ({
        id: m.id,
        n: visivel.atividades.filter((a) => a.marcos.includes(m.id)).length,
      }))
      .filter((x) => x.n < MIN_ATIVIDADES);
    console.info(
      `[${LINHA}] marcos publicados com menos de ${MIN_ATIVIDADES} atividades publicadas: ${poucos.length}` +
        (poucos.length ? ` (${poucos.map((x) => `${x.id}=${x.n}`).join(', ')})` : ''),
    );
  }
  it.todo('pré-requisitos de outras linhas existem no conteúdo (quando LG.LET chegar)');
  it.todo(`meta: todo marco de ${LINHA} com pelo menos ${MIN_ATIVIDADES} atividades publicadas`);
});

// Prova de que cada regra falha quando violada: dados sintéticos, sem tocar em app/content/.
describe('verificarCobertura detecta violações (dados sintéticos)', () => {
  const marcoBase = (n: number, extra: Partial<Marco> = {}): Marco => ({
    id: `LG.FON.${String(n).padStart(2, '0')}`,
    linha: LINHA,
    ordem: n,
    titulo: `Marco ${n}`,
    descricaoPais: 'x',
    orientacaoPais: {
      porQueImporta: 'x',
      comoParticipar: 'x',
      sinaisDeAtencao: 'x',
      referencias: [],
    },
    evidencias: [],
    idadeTipica: 4,
    idadeIntroducao: {},
    preRequisitos: [],
    bncc: ['EI03EF02'],
    ...extra,
  });
  const atvBase = (id: string, marcos: string[], extra: Partial<Atividade> = {}): Atividade =>
    ({
      id,
      titulo: id,
      marcos,
      vertentes: ['Clássico'],
      idade: [4, 6],
      duracaoMin: 10,
      objetivo: 'x',
      passos: [],
      observar: { consolidado: [], emDesenvolvimento: [] },
      materiais: [],
      evidencias: [],
      cuidados: 'Supervisione.',
      ...extra,
    }) as Atividade;

  function montar(total = 8) {
    const marcos = Array.from({ length: total }, (_, i) => marcoBase(i + 1));
    const atividades = marcos.flatMap((m, i) => [
      atvBase(`a${i}a`, [m.id], { vertentes: ['Clássico'] }),
      atvBase(`a${i}b`, [m.id], { vertentes: ['Clássico', 'Charlotte Mason'] }),
    ]);
    const sondagem = {
      itens: marcos.map((m) => ({ id: `sd-${m.id}`, marco: m.id })),
    } as unknown as Sondagem;
    const conteudo = { dominios: [], marcos, atividades, livros: [], acervo: [], referencias: [] };
    return { conteudo: conteudo as Conteudo, sondagem };
  }

  it('base sintética passa (controle)', () => {
    const { conteudo, sondagem } = montar();
    expect(verificarCobertura(conteudo, sondagem)).toEqual([]);
  });
  it('regra 1: poucos ou muitos marcos', () => {
    const { conteudo, sondagem } = montar();
    const pouco = { ...conteudo, marcos: conteudo.marcos.slice(0, 7) };
    expect(verificarCobertura(pouco, sondagem).join('\n')).toMatch(/tem 7 marcos/);
    const muitos = {
      ...conteudo,
      marcos: [...conteudo.marcos, ...[9, 10, 11, 12, 13].map((n) => marcoBase(n))],
    };
    expect(verificarCobertura(muitos, sondagem).join('\n')).toMatch(/tem 13 marcos/);
  });
  it('regra 1 (bordas): exatamente 8 e exatamente 12 marcos passam', () => {
    const { conteudo, sondagem } = montar();
    expect(verificarCobertura(conteudo, sondagem)).toEqual([]);
    const doze = montar(12);
    expect(verificarCobertura(doze.conteudo, doze.sondagem)).toEqual([]);
  });
  it('regra 2: BNCC apagado ou em branco', () => {
    const { conteudo, sondagem } = montar();
    conteudo.marcos[2] = marcoBase(3, { bncc: [] });
    conteudo.marcos[3] = marcoBase(4, { bncc: [' '] });
    const msg = verificarCobertura(conteudo, sondagem).join('\n');
    expect(msg).toContain('Marco LG.FON.03 está sem código BNCC');
    expect(msg).toContain('Marco LG.FON.04 está sem código BNCC');
  });
  it('regra 3: marco com menos de 2 atividades principais (revisar não conta)', () => {
    const { conteudo, sondagem } = montar();
    conteudo.atividades = conteudo.atividades.filter((a) => a.id !== 'a4b');
    const falha = 'Marco LG.FON.05 tem 1 atividade(s) principal(is)';
    expect(verificarCobertura(conteudo, sondagem).join('\n')).toContain(falha);
    // só revisar NÃO resolve, nem 1 principal + várias revisões
    conteudo.atividades.push(atvBase('rev1', ['LG.FON.01'], { revisa: ['LG.FON.05'] }));
    conteudo.atividades.push(atvBase('rev2', ['LG.FON.02'], { revisa: ['LG.FON.05'] }));
    expect(verificarCobertura(conteudo, sondagem).join('\n')).toContain(falha);
    // 2 principais passa
    conteudo.atividades.push(atvBase('a4c', ['LG.FON.05'], { vertentes: ['Charlotte Mason'] }));
    expect(verificarCobertura(conteudo, sondagem)).toEqual([]);
  });
  it('regra 8: principais do marco sem variedade de vertentes', () => {
    const { conteudo, sondagem } = montar();
    // todas iguais: falha
    conteudo.atividades[0] = atvBase('a0a', ['LG.FON.01'], { vertentes: ['Clássico'] });
    conteudo.atividades[1] = atvBase('a0b', ['LG.FON.01'], { vertentes: ['Clássico'] });
    expect(verificarCobertura(conteudo, sondagem).join('\n')).toContain(
      'Marco LG.FON.01: as atividades principais não variam de vertente',
    );
    // mesmo conjunto com 2 vertentes em ambas: ainda falha (todas idênticas)
    const dupla = ['Clássico', 'Charlotte Mason'] as Atividade['vertentes'];
    conteudo.atividades[0] = atvBase('a0a', ['LG.FON.01'], { vertentes: dupla });
    conteudo.atividades[1] = atvBase('a0b', ['LG.FON.01'], { vertentes: dupla });
    expect(verificarCobertura(conteudo, sondagem)).toEqual([
      'Marco LG.FON.01: as atividades principais não variam de vertente (união: Clássico, Charlotte Mason); precisa de pelo menos 2 vertentes e conjuntos diferentes entre elas.',
    ]);
    // 2 vertentes + as mesmas 2 + uma terceira com vertente diferente: passa
    conteudo.atividades.push(atvBase('a0c', ['LG.FON.01'], { vertentes: ['Religioso'] }));
    expect(verificarCobertura(conteudo, sondagem)).toEqual([]);
    conteudo.atividades.pop();
    // conjuntos diferentes: passa
    conteudo.atividades[0] = atvBase('a0a', ['LG.FON.01'], { vertentes: ['Clássico'] });
    expect(verificarCobertura(conteudo, sondagem)).toEqual([]);
  });
  it('regra 9: limites de idade da atividade', () => {
    const { conteudo, sondagem } = montar();
    conteudo.atividades[2] = atvBase('x1', ['LG.FON.02'], { idade: [6, 4] });
    conteudo.atividades[4] = atvBase('x2', ['LG.FON.03'], { idade: [4, 9] });
    conteudo.atividades[6] = atvBase('x3', ['LG.FON.04'], { idade: [1, 4], cuidados: 'ok' });
    const msg = verificarCobertura(conteudo, sondagem).join('\n');
    expect(msg).toContain('Atividade x1 tem idade [6, 4]');
    expect(msg).toContain('Atividade x2 tem idade [4, 9]');
    expect(msg).toContain('Atividade x3 tem idade [1, 4]');
  });
  it('regra 9 (bordas): idades [2, 8] e [3, 3] passam', () => {
    const { conteudo, sondagem } = montar();
    conteudo.atividades[2] = atvBase('b1', ['LG.FON.02'], {
      vertentes: ['Clássico'],
      idade: [2, 8],
      cuidados: 'ok',
    });
    conteudo.atividades[4] = atvBase('b2', ['LG.FON.03'], {
      vertentes: ['Clássico'],
      idade: [3, 3],
      cuidados: 'ok',
    });
    conteudo.marcos[2] = marcoBase(3, { idadeTipica: 3 });
    expect(verificarCobertura(conteudo, sondagem)).toEqual([]);
  });
  it('regra 10: pelo menos uma principal cobre a idade típica do marco', () => {
    const { conteudo, sondagem } = montar();
    conteudo.atividades[0] = atvBase('f1', ['LG.FON.01'], {
      vertentes: ['Clássico'],
      idade: [6, 8],
    });
    conteudo.atividades[1] = atvBase('f2', ['LG.FON.01'], {
      vertentes: ['Charlotte Mason'],
      idade: [6, 8],
    });
    expect(verificarCobertura(conteudo, sondagem)).toEqual([
      'Marco LG.FON.01 tem idade típica 4, mas nenhuma atividade principal cobre essa idade (faixas: f1 [6, 8]; f2 [6, 8]).',
    ]);
    // basta uma cobrir (limite incluído)
    conteudo.atividades[1] = atvBase('f2', ['LG.FON.01'], {
      vertentes: ['Charlotte Mason'],
      idade: [4, 6],
    });
    expect(verificarCobertura(conteudo, sondagem)).toEqual([]);
  });
  it('regra 6c: pré-requisito de outra linha precisa ter formato de id válido', () => {
    const { conteudo, sondagem } = montar();
    conteudo.marcos[2] = marcoBase(3, { preRequisitos: ['LG.LET.3'] });
    conteudo.marcos[3] = marcoBase(4, { preRequisitos: ['lg-let-03'] });
    const msg = verificarCobertura(conteudo, sondagem).join('\n');
    expect(msg).toContain('Marco LG.FON.03 exige "LG.LET.3", que não tem formato de id de marco');
    expect(msg).toContain('Marco LG.FON.04 exige "lg-let-03", que não tem formato de id de marco');
  });
  it('regra 6b: pré-requisito inexistente na própria linha falha', () => {
    const { conteudo, sondagem } = montar();
    conteudo.marcos[2] = marcoBase(3, { preRequisitos: ['LG.FON.99'] });
    expect(verificarCobertura(conteudo, sondagem).join('\n')).toContain(
      'Marco LG.FON.03 exige LG.FON.99, que não existe na linha LG.FON',
    );
  });
  it('regra 4: marco sem item de sondagem', () => {
    const { conteudo, sondagem } = montar();
    const sem = { itens: sondagem.itens.filter((s) => s.marco !== 'LG.FON.06') } as Sondagem;
    expect(verificarCobertura(conteudo, sem).join('\n')).toContain(
      'Marco LG.FON.06 está sem item de sondagem',
    );
  });
  it('regra 5: ordem com buraco ou repetida', () => {
    const { conteudo, sondagem } = montar();
    conteudo.marcos[4] = marcoBase(5, { ordem: 6 });
    conteudo.marcos[5] = marcoBase(6, { ordem: 7 });
    conteudo.marcos[6] = marcoBase(7, { ordem: 8 });
    conteudo.marcos[7] = marcoBase(8, { ordem: 9 });
    expect(verificarCobertura(conteudo, sondagem).join('\n')).toMatch(/quebrada em LG.FON.05/i);
    const repetida = montar();
    repetida.conteudo.marcos[3] = marcoBase(4, { ordem: 3 });
    expect(verificarCobertura(repetida.conteudo, repetida.sondagem).join('\n')).toMatch(
      /quebrada/i,
    );
  });
  it('regra 6: pré-requisito da própria linha com ordem igual ou maior; de outra linha não falha', () => {
    const { conteudo, sondagem } = montar();
    conteudo.marcos[1] = marcoBase(2, { preRequisitos: ['LG.FON.05'] });
    expect(verificarCobertura(conteudo, sondagem).join('\n')).toContain(
      'Marco LG.FON.02 exige LG.FON.05',
    );
    const outra = montar();
    outra.conteudo.marcos[1] = marcoBase(2, { preRequisitos: ['LG.LET.03'] });
    expect(verificarCobertura(outra.conteudo, outra.sondagem)).toEqual([]);
  });
  it('regressão dos ids: faltando ou sobrando marco falha', () => {
    const removido = montar(10);
    removido.conteudo.marcos.splice(4, 1);
    const msg1 = verificarIds(removido.conteudo, IDS_ESPERADOS).join('\n');
    expect(msg1).toContain('O marco LG.FON.05 sumiu da linha LG.FON');
    const renomeado = montar(10);
    renomeado.conteudo.marcos[4] = marcoBase(5, { id: 'LG.FON.15' });
    const msg2 = verificarIds(renomeado.conteudo, IDS_ESPERADOS).join('\n');
    expect(msg2).toContain('O marco LG.FON.05 sumiu da linha LG.FON');
    expect(msg2).toContain('O marco LG.FON.15 sobrou na linha LG.FON');
  });
  it('atividade que cita marco inexistente da linha falha (marcos e revisa)', () => {
    const { conteudo, sondagem } = montar(10);
    conteudo.atividades.push(atvBase('fantasma', ['LG.FON.11']));
    conteudo.atividades.push(atvBase('revisora', ['LG.FON.01'], { revisa: ['LG.FON.12'] }));
    const msg = verificarCobertura(conteudo, sondagem);
    expect(msg).toContain('Atividade fantasma cita o marco LG.FON.11, que não existe.');
    expect(msg).toContain('Atividade revisora cita o marco LG.FON.12, que não existe.');
  });
  it('regra 7: toda atividade da linha precisa de cuidados, qualquer idade inicial', () => {
    const { conteudo, sondagem } = montar();
    const vert = ['Clássico', 'Charlotte Mason'] as const;
    // início aos 4, 6 e 3 anos: sem `cuidados` (ausente ou só espaços) falha
    conteudo.atividades[0] = atvBase('i4', ['LG.FON.01'], {
      vertentes: [vert[0]],
      idade: [4, 6],
      cuidados: undefined,
    });
    conteudo.atividades[1] = atvBase('i6', ['LG.FON.01'], {
      vertentes: [vert[1]],
      idade: [6, 8],
      cuidados: '  ',
    });
    conteudo.atividades[2] = atvBase('i3', ['LG.FON.02'], { idade: [3, 5], cuidados: '' });
    const msg = verificarCobertura(conteudo, sondagem);
    for (const id of ['i4', 'i6', 'i3']) {
      expect(msg).toContain(
        `Atividade ${id} está sem \`cuidados\` (obrigatório em toda atividade de LG.FON).`,
      );
    }
    // com `cuidados` preenchido passam
    conteudo.atividades[0] = atvBase('i4', ['LG.FON.01'], { vertentes: [vert[0]], idade: [4, 6] });
    conteudo.atividades[1] = atvBase('i6', ['LG.FON.01'], { vertentes: [vert[1]], idade: [6, 8] });
    conteudo.atividades[2] = atvBase('i3', ['LG.FON.02'], { idade: [3, 5] });
    expect(verificarCobertura(conteudo, sondagem)).toEqual([]);
  });
});
