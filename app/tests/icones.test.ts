import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { carregarConteudoBruto } from '../src/conteudo';
import { validarConteudo } from '../src/domain/conteudo';
import { NOMES_ICONE, ehNomeDeIcone } from '../src/domain/icones';
import { HtmlSeguro, html } from '../src/ui/html';
import { ICONES, icone } from '../src/ui/icones';
import { conteudoBase } from './fabricas';

// Ícones de linha fina (#130, ADR 0034): Phosphor regular copiado como SVG, sem dependência.
function arquivos(dir: string): string[] {
  return readdirSync(dir).flatMap((nome) => {
    const caminho = join(dir, nome);
    return statSync(caminho).isDirectory() ? arquivos(caminho) : [caminho];
  });
}
const raizSrc = new URL('../src', import.meta.url).pathname;
const raizApp = new URL('..', import.meta.url).pathname;

describe('icone()', () => {
  it('é decorativo por padrão: aria-hidden, sem foco, currentColor, tamanho por classe', () => {
    const s = icone('plant');
    expect(s).toBeInstanceOf(HtmlSeguro);
    expect(s.valor).toContain('<svg');
    expect(s.valor).toContain('class="icone"');
    expect(s.valor).toContain('aria-hidden="true"');
    expect(s.valor).toContain('focusable="false"');
    expect(s.valor).toContain('fill="currentColor"');
    expect(s.valor).toContain('viewBox="0 0 256 256"');
    expect(s.valor).not.toContain('role=');
    expect(s.valor).not.toContain('aria-label');
  });

  it('com rótulo vira imagem nomeada (role="img" + aria-label), sem aria-hidden', () => {
    const s = icone('printer', { rotulo: 'Imprimir' }).valor;
    expect(s).toContain('role="img"');
    expect(s).toContain('aria-label="Imprimir"');
    expect(s).not.toContain('aria-hidden');
  });

  it('escapa o rótulo (texto do usuário nunca vira HTML)', () => {
    const s = icone('plant', { rotulo: '"><script>alert(1)</script>' }).valor;
    expect(s).not.toContain('<script>');
    expect(s).toContain('&quot;&gt;&lt;script&gt;');
  });

  it('tamanho grande usa a classe icone-g', () => {
    expect(icone('plant', { tamanho: 'g' }).valor).toContain('class="icone icone-g"');
  });

  it('nome desconhecido (dado de fora) falha em segurança: nada na tela, sem lançar erro', () => {
    for (const ruim of ['', 'nao-existe', '🌱', '<img src=x onerror=alert(1)>', '__proto__']) {
      expect(() => icone(ruim)).not.toThrow();
      expect(icone(ruim).valor).toBe('');
    }
  });

  it('compõe dentro de html`` sem ser escapado de novo', () => {
    expect(html`<b>${icone('plant')}</b>`.valor).toContain('<svg');
  });
});

describe('inventário de ícones', () => {
  it('o mapa tem exatamente os nomes de domain/icones.ts, todos só com <path>', () => {
    expect(Object.keys(ICONES).sort()).toEqual([...NOMES_ICONE].sort());
    for (const nome of NOMES_ICONE) {
      expect(ICONES[nome], nome).toMatch(/^(<path [^>]*\/>)+$/);
      expect(ICONES[nome], nome).not.toMatch(/script|on\w+=|href|style/i);
    }
  });

  it('ehNomeDeIcone só aceita nomes do conjunto', () => {
    expect(ehNomeDeIcone('plant')).toBe(true);
    expect(ehNomeDeIcone('constructor')).toBe(false);
    expect(ehNomeDeIcone(42)).toBe(false);
  });

  it('todo icone("nome") literal usado no código existe no mapa', () => {
    const usados = new Set<string>();
    for (const arq of arquivos(raizSrc).filter((a) => a.endsWith('.ts'))) {
      for (const m of readFileSync(arq, 'utf8').matchAll(/\bicone\(\s*'([a-z-]+)'/g)) {
        usados.add(m[1]!);
      }
    }
    expect(usados.size).toBeGreaterThan(15);
    for (const nome of usados) expect(ehNomeDeIcone(nome), nome).toBe(true);
  });

  it('todo ícone do mapa é usado (nada de SVG sobrando no app)', () => {
    const codigo = arquivos(raizSrc)
      .filter((a) => a.endsWith('.ts') && !a.endsWith('icones.ts'))
      .map((a) => readFileSync(a, 'utf8'))
      .join('\n');
    const dominios = JSON.stringify(carregarConteudoBruto().dominios);
    for (const nome of NOMES_ICONE) {
      const usado = codigo.includes(`'${nome}'`) || dominios.includes(`"${nome}"`);
      expect(usado, nome).toBe(true);
    }
  });
});

describe('domínios com ícone por nome', () => {
  it('o conteúdo real usa só nomes conhecidos', () => {
    for (const d of carregarConteudoBruto().dominios) {
      expect(ehNomeDeIcone(d.icone), d.id).toBe(true);
    }
  });

  it('a validação recusa ícone fora do conjunto (inclusive emoji ou HTML)', () => {
    for (const ruim of ['🗣️', '<b>', 'nao-existe', '']) {
      const c = conteudoBase();
      c.dominios[0]!.icone = ruim;
      const erros = validarConteudo(c).erros;
      expect(
        erros.some((e) => e.includes('ícone')),
        ruim,
      ).toBe(true);
    }
  });
});

describe('licença dos ícones (MIT exige o aviso em toda cópia)', () => {
  it('app/public/LICENCAS-TERCEIROS.md traz o copyright e o texto da licença', () => {
    const texto = readFileSync(join(raizApp, 'public', 'LICENCAS-TERCEIROS.md'), 'utf8');
    expect(texto).toContain('Copyright (c) 2023 Phosphor Icons');
    expect(texto).toContain('Permission is hereby granted, free of charge');
    expect(texto).toContain('THE SOFTWARE IS PROVIDED "AS IS"');
  });
});

describe('emoji de interface (ADR 0034)', () => {
  // Emojis que são conteúdo (ficha "circule", atividades) ou texto (☐ ✓ ○) ficam de fora desta regra.
  // `src/pacote/` é o documento impresso: tem as próprias regras e não entra aqui.
  const EMOJI = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B50}\u{23E9}-\u{23FF}\u{2197}\u{2B07}]/u;
  const PERMITIDOS = /[☐✓○]/gu;

  it('telas, componentes e index.html não têm emoji como ícone', () => {
    const alvos = [
      ...arquivos(join(raizSrc, 'pages')),
      ...arquivos(join(raizSrc, 'ui')),
      join(raizApp, 'index.html'),
    ].filter((a) => /\.(ts|html|css)$/.test(a));
    const achados: string[] = [];
    for (const arq of alvos) {
      readFileSync(arq, 'utf8')
        .split('\n')
        .forEach((linha, i) => {
          if (EMOJI.test(linha.replace(PERMITIDOS, ''))) achados.push(`${arq}:${i + 1}`);
        });
    }
    expect(achados).toEqual([]);
  });
});
