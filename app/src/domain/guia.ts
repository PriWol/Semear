// Guia pedagógico das vertentes (#30): validação do conteúdo de content/guia.json.
import { VERTENTES, type Referencia, type Revisao, type Vertente } from './tipos';
import { validarRevisao } from './revisao';

export interface SecaoVertente {
  vertente: Vertente;
  resumo: string;
  principios: string[];
  sessaoTipica: string;
  ritmo: string;
  marcosExtras: string;
  atividades: string;
  /** ids de referencias.json */
  referencias: string[];
  revisao?: Revisao;
}

export interface Guia {
  combinar: { titulo: string; texto: string; exemplos: string[] };
  vertentes: SecaoVertente[];
}

const CAMPOS_TEXTO = ['resumo', 'sessaoTipica', 'ritmo', 'marcosExtras', 'atividades'] as const;

/** Devolve os erros do guia (lista vazia = válido). Dado de fora: confere o formato antes de usar. */
export function validarGuia(guia: Guia, referencias: Referencia[]): string[] {
  const erros: string[] = [];
  const ids = new Set(referencias.map((r) => r.id));
  const vistas = new Set<string>();
  const vazio = (t: unknown) => typeof t !== 'string' || t.trim() === '';

  if (vazio(guia.combinar?.texto)) erros.push('Guia: "combinar" sem texto');
  if (!Array.isArray(guia.combinar?.exemplos) || guia.combinar.exemplos.length === 0)
    erros.push('Guia: "combinar" precisa de exemplos');

  for (const s of guia.vertentes) {
    const onde = `Guia, ${String(s.vertente)}`;
    if (!(VERTENTES as readonly string[]).includes(s.vertente)) {
      erros.push(`${onde}: vertente desconhecida`);
      continue;
    }
    if (vistas.has(s.vertente)) erros.push(`${onde}: seção repetida`);
    vistas.add(s.vertente);
    for (const campo of CAMPOS_TEXTO) {
      if (vazio(s[campo])) erros.push(`${onde}: "${campo}" vazio`);
    }
    if (!Array.isArray(s.principios) || s.principios.length === 0 || s.principios.some(vazio))
      erros.push(`${onde}: "principios" precisa de itens preenchidos`);
    if (!Array.isArray(s.referencias)) erros.push(`${onde}: "referencias" não é uma lista`);
    else
      for (const r of s.referencias)
        if (!ids.has(r)) erros.push(`${onde}: referência "${r}" não existe no catálogo`);
    if (s.revisao !== undefined) validarRevisao(s.revisao, onde, erros);
  }
  for (const v of VERTENTES) if (!vistas.has(v)) erros.push(`Guia: falta a seção de ${v}`);
  return erros;
}
