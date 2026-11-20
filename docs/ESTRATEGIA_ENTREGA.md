# Estratégia de entrega do Semear

Revisão do PM em 20/11/2026, a pedido da dona do produto. Cobre as 40 estórias abertas (todas com o rótulo `ideia`).
Nada foi alterado nas estórias nem nos rótulos: este documento é uma **proposta** para ela decidir.
Como li o código: conferi a existência de arquivos, ADRs e testes; **não** rodei o app nem auditei tela por tela.
Atualizado em 20/11/2026 depois de o `main` receber os ADRs 0027 (assinatura) e 0028 (app nativo e lembretes), o código de lembretes e os cadernos na Release. O texto das estórias no GitHub não foi relido nesta atualização (sem acesso); onde falo dele, é o que consta da revisão anterior.

## 1. Resumo executivo

1. O plano está **bem mais adiantado do que o GitHub mostra**: 12 das 40 estórias já têm código, ADR ou teste no `main` e só precisam ser conferidas e fechadas.
2. O que **falta de verdade** no núcleo é pouco e é a peça mais importante: **#11 Registrar a sessão** (sem ela o ciclo "preparar, imprimir, aplicar, registrar" não fecha e o selo "parece pronto" não existe no código).
3. O **conteúdo** é o maior trabalho que sobra: as linhas de Linguagem e Matemática têm 7 a 8 marcos cada e poucas atividades (cerca de 15), e o domínio de Línguas não tem marcos. Aqui o gargalo é o portão 2 (a aprovação dela).
4. **#3, #5, #6 e #26** (conta, pagamento, saída da conta, servidor) conflitam com a regra "dados da criança ficam no aparelho" e com o ADR 0010. Não são "estórias para fazer", são **decisões de negócio**. Proponho tratá-las juntas, depois do núcleo.
5. O modelo de assinatura agora tem um ADR próprio, o **0027** (R$ 49,90 para 1 criança e R$ 69,90 para 2 ou mais, teste de 7 dias, depois plano Livre reduzido), mas ele **ainda diverge** da decisão dela de 20/11 (seção 9) e de textos antigos (detalhes na linha #75 da tabela). O preço **não foi confirmado por ela**. Nenhuma estória de cobrança deve começar antes de ela fechar o plano básico e o preço.
6. **Mudar de endereço (#34) apaga os dados das famílias** no navegador (cada endereço tem seu banco). Fazer isso cedo, quando quase ninguém usa, é barato; depois do lançamento, é caro.
7. Proposta de 5 ondas: (0) arrumar a casa, (1) fechar o ciclo da sessão, (2) conteúdo de lançamento, (3) pronto para abrir, (4) conta e cobrança. Lançamento (v1.0) só depois da onda 4.
8. Atenção que ela precisa dar: cerca de **1 hora por semana** em média, concentrada em dois tipos de tarefa: ler/aprovar estórias (portão 1) e revisar lotes de conteúdo (portão 2).
9. Maior risco de custo: os agentes (ADR 0029) multiplicam o gasto de tokens por estória. Recomendo começar com **uma estória por vez** na onda 1 e medir.
10. Há decisões que só ela pode tomar (seção 7); a nova mais urgente é o **lembrete do #95**: ela decidiu `.ics` (20/11), mas o ADR 0028 já escolheu app nativo com notificação local e parte do código está no `main`.

## 2. Veredito por estória

Tamanho: P (pequeno, poucas horas de agente), M (médio), G (grande). Rótulos sugeridos entre parênteses.

| # | Título | Veredito | Evidência / justificativa | Tam. |
|---|---|---|---|---|
| 2 | Página principal | Reescrever | Parte 1 existe (`pages/inicio.ts`, cartão por criança, aviso de ressondagem). Falta só "sessões feitas na semana + próxima ação". Reduzir o escopo ao que falta. | P |
| 3 | Criar login | Unir com #26 | Depende do servidor; descreve cartão no cadastro (decisão 30 da especificação), superada pelo ADR 0010. | (G) |
| 4 | Landing page | Reescrever | Já há boas-vindas com passo a passo (commit 080889f); o app não mostra preço nem prazo de teste. O texto da estória ("30 dias", preço por criança) diverge do ADR 0027 e da decisão de 20/11. Reescrever depois de fechar #75 (plano básico e preço). | M |
| 5 | Página de pagamento | Reescrever | Pede "30 dias" e preço "por criança" contado no servidor; o ADR 0027 usa **faixa declarada** (1 criança ou 2+) e teste de 7 dias. Só faz sentido depois de #75 e #26; a cobrança dentro do app de loja (ADR 0028) pode mudar o preço por plataforma. | G |
| 6 | Logout | Unir com #26 | Hoje não há conta, então não há o que sair. A pergunta "apagar dados ao sair?" volta na decisão de #26. | P |
| 8 | Visualizar plano semanal | Já entregue (fechar) | ADR 0025, `domain/semana.ts`, `pages/semana.ts`, `e2e/semana.spec.ts`. | |
| 9 | Imprimir a semana | Já entregue (fechar) | ADR 0025, `pacote/semana.ts`, modo tablet (commit 2f7d507). | |
| 10 | Guardar evidências (fotos) | Adiar | Já rebaixada ("Depois"). Muda o formato de dados e o backup; só depois do lançamento. | G |
| 11 | Informar progresso | **Manter (prioridade 1)** | Não há tela de registro nem selo "parece pronto" no código (busca sem resultados). O tipo `origem: 'sessao'` já existe em `domain/tipos.ts`. Rótulos: `ui`, `dados`. | M |
| 12 | Acervo de livros digitais | Já entregue (fechar) | ADR 0016, `app/content/acervo.json` e `livros.json`, `pages/acervo.ts`, `e2e/acervo.spec.ts`. Ela confirma a curadoria. | |
| 13 | Atividades avulsas | Já entregue (fechar) | Commit 2fe838c, `domain/busca.ts`, `pages/atividades.ts`, `e2e/atividades.spec.ts`. | |
| 15 | Jornada do usuário | Reescrever | Vaga: "documentar" não tem critério verificável. Transformar em "roteiro de teste ponta a ponta do educador" (vira os e2e do QA). | P |
| 17 | Sondagem inicial | Dividir | Entregue para LG.FON e MA.SEN (commit 5440436, `domain/sondagem.ts`, `e2e/sondagem.spec.ts`). O que falta (outras linhas) vira parte do conteúdo #22. Fechar a #17 e abrir item de conteúdo. | P |
| 18 | Ressondagem a cada 8 semanas | Já entregue (fechar) | Commit 6a278e0, `domain/ressondagem.ts`, aviso em `pages/inicio.ts`. | |
| 19 | Sessão de irmãos | Adiar | Decisão 48 da especificação já adiou. Não afeta o afterschooling no dia 1. | G |
| 20 | Portfólio trimestral | Adiar | Depende de #29 (validação jurídica) e de #10. | G |
| 21 | Pipeline de conteúdo com IA | Reescrever | Não existe `content/prompts/`. Hoje o papel é do agente `curador-pedagogico` (ADR 0029). Reduzir a: briefings versionados + checklist do Curador + roteiro de revisão dela. | P |
| 22 | Lote Linguagem e Matemática | Manter | Marcos: LG 30, MA 41; atividades ~15. LG.FON tem 7 marcos (critério: 8 a 12). Foco real: **atividades** e revisão. Rótulo `conteudo`. | G |
| 23 | Línguas (inglês, francês, latim) | Dividir | O domínio LI existe sem marcos (`marcos/` só tem EM, LG, MA). Inglês vira o primeiro item (o caderno de inglês, ADR 0026, agora vai à Release com PR #97 e #98, mas não é a trilha no app). Francês e latim adiados. | M + adiar |
| 24 | Banco de ilustrações | Decisão pendente | Encomendar ou licenciar é decisão de custo e licença (ela). Hoje as folhas usam emoji. | G |
| 25 | Termos e política (LGPD) | Dividir | Política de privacidade em rascunho já está no app (`pages/privacidade.ts`), que já avisa que será atualizada quando houver conta e assinatura. Termos de uso e a revisão jurídica dependem do modelo de cobrança (#75) e, se houver app de loja, das regras das lojas e da notificação (ADR 0028). | M |
| 26 | Backend de contas | Decisão pendente | Fere a regra de privacidade se guardar mais que conta e assinatura. Exige ADR aprovado por ela. Absorve #3 e #6. | G |
| 27 | Sincronização entre aparelhos | Adiar | Já fora do caminho do lançamento; exige criptografia de ponta a ponta e ADR próprio. | G |
| 28 | Piloto 3 a 5 famílias | Reescrever | Decisão de 16/10: lançar aberto, piloto vira acompanhamento. Reescrever como "acompanhar os primeiros usuários" e decidir se faz um piloto pequeno antes (pergunta 5). | M |
| 29 | Validação jurídica | Adiar | Só bloqueia o portfólio (#20). Ação de fora do código (advogado); pode começar quando ela quiser. | P |
| 32 | CSP no app | Já entregue (fechar) | ADR 0022, `public/previa.html`, `e2e/csp.spec.ts`. | |
| 34 | Domínio próprio | Decisão pendente | Ação dela (comprar e apontar o domínio). Trocar o endereço **perde os dados locais** das famílias: exige aviso e backup. Faz mais sentido antes da abertura. | P |
| 41 | Visual novo no app | Já entregue (fechar) | ADR 0014, `docs/DESIGN.md`, `app/src/tokens.css`. Pedir ao Designer uma conferência rápida antes de fechar. | |
| 42 | Visual novo nas folhas | Já entregue (fechar) | Mesmas evidências; ficha em 1 página testada (`e2e/ficha-uma-pagina.spec.ts`). Mesma conferência. | |
| 71 | Faixa de 2 a 8 anos | Já entregue (fechar) | ADR 0023, commit cd6ea50, `domain/faixa.ts`. | |
| 72 | Domínio emocional | Já entregue (fechar) | ADR 0024, `marcos/EM.json` (16 marcos) e 5 atividades, **em rascunho**: a aprovação pedagógica dela segue pendente (portão 2). | |
| 73 | Obras e músicas + indicação | Já entregue (fechar) | Commit 2c56c40; `livros.json` e `acervo.json` com tipos. | |
| 74 | ADR de links de terceiros | Decisão pendente | Só ela decide o modelo de venda e afiliados; o ADR é escrito depois. Não bloqueia o lançamento se a estante vender nada no dia 1. | P |
| 75 | Revisar assinatura / ADR 0010 | Decisão pendente (parcial) | O ADR 0027 já existe, mas está "Aceito" com a ressalva de que a dona do produto ainda precisa aprovar o texto. O que ainda diverge: (a) ADR diz **plano Livre**, ela disse **plano básico**; (b) ADR diz **uma sugestão por fim de semana**, ela disse **uma atividade recomendada por semana**; (c) **R$ 49,90 / R$ 69,90** vêm do ADR e ela deixou preço e regras do plano básico "a definir", então não estão confirmados; (d) o ADR tira jornada, sondagem e histórico do Livre, e ela não disse isso; (e) `JORNADA_SPEC.md` §9 e a decisão 24, 29 e 30 ainda descrevem o ADR 0010 (R$ 29,90, 14 a 30 dias) e o ROADMAP ainda cita R$ 39,90 + R$ 10; (f) o ADR depende de #26 e de provedor de cobrança. Desbloqueia #4, #5, #25, #26, #76. | P |
| 76 | Restringir materiais por link assinado | Adiar | Exige servidor (#26). Até lá o Tesouro fica aberto: os PDFs, incluindo os cadernos de atividades e de inglês, vão a uma Release pública do GitHub (workflow `publicar-tesouro.yml`, ADR 0011). O "alguns materiais da biblioteca" do Livre (ADR 0027) ainda não tem lista. | G |
| 77 | Status de revisão (rascunho, revisado, aprovado) | Já entregue (fechar) | Commit 7b3d48f, `domain/revisao.ts`. | |
| 78 | Portal do preceptor | Adiar | Segundo produto; o fluxo por PR + `revisao` (#77) basta por ora. | G |
| 79 | Comunidade de trocas | Adiar | Só depois do lançamento; exige ADR de privacidade e moderação. | G |
| 84 | Migrar conteúdo do site antigo | Manter | Migrado em rascunho (commit 8256c22). Fecha quando ela aprovar o conteúdo (portão 2). | P |
| 95 | App de celular com lembrete diário | **Parcialmente entregue; decisão pendente** | Entrou no `main` a base do ADR 0028: regra pura `domain/lembretes.ts` (+ `tests/lembretes.test.ts`), preferência por família (liga, hora, nome da criança desligado por padrão) em `pages/config.ts` e no backup, adaptador `nativo/lembretes.ts` e reagendamento em `main.ts`. **Não há** projeto Capacitor (nenhuma dependência no `package.json`), build Android/iPhone, contas de loja nem arquivo `.ics`. Hoje o lembrete só funciona dentro de um app empacotado que ainda não existe; no navegador a tela explica isso. Decisão dela de 20/11 (`.ics`) conflita com o ADR 0028: ver seção 7, pergunta 2. Não fechar. | M |

Resumo dos vereditos: 12 já entregues, 3 manter, 6 reescrever, 3 dividir, 2 unir, 8 adiar, 6 decisão pendente (total 40). Dos 6 pendentes, #75 passou a "parcial" (ADR 0027) e #95 a "parcialmente entregue" (ADR 0028).

## 3. Ondas de entrega

Ordem por valor para a família e por dependência. O tamanho é do esforço dos agentes, não do tempo dela.

### Onda 0 · Arrumar a casa (P)
- Confirmar e fechar as 12 estórias já entregues, cada fechamento com a evidência da tabela (PM + QA, sem custo para ela além de ler a lista).
- Reescrever #2, #15 e #21 e dividir #17, #23 e #25, para ficarem pequenas e verificáveis.
- Atualizar o ROADMAP (ele ainda cita fases e etapas que já passaram).
- **Entrega para ela:** um GitHub limpo, com cerca de 20 estórias vivas em vez de 40.

### Onda 1 · Fechar o ciclo da sessão (M)
- #11 Registrar sessão pelo código impresso, com selo "parece pronto". É a única mudança de dados desta onda: exige migração testada e backup (ADR 0025 já mostra o padrão).
- #2 (parte que falta) e #15 (roteiro de teste e2e do educador completo).
- #95: o que já está no `main` (regra e preferência de lembrete) fica como está; nada novo aqui até ela responder a pergunta 2. Se ela escolher `.ics`, ele cabe nesta onda (P) porque reaproveita `domain/semana.ts`.
- **Entrega para ela:** o ciclo completo no site: preparar, imprimir, aplicar, registrar, ver a jornada sugerir o próximo passo.

### Onda 2 · Conteúdo de lançamento (G, em paralelo à onda 1)
- #22 (atividades e marcos que faltam em LG e MA), #21 (briefings e checklist), #84, trilha de inglês (parte de #23), sondagem das demais linhas.
- Lotes pequenos: **um PR por linha**, para ela revisar em 20 a 30 minutos cada.
- **Entrega para ela:** linhas de Linguagem e Matemática com sessões reais, marcadas como "aprovado".

### Onda 3 · Pronto para abrir (M)
- Decisões primeiro: #75 (fechar plano básico e preço contra o ADR 0027), #95 (`.ics`, Capacitor ou os dois), #34, #74, #24. Depois: #34 (domínio, com aviso de backup), #25 (termos), #4 (landing).
- **Entrega para ela:** o app em endereço próprio, com termos e landing, ainda 100% grátis e sem conta. **Já dá para abrir ao público no plano Livre** se ela quiser antecipar.

### Onda 4 · Conta e cobrança (G, só depois das decisões)
- ADR de servidor (#26, com #3 e #6 dentro), #5 pagamento, #76 restrição de materiais. Se ela mantiver o Capacitor (#95): empacotamento Android/iPhone, contas de loja e a cobrança dentro do app (ADR 0027 e 0028) entram aqui, não antes, porque dependem do preço e do provedor. É a primeira vez que algo sai do aparelho: privacidade e jurídico revisam cada passo.
- **Entrega para ela:** assinatura funcionando em ambiente de teste do gateway.

### Lançamento (v1.0) e depois
- Lançamento aberto e #28 como acompanhamento. Depois: #10, #19, #20 e #29, #27, #78, #79, francês e latim.

## 4. O que paraleliza entre os agentes

| Trilha | Agentes | Pode andar junto com |
|---|---|---|
| Software do ciclo (#11, #2) | Dev A implementa, Dev B revisa, QA escreve os casos | Conteúdo |
| Conteúdo (#22, #84, #23) | Curador + PM | Software (arquivos diferentes: `app/content/` x `app/src/`) |
| Decisões e ADRs (#75, #74, #26) | PM descreve opções, Dev B escreve o ADR | Tudo |
| Segurança, DevOps (#34) | Segurança, DevOps | Software, exceto no dia da troca de endereço |

Não paralelizar: duas estórias que mexem em `app/src/dados/` ao mesmo tempo (risco de duas migrações de banco colidirem).

## 5. Os dois portões da dona do produto

- **Portão 1, aprovar estória:** o PM deixa a estória em `aguardando-aprovacao`; ela lê e coloca `aprovada`. Sugestão: aprovar em **lotes por onda**, não uma a uma. Esta revisão propõe a ordem; ela só precisa dizer "aprovo os vereditos" ou ajustar.
- **Portão 2, aprovar conteúdo:** todo PR `conteudo` só é mesclado por ela, com o resumo do Curador. Em lotes pequenos (uma linha por vez). Hoje há conteúdo mesclado como **rascunho** (domínio emocional, músicas e histórias do site antigo): ela precisa dizer se esses itens já valem como aprovados ou se entram na fila de revisão.
- PRs que mexem em dados, CSP, workflows ou ADRs também passam por ela (ADR 0029); isso inclui #11 e #34.

## 6. Riscos

| Risco | O que pode dar errado | Como reduzir |
|---|---|---|
| Privacidade | Conta, pagamento, lembretes e links de afiliado tentam levar dados para fora. | Nenhuma dessas estórias começa sem ADR aprovado; Segurança tem veto; servidor só guarda conta e assinatura. |
| Migração de dados | #11 muda o formato; trocar o domínio (#34) abandona o banco antigo; o app antigo não abre banco novo (ADR 0025). | Migração testada, backup antes de cada onda, aviso no app, domínio trocado cedo. |
| Conteúdo infantil | Atividades para 2 anos (engasgo, água); orientação aos pais obrigatória (ADR 0017). | Curador segue as regras já aplicadas no caderno de 2 anos; nada vai ao ar sem portão 2. |
| Custo de tokens | 8 agentes por estória custam mais. | Uma estória por vez no início; QA e revisores só nos PRs que tocam código; medir após a onda 1. |
| Modelo de negócio | ADR 0027 e decisão de 20/11 ainda divergem (plano Livre x básico, "fim de semana" x "semana", preço não confirmado); a faixa é declarada pela família, sem verificação; lojas podem exigir compra dentro do app com comissão; teste de 7 dias com material restrito não funciona sem servidor. | Fechar #75 contra o ADR 0027 antes de qualquer código de cobrança. |
| Escopo do app nativo | O ADR 0028 acrescenta Capacitor, contas de loja (Apple cerca de US$ 99 por ano; Mac para compilar) e revisão das lojas, o que a decisão de 20/11 (`.ics`, "sem app de loja") queria evitar. | Ela escolhe a opção na pergunta 2 antes de qualquer empacotamento. |
| Processo | Os workflows e o segredo do ADR 0029 ainda dependem de ações dela no GitHub. | Fazer a "configuração única" do `docs/PROCESSO_AI_SDLC.md` antes da onda 1. |
| Jurídico | Termos e portfólio sem validação. | #25 e #29 com advogado(a); só o rascunho da política existe hoje. |

## 7. Perguntas abertas para ela

1. **Preço e teste (#75), reaberta após o ADR 0027:** o ADR fixou R$ 49,90 (1 criança) e R$ 69,90 (2 ou mais), teste de 7 dias e volta ao Livre. Ela decidiu teste de 7 dias e plano básico com uma atividade por semana. Perguntas: (a) os R$ 49,90 e R$ 69,90 valem? (b) "plano Livre" e "plano básico" são o mesmo plano? (c) é "uma atividade por semana" ou "uma sugestão por fim de semana" (o ADR 0027 deve seguir a decisão dela)? (d) o plano básico mantém ou perde a jornada, a sondagem e o histórico (o ADR 0027 tira)? (e) o portfólio completo fica em qualquer plano?
2. **Lembrete diário (#95), conflito com o ADR 0028 (aberta, o PM não decide):** em 20/11 ela escolheu `.ics` (sem app de loja); o ADR 0028 já escolheu app nativo (Capacitor) com notificação local, e a regra, a preferência e o adaptador estão no `main`; falta empacotar. Opções: (a) **manter o `.ics` como complemento**: o `.ics` vira o lembrete no navegador e na PWA (P), o código de lembrete local fica pronto e o Capacitor só entra se ela quiser lojas depois; (b) **manter o Capacitor** como o ADR 0028 (M a G, contas de loja, Mac para iPhone, cobrança na loja), `.ics` descartado; (c) **substituir**: seguir só com `.ics`, congelar o Capacitor e reverter ou deixar dormente o código de lembrete e a preferência na configuração (o ADR 0028 teria de ser revisto e a tela de configuração hoje oferece um lembrete que só funciona no app). Efeito na privacidade: igual nas três (nada sai do aparelho). Sem a resposta, o #95 não avança além do que já entrou.
3. **Aprovação do que está em rascunho:** os marcos emocionais, as músicas e histórias do site antigo e o conteúdo de 2 anos já valem ou vão para a fila de revisão dela?
4. **Ilustrações (#24):** encomendar a ilustradores(as) ou licenciar banco? Há verba?
5. **Piloto:** manter lançamento aberto direto, ou fazer um teste pequeno (3 famílias, 4 semanas) antes de cobrar?
6. **Endereço próprio (#34):** já existe o domínio? Quem compra e configura? Aceita que quem já usa o endereço atual precise de um backup para migrar?
7. **Abrir no plano Livre antes da conta?** (Respondida em 20/11: só na onda 4. Com o ADR 0027, o Livre perderia a jornada, então a abertura sem conta mostraria um produto menor; confirmar se isso ainda vale.) Pergunta original: O app já funciona sem conta. Quer lançar na onda 3 e cobrar só depois, ou esperar a onda 4?

## 8. Plano de entrega para ela

| Quando (ordem) | O que ela faz | Atenção | O que recebe ao fim |
|---|---|---|---|
| Antes de tudo | Fazer a configuração única do GitHub (segredo, auto-merge, rótulos; `docs/PROCESSO_AI_SDLC.md`). Aprovar este documento. | 30 a 45 min, uma vez | Processo dos agentes funcionando |
| Onda 0 | Ler a lista de fechamentos; responder as perguntas 3 e 7. | 20 min | GitHub limpo, ROADMAP fiel |
| Onda 1 | Aprovar a estória #11 (portão 1); depois rodar o roteiro de teste no celular. Mesclar o PR (mexe em dados). | 15 min para aprovar, 20 min de teste | Ciclo completo da sessão no site |
| Onda 2 | Revisar lotes de conteúdo, um por linha (portão 2). | 20 a 30 min por lote, cerca de 1 hora por semana | Linhas de LG e MA aprovadas |
| Onda 3 | Decidir as perguntas 1, 4 e 6; aprovar termos; mesclar a troca de domínio. | 1 a 2 horas, espalhadas | Endereço próprio, termos, landing; abertura possível |
| Onda 4 | Aprovar o ADR de servidor; contratar o gateway; revisar o jurídico. | 2 a 3 horas, mais conversa com advogado(a) | Assinatura em ambiente de teste |
| Lançamento | Rodar o roteiro "do anúncio à assinatura" (ROADMAP, Fase 6). | 1 hora | v1.0 aberto ao público |

Cronograma por ordem (sem datas): 0 (P) antes de 1 (M); 2 (G) corre ao lado de 1; 3 (M) começa quando 1 fecha e as decisões 1, 4 e 6 chegam; 4 (G) só depois da 3 e da decisão 1.

## 9. Decisões da dona do produto (20/11/2026)
Respostas às perguntas da seção 7. Valem como decisão registrada para as estórias com rótulo `decisao`.

| # | Decisão |
|---|---|
| #75 Assinatura | **Teste de 7 dias** com o produto completo; depois, um **plano básico** com **uma atividade recomendada por semana**. Preço e regras do plano básico ainda a definir (o PM descreve as opções). |
| #95 Lembrete | **Arquivo de calendário (`.ics`)**: sem servidor, sem app de loja. |
| Conteúdo em rascunho | Emocional, músicas e histórias do site antigo e conteúdo de 2 anos **valem como aprovados**. É preciso **diferenciar** o que o agente pedagógico revisou do que ela aprovou sem essa revisão (nova estória). |
| #24 Ilustrações | **Gratuitas** (domínio público ou licença livre, com fonte registrada; ver CLAUDE.md). Sem verba para encomendar. |
| Lançamento / #28 | **Lançamento aberto direto**, sem piloto antes. Pode haver **promoções com vouchers de uso** (nova estória). |
| #34 Domínio | Ainda **não existe**; ninguém usa o site para valer. Resolver depois, quando ela comprar o domínio. O aviso de backup só é necessário se houver usuários. |
| Plano Livre sem conta | **Onda 4**: a abertura ao público espera conta e cobrança. |

Efeitos na ordem das ondas: a onda 3 deixa de ser "abrir ao público" e vira "pronto para abrir"; a abertura acontece depois da onda 4.

**Nota de conflito (20/11):** a decisão sobre o #95 (`.ics`, "sem app de loja") e a do #75 ("plano básico", "uma atividade por semana") diferem do que os ADR 0028 e 0027 já registram no `main`. Esta tabela mantém a decisão dela como registrada; o que fazer com os ADRs está nas perguntas 1 e 2 da seção 7 e só ela escolhe.
