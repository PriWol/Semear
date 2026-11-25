# 0038. Quadro de verificações humanas e retro semanal

- **Status:** Proposto (altera o ADR 0029: portões humanos e mesclagem automática)
- **Data:** 2026-11-25

## Contexto
O ADR 0029 deu à dona do produto dois portões (estória e conteúdo) e deixou a automação mesclar PRs "de baixo risco".
Na prática ela quer ver o trabalho dos agentes em mais momentos, com **provas** (prints, vídeos, relatório de teste),
e ser quem mescla e confere em produção. O PR #160 foi mesclado com o e2e falhando, o que mostrou o risco de deixar a
automação decidir. Também não havia um lugar único onde ela visse "o que espera por mim".

## Opções consideradas
1. Manter o ADR 0029 e só acrescentar um quadro para visualizar: o quadro mostraria o processo, mas as decisões
   continuariam fora dele.
2. Quadro como **fila de verificações humanas**, uma coluna por verificação, com a automação de mescla desligada: escolhida.
3. Dois portões de evidência seguidos (implementação e resultado de teste): descartada; a segunda verificação
   repetiria a primeira.

## Decisão
- O quadro (GitHub Projects) tem uma coluna por etapa, e cada coluna diz de quem é a vez (detalhes em
  `docs/PROCESSO_AI_SDLC.md`). Há **um cartão por estória**, não por PR.
- Verificações humanas: **Aprovar estória**, **Pergunta para você**, **Aprovar entrega** (com evidência por
  critério de aceite), **Pronto para mesclar** e **Em produção**.
- **Mesclagem automática desligada**: só a dona do produto mescla. O workflow `merge-automatico.yml` é removido.
  O e2e ("Testes ponta a ponta") passa a ser exigido: cartão com e2e vermelho não chega a "Pronto para mesclar".
- A estória só sai de "Aprovar estória" com os critérios de aceite **e o "Como testar"** escritos.
- `bloqueado` continua sendo só o veto de revisão em PR. Perguntas à dona do produto usam `quadro:pergunta`.
- Os cartões se movem por rótulo (`mover-cartao.yml`), com o segredo `PROJECT_TOKEN` (token com escopo `project`,
  expiração de 90 dias) e a variável `PROJECT_NUMBER`. O token só existe no Actions; nenhum agente o recebe.
- **Retro semanal obrigatória** (`/retro`, agendada): os 8 agentes avaliam o próprio trabalho e o processo, medem o que já
  se pode medir e propõem no máximo 3 experimentos, que a dona aprova. É etapa do processo, não opcional. A primeira foi a #169.
  Tudo o que for aprovado entra em `docs/APRENDIZADOS.md`, que todos leem ao começar.

## Consequências
- Mais verificações para ela; em troca há fila visível, limite de 3 cartões em "Aprovar entrega" e a retro mede
  quanto tempo cada coluna dela espera.
- Evidência na primeira versão: relatório do QA por critério e link para o artefato `relatorio-playwright` do CI.
  Pré-visualização do PR e vídeo anexado ficam para uma estória do DevOps.
- Ações dela no GitHub: criar o segredo `PROJECT_TOKEN` e a variável `PROJECT_NUMBER`; deixar o campo Status do quadro
  com os nomes de coluna deste ADR; desligar o fluxo nativo "Item closed → Done" do quadro; incluir "Testes ponta a ponta"
  nas verificações obrigatórias do ruleset "Proteger main".
- **Repositório público:** o segredo não aparece no código nem nos logs, e PR de fork não o recebe. Quem tem escrita (inclusive
  agentes) poderia, numa branch, criar um workflow que lesse segredos de repositório. Por isso o `PROJECT_TOKEN` fica no
  **Environment `quadro`**, com implantação só a partir do `main`, e o `mover-cartao.yml` usa `pull_request_target` (roda o
  arquivo do `main`, sem checkout). Artefatos, prints e vídeos do CI também ficam públicos: a evidência usa só a família de exemplo.
- O workflow não foi exercitado antes do merge (workflows só rodam depois de estarem no `main`).
  Conferir a primeira execução; a retro revisita os rótulos que não moveram cartão.
- Renovar o `PROJECT_TOKEN` a cada 90 dias.
