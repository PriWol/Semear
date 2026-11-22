# 0036. Gerador de sessão v2

- **Status:** Aceito (etapa 1: duração e mistura de áreas; adendo de 2026-11-22: etapas 2 e 3, regra de idade, ponto de partida pela idade e vertente); o ritmo calma, ativa, calma segue em #146
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

**Fora desta etapa.** Regra de idade, ponto de partida pela idade e vertente: ver o adendo abaixo. O ritmo calma, ativa, calma (campo `energia`, depende do Curador) segue em #146.

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

## Adendo (2026-11-22): etapas 2 e 3, regra de idade, ponto de partida e vertente (#146)
A dona do produto aprovou as recomendações D4 e D6 (#138). Tudo continua em funções puras de `src/domain/`
(`idade-sugestao.ts` é novo; `sessao.ts` e `jornada.ts` mudam), com constantes nomeadas e documentadas. Sem migração:
`Sessao` e `PlanoSemana` não ganham campos e nada é gravado pelas regras novas.

**Regra de idade (D4): peso graduado, não filtro** (`adequacaoDeIdade`, `filtrarForaDaFaixa`).
- Dentro da faixa da atividade: +2 e um bônus de até +0,5 pela proximidade ao centro (só desempate).
- Criança mais velha que o máximo: -2 por ano até 2 anos; passando disso, -6.
- Atividade que começa acima da criança: -3 por ano; **exclusão dura** quando começa 2 anos ou mais acima.
- **Menores de 3 anos nunca recebem** atividade cuja faixa começa aos 3 ou mais, mesmo sem alternativa (ADR 0021: só as atividades da faixa pequena trazem cuidados e tempo curto).
- Fora da faixa só entra se a linha não tem alternativa dentro dela: mais de 1 ano fora, nunca havendo alternativa; **até 1 ano fora, só com o `ajustes` do lado certo** (`dificil` para a criança menor, `facil` para a maior; regra do Curador), e então a proposta mostra "Versão mais simples/mais exigente: ..." com o texto do ajuste. Sem alternativa e sem ajuste, entra com "Pouco comum para esta idade". A nota "versão..." só existe com `ajustes`, como pedido.
- Fora da faixa **não é nível 0 ("ideal")**: entra na segunda passada do preenchimento, depois de quem serve à idade. Exceção: enquanto a sessão tem menos de 2 domínios, um domínio ainda sem atividade pode usar uma atividade fora da faixa (mantém a meta de 2 domínios em 30 min).
- Se todas as candidatas de uma linha são excluídas pela idade, a linha vira `lacuna` com `motivo: 'idade'` e a proposta avisa "Sem atividade adequada para N anos em: ...". As complementares seguem a mesma regra (antes eram filtro rígido). A faixa é lida em anos fracionados, como `idadeEmAnos` já devolve.
- O botão **Trocar** (`proximaAlternativa`, também no plano da semana) só oferece quem passa por essas regras (as candidatas já vêm filtradas) e cabe no teto de duração (novo parâmetro `teto`; a tela não mostra o botão se não há opção).

**Ponto de partida pela idade (D6)** (`marcoDePartidaPelaIdade`, `posicaoParaSugestao`). Numa linha **sem nenhum registro** (nem um "não observado" marcado de propósito) a sugestão parte de um ponto provisório, em memória: o último marco com `idadeTipica` até 6 meses abaixo da idade (ou igual a ela); sem marco nessa janela, o de `idadeTipica` mais próxima, e no empate o mais fácil. Os marcos anteriores contam como consolidados só nesse cálculo. A tela avisa "X ainda não foi posicionada em <linhas>: usamos a idade (N anos) como ponto de partida", só das linhas que deram atividade à sessão. A jornada continua com `posicaoDaLinha`; nela, o marco ativo com `idadeTipica` mais de 1,5 ano acima da idade ganha `aindaCedo` e o aviso "Ainda cedo para esta linha", sem bloquear. A leitura de "preferindo o último marco até 6 meses abaixo" é nossa: o Dev B escreveu "≤ idade - 0,5", a D6 e o Curador, "mais próxima"; adotamos a janela [idade - 0,5; idade], depois o mais próximo.

**Vertente (F).** Se **todos** os marcos ativos que levam à atividade são anteriores à `idadeIntroducao` da vertente principal, ela perde 4 pontos (mais que o +3 da vertente, para a atividade Waldorf com folha de ligar sílabas não abrir a sessão de 5 anos) e a escolha traz o aviso da §5.3. Um marco que a vertente já aceita basta para não penalizar. Só a vertente principal conta.

**Medições** (conteúdo real, `tests/sugestor-conteudo.test.ts`; 5 vertentes x 7 idades x 4 durações x {posicionada, sem sondagem} = 280 sessões "Equilibrado"; e as 7 idades x todas as linhas, Montessori, 30 min, com foco numa linha só):

| Medida | Antes | Depois |
|---|---|---|
| Fora da faixa, equilibrado, posicionada | 16 de 484 (3,3%) | 5 de 465 (1,1%) |
| Fora da faixa, equilibrado, sem sondagem | 247 de 616 (40,1%) | 20 de 479 (4,2%) |
| Fora da faixa, equilibrado, as 280 sessões | 263 de 1100 (23,9%) | 25 de 944 (2,6%) |
| Fora da faixa, foco numa linha, posicionada | 21 de 284 (7,4%) | 13 de 275 (4,7%) |
| Fora da faixa, foco numa linha, sem sondagem | 255 de 465 (54,8%) | 14 de 319 (4,4%) |
| Atividade que começa 2+ anos acima / de 3+ para menor de 3 (equilibrado) | 0 / 0 | 0 / 0 (garantido por regra e por teste unitário) |
| Sem sondagem, 30 min: a primeira atividade está fora da faixa | 20 de 35 (15 a mais de 1 ano; até 4 anos) | 0 de 35 |
| Sem sondagem: atividades diferentes abrindo as 7 idades | 2 (a mesma de 4 a 8 anos) | 6 |
| Lacunas por idade (linha sem atividade adequada) | 0 | 80 nas 280 sessões (sempre as mesmas 2 linhas aos 2 anos: AR.NAT e LG.ESC); 2 no foco numa linha |
| Sessões de 30 min com 2 atividades e 2 domínios | 35 de 35 | 35 de 35 |
| Sessões de uma atividade só (de 280) | 10 | 15 (as 5 a mais são sem sondagem aos 7 e 8 anos) |

O teste de propriedades passou a exigir: nenhuma atividade que começa 2 anos ou mais acima, nenhuma de 3+ para menor de 3, fora da faixa em até 3% das sugestões "Equilibrado", primeira atividade sem sondagem diferente por idade e a no máximo 1 ano da faixa, determinismo, e em 30 min pelo menos 2 atividades e 2 domínios "quando houver" (contando só atividades que servem à idade). O foco numa linha só tem um teto de 6% (4,5% medido): o que sobra é falta de conteúdo para 7 e 8 anos (por exemplo EM.REG aos 8 anos só tem uma atividade, de 5 a 7), lista de trabalho do Curador (lote 4 e auditoria de `ajustes`, C2-7).

**Consequências do adendo.**
- Mais lacunas visíveis: hoje só aos 2 anos (AR.NAT e LG.ESC só têm atividade a partir dos 3 ou 4 anos). Aos 7 e 8 anos a falta de conteúdo aparece como atividade 1 ano fora da faixa com nota, não como lacuna. É o efeito desejado da D4: a tela diz por quê em vez de forçar uma atividade inadequada.
- A regra "até 1 ano fora só com `ajustes`" depende de o Curador preencher `ajustes` (C2-7). Enquanto são poucos, atividades 1 ano fora sem ajuste só entram se a linha não tem outra; quando a auditoria sair, a regra libera mais opções sem mudar o código.
- As notas de idade e de vertente aparecem na tela da sessão; **o pacote impresso ainda não as mostra** (fica para depois, junto de S2-5).
- As constantes (`PENALIDADE_*`, `ANOS_EXCLUSAO_ACIMA`, `TOLERANCIA_FORA_DA_FAIXA`, `ANOS_ABAIXO_PREFERIDO`, `ANOS_AINDA_CEDO`, `PENALIDADE_ANTES_DA_INTRODUCAO`) ficam em um só lugar e podem ser revistas pela dona do produto.
- **Continua fora:** ritmo calma, ativa, calma (campo `energia`, depende de o Curador marcar cerca de 440 atividades) e a regra do idioma (S2-4).
