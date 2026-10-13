# 🧭 Jornada de Aprendizado: Especificação

> Documento resultante do *grilling* de outubro/2026. Ele define **como o Semear posiciona cada criança numa jornada por domínios** e como isso alimenta a geração de materiais para imprimir.
> Status: **rascunho v0.1**, a ser validado com as famílias piloto.

---

## 1. Princípios (não negociáveis)

1. **A criança não usa o app.** Só o educador (pai, mãe ou tutor) interage com ele, antes e depois das sessões.
2. **Papel primeiro.** Tudo o que a criança vê sai num PDF: A4 para imprimir, ou um "modo tablet" com uma página por tela, sem links e sem interação.
3. **O pai decide.** O app sugere, avisa e organiza, mas avançar na jornada é sempre uma decisão do educador.
4. **Sem nota, sem comparação.** A escala é qualitativa e não existe ranking entre crianças.
5. **Local e privado.** Segue a arquitetura atual do Semear: dados no dispositivo, exportáveis.

---

## 2. Decisões tomadas

| # | Tema | Decisão |
|---|------|---------|
| 1 | Produto | **Evolução do Semear**: a jornada vira o "cérebro" do plano semanal, do explorador e do diário. |
| 2 | Faixa etária | **3 a 8 anos** (da educação infantil até o 2º ano / alfabetização consolidada). |
| 3 | Vertentes × jornada | **Mapa único** para todas as vertentes, com **marcos extras** por vertente. |
| 4 | Posicionamento | **Independente por linha**: a criança tem uma posição em cada linha de cada domínio. |
| 5 | Hierarquia | **Domínio → Linha → Marco**, com marcos ordenados dentro da linha e pré-requisitos opcionais entre linhas. |
| 6 | Domínios no lançamento | Linguagem e Alfabetização · Matemática · Natureza, Mundo e Sociedade · Desenvolvimento Integral. |
| 7 | Avaliação | **Sondagem formal impressa**, com lançamento no app, **mais o registro contínuo** a cada sessão. |
| 8 | Escala | **3 estados**: Não observado · Em desenvolvimento · Consolidado. |
| 9 | Avanço | **Manual, pelo pai.** O app só indica "parece pronto". |
| 10 | Sessões | O pai escolhe **duração e foco**, o app sugere as atividades e o pai pode trocar qualquer uma. |
| 11 | Irmãos | **Vários perfis**, com **sessão conjunta opcional** (tema comum e folhas diferenciadas). |
| 12 | Livros | Curadoria **ligada à vertente, ao marco e à idade**, com uso sugerido. |
| 13 | Ressondagem | **A cada 8 semanas, por linha**, só nas linhas paradas ou pouco observadas. |
| 14 | Mistura de vertentes | **Uma principal + inspirações.** |
| 15 | Ritmo da vertente | **Idade de introdução por vertente, só como aviso** (sem bloquear). |
| 16 | Pacote da sessão | Roteiro do educador · Folhas da criança · Ficha de registro · Materiais + livro. |

---

## 3. O mapa: domínios e linhas

O mapa completo, com códigos e idades, está em [`data/journey/dominios.json`](../data/journey/dominios.json). Resumo:

### 🗣️ LG: Linguagem e Alfabetização
| Linha | O que acompanha |
|-------|-----------------|
| LG.ORA Oralidade e vocabulário | Narrar, recontar, perguntar, ampliar vocabulário |
| LG.FON Consciência fonológica | Rimas, sílabas, sons iniciais, fonemas |
| LG.LET Conhecimento das letras | Nome, forma e som das letras (princípio alfabético) |
| LG.ESC Escrita | Hipóteses de escrita (pré-silábica → alfabética) e produção de texto |
| LG.LEI Leitura | Decodificação → fluência → compreensão |
| LG.GRA Grafomotricidade | Preensão, traçado e letra cursiva/bastão |
| LG.LIT Apreciação literária | Escuta de histórias, poesia, memorização, preferências |

