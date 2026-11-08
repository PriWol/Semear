import { describe, expect, it } from 'vitest';
import { linhasParaRessondar, SEMANAS_SEM_MUDAR } from '../src/domain/ressondagem';
import { carregarConteudoBruto, carregarSondagem } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import { pistasDaCrianca } from '../src/domain/jornada';
import type { EstadosCrianca } from '../src/domain/tipos';
import { crianca, familia } from './fabricas';

const idx = criarIndice(carregarConteudoBruto());
const sondagem = carregarSondagem();
const AGORA = '2026-11-09T12:00:00.000Z';
const dias = (n: number) => new Date(new Date(AGORA).getTime() - n * 86_400_000).toISOString();
const reg = (estado: 'em-desenvolvimento' | 'consolidado', quando: string) => ({
  estado,
  atualizadoEm: quando,
  origem: 'manual' as const,
});
const pistas = pistasDaCrianca(idx, familia(), crianca()).filter((p) =>
  ['LG.FON', 'MA.SEN'].includes(p.linha.id),
);
const motivos = (estados: EstadosCrianca, criadaEm = dias(200)) =>
  Object.fromEntries(
    linhasParaRessondar(idx, pistas, sondagem, estados, criadaEm, AGORA).map((r) => [
      r.pista.linha.id,
      r.motivo,
    ]),
  );

describe('ressondagem das linhas paradas (#18, §5.5)', () => {
  it('8 semanas é o limite', () => {
    expect(SEMANAS_SEM_MUDAR).toBe(8);
  });
  it('linha parada: marco em desenvolvimento sem mudar há 8 semanas ou mais', () => {
    const e: EstadosCrianca = {
      'LG.FON.04': reg('em-desenvolvimento', dias(56)),
      'MA.SEN.06': reg('em-desenvolvimento', dias(55)),
    };
    expect(motivos(e)['LG.FON']).toBe('parada');
    expect(motivos(e)['MA.SEN']).toBeUndefined(); // 55 dias: ainda não
  });
  it('um registro recente em qualquer marco da linha tira a linha da lista', () => {
    const e: EstadosCrianca = {
      'LG.FON.03': reg('consolidado', dias(3)),
      'LG.FON.04': reg('em-desenvolvimento', dias(90)),
    };
    expect(motivos(e)['LG.FON']).toBeUndefined();
  });
  it('linha sem observação: nenhum registro e família com 8 semanas ou mais', () => {
    expect(motivos({}, dias(60))['LG.FON']).toBe('sem-observacao');
    expect(motivos({}, dias(10))['LG.FON']).toBeUndefined(); // família nova
  });
  it('linha toda consolidada não precisa de ressondagem', () => {
    const e: EstadosCrianca = Object.fromEntries(
      idx.marcosDaLinha('LG.FON').map((m) => [m.id, reg('consolidado', dias(100))]),
    );
    expect(motivos(e)['LG.FON']).toBeUndefined();
  });
  it('só considera linhas que têm item de sondagem', () => {
    const todas = pistasDaCrianca(idx, familia(), crianca());
    const r = linhasParaRessondar(idx, todas, sondagem, {}, dias(200), AGORA);
    expect(r.map((x) => x.pista.linha.id).sort()).toEqual(['LG.FON', 'MA.SEN']);
  });
});
