# 0005. Conteúdo curado em JSON versionado e validado por testes

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto

Marcos, atividades e livros serão escritos por IA + revisão humana (especificação §7) e vão crescer
para centenas de itens. Um erro de conteúdo (marco inexistente, resposta fora das opções) quebra o app
ou confunde a família.

## Decisão

O conteúdo fica em `app/content/` como arquivos JSON, versionados no Git e embutidos no build.
Um validador puro (`validarConteudo`) roda nos testes e na tela "Conteúdo":

- **erros** (quebram o app) fazem o CI falhar;
- **avisos** (conteúdo incompleto) aparecem para a curadoria, sem bloquear.

## Consequências

- Todo conteúdo novo passa por PR e por revisão, com histórico de quem mudou o quê.
- Não há painel de edição: a curadoria edita JSON (ou pede à IA). Um editor visual pode vir depois.
- O conteúdo sai junto com cada versão do app (sem atualização separada).
