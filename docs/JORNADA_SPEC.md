# 🧭 Jornada de Aprendizado: Especificação

> Documento resultante do *grilling* de outubro/2026. Ele define **como o Semear posiciona cada criança numa jornada por domínios** e como isso alimenta a geração de materiais para imprimir.
> Status: **rascunho v0.6** (7 rodadas de grilling + protótipos + app v1 em construção + revisão do modelo de negócio, ADR 0010), a ser validado com as famílias piloto.

---

## 1. Princípios (não negociáveis)

1. **A criança não usa o app.** Só o educador (pai, mãe ou tutor) interage com ele, antes e depois das sessões.
2. **Papel primeiro.** Tudo o que a criança vê sai num PDF: A4 para imprimir, ou um "modo tablet" com uma página por tela, sem links e sem interação.
3. **O pai decide.** O app sugere, avisa e organiza, mas avançar na jornada é sempre uma decisão do educador.
4. **Sem nota, sem comparação.** A escala é qualitativa e não existe ranking entre crianças.
5. **Dados da criança ficam no aparelho.** Observações, marcos e fotos ficam guardados localmente. A conta (só para quem testa ou assina, ver §9) guarda só os dados do responsável e da assinatura, além do *sync* opcional.
6. **Conteúdo sempre revisado por um humano.** A IA ajuda a produzir, mas nada chega às famílias sem revisão.

---

## 2. Decisões tomadas

| # | Tema | Decisão |
|---|------|---------|
| 1 | Produto | **Evolução do Semear**: a jornada vira o "cérebro" do plano semanal, do explorador e do diário. |
| 2 | Faixa etária | **3 a 8 anos** (da educação infantil até o 2º ano / alfabetização consolidada). |
| 3 | Vertentes × jornada | **Mapa único** para todas as vertentes, com **marcos extras** por vertente. |
| 4 | Posicionamento | **Independente por linha**: a criança tem uma posição em cada linha de cada domínio. |
| 5 | Hierarquia | **Domínio → Linha → Marco**, com marcos ordenados dentro da linha e pré-requisitos opcionais entre linhas. |
| 6 | Domínios no lançamento | **Com jornada:** Linguagem e Alfabetização · Matemática · Línguas (inglês, francês, latim). **Só atividades:** Artes e Música · Natureza, Mundo e Sociedade · Desenvolvimento Integral. Ver §3.0. |
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
| 17 | Produção de conteúdo | **IA rascunha e humano revisa** (o time fundador também escreve). Uma equipe pequena entra quando escalar. Ver §7. |
| 18 | Línguas estrangeiras | **Domínio único "Línguas"** com as mesmas linhas, e cada idioma é uma *trilha* (inglês, francês, latim). O latim tem marcos próprios. |
| 19 | Pronúncia | **Partimos do princípio de que o educador fala a língua.** O onboarding pergunta quais línguas ele domina e só oferece essas trilhas. |
| 20 | Artes e música | **Só atividades**, sem marcos nem posicionamento. |
| 21 | Uso de IA | **Só na produção do conteúdo.** As famílias recebem conteúdo estático e revisado. |
| 22 | PDF | **Gerado no dispositivo** a partir de templates HTML/SVG com CSS de impressão (A4 e modo tablet). |
| 23 | Sincronização | ~~Conta opcional~~ → ~~conta obrigatória~~ → **conta só para teste e assinatura** (decisão 30, ADR 0010). O *sync* entre aparelhos e responsáveis é opcional e criptografado. |
| 24 | Modelo de negócio | ~~Freemium~~ → ~~teste de 30 dias e depois pago~~ → **plano Livre permanente + plano Família pago** (decisão 29, ADR 0010). Ver §9. |
| 25 | Portfólio | **Portfólio de evidências trimestral**, com anexo BNCC, pensado para proteger a família. Ver §8. |
| 26 | Necessidades específicas | **Fica para depois** do lançamento. |
| 27 | Idade das línguas | **Escalonar:** inglês e francês orais a partir dos 3 anos. Latim a partir dos 6, com pré-requisito de leitura em português (LG.LEI). **No máximo 2 trilhas de língua ativas** por criança (o app avisa e o pai pode forçar). |
| 28 | Novas vertentes | **Charlotte Mason entra** como 5ª vertente. **Unschooling não entra**, porque rejeita sequência e sondagem, que são o núcleo do produto. |
| 29 | Monetização | ~~Teste de 30 dias e depois assinatura, sem plano gratuito~~ → **Semear Livre (grátis para sempre) + Semear Família (assinatura)**. A família paga pelo conteúdo novo toda semana, não pelo acesso ao histórico (ADR 0010). |
| 30 | Cadastro | ~~Conta + cartão no início do teste~~ → **Livre sem conta. Teste de 14 a 30 dias com e-mail, sem cartão** (ADR 0010). |
| 31 | Fim do teste sem assinatura | ~~Bloqueio total, só exportação~~ → **volta para o Livre**. Histórico, backup e **portfólio completo** continuam acessíveis em qualquer plano (§9.2, ADR 0010). |
| 32 | Distribuição | **PWA** (celular + computador) com **pagamento na web** (Pix e cartão). Lojas de apps ficam para depois. |
| 33 | Preço | ~~Por criança~~ → **por família, com crianças ilimitadas e plano anual como padrão** (ADR 0010). |
| 34 | Fotos do portfólio | **Só no aparelho**, sem nuvem. |
| 35 | Visual das folhas | **Colorido suave** (fundos pastel, traço escuro). Ver §5.8. |
| 36 | Vertente × aparência | A identidade visual é a mesma para todas. A vertente muda **só a tipografia e o tipo de atividade**. |
| 37 | Letra da criança | **Configurável por criança:** bastão (caixa alta) → script minúsculo → cursiva. O padrão depende da idade e da vertente. |
| 38 | Primeiro passo | **Protótipo do pacote impresso** testado com famílias antes de construir o app. Ver §12. |
| 39 | Tecnologia | **Reconstruir com Vite + TypeScript**, mantendo PWA, na pasta `app/` (ADR 0001). |
| 40 | Escopo da v1 | **Família, crianças e mapa da jornada + gerar e baixar o pacote.** Registro da ficha e sondagem impressa ficam para depois. |
| 41 | Banco de dados | **IndexedDB com `idb`**, atrás de um repositório (ADR 0002). Servidor (Supabase) só quando houver contas. |
| 42 | Qualidade | **Pirâmide de testes + CI obrigatória** (ADR 0006). |
| 43 | Fluxo com IA | **Spec → plano → testes → código → revisão**, documentado no `CLAUDE.md`. |
| 44 | Revisão | **Dois agentes revisores** (correção; segurança e privacidade) **+ aprovação da dona do produto**. A v1 vai num PR único (ADR 0007). |
| 45 | Publicação | O app novo **substitui o site atual só quando a v1 estiver completa**. |
| 46 | Posicionamento inicial (v1) | **"Está aqui" em cada linha**: os anteriores viram consolidados; depois, ajuste marco a marco. |
| 47 | Tela inicial | **Painel por criança** com progresso, "Preparar sessão" em destaque e as últimas sessões. |
| 48 | Irmãos na v1 | **Vários perfis**, sessões individuais. Sessão conjunta numa versão seguinte. |
| 49 | Backup | **Exportar/importar arquivo + lembrete após 30 dias** sem backup + pedido de armazenamento persistente. |