### 🔢 MA: Matemática
| Linha | O que acompanha |
|-------|-----------------|
| MA.SEN Senso numérico e contagem | Subitização, correspondência, contagem com sentido |
| MA.SND Sistema de numeração | Leitura e escrita de números, valor posicional |
| MA.OPE Operações | Juntar e tirar → adição e subtração → multiplicação e divisão (ideias iniciais) |
| MA.GEO Geometria e espaço | Formas, posição, deslocamento, simetria |
| MA.MED Grandezas e medidas | Comprimento, massa, capacidade, tempo, dinheiro |
| MA.PAD Padrões e classificação | Sequências, seriação, classificação (pré-álgebra) |
| MA.DAD Dados | Contar e registrar em tabelas e gráficos simples (6+) |

### 🌎 NM: Natureza, Mundo e Sociedade
| Linha | O que acompanha |
|-------|-----------------|
| NM.VIV Seres vivos e corpo | Plantas, animais, corpo humano, cuidados |
| NM.TER Terra e céu | Clima, estações, água, dia e noite, materiais |
| NM.TEM Tempo e história | Rotina, calendário, história pessoal, familiar e do Brasil |
| NM.ESP Espaço e lugares | Casa, bairro, cidade, mapas, Brasil |
| NM.CUL Cultura e diversidade | Folclore, festas, povos e regiões brasileiras |

### 🌱 DI: Desenvolvimento Integral
| Linha | O que acompanha |
|-------|-----------------|
| DI.SOC Socioemocional e valores | Nomear emoções, autorregulação, convivência. Liga-se aos 8 valores do Semear. |
| DI.VPR Vida prática e autonomia | Cuidado de si, da casa e do outro |
| DI.MAM Motor amplo | Equilíbrio, coordenação, ritmo corporal |
| DI.MFI Motor fino | Pinça, recorte, encaixe, costura |
| DI.ART Artes visuais | Desenho, pintura, modelagem |
| DI.MUS Música e ritmo | Cantigas, pulso, escuta, instrumentos simples |

### ✨ Marcos extras por vertente
São linhas ou marcos **adicionais**, que só aparecem quando a vertente é a principal da família (ou entra como inspiração, se o pai quiser):

- **Montessori:** DI.SEN *Educação dos sentidos* (gradações, pares, discriminação sensorial). Marcos extras em DI.VPR (verter, dobrar, preparar alimentos).
- **Waldorf:** DI.RIT *Ritmo e festivais* (rotina, festas sazonais). Marcos de *desenho de formas* em LG.GRA e de *aquarela úmida* em DI.ART.
- **Clássico:** LG.MEM *Memorização e recitação* (poemas, cronologias, listas). Marcos de *narração* em LG.ORA.
- **Religioso:** DI.ESP *Vida espiritual* (oração, histórias sagradas, virtudes), configurável pela tradição da família.

> Os marcos extras usam o mesmo formato dos marcos comuns. A única diferença é o campo `vertentes`, que indica em quais vertentes eles aparecem.

---

## 4. Modelo de dados

### 4.1 Conteúdo (curado pela equipe, em `data/journey/`)

```jsonc
// Marco
{
  "id": "LG.FON.03",
  "linha": "LG.FON",
  "ordem": 3,
  "titulo": "Identifica a sílaba inicial de palavras",
  "descricaoPais": "A criança percebe que BOLA e BOTA começam com o mesmo pedaço.",
  "evidencias": ["Separa figuras pela sílaba inicial", "Diz outra palavra que começa igual"],
  "idadeTipica": 5,                       // em anos, referência geral
  "idadeIntroducao": { "Waldorf": 7 },    // só gera aviso, nunca bloqueia
  "preRequisitos": ["LG.ORA.02"],         // opcional, entre linhas
  "vertentes": null,                      // null = comum a todas; ["Montessori"] = marco extra
  "bncc": []                              // códigos da BNCC, preenchidos na curadoria
}
```

