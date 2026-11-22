// Relatório para a migração da nota de conferência (#147, ADR 0037). SOMENTE LÊ: não escreve em
// app/content/. Lista os arquivos e os itens (marcos e atividades) que ainda trazem a frase interna
// ("conferência por profissional pendente", "Orientação ainda sem conferência...") dentro do texto.
// Uso (dentro de app/):  node scripts/migrar-conferencia.mjs [--json]
//
// Para cada item listado, a leva de conteúdo faz duas coisas: (1) tira a frase do texto (mantendo o
// cuidado concreto e "não substitui o pediatra" onde fizer parte da orientação) e (2) acrescenta
// "conferenciaProfissional": { "estado": "pendente" } dentro de "revisao" (criando "revisao" se
// faltar; o estado de revisão do item segue o que a dona do produto decidir).
import { readdirSync, readFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = fileURLToPath(new URL('../content', import.meta.url));
const FRASES = [
  /confer[êe]ncia por profissional( de sa[úu]de)?( ainda)? pendente/i,
  /orienta[çc][ãa]o ainda sem confer[êe]ncia/i,
];

function jsons(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory()
      ? jsons(join(dir, e.name))
      : e.name.endsWith('.json')
        ? [join(dir, e.name)]
        : [],
  );
}

/** Caminhos dos campos de texto que têm a frase. */
function achar(valor, caminho, saida) {
  if (typeof valor === 'string') {
    if (FRASES.some((f) => f.test(valor))) saida.push(caminho);
  } else if (Array.isArray(valor)) {
    valor.forEach((v, i) => achar(v, `${caminho}[${i}]`, saida));
  } else if (valor && typeof valor === 'object') {
    for (const [k, v] of Object.entries(valor)) {
      if (k !== 'revisao') achar(v, caminho ? `${caminho}.${k}` : k, saida);
    }
  }
}

/** Itens de um arquivo: { marcos: [...] } (vários itens) ou uma atividade solta (um item). */
function itensDoArquivo(dados) {
  if (dados && typeof dados === 'object' && typeof dados.id === 'string') return [dados];
  if (Array.isArray(dados?.marcos)) return dados.marcos.filter((m) => typeof m === 'object');
  return [];
}

const relatorio = [];
for (const arquivo of jsons(raiz)) {
  const dados = JSON.parse(readFileSync(arquivo, 'utf8'));
  for (const item of itensDoArquivo(dados)) {
    const campos = [];
    achar(item, '', campos);
    if (campos.length > 0) {
      relatorio.push({
        arquivo: relative(raiz, arquivo),
        id: item.id,
        campos,
        jaTemConferenciaProfissional: item.revisao?.conferenciaProfissional !== undefined,
      });
    }
  }
}

if (process.argv.includes('--json')) {
  console.log(JSON.stringify(relatorio, null, 2));
} else {
  const arquivos = new Set(relatorio.map((r) => r.arquivo));
  for (const r of relatorio) {
    const marca = r.jaTemConferenciaProfissional ? ' [já tem o campo: tirar só a frase]' : '';
    console.log(`${r.arquivo}\t${r.id}\t${r.campos.join(', ')}${marca}`);
  }
  console.log(`\n${relatorio.length} itens em ${arquivos.size} arquivos ainda trazem a frase.`);
}