> **O que a v1 do app ainda não implementa** (fica para versões seguintes; registrado após a revisão do PR #1):
> selo "🌱 parece pronto" (§5.2); sondagem impressa e ressondagem (§5.4–5.5); no gerador de sessão (§5.6),
> o ponto de "materiais disponíveis", a alternância sentada/movimento e a sessão conjunta de irmãos;
> e o lançamento da ficha de registro no app (§5.7). O avanço continua manual, marco a marco, na tela da jornada.

---

## 3. O mapa: domínios e linhas

O mapa completo, com códigos e idades, está em [`data/journey/dominios.json`](../data/journey/dominios.json).

### 3.0 Escopo do lançamento

| Domínio | No lançamento | Observação |
|---|---|---|
| 🗣️ LG Linguagem e Alfabetização | **Jornada completa** | Prioridade nº 1 |
| 🔢 MA Matemática | **Jornada completa** | |
| 🌍 LI Línguas (inglês, francês, latim) | **Jornada completa**, por trilha | Só as trilhas que o educador domina |
| 🎨 AR Artes e Música | **Só atividades** | Inclui artistas e música brasileira (Tarsila, Portinari, Villa-Lobos, cantigas) |
| 🌎 NM Natureza, Mundo e Sociedade | **Só atividades** | Reaproveita os recursos atuais (folclore, plantio…). Jornada na v2. |
| 🌱 DI Desenvolvimento Integral | **Só atividades** | Valores e rituais atuais do Semear. Jornada na v2. |

As atividades de domínios sem jornada entram nas sessões como **"complementares"**, escolhidas por idade, vertente e tema. Elas aparecem no portfólio como horas e evidências, mas sem marcos.

> ⚠️ **Alerta de escopo:** são 3 domínios com jornada, sendo que Línguas tem 3 trilhas, mais 3 domínios só com atividades. Mesmo com a IA rascunhando, **a revisão humana é o gargalo**. Sugestão de ordem de publicação: LG e MA primeiro, depois Inglês, depois Francês e Latim. Dá para lançar com LG e MA completos e as trilhas de língua marcadas como "em breve".

Resumo das linhas:

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

### 🌍 LI: Línguas (trilhas: inglês · francês · latim)
Cada marco de Línguas vale para uma ou mais trilhas (`idiomas: ["en","fr","la"]`). A posição da criança é guardada **por trilha**: ela pode estar no marco 5 de inglês e no marco 1 de francês.

| Linha | O que acompanha | Trilhas |
|-------|-----------------|---------|
| LI.ESC Escuta e compreensão | Entende comandos, histórias curtas, perguntas | en, fr, la |
| LI.FAL Fala | Repete, responde, conversa com frases simples | en, fr, la |
| LI.VOC Vocabulário por temas | Cores, números, corpo, família, casa, animais, comida… | en, fr, la |
| LI.CAN Canções, rimas e recitação | Cantigas, *nursery rhymes*, *comptines*, orações e poemas em latim | en, fr, la |
| LI.LEI Leitura (6+) | Palavras visuais → frases → livrinhos | en, fr, la |
| LI.ESR Escrita (6+) | Copiar → escrever palavras → frases | en, fr, la |
| LI.RAI Raízes latinas no português | *aqua* → aquário, aquático… | la |
| LI.GRA Gramática inicial (7–8) | Gênero, primeiras declinações e conjugações (latim clássico) | la |

**Regras das trilhas:**
- **Inglês e francês:** a partir dos 3 anos, começando pela parte oral (escuta, fala, canções). Leitura e escrita a partir dos 6, depois que a criança estiver lendo em português.
- **Latim:** a partir dos 6 anos. A trilha só é sugerida quando a criança tem marcos iniciais de **LG.LEI** em andamento, para não competir com a alfabetização em português. É muito usado nas vertentes Clássica e Charlotte Mason, mas fica disponível para todas.
- **No máximo 2 trilhas ativas** por criança. Ao ativar a 3ª, o app avisa ("aprender muitas línguas ao mesmo tempo costuma diluir o progresso") e o pai pode confirmar mesmo assim.
- O onboarding pergunta **quais línguas o educador domina** e só oferece essas.

### 🎨 AR: Artes e Música (só atividades)
Desenho · Pintura · Modelagem · Ritmo e pulso · Canto · Escuta musical · Apreciação de artistas. Essas categorias servem para **filtrar e equilibrar** as atividades nas sessões, não para posicionar a criança.

### 🌎 NM: Natureza, Mundo e Sociedade *(só atividades no lançamento)*
| Linha | O que acompanha |
|-------|-----------------|
| NM.VIV Seres vivos e corpo | Plantas, animais, corpo humano, cuidados |
| NM.TER Terra e céu | Clima, estações, água, dia e noite, materiais |
| NM.TEM Tempo e história | Rotina, calendário, história pessoal, familiar e do Brasil |
| NM.ESP Espaço e lugares | Casa, bairro, cidade, mapas, Brasil |
| NM.CUL Cultura e diversidade | Folclore, festas, povos e regiões brasileiras |

### 🌱 DI: Desenvolvimento Integral *(só atividades no lançamento)*
| Linha | O que acompanha |
|-------|-----------------|
| DI.SOC Socioemocional e valores | Nomear emoções, autorregulação, convivência. Liga-se aos 8 valores do Semear. |
| DI.VPR Vida prática e autonomia | Cuidado de si, da casa e do outro |
| DI.MAM Motor amplo | Equilíbrio, coordenação, ritmo corporal |
| DI.MFI Motor fino | Pinça, recorte, encaixe, costura |

### ✨ Marcos extras por vertente
São linhas ou marcos **adicionais**, que só aparecem quando a vertente é a principal da família (ou entra como inspiração, se o pai quiser):

- **Montessori:** DI.SEN *Educação dos sentidos* (gradações, pares, discriminação sensorial). Marcos extras em DI.VPR (verter, dobrar, preparar alimentos).
- **Waldorf:** DI.RIT *Ritmo e festivais* (rotina, festas sazonais). Marcos de *desenho de formas* em LG.GRA e de *aquarela úmida* em DI.ART.
- **Clássico:** LG.MEM *Memorização e recitação* (poemas, cronologias, listas). Marcos de *narração* em LG.ORA.
- **Religioso:** DI.ESP *Vida espiritual* (oração, histórias sagradas, virtudes), configurável pela tradição da família.
- **Charlotte Mason** *(nova)*: LG.NAR *Narração oral → escrita* (compartilhada com a Clássica), marcos de *copywork* em LG.GRA e de *ditado preparado* em LG.ESC. Nas atividades: *caderno da natureza*, *estudo de pintores* e *estudo de compositores* (categorias de AR). No ritmo: **lições curtas** (o gerador de sessão limita atividades a 10–20 minutos) e **livros vivos** (a curadoria marca livros como "vivos" segundo os critérios de CM).

> **Por que o Unschooling ficou de fora:** ele não usa sequência, sondagem nem sessões planejadas, que são justamente o que o Semear faz. Famílias *unschoolers* ainda podem usar o app como registro (marcar marcos observados), mas não vamos desenhar o produto para elas.

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
  "idiomas": null,                        // só no domínio LI: ["en","fr","la"]
  "bncc": [],                             // códigos da BNCC: OBRIGATÓRIO em LG e MA (portfólio, §8)
  "autoria": { "origem": "ia" | "humano", "revisadoPor": "...", "revisadoEm": "2026-10-20", "status": "rascunho" | "revisado" | "publicado" }
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
  "idioma": null,                         // "en" | "fr" | "la" quando o marco é do domínio LI
  "estado": "nao-observado" | "em-desenvolvimento" | "consolidado",
  "atualizadoEm": "2026-10-13",
  "origem": "sondagem" | "sessao" | "manual"
}

