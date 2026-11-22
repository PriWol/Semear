// Estilo do conteúdo (#147, ADR 0037): a nota interna "conferência por profissional pendente" não
// pode ficar dentro dos textos que a família lê; o estado vive em `revisao.conferenciaProfissional` e
// a tela mostra um selo único.
import { describe, expect, it } from 'vitest';
import { carregarConteudoBruto } from '../src/conteudo';
import type { Conteudo, Revisao } from '../src/domain/tipos';
import { atividade, conteudoBase, marco } from './fabricas';

/** Frases internas que não devem aparecer nos textos visíveis. */
export const FRASES_PROIBIDAS = [
  /confer[êe]ncia por profissional( de sa[úu]de)?( ainda)? pendente/i,
  /orienta[çc][ãa]o ainda sem confer[êe]ncia/i,
];

export interface Achado {
  item: string;
  campo: string;
  conferenciaProfissional: boolean;
}

function textosDe(valor: unknown, caminho: string, saida: [string, string][]): void {
  if (typeof valor === 'string') saida.push([caminho, valor]);
  else if (Array.isArray(valor)) valor.forEach((v, i) => textosDe(v, `${caminho}[${i}]`, saida));
  else if (typeof valor === 'object' && valor !== null)
    for (const [k, v] of Object.entries(valor)) {
      if (k === 'revisao' || k === 'id') continue; // o registro de revisão não é texto de família
      textosDe(v, caminho ? `${caminho}.${k}` : k, saida);
    }
}

/** Procura a frase interna em todos os textos de marcos e atividades. */
export function acharFrasesInternas(c: Pick<Conteudo, 'marcos' | 'atividades'>): Achado[] {
  const achados: Achado[] = [];
  const itens: { id: string; revisao?: Revisao }[] = [...c.marcos, ...c.atividades];
  for (const item of itens) {
    const textos: [string, string][] = [];
    textosDe(item, '', textos);
    for (const [campo, texto] of textos) {
      if (FRASES_PROIBIDAS.some((f) => f.test(texto)))
        achados.push({
          item: item.id,
          campo,
          conferenciaProfissional: item.revisao?.conferenciaProfissional !== undefined,
        });
    }
  }
  return achados;
}

describe('estilo do conteúdo: nota de conferência nos textos', () => {
  it('detecta a frase em marcos e atividades (e só ali)', () => {
    const c = conteudoBase({
      marcos: [
        marco('LG.FON.01', 1, {
          orientacaoPais: {
            porQueImporta: 'ok',
            comoParticipar: 'ok',
            sinaisDeAtencao: 'Converse com o pediatra. Conferência por profissional pendente.',
            referencias: [],
          },
        }),
      ],
      atividades: [
        atividade('a1', ['LG.FON.01'], {
          cuidados: 'Orientação ainda sem conferência por profissional.',
        }),
        atividade('a2', ['LG.FON.01'], { cuidados: 'Fique junto.' }),
      ],
    });
    expect(acharFrasesInternas(c).map((a) => a.item)).toEqual(['LG.FON.01', 'a1']);
  });

  // AVISO por ora: ~230 itens ainda trazem a frase. Depois da migração do conteúdo (script
  // app/scripts/migrar-conferencia.mjs, leva do Curador) este teste passa a FALHAR se restar alguma:
  // troque o console.warn por `expect(achados).toEqual([])`.
  it('lista (aviso, não falha) os itens do conteúdo real que ainda trazem a frase', () => {
    const achados = acharFrasesInternas(carregarConteudoBruto());
    if (achados.length > 0) {
      const itens = new Set(achados.map((a) => a.item));
      console.warn(
        `[estilo-conteudo] ${itens.size} itens ainda trazem a nota de conferência no texto ` +
          `(migrar para revisao.conferenciaProfissional, ADR 0037): ${[...itens].slice(0, 10).join(', ')}…`,
      );
    }
    expect(Array.isArray(achados)).toBe(true);
  });

  // JÁ falha: item que tem o campo não repete a nota no texto (seria o aviso duplicado).
  it('item com conferenciaProfissional não pode ter a frase no texto', () => {
    const duplicados = acharFrasesInternas(carregarConteudoBruto()).filter(
      (a) => a.conferenciaProfissional,
    );
    expect(duplicados).toEqual([]);
  });

  it('o teste pega o duplicado quando existe', () => {
    const c = conteudoBase({
      marcos: [marco('LG.FON.01', 1)],
      atividades: [
        atividade('a1', ['LG.FON.01'], {
          cuidados: 'Conferência por profissional pendente.',
          revisao: {
            estado: 'aprovado',
            por: 'P',
            em: '2026-11-08',
            conferenciaProfissional: { estado: 'pendente' },
          },
        }),
      ],
    });
    expect(acharFrasesInternas(c).filter((a) => a.conferenciaProfissional)).toHaveLength(1);
  });
});
