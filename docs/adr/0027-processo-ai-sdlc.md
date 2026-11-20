# 0027. Processo AI-SDLC com 8 agentes e dois portões humanos

- **Status:** Aceito (altera parcialmente o ADR 0007 e o fluxo do CLAUDE.md)
- **Data:** 2026-11-20

## Contexto
A dona do produto quer participar só de partes do ciclo. Hoje há CI e dois revisores de PR (ADR 0006 e 0007),
mas nenhum agente atua em estória, plano, design, qualidade, conteúdo ou release. O CLAUDE.md e o ADR 0007
exigiam aprovação humana no plano e no merge.

## Opções consideradas
1. Manter aprovação humana em estória, plano, conteúdo e merge: máxima segurança, mas ela vira o gargalo.
2. Portões só em estória e conteúdo, com merge automático de tudo: rápido, mas arriscado, pois o app guarda dados de crianças.
3. Portões em estória e conteúdo, merge automático **apenas** de PRs de baixo risco: escolhida.

## Decisão
**Agentes** (`.claude/agents/`): `pm`, `designer`, `dev-senior-a`, `dev-senior-b`, `qa`,
`curador-pedagogico`, `seguranca-privacidade`, `devops-release`. Os dois devs se revisam; ninguém revisa o próprio PR.

**Portões humanos:** (1) aprovação da estória (rótulo `aprovada`); (2) aprovação do conteúdo pedagógico
(PRs com `app/content/` só são mesclados por ela).

**O que muda nas regras anteriores:**
- Plano técnico: aprovado por Dev B e Designer; a dona do produto vê só o resumo (substitui o passo 2 do CLAUDE.md).
- Merge: automático somente com CI verde, sem rótulo `bloqueado`/`conteudo`/`decisao`, revisores concluídos
  e sem tocar `app/content/`, `app/src/dados/`, CSP, `.github/`, `CLAUDE.md` ou `docs/adr/`.
  O resto continua exigindo a aprovação dela (mantém o ADR 0007 nesses casos).
- Teste manual no site vira relatório do QA; ela pode reabrir a estória.
- Segurança e Privacidade tem poder de veto (`bloqueado`).

**Mecanismo:** Claude Code (`/ciclo`) e GitHub Actions (`ciclo-agentes.yml`, `revisao-agentes.yml`, `merge-automatico.yml`).
Rótulos colocados pelo `GITHUB_TOKEN` não disparam workflows, então só quem tem permissão de escrita aciona `ideia` e `aprovada`.

## Consequências
- Exige segredo `CLAUDE_CODE_OAUTH_TOKEN` ou `ANTHROPIC_API_KEY`, "Allow auto-merge" ligado no repositório e
  ajuste do ruleset "Proteger main": a exigência de aprovação humana precisa sair para os PRs elegíveis ao merge automático
  (ou ela aprova só os sensíveis por CODEOWNERS nos caminhos acima). Sem isso, nenhum PR mescla sozinho.
- Os workflows só rodam depois de existirem no `main`; este PR não os exercita.
- Custo de tokens por estória aumenta; revisar após as primeiras fases.
- Agentes erram: a rede de segurança são os testes, o CI, o veto de segurança e os caminhos sensíveis reservados a ela.