// Observação (histórico: nada é apagado, o estado atual é o mais recente)
{ "childId": "...", "marco": "...", "estado": "...", "data": "...", "sessaoId": "...", "nota": "texto livre" }

// Comprovante de licença (§9.4): emitido e assinado pelo servidor; o app nunca cria nem edita
{
  "contaId": "c_8f3a...",                 // identificador opaco da conta (nunca o e-mail)
  "plano": "familia" | "teste",
  "periodicidade": "mensal" | "anual" | null,   // null no teste
  "inicio": "2026-11-01",                 // inclusivo
  "fim": "2027-11-01",                    // exclusivo; datas no fuso America/Sao_Paulo
  "emitidoEm": "2026-11-01T10:00:00Z",
  "kid": "2026-1",                        // qual chave pública confere a assinatura (permite trocar a chave)
  "assinatura": "..."                     // cobre TODOS os campos acima, numa serialização canônica
}

// Resposta do servidor (§9.4): envelope assinado em volta dos comprovantes; não é guardado como comprovante
{
  "comprovantes": [ /* comprovantes da conta, no formato acima */ ],
  "agoraServidor": "2026-11-01T10:00:05Z", // hora do servidor, usada só para a maior data vista
  "kid": "2026-1",
  "assinatura": "..."                     // cobre comprovantes + agoraServidor
}
```

---

## 5. Regras da jornada

### 5.1 Posição numa linha
- **Fronteira** = o primeiro marco da linha (na ordem) que **não** está *Consolidado*.
- **Marcos ativos** = a fronteira, mais o marco seguinte **se** a fronteira já estiver *Em desenvolvimento* (no máximo 2 por linha).
- Marcos com pré-requisito de outra linha ainda não consolidado aparecem como **"aguardando"** e não são sugeridos, mas o pai pode forçá-los marcando-os como *Em desenvolvimento*. Pré-requisitos da mesma linha não geram "aguardando": a ordem da linha já garante a sequência. Em Línguas, o pré-requisito é lido no mesmo idioma.

### 5.2 Avanço (manual)
- Só o pai muda um marco para *Consolidado*, seja na ficha de registro ou no mapa.
- O app mostra um selo **"parece pronto"** (ícone de broto em linha + texto, sem emoji) quando o marco teve *Consolidado* registrado em **2 sessões diferentes**: a mesma sessão registrada duas vezes conta uma só. É só uma dica. A regra é pura e tem teste unitário.
- O pai também pode marcar um marco como *Consolidado* direto no mapa, por exemplo algo que a criança aprendeu sozinha.
- **"Está aqui"** (posicionamento rápido): os marcos anteriores viram *Consolidado*, o escolhido fica *Em desenvolvimento* e os posteriores que tinham registro voltam a *Não observado*.

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

### 5.8 Diretrizes visuais das folhas
- **Colorido suave:** fundos pastel (azul, pêssego, amarelo, verde, lilás) atrás das figuras, com texto e contornos escuros. As cores servem de apoio, nunca de informação: a atividade precisa funcionar impressa em preto e branco (ex.: nunca "pinte o que está no quadro azul").
- **Economia de tinta:** a cor fica só nos cartões e figuras. O fundo da página e as áreas de escrita são brancos.
- **O verde Semear** aparece só nas páginas do educador (roteiro, materiais, ficha). As folhas da criança levam apenas um 🌱 discreto.
- **Tipografia da criança:**
  - *Bastão* = Andika em caixa alta (fonte feita para alfabetização).
  - *Script* = Andika minúscula.
  - *Cursiva* = Playwrite BR (modelo de letra cursiva escolar brasileira).
  - O padrão por idade e vertente:

    | | 3–5 anos | 5–6 anos | 6+ anos |
    |---|---|---|---|
    | **Padrão** | bastão | script | cursiva |
    | **Montessori / Waldorf** | cursiva desde o início | cursiva | cursiva |

- **Tipo de atividade por vertente** (mesma identidade visual):

  | Vertente | Mais | Menos |
  |---|---|---|
  | Montessori | recortar, parear, manipular (cartas, bandeja com objetos reais) | exercícios repetitivos |
  | Waldorf | desenho livre, espaço em branco, versos e movimento | figuras prontas, letras isoladas cedo |
  | Charlotte Mason | narração, cópia, caderno da natureza, lições curtas | fichas de completar |
  | Clássico | recitação, cópia, listas para memorizar | |
  | Religioso | segue a base comum, mais atividades de DI.ESP | |

- **Modo tablet:** só as folhas da criança, uma por tela. As páginas do educador ficam de fora.
- **Ilustrações:** o protótipo usa emojis. A versão final precisa de **um banco próprio de ilustrações** (licenciadas ou encomendadas), com traço consistente e que funcione em preto e branco.

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

## 7. Pipeline de conteúdo com IA

A IA é usada **só pela equipe**, na produção. As famílias recebem arquivos JSON estáticos e revisados, então o app continua offline e sem custo de IA por uso.

```
 1. Briefing       →  2. Rascunho IA       →  3. Validação automática  →  4. Revisão humana  →  5. Publicação
 (linha, idade,       (marcos, sondagens,     (schema JSON, campos        (checklist abaixo,    (status
  vertente, BNCC)      atividades, folhas)     obrigatórios, BNCC          edição livre)         "publicado",
                                               existe, idade coerente)                          entra no app)