```jsonc
// Item de sondagem (gera a folha impressa + o roteiro de observação)
{
  "id": "SD.LG.FON.03.a",
  "marco": "LG.FON.03",
  "tipo": "folha" | "oral" | "observacao",
  "instrucaoEducador": "Mostre as 6 figuras e peça: 'quais começam igual a BOLA?'",
  "template": "pares-figuras",            // template de PDF
  "criterio": {
    "consolidado": "5 ou 6 acertos sem ajuda",
    "emDesenvolvimento": "3 ou 4 acertos, ou acertos com ajuda"
  }
}
```

```jsonc
// Atividade (evolução dos "resources" atuais)
{
  "id": "atv-caca-silabas",
  "titulo": "Caça às sílabas na feira",
  "marcos": ["LG.FON.03", "LG.FON.04"],
  "vertentes": ["Montessori", "Clássico"],
  "idade": [4, 7],
  "duracaoMin": 15,
  "conjunta": true,                        // serve para sessão de irmãos
  "variacoes": { "LG.FON.03": "...", "LG.FON.04": "..." }, // folha diferente por marco
  "materiais": ["Figuras impressas", "Cesto"],
  "printables": ["folha-caca-silabas-v1"],
  "roteiro": ["...passo a passo para o pai..."]
}
```

```jsonc
// Livro curado
{
  "id": "livro-menina-bonita",
  "titulo": "Menina Bonita do Laço de Fita",
  "autor": "Ana Maria Machado",
  "vertentes": ["Waldorf", "Clássico", "Montessori"],
  "marcos": ["LG.LIT.02", "NM.CUL.03", "DI.SOC.04"],
  "idade": [4, 8],
  "uso": "leitura-em-voz-alta" | "leitura-pela-crianca" | "apoio-ao-educador",
  "porQue": "Texto curto com repetição, ótimo para reconto e para conversar sobre identidade."
}
```

### 4.2 Dados da família (locais, no dispositivo)

```jsonc
// Perfil (estende o family-profile atual)
{
  "vertentePrincipal": "Montessori",
  "inspiracoes": ["Waldorf"],
  "children": [{ "id": "crianca-ana", "name": "Ana", "birthdate": "2020-03-15" }]
}

// Estado de um marco para uma criança (a fonte da "posição")
{
  "childId": "crianca-ana",
  "marco": "LG.FON.03",
  "estado": "nao-observado" | "em-desenvolvimento" | "consolidado",
  "atualizadoEm": "2026-10-13",
  "origem": "sondagem" | "sessao" | "manual"
}

// Observação (histórico: nada é apagado, o estado atual é o mais recente)
{ "childId": "...", "marco": "...", "estado": "...", "data": "...", "sessaoId": "...", "nota": "texto livre" }
```

---

## 5. Regras da jornada

### 5.1 Posição numa linha
- **Fronteira** = o primeiro marco da linha (na ordem) que **não** está *Consolidado*.
- **Marcos ativos** = a fronteira, mais o marco seguinte **se** a fronteira já estiver *Em desenvolvimento* (no máximo 2 por linha).
- Marcos com pré-requisito de outra linha ainda não consolidado aparecem como **"aguardando"** e não são sugeridos, mas o pai pode forçá-los.

### 5.2 Avanço (manual)
- Só o pai muda um marco para *Consolidado*, seja na ficha de registro ou no mapa.
- O app mostra um selo **"🌱 parece pronto"** quando o marco teve *Consolidado* registrado em 2 sessões diferentes. É só uma dica.
- O pai também pode marcar um marco como *Consolidado* direto no mapa, por exemplo algo que a criança aprendeu sozinha.

### 5.3 Ritmo da vertente
- Se `idadeIntroducao[vertentePrincipal]` for maior que a idade da criança, o marco aparece com um aviso: *"Na pedagogia Waldorf, este marco costuma ser introduzido por volta dos 7 anos."* O app não bloqueia nada.

