// Funções de data puras: recebem "hoje" como parâmetro para serem testáveis.

/** Idade em anos com uma casa decimal (ex.: 5.5), calculada a partir de AAAA-MM-DD. */
export function idadeEmAnos(nascimento: string, hoje: Date): number {
  const [a, m, d] = nascimento.split('-').map(Number);
  if (!a || !m || !d) throw new Error(`Data de nascimento inválida: ${nascimento}`);
  const nasc = new Date(Date.UTC(a, m - 1, d));
  const hojeUtc = Date.UTC(hoje.getFullYear(), hoje.getMonth(), hoje.getDate());
  const dias = (hojeUtc - nasc.getTime()) / 86_400_000;
  return Math.floor((dias / 365.25) * 10) / 10;
}

export function idadeInteira(nascimento: string, hoje: Date): number {
  return Math.floor(idadeEmAnos(nascimento, hoje));
}

export function diasEntre(isoA: string, isoB: string): number {
  return Math.abs(new Date(isoB).getTime() - new Date(isoA).getTime()) / 86_400_000;
}
