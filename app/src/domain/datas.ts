// Funções de data puras: recebem "hoje" como parâmetro para serem testáveis.

/**
 * Idade em anos com uma casa decimal (ex.: 5.5), pelo calendário: anos completos (o aniversário
 * conta no próprio dia) mais a fração do ano desde o último aniversário, arredondada para baixo.
 */
export function idadeEmAnos(nascimento: string, hoje: Date): number {
  const [a, m, d] = nascimento.split('-').map(Number);
  if (!a || !m || !d) throw new Error(`Data de nascimento inválida: ${nascimento}`);
  const dia = (ano: number, mes: number, diaMes: number) => Date.UTC(ano, mes - 1, diaMes);
  const hojeUtc = dia(hoje.getFullYear(), hoje.getMonth() + 1, hoje.getDate());
  let anos = hoje.getFullYear() - a;
  if (hojeUtc < dia(hoje.getFullYear(), m, d)) anos--;
  const ultimo = dia(a + anos, m, d);
  const proximo = dia(a + anos + 1, m, d);
  const fracao = (hojeUtc - ultimo) / (proximo - ultimo);
  return Math.floor((anos + fracao) * 10 + 1e-9) / 10;
}

export function idadeInteira(nascimento: string, hoje: Date): number {
  return Math.floor(idadeEmAnos(nascimento, hoje));
}

export function diasEntre(isoA: string, isoB: string): number {
  return Math.abs(new Date(isoB).getTime() - new Date(isoA).getTime()) / 86_400_000;
}

/** Data local do aparelho em AAAA-MM-DD (ex.: para o campo de data e o "hoje"). */
export function dataLocalISO(data: Date): string {
  const mm = String(data.getMonth() + 1).padStart(2, '0');
  const dd = String(data.getDate()).padStart(2, '0');
  return `${data.getFullYear()}-${mm}-${dd}`;
}

/** DD/MM/AAAA no fuso do aparelho. Uma sessão criada às 22h é do dia local, não do dia em UTC. */
export function dataBR(iso: string): string {
  const [a, m, d] = dataLocalISO(new Date(iso)).split('-');
  return `${d}/${m}/${a}`;
}
