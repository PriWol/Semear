# 0036. Gerador de sessão v2

- **Status:** Aceito (etapa 1: duração e mistura de áreas); as etapas 2 e 3 estão em #146 (regra de idade, ponto de partida, ritmo calmo/ativo)
- **Data:** 2026-11-22

## Contexto
O Dev Sênior B e os três QAs mediram o sugestor de sessões (`domain/sessao.ts`, §5.6) com o conteúdo real em 21/11/2026 (estória #138, relatório QA3-17 a QA3-20). O modo "Equilibrado" de 30 minutos não equilibrava:
- a primeira atividade entrava **sempre**, qualquer que fosse a duração (`cabe || escolhas.length === 0`); aos 4 anos saía 1 atividade de 25 min, aos 5 uma de 35 min, aos 6 a 8 uma de 26 min;
- a escolha ignorava a duração; só pontuava vertente, idade e novidade;
- o rodízio era por **linha**, e no empate (criança sem histórico) valia a ordem do arquivo: a consciência fonológica (LG.FON) abria toda sessão e levava o tempo todo; pacotes de 4 a 7 páginas só de Linguagem;
- o aviso "tem 25 min, mais do que os 20 escolhidos" aparecia mesmo havendo atividade mais curta.

A dona do produto aprovou as recomendações do time (D4 e D5 em #138). Esta etapa 1 cobre só duração e mistura; ela não muda conteúdo nem a regra de idade.

## Opções consideradas
1. **Só cortar a primeira atividade longa:** corrige o caso extremo, mas deixa a fonologia abrir todas as sessões e não limita o resto.
2. **Teto de duração por idade + rodízio por domínio + semente do dia** (escolhida): ataca as duas causas (duração e ordem fixa) com regras puras e testáveis.
3. **Sorteio:** mistura, mas a mesma entrada deixaria de dar a mesma sessão (§5.6 exige determinismo) e não se testaria.

## Decisão
Opção 2, tudo em funções puras de `src/domain/sessao.ts`, com constantes nomeadas:

**Duração por atividade.**
- Teto suave por idade inteira (D5): 2 anos até 10 min, 3 anos 12, 4 anos 15, 5 a 6 anos 20, 7 a 8 anos 25; Charlotte Mason nunca passa de 20 (§3 fala em lições de 10 a 20 min). 2 anos já era regra do ADR 0021. São regra prática de rotina, sem fonte citável.
- A **primeira atividade também precisa caber** no tempo (com a folga de 10% de sempre). A próxima é a melhor pontuada que caiba no que resta.
- Cada atividade é classificada em quatro níveis: **0** cabe, está no teto e não passa da parcela (metade do tempo; 30% para menores de 4 anos, o que dá 4 a 6 blocos curtos em 30 min); **1** cabe e está no teto, mas passa da parcela; **2** passa do teto; **3** não cabe no tempo. O nível 0 preenche primeiro; o 1 só entra depois de outra atividade.
- Atividade acima do teto (nível 2) só entra se for a **única possível**: com a sessão ainda vazia, entra a mais curta que caiba no tempo e no teto; se nenhuma serve, a mais curta de todas. Ela fica sozinha e a tela mostra um aviso com o teto da idade. O aviso "mais do que os M min" só aparece quando mesmo a mais curta não cabe: o gerador **troca antes de avisar**.
- No modo equilibrado, uma complementar (§3.0) entra se couber no tempo e no teto; com a sessão vazia ela passa na frente do último recurso.

**Mistura de áreas.**
- Rodízio por **domínio**: em cada rodada entra no máximo uma atividade por domínio, e quem tem menos atividades na sessão vai primeiro (um domínio não consome o tempo antes de os outros terem a vez). Dentro do domínio vem primeiro a linha com menos atividades já escolhidas.
- No modo equilibrado, as linhas empatadas em "minutos trabalhados" giram por uma **semente determinística** (FNV-1a de `data (AAAA-MM-DD) | id da linha`), em vez da ordem do arquivo. Mesma entrada, mesma saída; dia diferente, linha diferente abre a sessão. O histórico continua mandando: a linha menos trabalhada vem antes.
- Com linhas de foco escolhidas à mão a ordem é a da educadora, e o rodízio por domínio vale dentro dela.

**Retrocompatibilidade.** Nada muda nos dados gravados: `Sessao` e `PlanoSemana` não ganham campos, e sessões já gravadas continuam abrindo. O plano semanal usa o mesmo gerador; qual linha abre cada dia passa a depender da data (a ordem fixa "Linguagem primeiro" deixou de valer).

**Fora desta etapa (#146).** Regra nova de idade (D4: peso graduado, exclusão aos 2 anos acima, menores de 3 anos), ponto de partida pela idade para criança sem sondagem (D6), penalidade por `idadeIntroducao` da vertente e o ritmo calma, ativa, calma (campo `energia`, depende do Curador).

## Consequências
- Medição com o conteúdo real (5 vertentes x 7 idades x criança posicionada ou sem sondagem x 20/30/40/60 min, 280 sessões; `tests/sugestor-conteudo.test.ts`). Sessão de 30 min, criança posicionada pela idade:

  | Idade | Antes | Depois |
  |---|---|---|
  | 2 anos | 3 atividades (até 24 min) | 5 a 6 blocos de até 9 min |
  | 3 anos | 2 a 3 (até 24 min) | 6 blocos de até 8 min |
  | 4 anos | 1 a 2 (1 sozinha de 25 min) | 2, de até 15 min |
  | 5 anos | 1 sozinha de 35 min, com aviso | 3, de até 15 min |
  | 6 anos | 1 sozinha de 25 a 26 min | 2, de até 15 min |
  | 7 anos | 1 sozinha de 20 min | 2, de até 15 min |
  | 8 anos | 1 sozinha de 25 min | 2, de até 20 min |

  Nas 280 sessões: soma acima de 110% do tempo, 36 antes e 0 depois; sessões de uma atividade só, 90 antes e 10 depois (20 min aos 7 e 8 anos, por falta de atividade curta no conteúdo); sessões de 30 min com menos de 2 domínios, 36 de 70 antes e 0 depois; nenhuma sessão de 30 min com uma única atividade de mais de 20 min.
- O teste de propriedades vai falhar se o conteúdo futuro quebrar uma regra; ele também serve de lista de trabalho do Curador (cerca de 45 atividades acima do teto: C3-4).
- O botão "Trocar" (`proximaAlternativa`) continua percorrendo as candidatas da linha em ciclo, sem olhar o teto; a etapa 2 pode refiná-lo.
- Os tetos podem ser revistos pela dona do produto: são constantes em um só lugar (`TETOS_DURACAO_POR_IDADE`).
