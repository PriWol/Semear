import { describe, expect, it } from 'vitest';
import { nascimentoPlausivel, problemaDeNascimento } from '../src/domain/datas';
import { criancaPadrao } from '../src/domain/criancas';
import { familiaSemNome } from '../src/domain/pendencias';

// D18: bloqueia só o impossível (formato falso, futuro, mais de 18 anos); o resto só avisa no formulário.
const HOJE = new Date(2026, 10, 22, 12); // 22/11/2026, horário local

describe('nascimentoPlausivel', () => {
  it('aceita datas reais dentro de 18 anos, inclusive fora de 2 a 8 anos', () => {
    expect(nascimentoPlausivel('2021-03-15', HOJE)).toBe(true);
    expect(nascimentoPlausivel('2026-11-22', HOJE)).toBe(true); // nasceu hoje
    expect(nascimentoPlausivel('2026-06-01', HOJE)).toBe(true); // 0 anos: só avisa
    expect(nascimentoPlausivel('2012-01-01', HOJE)).toBe(true); // 14 anos: só avisa
    expect(nascimentoPlausivel('2008-11-22', HOJE)).toBe(true); // faz 18 hoje
  });

  it('recusa data no futuro', () => {
    expect(problemaDeNascimento('2099-01-01', HOJE)).toBe('futuro');
    expect(problemaDeNascimento('2026-11-23', HOJE)).toBe('futuro');
  });

  it('recusa mais de 18 anos', () => {
    expect(problemaDeNascimento('2008-11-21', HOJE)).toBe('antigo'); // 18 anos e 1 dia
    expect(problemaDeNascimento('2000-03-15', HOJE)).toBe('antigo');
    expect(problemaDeNascimento('1900-01-01', HOJE)).toBe('antigo');
  });

  it('recusa formato falso, inclusive o ano 0001 e dias que não existem', () => {
    expect(problemaDeNascimento('0001-01-01', HOJE)).toBe('formato');
    expect(problemaDeNascimento('0000-01-01', HOJE)).toBe('formato');
    expect(problemaDeNascimento('2021-02-30', HOJE)).toBe('formato');
    expect(problemaDeNascimento('15/03/2021', HOJE)).toBe('formato');
    expect(problemaDeNascimento('', HOJE)).toBe('formato');
  });
});

describe('criancaPadrao (D19)', () => {
  const velha = { id: 'theo' };
  const nova = { id: 'ana' };
  const sessao = (criancaId: string, criadaEm: string) => ({ criancaId, criadaEm });

  it('é a criança da sessão mais recente, não a mais velha da lista', () => {
    const sessoes = [sessao('theo', '2026-11-01T10:00:00Z'), sessao('ana', '2026-11-20T10:00:00Z')];
    expect(criancaPadrao([velha, nova], sessoes)).toBe(nova);
  });

  it('ignora sessão de criança que não existe mais', () => {
    expect(criancaPadrao([velha, nova], [sessao('fantasma', '2026-11-30T10:00:00Z')])).toBe(velha);
  });

  it('sem sessões, usa a primeira da lista; sem crianças, null', () => {
    expect(criancaPadrao([velha, nova], [])).toBe(velha);
    expect(criancaPadrao([], [sessao('ana', '2026-11-20T10:00:00Z')])).toBeNull();
  });
});

describe('familiaSemNome (D12)', () => {
  it('nome vazio ou só espaços é pendência', () => {
    expect(familiaSemNome({ educador: '' })).toBe(true);
    expect(familiaSemNome({ educador: '  ' })).toBe(true);
    expect(familiaSemNome({ educador: 'Priscila' })).toBe(false);
  });
});