### 5.4 Sondagem inicial (adaptativa, por linha)
1. Para cada linha, comece pelo marco cuja `idadeTipica` está mais próxima da idade da criança.
2. Se ele estiver **Consolidado**, suba 1 ou 2 marcos. Se **Não observado**, desça.
3. Pare quando achar a fronteira, com **3 a 5 itens por linha** e no máximo cerca de 20 minutos por domínio.
4. Como a criança faz no papel, o app gera **duas etapas** de folhas: uma etapa base e, depois que o pai lança os resultados, uma etapa de ajuste só nas linhas onde a fronteira não ficou clara.
5. A sondagem pode ser **dividida em vários dias** (um domínio por dia).

### 5.5 Ressondagem
- A cada **8 semanas**, o app lista as linhas que estão **paradas** (fronteira igual há 8 semanas ou mais) ou **sem observação** há 8 semanas ou mais.
- O app gera uma mini-sondagem só dessas linhas.

### 5.6 Gerador de sessão
**Entradas:** crianças (1 ou mais), duração (ex.: 20, 40 ou 60 min), foco (linhas escolhidas ou "equilibrado").

**Algoritmo (v1):**
1. Linhas candidatas = o foco do pai, ou as linhas com menos tempo trabalhado nas últimas 2 semanas.
2. Para cada linha, pegue os marcos ativos e as atividades ligadas a eles.
3. Pontue cada atividade: vertente principal (+3), inspiração (+1), faixa de idade compatível (+2), sem repetição nos últimos 14 dias (+2), materiais já disponíveis (+1).
4. Preencha a duração (com folga de cerca de 10%), alternando atividade sentada e de movimento.
5. **Sessão conjunta:** procure atividades com `conjunta: true` que cubram os marcos ativos de todas as crianças. Use a `variacao` de cada criança para gerar folhas diferentes com o mesmo tema.
6. Sugira **1 livro** da curadoria ligado aos marcos da sessão.
7. O pai revisa, troca o que quiser e gera o pacote.

### 5.7 Pacote impresso da sessão
1. **Roteiro do educador** (1 ou 2 páginas): objetivo, passo a passo, falas sugeridas, "o que observar" por marco.
2. **Folhas da criança**: A4 retrato, letra grande, sem nome da marca em destaque. No **modo tablet**, uma página por tela, num PDF sem links.
3. **Ficha de registro rápido**: uma linha por marco trabalhado, com ☐ Não observado ☐ Em desenvolvimento ☐ Consolidado e espaço para nota. O pai lança no app em cerca de 2 minutos, e cada linha tem um código curto que facilita achar o marco.
4. **Materiais + livro**: checklist do que separar, com itens de casa destacados.

---

## 6. Como isso se encaixa no Semear atual

| Hoje | Com a jornada |
|------|---------------|
| `resources.json` (atividades com valores e estilos) | Atividades ganham `marcos`, `variacoes` e `printables` |
| Plano semanal por valores e estilo | Plano semanal = várias sessões geradas pelo algoritmo 5.6 |
| Diário de memórias | Diário + observações de marcos (o registro rápido alimenta os dois) |
| Guia pedagógico (4 estilos) | Guia + idades de introdução e marcos extras de cada vertente |
| Explorador | Explorador filtrável por domínio, linha e marco, e a estante de livros |
| Onboarding em 4 etapas | + vertente principal/inspirações, + perfis das crianças, + agendar sondagem inicial |

---

## 7. Benchmark: o que existe lá fora e onde o Semear se diferencia

