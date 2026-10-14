# Roteiro de desenvolvimento do Semear

Este documento organiza as estórias do GitHub em **fases**. Cada fase termina com algo que funciona
e que dá para **demonstrar e testar no site publicado** (https://priwol.github.io/Semear/), no
celular e no computador. A fase só fecha quando a dona do produto roda o **roteiro de teste** dela e
aprova.

Cada fase também é uma **versão** do app (Fase 0 = v0.2, Fase 1 = v0.3…). A versão aparece no próprio
app (estória "Versão publicada e novidades"), então dá para saber exatamente o que está no ar.

## Como uma estória vira algo testável

```mermaid
flowchart LR
  A[Estória com critérios de aceite] --> B[Plano aprovado]
  B --> C[Testes automáticos + código]
  C --> D[PR: CI verde + 2 revisores]
  D --> E[Merge no main]
  E --> F[Publicação automática]
  F --> G[Roteiro de teste no site]
  G -->|aprovado| H[Estória fechada]
  G -->|ajustes| B
```

- **Testes automáticos** (rodam em todo PR): unitários nas regras, integração no banco do aparelho e
  ponta a ponta (e2e) simulando o uso no computador e no celular.
- **Seus testes** (manuais, no site publicado): cada fase tem um roteiro curto, abaixo. A **família de
  exemplo** (Fase 0) deixa você testar tudo em 1 minuto, sem digitar dados.

## Visão geral

| Fase | Versão | O que você consegue demonstrar no fim | Estórias |
|---|---|---|---|
| 0 · Base para testar | v0.2 | Abrir o site, ver a versão, carregar uma família de exemplo e imprimir uma sessão numa folha só | #38 #39 #40 #33 #36 #31 (#7 fecha) |
| 1 · Visual novo | v0.3 | Todas as telas e as folhas no visual "moderno e clássico", com navegação de app no celular | #14 #41 #42 #2 (parte 1) #15 |
| 2 · Ciclo da sessão | v0.4 | Preparar → imprimir → aplicar → **registrar no celular** → jornada atualiza sozinha; buscar e imprimir uma atividade avulsa | #11 #13 · conteúdo: #21 #22 |
| 3 · Rotina da semana | v0.5 | Planejar a semana (ex.: seg/qua/sex), imprimir tudo num arquivo só e acompanhar os dias feitos | #8 #9 #2 (parte 2) |
| 4 · Pronto para o piloto | v0.6 | Endereço próprio, sondagem impressa para posicionar, guia das vertentes e estante de livros; 3 a 5 famílias usando | #34 #32 #17 #30 #12 → #28 |
| 5 · Evidências e portfólio | v0.7 | Fotos dos trabalhos, ressondagem, sessão de irmãos e o **portfólio trimestral em PDF** | #10 #18 #19 #29 #20 |
| 6 · Abrir ao público | v1.0 | Landing page, conta, teste de 30 dias, pagamento por criança e sincronização | #25 #26 #3 #6 #5 #4 #27 |
| Trilha de conteúdo | contínua | Mais marcos, atividades, livros e ilustrações a cada lote | #21 #22 #23 #24 |

**Por que esta ordem:**
- A Fase 0 vem primeiro porque tudo depois depende de você conseguir testar rápido o que foi publicado.
- O visual (Fase 1) vem antes das telas novas: assim cada tela nova já nasce no estilo final, sem retrabalho.
- O ciclo da sessão (Fase 2) fecha o "loop" do produto: sem registrar o progresso, a jornada não anda sozinha.
- O **domínio próprio vem antes do piloto** (Fase 4): os dados ficam presos ao endereço onde foram criados.
  Se as famílias do piloto começarem em `priwol.github.io` e depois mudarmos, elas teriam que exportar e importar.
- Conta e pagamento (Fase 6) só depois do piloto confirmar que o núcleo do produto funciona (§12.2).

---

## Fase 0 · Base para testar (v0.2)

**Objetivo:** deixar o site publicado fácil de testar e transparente sobre o que está no ar.

| Estória | O que entrega |
|---|---|
| #38 Versão publicada e novidades | Versão + data no topo e em Configurações; página "Novidades" com o que mudou em cada versão |
| #39 Família de exemplo | Botão "Explorar com uma família de exemplo": cria 2 crianças posicionadas e sessões no histórico; "Apagar exemplo" remove tudo |
| #40 Prévia de cada PR (decisão) | Ver a versão de um PR antes do merge, num endereço separado |
| #33 Ficha em 1 página | A ficha de registro cabe numa folha A4 com até 2 atividades |
| #36 Actions por SHA | Segurança da publicação (sem efeito visível) |
| #31 Arquivar site antigo | Repositório limpo (sem efeito visível) |
| #7 | Já entregue na v1: fechar |

**Roteiro de teste (celular e computador):**
1. Abra o site numa janela anônima. A versão `v0.2` aparece no topo.
2. Toque em "Explorar com uma família de exemplo". Em segundos, aparecem Ana (5 anos) e Theo (7 anos), já posicionados.
3. Prepare uma sessão de 40 min para a Ana com 2 atividades, imprima e salve em PDF: a ficha ocupa **uma** página.
4. Abra "Novidades" e confira o que mudou na v0.2.
5. Em Configurações, toque em "Apagar exemplo": o app volta para a tela de boas-vindas.

---

## Fase 1 · Visual novo, moderno e clássico (v0.3)

**Objetivo:** trocar a identidade visual do app e das folhas, sem mudar os fluxos.
Protótipo com as duas direções propostas: `prototipos/design/direcoes-visuais.html`.

| Estória | O que entrega |
|---|---|
| #14 Look and feel | Escolha da direção, `docs/DESIGN.md` com as regras e os tokens (cores, fontes, espaços) |
| #41 Aplicar o visual ao app | Todas as telas no estilo novo; navegação inferior no celular; sem emojis na interface |
| #42 Aplicar o visual às folhas | Roteiro, folhas e ficha no estilo novo, em preto e branco, economizando tinta |
| #2 Página principal (parte 1) | Cartão da criança com a próxima sessão sugerida e o progresso por domínio |
| #15 Jornada do usuário | Documento do caminho do educador; vira o roteiro dos testes e2e |

**Roteiro de teste:**
1. Com a família de exemplo, passe por todas as telas no celular: início, jornada, preparar sessão, sessão, família e configurações.
2. A navegação inferior leva às seções principais com um toque; nada fica cortado nem precisa de rolagem para o lado.
3. Imprima uma sessão em preto e branco: títulos legíveis, ilustrações em traço e nenhum fundo colorido grande.
4. Compare com o protótipo aprovado.

**Testes automáticos:** os e2e existentes continuam verdes (os fluxos não mudam) e uma verificação de contraste (AA) roda nas telas principais.

---

## Fase 2 · Ciclo completo da sessão (v0.4)

**Objetivo:** depois de aplicar a sessão, o educador registra o que observou, e a jornada se atualiza sozinha.

| Estória | O que entrega |
|---|---|
| #11 Informar progresso | "Registrar sessão" pelo código impresso, em cerca de 2 minutos no celular; selo "🌱 parece pronto" |
| #13 Atividades avulsas | Buscar ("rimas", "contar") e imprimir uma atividade só |
| #21 + #22 (conteúdo) | Pipeline de conteúdo e as linhas LG.FON e MA.SEN completas, com BNCC |

**Roteiro de teste:**
1. Família de exemplo → prepare e imprima uma sessão para a Ana.
2. Em "Registrar sessão", digite o código impresso (ex.: `S-1014-A1`) e marque os marcos. A jornada da Ana muda.
3. Registre o mesmo marco como consolidado numa segunda sessão: aparece o selo "parece pronto".
4. Busque "sílaba" (sem acento) e imprima a atividade encontrada.

---

## Fase 3 · Rotina da semana (v0.5)

| Estória | O que entrega |
|---|---|
| #8 Plano semanal | Escolher dias e duração; o app distribui as atividades pela semana; calendário por criança |
| #9 Imprimir a semana | Um arquivo com todas as sessões, separadores por dia e a lista de materiais consolidada |
| #2 Página principal (parte 2) | Sessões feitas na semana e a próxima ação sugerida |

**Roteiro de teste:** planeje seg/qua/sex de 40 min para a Ana, imprima a semana (um PDF só, com a lista de materiais no começo), registre a sessão de segunda e veja o dia marcado como feito no início.

---

## Fase 4 · Pronto para o piloto (v0.6)

| Estória | O que entrega |
|---|---|
| #34 Domínio próprio | App em endereço próprio (ex.: `app.semear.com.br`), isolando os dados das famílias |
| #32 CSP no app | Segunda camada de proteção contra injeção de código |
| #17 Sondagem inicial | Avaliação impressa que posiciona a criança em cada linha |
| #30 Guia das vertentes | Página que explica as 5 vertentes, com link no cadastro |
| #12 Estante de livros | Livros digitais gratuitos, clássicos e com belas ilustrações, filtráveis |
| #28 Piloto | 3 a 5 famílias por 8 semanas; o relatório define a Fase 5 |

**Roteiro de teste:** crie uma família nova no endereço próprio, aplique a sondagem impressa, lance os resultados e confira a posição; abra o guia pelo cadastro e um livro da estante.

---

## Fase 5 · Evidências e portfólio (v0.7)

#10 fotos dos trabalhos (só no aparelho, no backup) · #18 ressondagem a cada 8 semanas · #19 sessão de irmãos ·
#29 validação jurídica → #20 portfólio trimestral em PDF com anexo BNCC.

**Roteiro de teste:** fotografe 2 trabalhos, gere o portfólio do trimestre, confira frequência, marcos, fotos e o anexo BNCC no PDF; exporte e importe o backup com as fotos.

---

## Fase 6 · Abrir ao público (v1.0)

#25 termos e LGPD (bloqueia o resto) · #26 backend de contas · #3 login · #6 logout · #5 pagamento por criança ·
#4 landing page · #27 sincronização entre aparelhos.

**Roteiro de teste:** do anúncio à assinatura: landing → cadastro → teste de 30 dias → uso → pagamento em ambiente de teste do gateway → cancelamento → exportação dos dados.

---

## Trilha de conteúdo (contínua, a partir da Fase 2)

#21 pipeline de produção (IA rascunha, pessoa revisa) → #22 Linguagem e Matemática com BNCC → #23 Línguas
(inglês, francês, latim) → #24 banco de ilustrações (substitui os emojis das folhas; segue o visual da Fase 1).
Cada lote de conteúdo é um PR próprio e entra no ar sem esperar as fases de software.
