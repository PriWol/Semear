// Família de exemplo (#39): dados fictícios para demonstrar e testar o app sem cadastrar nada.
// Função pura: recebe o conteúdo e a data de hoje, então as idades nunca "envelhecem".
import type { IndiceConteudo } from './conteudo';
import { dataLocalISO } from './datas';
import { posicionarAqui } from './jornada';
import { gerarCodigoSessao } from './sessao';
import type { Atividade, Crianca, EstadosCrianca, Familia, Sessao } from './tipos';

export interface DadosExemplo {
  familia: Familia;
  criancas: Crianca[];
  estados: { criancaId: string; estados: EstadosCrianca }[];
  sessoes: Sessao[];
}

interface Modelo {
  id: string;
  nome: string;
  anos: number;
  meses: number;
  /** linha → marco onde a criança "está" */
  posicoes: Record<string, string>;
}

const ANA: Modelo = {
  id: 'exemplo-ana',
  nome: 'Ana',
  anos: 5,
  meses: 4,
  posicoes: { 'LG.FON': 'LG.FON.04', 'MA.SEN': 'MA.SEN.06' },
};
const THEO: Modelo = {
  id: 'exemplo-theo',
  nome: 'Theo',
  anos: 7,
  meses: 3,
  posicoes: { 'LG.FON': 'LG.FON.05', 'MA.SEN': 'MA.SEN.07' },
};
const MODELOS = [ANA, THEO];

const DIA = 86_400_000;

/** Volta anos e meses no calendário, sem cair num dia inexistente (ex.: 31 de fevereiro). */
function nascimentoPara(hoje: Date, anos: number, meses: number): string {
  const total = hoje.getFullYear() * 12 + hoje.getMonth() - anos * 12 - meses;
  const ano = Math.floor(total / 12);
  const mes = total % 12;
  const ultimoDia = new Date(ano, mes + 1, 0).getDate();
  return dataLocalISO(new Date(ano, mes, Math.min(hoje.getDate(), ultimoDia)));
}

export function criarExemplo(idx: IndiceConteudo, hoje: Date): DadosExemplo {
  const agora = hoje.toISOString();
  const familia: Familia = {
    educador: 'Marina',
    vertentePrincipal: 'Montessori',
    inspiracoes: ['Charlotte Mason'],
    idiomasEducador: [],
    criadaEm: agora,
    exemplo: true,
  };

  const criancas: Crianca[] = MODELOS.map((m) => ({
    id: m.id,
    nome: m.nome,
    nascimento: nascimentoPara(hoje, m.anos, m.meses),
    letra: null,
    trilhas: [],
    exemplo: true,
  }));

  // A jornada foi posicionada há duas semanas, como faria uma família que já usa o app.
  const posicionadoEm = new Date(hoje.getTime() - 14 * DIA).toISOString();
  const estados = MODELOS.map((m) => {
    let atual: EstadosCrianca = {};
    for (const [linhaId, marcoId] of Object.entries(m.posicoes)) {
      const linha = idx.linha(linhaId);
      // Se o conteúdo mudar e o marco sumir, a linha fica sem posição em vez de quebrar o exemplo.
      if (!linha || !idx.marco(marcoId)) continue;
      atual = { ...atual, ...posicionarAqui(idx, { linha }, marcoId, atual, posicionadoEm) };
    }
    return { criancaId: m.id, estados: atual };
  });

  // Primeiro as atividades dos marcos em que a criança está; depois as das mesmas linhas (revisão).
  // Nunca uma atividade de outra trilha: quem usa o exemplo para entender o app veria uma incoerência.
  const daCrianca = (m: Modelo): Atividade[] => {
    const dosMarcos = Object.values(m.posicoes).flatMap((marcoId) =>
      idx.atividadesDoMarco(marcoId),
    );
    const dasLinhas = Object.keys(m.posicoes).flatMap((linhaId) => idx.atividadesDaLinha(linhaId));
    return [...new Set([...dosMarcos, ...dasLinhas])];
  };
  const planos: { modelo: Modelo; atividade: Atividade | undefined; diasAtras: number }[] = [
    { modelo: ANA, atividade: daCrianca(ANA)[0], diasAtras: 10 },
    { modelo: THEO, atividade: daCrianca(THEO)[0], diasAtras: 6 },
    { modelo: ANA, atividade: daCrianca(ANA)[1], diasAtras: 3 },
  ];

  const sessoes: Sessao[] = [];
  for (const { modelo, atividade, diasAtras } of planos) {
    if (!atividade) continue;
    const criadaEm = new Date(hoje.getTime() - diasAtras * DIA);
    const codigo = gerarCodigoSessao(
      modelo.nome,
      criadaEm,
      sessoes.map((s) => s.codigo),
    );
    sessoes.push({
      id: `exemplo-sessao-${sessoes.length + 1}`,
      codigo,
      criancaId: modelo.id,
      criadaEm: criadaEm.toISOString(),
      duracaoMin: atividade.duracaoMin,
      foco: 'equilibrado',
      atividadeIds: [atividade.id],
      livroId: null,
      exemplo: true,
    });
  }

  return { familia, criancas, estados, sessoes };
}
