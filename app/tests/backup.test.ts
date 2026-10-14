import { describe, expect, it } from 'vitest';
import { precisaLembreteBackup } from '../src/domain/backup';

const AGORA = '2026-10-14T12:00:00.000Z';
const real = { exemplo: undefined };
const deExemplo = { exemplo: true as const };

describe('lembrete de backup', () => {
  it('sem crianças, não lembra', () => {
    expect(precisaLembreteBackup([], null, AGORA)).toBe(false);
  });

  it('criança real e nenhum backup: lembra', () => {
    expect(precisaLembreteBackup([real], null, AGORA)).toBe(true);
  });

  it('mais de 30 dias desde o último backup: lembra; até 30, não', () => {
    expect(precisaLembreteBackup([real], '2026-09-10T12:00:00.000Z', AGORA)).toBe(true); // 34 dias
    expect(precisaLembreteBackup([real], '2026-09-20T12:00:00.000Z', AGORA)).toBe(false); // 24 dias
  });

  it('só crianças do exemplo (fictícias): não lembra', () => {
    expect(precisaLembreteBackup([deExemplo, deExemplo], null, AGORA)).toBe(false);
  });

  it('uma criança real cadastrada durante o exemplo já pede backup', () => {
    expect(precisaLembreteBackup([deExemplo, deExemplo, real], null, AGORA)).toBe(true);
  });
});
