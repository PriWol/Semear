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

/** Data real no formato AAAA-MM-DD (recusa 2026-02-30 e 31/12/2026). */
export function dataValida(texto: string): boolean {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(texto);
  if (!m) return false;
  const [ano, mes, dia] = [Number(m[1]), Number(m[2]), Number(m[3])];
  const d = new Date(Date.UTC(ano, mes - 1, dia));
  return d.getUTCFullYear() === ano && d.getUTCMonth() === mes - 1 && d.getUTCDate() === dia;
}

/** Idade máxima aceita no cadastro: irmãos maiores ainda cabem, mas além disso é erro de digitação (D18). */
export const IDADE_MAXIMA_CADASTRO = 18;

export type ProblemaNascimento = 'formato' | 'futuro' | 'antigo';

export const MENSAGEM_NASCIMENTO: Record<ProblemaNascimento, string> = {
  formato: 'Informe uma data de nascimento que exista no calendário.',
  futuro: 'A data de nascimento não pode ser no futuro.',
  antigo: `A data de nascimento indica mais de ${IDADE_MAXIMA_CADASTRO} anos. Confira o ano.`,
};

/**
 * Por que uma data de nascimento é impossível, ou null se for plausível. Bloqueia só o impossível:
 * formato falso (ano 0001, 31/02), futuro, ou mais de 18 anos. Fora de 2 a 8 anos continua permitido,
 * só com aviso (decisão #71 e D18); por isso esta regra não olha `faixa.ts`.
 */
export function problemaDeNascimento(nascimento: string, hoje: Date): ProblemaNascimento | null {
  if (!dataValida(nascimento)) return 'formato';
  if (nascimento > dataLocalISO(hoje)) return 'futuro';
  // 19 anos completos já é "mais de 18"; quem tem 18 e alguns meses ainda cabe (irmão mais velho).
  return idadeInteira(nascimento, hoje) > IDADE_MAXIMA_CADASTRO ? 'antigo' : null;
}

export function nascimentoPlausivel(nascimento: string, hoje: Date): boolean {
  return problemaDeNascimento(nascimento, hoje) === null;
}
