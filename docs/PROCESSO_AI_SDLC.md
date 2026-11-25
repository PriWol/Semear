# Processo AI-SDLC do Semear

Decisão e motivos: [ADR 0038](adr/0038-quadro-de-verificacoes-humanas.md) (que altera o [ADR 0029](adr/0029-processo-ai-sdlc.md)).
Agentes em `.claude/agents/`. O quadro é o GitHub Projects "Semear: fila da dona": **um cartão por estória**.

## O quadro
| # | Coluna | De quem é a vez | O que entrega ao sair |
|---|---|---|---|
| 1 | **Backlog** | **Você** | Problema descrito no modelo do formulário "Problema" |
| 2 | **Detalhando** | PM | Estória com problema, critérios de aceite e **Como testar** |
| 3 | **Aprovar estória** | **Você** | Você aprova (rótulo `aprovada`) ou devolve com comentário |
| 4 | **Em desenvolvimento** | Dev A/B, Designer, QA, Curador, Segurança | PR revisado, e2e verde, plano e testes feitos |
| 5 | **Pergunta para você** | **Você** | Você responde; o cartão volta à coluna 4 |
| 6 | **Testando** | QA | Relatório com a prova de cada critério |
| 7 | **Aprovar entrega** | **Você** | Você confere critérios, prints, vídeos e relatório |
| 8 | **Pronto para mesclar** | **Você** | Você mescla o PR |
| 9 | **Em produção** | **Você** | Você confere o site publicado e conclui |
| | **Feito** | | |

Conteúdo pedagógico (rótulo `conteudo`): na coluna 7 vem junto o resumo do Curador, e a mescla é sua, como sempre.

> Repositório público: prints, vídeos e artefatos do CI são públicos. A evidência usa só a família de exemplo, nunca dados reais.

## Regras do acordo
1. O agente só move o cartão para uma coluna sua com o trabalho pronto e um **resumo de 3 linhas**: o que mudou, o que conferir
   e o que acontece se você aprovar ou recusar.
2. Cartão parado numa coluna sua **não avança**. Nenhum agente aprova ou mescla em seu nome.
3. Toda entrega traz a **prova de cada critério de aceite** (relatório por critério, link do artefato `relatorio-playwright`
   do CI e, quando houver, print ou vídeo). Critério sem teste não passa na estória.
4. Você devolve com um comentário; o agente responsável retoma dali e o cartão volta à coluna certa.
5. Máximo de **3 cartões** em "Aprovar entrega". O resto espera em "Testando".
6. **Mesclagem só sua.** O e2e ("Testes ponta a ponta") precisa estar verde para o cartão chegar a "Pronto para mesclar".
7. Depois de mesclar, o cartão vai para "Em produção". Se o site tiver problema, o cartão volta para "Em desenvolvimento" com o
   rollback do DevOps (reverter o merge) e a estória ganha o critério que faltou.
8. Estória com rótulo `decisao`, quando a decisão for sua, fica em "Pergunta para você" e só fecha depois que a resposta
   estiver registrada na própria estória.

## Como o cartão se move (rótulos)
| Rótulo na estória | Coluna |
|---|---|
| (estória nova) | Backlog |
| `ideia` | Detalhando |
| `aguardando-aprovacao` | Aprovar estória |
| `aprovada` | Em desenvolvimento |
| `quadro:pergunta` | Pergunta para você |
| `quadro:testando` | Testando |
| `quadro:aprovar-entrega` | Aprovar entrega |
| `quadro:pronto` | Pronto para mesclar |
| (PR com `Closes #N` mesclado) | Em produção |
| `quadro:feito` | Feito |

Quem aplica: o PM (`ideia` → `aguardando-aprovacao`), você (`aprovada`), o Dev B ao fechar as revisões (`quadro:testando`),
o QA ao entregar a evidência (`quadro:aprovar-entrega`), você ao aprovar a entrega (`quadro:pronto`) e depois da conferência em
produção (`quadro:feito`). Qualquer agente pode abrir `quadro:pergunta` com a pergunta numa linha.
`bloqueado` continua só para veto de revisão em PR (segurança ou QA) e não move cartão.

