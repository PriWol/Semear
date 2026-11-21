// Nomes dos ícones de linha fina (ADR 0034). Fica em domain/ para a validação do conteúdo
// (`dominios.json` guarda o NOME do ícone) não depender de ui/. Os desenhos estão em ui/icones.ts.
export const NOMES_ICONE = [
  'plant',
  'check-circle',
  'books',
  'compass',
  'book-open',
  'printer',
  'download-simple',
  'arrow-square-out',
  'floppy-disk',
  'note-pencil',
  'hourglass',
  'clock',
  'target',
  'eye',
  'arrows-clockwise',
  'basket',
  'warning',
  'leaf',
  'gift',
  'chat-circle-text',
  'calculator',
  'translate',
  'heart',
  'palette',
  'tree',
  'person-simple',
] as const;

export type NomeIcone = (typeof NOMES_ICONE)[number];

/** Dado de fora (conteúdo, backup): só nomes do conjunto passam; qualquer outra coisa é recusada. */
export function ehNomeDeIcone(valor: unknown): valor is NomeIcone {
  return typeof valor === 'string' && (NOMES_ICONE as readonly string[]).includes(valor);
}