| Referência | O que faz bem | Limitação | O que copiar / melhorar |
|---|---|---|---|
| **Kinedu** (LatAm, 0–4 anos) | Avaliação de marcos pelos pais, posicionamento **por área**, atividades diárias sugeridas | Só até cerca de 4 anos, baseado em vídeo e tela | O fluxo "avalia → posiciona por área → sugere" é exatamente o nosso núcleo. Levar isso até 8 anos, em papel. |
| **Khan Academy Kids / IXL** | Diagnóstico adaptativo e trilhas por habilidade | **A criança usa a tela** | A lógica adaptativa (sondagem 5.4), mas aplicada pelo pai e no papel. |
| **Homeschool Planner, Homeschool Planet** (EUA) | Planejamento, presença, relatórios, vários alunos | Focados em horas e notas, não em domínio de habilidades. Pais montam tudo sozinhos | Relatório/portfólio exportável. Nós geramos o conteúdo, não só a agenda. |
| **Twinkl, TpT, Montessori for Everyone** | Grande acervo de imprimíveis (Twinkl tem versão BR alinhada à BNCC) | Acervo solto, sem saber **onde a criança está** | Qualidade visual das folhas. Nosso valor é a **ligação folha ↔ marco ↔ criança**. |
| **AmblesideOnline** (Charlotte Mason) | Curadoria de livros por ano, gratuita, comunitária | Só uma vertente, em inglês, sem avaliação | A curadoria de livros por vertente e idade com um "por quê". Candidata a 5ª vertente. |
| **The Good and the Beautiful, Lovevery** | Currículo/kits bonitos, prontos e por estágio | Caros, importados, fechados numa visão | A sensação de "está tudo pronto". Lovevery organiza por estágio, como nossos marcos. |

**Lacunas no Brasil, que são a nossa oportunidade:**
1. Não encontramos um app brasileiro que una **avaliação, jornada por domínio e material imprimível gerado**. Existem planejadores e portfólios em teste (ex.: "Nosso Homeschool") e lojas de PDFs avulsos.
2. **Cultura brasileira e literatura nacional** (folclore, Ana Maria Machado, Ruth Rocha, Ziraldo) como conteúdo de primeira classe, não como tradução.
3. **Alfabetização do jeito brasileiro:** hipóteses de escrita (Emília Ferreiro), método fônico ou silábico conforme a vertente e o mapeamento para a **BNCC**.
4. **Portfólio para segurança jurídica:** o homeschooling não é regulamentado no Brasil, e um histórico de marcos, observações e amostras de trabalho (exportável em PDF) é valioso para as famílias.
5. **Afterschooling:** pais de crianças que estão na escola querem reforçar *exatamente* o que falta. O posicionamento por linha responde a isso.
6. **Offline, de baixo custo, sem conta**, combinando com a realidade de muitas famílias e com o "a criança não usa tela".

---

## 8. Questões em aberto (próximas rodadas de grilling)

- [ ] **Quem produz o conteúdo?** Equipe pedagógica própria, parceiras educadoras, comunidade? Quantos marcos e atividades por linha para lançar? (sugestão: começar só com **LG e MA**, com cerca de 8 a 12 marcos por linha)
- [ ] **Geração de PDF:** no próprio navegador (CSS de impressão e/ou jsPDF) ou num serviço? O app hoje é 100% local.
- [ ] **Sincronização** entre celular e computador sem servidor (arquivo exportado? conta opcional?).
- [ ] **Uso de IA** para criar variações de folhas (ex.: trocar o tema "feira" por "dinossauros"), com revisão humana?
- [ ] **Charlotte Mason e Unschooling** como vertentes?
- [ ] **Necessidades específicas** (TEA, TDAH, dislexia, altas habilidades): adaptações de folhas e de ritmo.
- [ ] **Relatório/portfólio**: formato e periodicidade.
- [ ] **Modelo de negócio** (o app hoje é gratuito): pacotes de conteúdo pagos? Assinatura? Livros com link de afiliado?

---

## 9. Próximos passos sugeridos

1. Validar este documento com 3 a 5 famílias piloto (uma de cada vertente, incluindo afterschooling).
2. Curar os marcos de **LG.FON, LG.ESC, MA.SEN e MA.OPE** primeiro (são o coração dos 4 a 7 anos).
3. Desenhar 3 templates de folha + o roteiro + a ficha, e testar a impressão real em A4 e no tablet.
4. Implementar: modelo de dados → mapa visual da jornada → sondagem → gerador de sessão → PDF.