## Quem faz o quê
| Agente | Faz | Edita |
|---|---|---|
| `pm` | estória, critérios, Como testar, ROADMAP | issues, ROADMAP, spec |
| `designer` | desenho e revisão visual | DESIGN.md, prototipos/, CSS |
| `dev-senior-a` | testes primeiro, código, PR | `app/` |
| `dev-senior-b` | plano técnico, ADR, revisão de PR | `app/`, ADRs |
| `qa` | casos de teste antes, evidência por critério, roteiro de produção | `app/tests`, `app/e2e` |
| `curador-pedagogico` | conteúdo e orientação aos pais | `app/content/` |
| `seguranca-privacidade` | revisão com veto | nada (só comenta) |
| `devops-release` | CI, release, rollback, workflows | `.github/`, ADRs |

## Modelo "Como testar" (vai no corpo da estória, escrito pelo QA no rascunho do PM)
```
Onde: iPhone/Safari | impressão A4 | leitor de tela | desktop
Antes de começar: estado necessário (ex.: família com criança de 5 anos)
Passos: 1. ... 2. ...
Esperado: por critério de aceite (CA1, CA2...)
Sinal de problema: o que mostra que falhou
Já coberto pelo e2e: o que não precisa testar à mão
Resultado: passou | falhou (como, em qual aparelho)
```

## Resumo de 3 linhas (a cada passagem para uma coluna sua)
```
Mudou: ...
Conferir: ...
Se aprovar / se recusar: ...
```

## Retro semanal
O comando `/retro` (agendado) mede o processo, junta o que cada agente observou e abre uma issue "Retro AAAA-MM-DD" com
no máximo 3 experimentos para você aprovar. O que for aprovado vai para `docs/APRENDIZADOS.md`. Mudanças de regra passam por ADR.

## Configuração única (ações suas no GitHub)
1. Segredo `CLAUDE_CODE_OAUTH_TOKEN` (ou `ANTHROPIC_API_KEY`) em Settings → Secrets → Actions.
2. Settings → Environments → **New environment** `quadro`, com *Deployment branches* só `main`. Nele, o segredo `PROJECT_TOKEN`
   (token classic com escopo `project`, 90 dias); apague o mesmo segredo se ele existir no nível do repositório. Variável
   `PROJECT_NUMBER` (número do quadro) pode ficar no repositório.
3. Campo Status do quadro com os nomes de coluna acima; desligar o fluxo nativo "Item closed → Done".
4. Ruleset "Proteger main": incluir "Testes ponta a ponta" nas verificações obrigatórias; a mescla é manual.
5. Rótulos: `ideia`, `aguardando-aprovacao`, `aprovada`, `conteudo`, `ui`, `dados`, `decisao`, `bloqueado`,
   `quadro:pergunta`, `quadro:testando`, `quadro:aprovar-entrega`, `quadro:pronto`, `quadro:feito`.
6. Os workflows só passam a valer depois de mesclados no `main`.

## Se os agentes falharem em cerca de 1 segundo
PR aberto por um agente do ciclo sai como `claude[bot]`; o `revisao-agentes.yml` aceita só esse bot
(`allowed_bots: 'claude'`). Sem isso os 4 revisores falham em ~1 s com "non-human actor".

Falha rápida, sem turno e com custo zero costuma ser a credencial recusada pela API. Ligue `show_full_output: true`
no passo da ação por uma rodada para ler a mensagem. `401 Invalid API key` significa segredo inválido: se houver os
dois (`CLAUDE_CODE_OAUTH_TOKEN` e `ANTHROPIC_API_KEY`), apague o que não usa. Depois de corrigir, desligue o
`show_full_output`, porque o log completo mostra a conversa do agente.
