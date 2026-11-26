// Lê o JSON do Playwright e escreve, no resumo do CI, os testes instáveis (falharam e passaram na repetição). ADR 0039.
// Uso: node resumo-e2e-instaveis.mjs <resultados.json>  (o texto sai na saída padrão; o workflow anexa ao GITHUB_STEP_SUMMARY)
// Só escreve nome do teste, projeto (desktop/celular) e arquivo; nunca mensagem de erro nem variável de ambiente.
import { readFileSync } from 'node:fs';

export function coletarInstaveis(relatorio) {
  const achados = [];
  const visitar = (suite, caminho) => {
    const titulo = suite.title && !suite.file ? [...caminho, suite.title] : caminho;
    for (const spec of suite.specs ?? []) {
      for (const t of spec.tests ?? []) {
        const tentativas = t.results ?? [];
        const passouNoFim = tentativas.at(-1)?.status === 'passed';
        const falhouAntes = tentativas
          .slice(0, -1)
          .some((r) => r.status !== 'passed' && r.status !== 'skipped');
        if (t.status === 'flaky' || (passouNoFim && falhouAntes)) {
          achados.push({
            arquivo: spec.file ?? suite.file ?? '',
            nome: [...titulo, spec.title].join(' > '),
            projeto: t.projectName ?? '?',
          });
        }
      }
    }
    for (const filha of suite.suites ?? []) visitar(filha, titulo);
  };
  for (const s of relatorio.suites ?? []) visitar(s, []);
  return achados;
}

// Texto de tabela Markdown: sem barras verticais, crases, tags nem quebras de linha vindas do título.
const limpar = (s) =>
  String(s)
    .replace(/[|\r\n`<>]/g, ' ')
    .trim();

export function montarResumo(achados) {
  if (achados.length === 0) return '### Testes instáveis\nNenhum teste instável encontrado.\n';
  const linhas = achados.map(
    (a) => `| ${limpar(a.nome)} | ${limpar(a.projeto)} | ${limpar(a.arquivo)} |`,
  );
  return [
    '### Testes instáveis',
    `${achados.length} teste(s) falharam na 1ª tentativa e passaram na 2ª. Abra uma issue com o rótulo \`e2e-instavel\` e a causa. O trace está no artefato \`relatorio-playwright\`.`,
    '',
    '| Teste | Aparelho | Arquivo |',
    '|---|---|---|',
    ...linhas,
    '',
  ].join('\n');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  let texto;
  try {
    texto = montarResumo(coletarInstaveis(JSON.parse(readFileSync(process.argv[2], 'utf8'))));
  } catch {
    texto = '### Testes instáveis\nNão foi possível ler o relatório JSON do Playwright.\n';
  }
  process.stdout.write(texto);
}