```

**Checklist de revisão (por marco ou atividade):**
- [ ] O marco é **observável** (dá para o pai ver acontecer)?
- [ ] A ordem dentro da linha faz sentido pedagogicamente?
- [ ] O código BNCC está correto (conferido na base oficial, sem confiar na IA)?
- [ ] O critério da sondagem é claro para um pai leigo?
- [ ] A atividade é viável em casa, com materiais comuns?
- [ ] Para línguas: a grafia, os acentos e a pronúncia de referência estão corretos?
- [ ] O tom é brasileiro e natural, sem cara de tradução?

**Regras:**
- Todo item tem `autoria` (ver §4.1). Só itens com status `publicado` aparecem no app.
- Prompts e briefings ficam versionados no repositório (`content/prompts/`), para gerar lotes consistentes.
- Os rascunhos ficam separados do conteúdo publicado (`content/rascunhos/` → `data/journey/`).

---

## 8. Portfólio: proteção das famílias

### 8.1 Contexto (out/2026)
- Em 2018 o STF decidiu que a educação domiciliar **não é inconstitucional, mas depende de lei federal** que a regulamente. Até hoje essa lei não existe.
- O **PL 1338/2022** foi aprovado na Câmara em maio/2022 e **segue no Senado**. Em 2026 houve audiência pública (junho) e um pedido de urgência (julho), mas ainda sem votação.
- Na prática, a família corre o risco de ser questionada pelo **Conselho Tutelar** ou pelo **Ministério Público** (alegação de abandono intelectual). A melhor defesa conhecida é **demonstrar, com evidências organizadas e datadas, que a criança está sendo educada e está aprendendo**.
- Pelo que lembramos do texto aprovado pela Câmara (**precisa ser conferido** e pode mudar no Senado), ele prevê **matrícula em instituição credenciada**, **relatórios periódicos (trimestrais)** das atividades e **avaliações anuais** com base na **BNCC**. Nada disso está confirmado nas fontes que consultamos.

### 8.2 Recomendação: portfólio de evidências trimestral com anexo BNCC
Recomendo **combinar as duas opções** do grilling, porque cada uma protege de um jeito:

| Parte | O que contém | Por que protege |
|---|---|---|
| **1. Relatório narrativo do trimestre** | Período, carga horária por domínio, frequência (dias de sessão), vertente, resumo do educador | Mostra **regularidade**, o principal argumento contra o "abandono" |
| **2. Progresso na jornada** | Marcos consolidados no período por domínio e linha, com data e origem (sondagem ou sessão) | Mostra **aprendizagem**, não só atividade |
| **3. Evidências** | Amostras dos trabalhos (fotos das folhas preenchidas, desenhos, gravação de leitura), sondagens datadas, livros lidos | É **prova material**, difícil de contestar |
| **4. Anexo BNCC** | Tabela marco → código BNCC → data em que foi consolidado | Mostra **equivalência com a escola** e já se adianta ao provável critério legal |

**Decisões de produto que isso implica:**
1. **O código BNCC é obrigatório** em todo marco de LG e MA. Línguas e artes não têm equivalente direto na BNCC antes do 6º ano: aparecem como "enriquecimento curricular".
2. **Período trimestral** (jan–mar, abr–jun…), alinhado ao que o PL prevê, com a opção de gerar um relatório anual consolidado.
3. **Integridade:** ao "fechar o trimestre", o relatório é gerado com data e um resumo verificável (*hash*) e os registros daquele período ficam bloqueados para edição, só aceitando adendos datados. Isso dá credibilidade ao documento.
4. **Foto da folha** direto da ficha de registro: o pai fotografa a folha preenchida e ela fica ligada à sessão e aos marcos. É o único momento em que o app usa câmera, e quem tira a foto é sempre o pai.
5. **Registro de frequência automático:** toda sessão registrada conta como dia letivo, com duração.
6. **Exportação em PDF** pronta para imprimir e arquivar, mais o JSON de backup. Tudo gerado no dispositivo.
7. **Fotos só no aparelho** (decisão 34), comprimidas, e o app orienta a fotografar **o trabalho, não o rosto da criança**.
8. **Risco de perda:** como não há nuvem, se o aparelho for perdido as evidências vão junto. Para reduzir esse risco:
   - **Lembrete de fechamento trimestral:** gerar o PDF do portfólio (com as fotos embutidas) e salvá-lo fora do app (e-mail, Drive, pendrive).
   - **Backup completo** (JSON + fotos num arquivo .zip) a qualquer momento, com lembrete mensal.
   - Aviso claro no onboarding: *"Seus dados e fotos ficam só neste aparelho."*
9. **Fim do teste ou cancelamento** (decisão 31): a família volta para o plano Livre e **nunca perde o histórico**. O portfólio completo (evidências + anexo BNCC) é gerado em **qualquer plano e para qualquer período**, inclusive os que a família passou só no Livre. Ver §9.

**Antes de lançar:** validar o modelo de relatório com um advogado da área e com associações de famílias educadoras (ex.: ANED). O app **não oferece aconselhamento jurídico** e precisa dizer isso no próprio relatório.

---

## 9. Modelo de negócio: plano Livre + assinatura por família

> Revisado em out/2026 (ADR 0010). Substitui o modelo anterior: teste de 30 dias com cartão, assinatura por criança e bloqueio total depois do teste.

### 9.1 Por que este modelo
> Fontes consultadas em 14/10/2026, a conferir antes de usar fora deste documento: estimativa da ANED citada pelo Correio Braziliense (17/07/2026) e pelo Portal Tela (02/07/2026); situação do PL 1338/2022 na página da Comissão de Educação do Senado e na Gazeta do Povo; requisito de CNPJ do Pix Automático no blog do Mercado Pago. A decisão do modelo não depende dos números exatos.

- **O mercado de homeschooling é pequeno e cresce rápido.** A ANED estima cerca de 75 mil famílias e 150 mil estudantes em 2026; em 2022 eram cerca de 35 mil famílias. São estimativas da associação, não há dado oficial. A **escala está no afterschooling**, e o homeschooling é a comunidade de entrada.
- **A regulação está parada.** O PL 1338/2022 aguarda a Comissão de Educação do Senado e deve andar só a partir de 2027. Enquanto isso, o histórico e o portfólio (§8) são o que protege a família, então **não podem ficar reféns de pagamento**.
- **O custo por usuário é quase zero** (local-first, ADR 0002). O custo real é produzir conteúdo, e **é isso que a família paga**: pacotes novos toda semana.
- **Cobrar por criança não se sustenta.** O número de crianças só existe no aparelho; conferir isso no servidor iria contra o princípio de privacidade (§1.5).
- **O Semear antigo era 100% gratuito** e as comunidades de famílias educadoras divulgam boca a boca. Um plano gratuito permanente preserva esse alcance.
- **ECA Digital (Lei 15.211, em vigor desde 17/03/2026):** mesmo com a criança fora do app, o modelo é pago pela família, **sem anúncios e sem perfilamento**.

### 9.2 Planos
| | **Semear Livre** (grátis para sempre) | **Semear Família** (assinatura) |
|---|---|---|
| Conta | Não precisa | E-mail (só dados do responsável e da assinatura) |
| Crianças | Ilimitadas | Ilimitadas |
| Mapa da jornada e posicionamento | ✅ | ✅ |
| Sondagem impressa | ✅ | ✅ |
| Histórico, backup e exportação | ✅ sempre | ✅ |
| Pacotes de sessão gerados | **Limitado** (1 por semana ou uma amostra por domínio, a decidir no piloto) | **Ilimitados** + sessão conjunta de irmãos |
| Livros, vertentes e trilhas de línguas | Básico | Completo |
| Portfólio trimestral | **Completo** (evidências + anexo BNCC, §8) | **Completo** (evidências + anexo BNCC, §8) |

**O portfólio não depende do plano:** é ele que protege a família (§8), então sai completo para qualquer período, assinado ou não, e não depende de comprovante de licença. O app nunca bloqueia o acesso aos dados da família. A família paga pelo **conteúdo novo toda semana**, não pela proteção.

**Por que esse recorte:** a sondagem grátis é o gancho de aquisição, principalmente no afterschooling ("descubra em 15 minutos onde seu filho está na alfabetização"). A família assina quando quer o conteúdo novo toda semana.

### 9.3 Teste e preço
1. **Teste de 14 a 30 dias com tudo liberado, só com e-mail, sem cartão.** No fim, a família volta para o Livre ("reverse trial"). O app avisa alguns dias antes. **Um teste por e-mail verificado** (o e-mail é confirmado antes de o teste começar).
2. **Preço por família**, com crianças ilimitadas (valores a testar no piloto):
   - **Mensal:** R$ 29,90.
   - **Anual (padrão):** R$ 239 (cerca de R$ 20 por mês), em até 12x no cartão ou **Pix à vista**.
3. **Família fundadora:** quem entra no piloto paga R$ 149 por ano, com o preço garantido enquanto continuar assinando. É uma **pré-venda fora do app** (link de pagamento do gateway, que recebe só nome, e-mail e dados de cobrança do responsável), e a licença é ativada quando a conta existir (§12.3): a compra é ligada à conta pelo e-mail do pagamento, **só depois de esse e-mail ser verificado na conta** (senão alguém que soubesse o e-mail poderia criar a conta antes e ficar com a licença), e o `inicio` do comprovante é a **data de ativação**, para a família não perder parte do ano pago (é a única exceção à regra de renovação contígua do §9.4). Manter o preço de fundadora é regra de cobrança do backend, não do app. O prazo máximo para ativar e o reembolso de uma pré-venda nunca ativada ficam nos termos da pré-venda (§11). **Antes de abrir a pré-venda:** gateway escolhido, com contrato de operador de dados; termos de uso e política de privacidade publicados (quais dados, finalidade, base legal, retenção, contato do encarregado); e a página de pagamento dizendo que nenhum dado da criança é coletado, sem campos sobre os filhos nem campos extras. A pré-venda é uma coleta de dados fora do código, então essa trava vale mesmo antes do ADR de backend. O link de pagamento **nunca** é chamado nem embutido no app (sem `fetch` nem iframe): ele vive só fora do app. Quem renova dentro dos 7 dias de tolerância mantém o preço de fundadora. Isso ajuda a financiar o primeiro lote de conteúdo.
4. **Por que o anual como padrão:** combina com o ano letivo das famílias, reduz cancelamentos e dispensa cobrança recorrente no lançamento. O **Pix Automático exige CNPJ ativo há mais de 6 meses**, então a recorrência mensal pode entrar depois.
5. **Distribuição:** PWA instalável, com cobrança na web por um gateway brasileiro com Pix e cartão (Asaas, Mercado Pago, Pagar.me ou Stripe BR), sem a taxa de 15–30% das lojas.

### 9.4 Arquitetura que isso exige
- **O plano Livre funciona sem conta e sem servidor**, como a v1 de hoje.
- **Backend mínimo**, só para quem testa ou assina: autenticação, status da assinatura e webhooks do gateway (ex.: Supabase + função serverless).
- **O servidor não sabe quantas crianças existem**, nem quem são, nem o que aprenderam. Ele só sabe que aquela conta tem uma licença válida até uma data.
- **Licença como "data de validade":** o app guarda um comprovante assinado (§4.2) com o início e o fim do período e funciona offline. Só a **chave pública** fica no app; a privada fica só no servidor.
- **Regra pura no domínio:** `planoEfetivo(comprovantesVerificados, agora, maiorDataVista, contaIdAtual)` decide o plano (ADR 0003); `contaIdAtual` é nulo quando não há conta conectada. O `contaId` vale para os dois planos: comprovante `familia` ou `teste` de outra conta, ou sem conta conectada, não dá plano. Precedência: o plano efetivo é o maior entre `familia` com hoje < `fim + 7 dias` (inclui a tolerância) e `teste` com hoje < `fim`; sem nenhum dos dois, Livre. O **limite do Livre** fica em outra função pura, `podeGerarPacote(plano, limiteLivre, pacotesNaSemana)`, com o limite injetado (como "agora"), sem valor fixo no domínio, até o piloto decidir (§11). A conferência da assinatura usa WebCrypto (assíncrona) e fica em `dados/`; o domínio só recebe comprovantes **já verificados**. Testes de integração em `dados/` (store de licença): comprovante com assinatura alterada, fora do esquema fechado ou com `kid` desconhecido é descartado, e o backup da família nunca inclui o store de licença. Testes unitários: vencimento exato, `fim - 1` → Família, `fim + 6` → Família, `fim + 7` → Livre, `teste` em `fim` → Livre, virada das 21h às 24h em São Paulo (já outro dia em UTC), `familia` na tolerância com `teste` vigente → Família, `teste` de outra conta → Livre, renovação contígua (novo `inicio` = `fim` anterior), `plano: teste` com `periodicidade` não nula e `familia` com `periodicidade` nula descartados, `familia` e `teste` vigentes ao mesmo tempo, relógio voltado, relógio adiantado e depois corrigido (a licença vigente não vira Livre depois da consulta ao servidor), licença vencida com relógio voltado e offline → Livre, relógio adiantado no Livre e depois assinatura → Família, `kid` desconhecido num comprovante novo → mantém o último plano já verificado e pede atualização do app, primeiro comprovante da pré-venda com `inicio` na ativação (não contíguo) → aceito, renovação recebida dentro da tolerância → Família sem buraco, resposta reapresentada com `agoraServidor` anterior ao último aceito → recusada, comprovante inválido ou com `kid` desconhecido descartado antes do domínio, `contaId` diferente da conta conectada → Livre (sem conteúdo novo, mesmo com assinatura válida) e períodos sobrepostos ou com intervalos (família que assina, cancela e volta).
- **Vínculo com a conta:** o plano só vale quando o `contaId` do comprovante é o da conta conectada no aparelho. Repassar um comprovante para outra família não libera nada.
- **Checagem e tolerância:** cada comprovante cobre exatamente o ciclo pago. **Convenção única:** `inicio` inclusivo, `fim` exclusivo (o primeiro dia já fora do ciclo, também no teste), datas no fuso `America/Sao_Paulo`; uma renovação começa no `fim` anterior, sem sobreposição nem buraco. No plano `familia` (mensal e anual), o app tenta renovar a partir de 7 dias antes do `fim`. Depois do `fim`, há **7 dias de tolerância**: o plano Família vale enquanto a data de hoje em São Paulo for menor que `fim + 7 dias` (`fim + 6` é o último dia; `fim + 7` já é Livre). O domínio converte `agora` (instante UTC) para a data de São Paulo com uma função pura, sem depender do fuso do aparelho. A tolerância vale só para o plano `familia` e só para o plano efetivo: o plano `teste` **não** tem tolerância, e os dias de tolerância **não** ampliam o período coberto para o portfólio.
- **Assinatura do comprovante:** cobre todos os campos (§4.2), inclusive `plano` e `contaId`. O algoritmo (ex.: Ed25519 via WebCrypto), a serialização canônica e a troca de chaves (`kid`) ficam no ADR de backend. Ao ser recebido do servidor e ao ser lido do store de licença, o comprovante passa por um **esquema fechado** (só os campos do §4.2, formato e tamanho máximo de `contaId`, `kid` e `assinatura`, `kid` conhecido, `periodicidade` só `mensal`, `anual` ou nula, e um limite de comprovantes guardados; os valores exatos desses limites ficam no ADR de backend, antes de o validador ser escrito). Os campos `contaId`, `kid` e `assinatura` só são exibidos através do `html``` de `src/ui/html.ts`, para evitar injeção de HTML. O comprovante também passa por regras de coerência (`plano` só `familia` ou `teste`; `teste` exige `periodicidade` nula e `familia` exige `mensal` ou `anual`; datas válidas; `fim` depois de `inicio`). Comprovante que falha é **descartado**.
- **Relógio do aparelho:** o app guarda a maior data que já viu e usa a maior entre ela e o relógio, então voltar a data do aparelho não estende a licença. Essa data fica no store de licença do IndexedDB (separado dos dados da família e fora do backup) e é validada ao ser lida (data ISO válida; valor mal formado é descartado). Ela só muda por dois caminhos: (1) o relógio do aparelho, quando é maior; (2) a **hora do servidor** (`agoraServidor`), que vem assinada em toda resposta do servidor (consulta de status a cada abertura com internet e conta conectada, renovação e o recebimento do primeiro comprovante). Com a hora do servidor verificada, a maior data vista passa a ser **exatamente** ela: sobe se o relógio estava atrasado e desce se estava adiantado por engano. O `emitidoEm` de comprovantes, inclusive importados, nunca altera essa data. No plano Livre não há licença, mas o primeiro comprovante recebido já traz a hora do servidor, então uma licença nova nunca nasce vencida. **Risco aceito:** a proteção vale só no mesmo aparelho e se perde ao restaurar o backup em outro ou limpar o navegador. Fraude de licença não ameaça a privacidade da criança.
- **Comprovantes fora do backup:** os comprovantes ficam só no store de licença do IndexedDB e **nunca vão no backup** da família, então o arquivo exportado não leva o `contaId` e não liga os dados das crianças à conta do responsável. Ao entrar na conta em outro aparelho, o app baixa os comprovantes de novo. Como o portfólio não depende deles, restaurar um backup nunca muda o que a família pode gerar.
- **Fim da licença:** o app volta para os limites do Livre. Nenhum dado é apagado ou escondido.
- **Antes de qualquer código de conta ou assinatura:** um **ADR próprio de backend e privacidade**. Nada da criança vai para o servidor. O ADR precisa cobrir, no mínimo:
  - dados que o gateway e o Supabase recebem (só e-mail e dados de cobrança do responsável), retenção, base legal na LGPD, consentimento e **transferência internacional** (LGPD art. 33) se algum serviço estiver fora do Brasil;
  - algoritmo e serialização canônica da assinatura, e troca de chaves (`kid`);
  - a renovação envia **só** o token da conta: um teste falha se o corpo, os cabeçalhos ou a URL levarem qualquer outro dado; logs do servidor guardam o mínimo (retenção do IP definida, sem `User-Agent`, `Referer`, cookies ou dados além do necessário; a requisição não leva a maior data vista nem nada derivado das crianças);
  - token guardado num store separado, **fora do backup e do `localStorage`**; todo texto vindo do servidor passa pelo `html```;
  - toda resposta do servidor traz `agoraServidor` assinado; o app só aceita a hora do servidor com assinatura válida, e uma resposta antiga reapresentada (com `agoraServidor` anterior ao último aceito) é recusada;
  - token de **curta duração, revogável e com escopo só de renovação da licença** (um token roubado não dá acesso a nada além de e-mail e validade); CSP estrita, sem `unsafe-inline`, com `connect-src` restrito ao domínio do backend;
  - atualizar a regra de chamadas externas do `CLAUDE.md` (hoje só as Fontes do Google);
  - um teste por e-mail verificado e o vínculo da pré-venda só com conta de e-mail verificado.
- **Sync opcional** entre aparelhos e responsáveis: criptografado de ponta a ponta, para o servidor não conseguir ler os dados da criança. As fotos não sincronizam (decisão 34). **Fica fora da primeira fase** de conta e assinatura e terá ADR próprio.

### 9.5 Riscos e o que medir no piloto
> **Como medir sem telemetria:** o app não envia dados de uso (CLAUDE.md, Privacidade). No piloto, os números vêm de **entrevistas e de um questionário voluntário**, em que a família informa quantos pacotes gerou (o app pode mostrar essa contagem na tela, sem enviá-la), e da conversão registrada pelo gateway de pagamento. Qualquer telemetria futura exige um ADR próprio.

| Risco | Por que importa | Como acompanhar |
|---|---|---|
| **Livre generoso demais** | Pouca gente assina. | Medir a conversão do Livre e do teste para o pago. Ajustar o limite de pacotes, nunca o acesso ao histórico. |
| **Livre restrito demais** | A família não percebe valor e abandona antes de assinar. | Medir quantos pacotes por semana as famílias geram e em que ponto param. |
| **Preço** | Errar para cima trava a conversão; para baixo, não paga o conteúdo. | Testar duas faixas (ex.: R$ 19,90 × R$ 29,90 por mês) e perguntar o preço "caro demais" e "barato demais para confiar" (§12.2). |
| **Teste repetido com outros e-mails** | A família ganha pacotes ilimitados por mais tempo sem pagar. | **Risco aceito:** um teste por e-mail verificado barra o caso comum; criar vários e-mails não compensa para a maioria e não afeta a privacidade de ninguém. Acompanhar no piloto. |
| **Afterschooling não chega** | A escala depende dele. | Medir quantas famílias de afterschooling chegam pela sondagem grátis. |

### 9.6 Receitas futuras (nesta ordem)
1. **Plano Educador** (faixa de R$ 49 a 79 por mês): tutoras de alfabetização, psicopedagogas e microescolas que acompanham muitas crianças. Os dados continuam no aparelho dela.
2. **Parcerias com associações** (ANED, cooperativas, grupos regionais): cupom para associados.
3. **Kits físicos ou gráfica sob demanda:** só depois de validar a retenção.
4. **Nunca:** anúncios, venda de dados ou qualquer receita que dependa de enviar dados da criança para fora do aparelho.

---

## 10. Benchmark: o que existe lá fora e onde o Semear se diferencia

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

## 11. Questões em aberto (próximas rodadas)

- [x] ~~**Reconsiderar o bloqueio total**~~: resolvido. O fim do teste volta para o plano Livre (decisão 31, ADR 0010).
- [ ] **Preço exato** do plano Família (por família, ver §9.3). Testar 2 faixas no piloto.
- [ ] **Duração do teste:** 14 ou 30 dias? Para o piloto, usar **30 dias** e comparar com 14 na primeira turma de lançamento.
- [ ] **Termos da pré-venda:** prazo máximo para ativar e reembolso de pré-venda nunca ativada.
- [ ] **Pré-condições da pré-venda** (§9.3): gateway com contrato de operador, termos e política de privacidade publicados.
- [ ] **ADR de backend e privacidade** (conta, comprovante de licença, gateway, CSP), antes de qualquer código de assinatura (§9.4).
- [ ] **Limite do plano Livre:** 1 pacote por semana ou uma amostra por domínio? Decidir com os dados do piloto (§9.5).
- [ ] **Gateway de pagamento:** Asaas × Mercado Pago × Pagar.me × Stripe BR (Pix à vista, parcelamento no cartão; Pix Automático exige CNPJ com mais de 6 meses).
- [ ] **Necessidades específicas** (TEA, TDAH, dislexia): adiado. Revisitar depois do piloto.
- [ ] **Validação jurídica** do modelo de portfólio (advogado + associação de famílias).
- [ ] **Termos de uso e política de privacidade** (LGPD, dados de crianças, cobrança recorrente).
- [ ] **Banco de ilustrações** próprio (encomendar × licenciar) para substituir os emojis do protótipo.

---

### 11.1 Ideias guardadas para a curadoria de livros (usar quando montarmos a curadoria)
- **Preferência da fundadora:** literatura **mais clássica, com ilustrações belas**.
- **Fonte sugerida por ela:** [Free Kids Books](https://freekidsbooks.org/toddler/) (livros infantis gratuitos em inglês, para leitura online). Útil para a trilha de inglês.
- **Outras fontes a pesquisar (sem verificar ainda):** Project Gutenberg e Internet Archive (clássicos ilustrados em domínio público, ex.: Beatrix Potter, Randolph Caldecott), StoryWeaver (livros com licença aberta em vários idiomas, inclusive francês e português), International Children's Digital Library, e o portal Domínio Público do governo brasileiro.
- **Cuidado:** conferir a **licença** de cada livro antes de linkar ou reproduzir ilustrações em folhas (domínio público ≠ licença Creative Commons ≠ só leitura online).

---

## 12. Próximos passos: protótipo do pacote primeiro

### 12.1 Protótipos prontos
Dois pacotes completos, de domínios e vertentes diferentes, para testar com as famílias:

| Pacote | Marco | Criança de exemplo | Vertente | Letra | Arquivos |
|---|---|---|---|---|---|
| Caça às sílabas | **LG.FON.04** sílaba inicial (+ revisão LG.FON.03) | 5 anos | Montessori + Waldorf | bastão | [HTML](../prototipos/sessao-lg-fon-04.html) · [PDF](../prototipos/sessao-lg-fon-04.pdf) |
| Feira dos números | **MA.SEN.06** contar até 20 com objetos (+ revisão MA.SEN.05) | 6 anos | Charlotte Mason + Clássico | script | [HTML](../prototipos/sessao-ma-sen-06.html) · [PDF](../prototipos/sessao-ma-sen-06.pdf) |

Os dois usam o mesmo estilo compartilhado ([`pacote.css`](../prototipos/pacote.css)), que vira a base dos templates do gerador de sessões. A estrutura do pacote de Linguagem está abaixo; o de Matemática segue a mesma ordem (conte e circule, quadros de dez, onde tem mais, cartas para recortar).

| Pág. | Para quem | Conteúdo |
|---|---|---|
| 1 | Educador | Roteiro: objetivo, passo a passo com falas sugeridas, o que observar, ajustes na hora |
| 2 | Educador | Materiais (destaca o que já existe em casa), livro sugerido e toque da vertente |
| 3 | Criança | Folha 1: ligue as figuras que começam igual |
| 4 | Criança | Folha 2: pinte o quadradinho (SA·PO, BA·NA·NA) |
| 5 | Criança | Folha 3: jogo da memória para recortar (o par começa igual) |
| 6 | Criança | Folha 4: desenho livre |
| 7 | Educador | Ficha de registro rápido (marcos × 3 estados, evidências, engajamento) |

Para usar, abra no navegador e use a barra no topo:
- **Imprimir / salvar PDF:** gera o pacote em A4.
- **Modo tablet:** mostra só as folhas da criança.
- **Letra da criança:** troca entre bastão, script e cursiva.

### 12.2 Teste com famílias (2 a 3 semanas)
**Quem:** 3 a 5 famílias com crianças de 4 a 6 anos. Pelo menos uma de afterschooling, uma Montessori ou Waldorf e uma que use tablet.

**Como:**
1. Enviar o PDF (ou o HTML) **sem explicar nada** além de "prepare e aplique esta sessão".
2. A família aplica a sessão e preenche a ficha.
3. Fazer uma conversa de 20 minutos depois, com as perguntas abaixo.

**Perguntas:**
- Quanto tempo levou para **preparar**? E a sessão em si?
- O roteiro deixou claro **o que fazer e o que falar**? O que ficou confuso?
- A criança entendeu as folhas **sem ajuda** para entender o enunciado?
- A ficha de registro foi fácil? Você saberia decidir entre "em desenvolvimento" e "consolidado"?
- Imprimiu em cores ou em P&B? Ficou bom? Usou o tablet?
- **Você pagaria por um app que gerasse isso toda semana, ajustado ao seu filho?** Quanto?
- A partir de que preço por mês, para a família toda, isso seria **caro demais**? E abaixo de que preço você **desconfiaria** da qualidade?

**Sinais de sucesso:**
- Preparação em ≤ 10 minutos.
- A criança se engaja (😄 ou 🤩 na ficha) em pelo menos 3 de 5 famílias.
- Os pais conseguem classificar o marco sem nos perguntar.
- Pelo menos 2 famílias dizem que pagariam.

### 12.3 Depois do teste
1. Ajustar o template do pacote com base no que as famílias disseram.
2. Pipeline de conteúdo (§7): primeiro lote de LG.FON, LG.ESC, MA.SEN e MA.OPE.
3. App: modelo de dados → mapa da jornada → sondagem → gerador de sessão (reaproveitando este HTML como template) → portfólio.
4. Conta + assinatura por último, quando o núcleo estiver validado. Antes disso, a pré-venda da família fundadora (§9.3) usa só um link de pagamento do gateway, fora do app.
