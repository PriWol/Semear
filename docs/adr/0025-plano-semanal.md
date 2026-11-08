# 0025. Plano semanal guardado no aparelho

- **Status:** Aceito
- **Data:** 2026-11-08

## Contexto
As estórias #8 e #9 pedem o plano da semana de cada criança (várias sessões em dias escolhidos, sem repetir atividade) e a impressão da semana inteira num documento só.

## Decisão
- **Distribuidor puro** (`domain/semana.ts`): reaproveita o gerador de sessão (§5.6) dia a dia. O que já entrou na semana vira histórico simulado, para as linhas se alternarem, e vai para `excluir` (novo campo do pedido de sessão), para nenhuma atividade se repetir. Determinístico: `agora` e o id do plano vêm de fora.
- **Armazenamento:** nova loja `planos` no IndexedDB, **versão 2 do banco**, com migração testada (um banco v1 ganha a loja e mantém os dados). O plano entra no backup como campo opcional `planos`: backups anteriores continuam valendo, e quando o campo existe é validado inteiro (dias, datas, listas). `removerCrianca` e `apagarExemplo` também apagam os planos.
- **Rotina por criança:** `Crianca.rotina` guarda dias e duração para não escolher toda semana.
- **Dia feito:** marcar cria uma sessão no histórico (a mesma de "Preparar sessão") e liga o dia a ela; desmarcar apaga a sessão.
- **Imprimir a semana** (`pacote/semana.ts`): um único documento, com a mesma CSP e CSS do pacote de sessão. Começa pela lista de materiais da semana (cada item uma vez, com os dias), separa por dia e traz uma ficha por sessão. Opções: tudo, só as folhas da criança ou só roteiros e fichas. O arquivo se chama `semear-semana-<criança>-<data>.html`.

## Consequências
- O app antigo (versão 1 do banco) não abre um banco já migrado para a versão 2 (`VersionError`); por isso, antes de testar, faça o backup (ver `docs/ROADMAP.md`, "Como uma estória vira algo testável").
- Fica para depois: o modo tablet com navegação por dia, e a sessão conjunta de irmãos.
- Com pouco conteúdo publicado, algumas crianças terão dias sem atividade; o app mostra "Sem atividade neste dia".
