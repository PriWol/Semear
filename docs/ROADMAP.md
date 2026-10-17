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
- **Sem prévia por PR, por enquanto** (proposta de 14/10/2026, a ser decidida na #40 e registrada em ADR): cada mudança é testada no site publicado, logo depois do merge, então um bug chega ao site antes do teste manual. O rollback é reverter o merge no `main`, mas **dados já gravados no IndexedDB por uma versão ruim não voltam com o revert**; por isso toda mudança de formato de dados precisa de migração testada. Além disso, o IndexedDB recusa abrir um banco de versão mais nova com o app antigo (`VersionError`), então, antes de testar uma fase com migração, faça o **backup** pela tela do app, e o ADR da #40 deve exigir migrações que o app anterior consiga ler e descrever como o service worker do PWA é atualizado depois de um revert.
- **Seus testes** (manuais, no site publicado): cada fase tem um roteiro curto, abaixo. A **família de
  exemplo** (Fase 0) deixa você testar tudo em 1 minuto, sem digitar dados.
- As fases 0 a 3 listam os testes automáticos novos que entram com elas. Nas fases 4 a 6, eles estão nos critérios de
  aceite de cada estória e serão detalhados quando a fase chegar.

## Revisão de out/2026: lançar aberto ao público, afterschooling primeiro

Decisões da dona do produto (16/10/2026) que reordenam o plano:

- **Meta:** lançar aberto ao público, com tudo polido (não há piloto fechado antes). O piloto (#28) vira
  acompanhamento dos primeiros usuários depois do lançamento.
- **Público inicial:** afterschooling (famílias com filhos na escola ou creche que complementam em casa).
  Homeschooling vem depois.
- **Faixa etária:** de **2 a 8 anos** (antes 3 a 8). Inclui creche, maternal e jardim.
- **Sessão:** 30 minutos de atividade, mais o tempo de preparação do pai.
- **Novo domínio:** formação e regulação emocional (hoje só existe o esboço DI.SOC na especificação, §5).
- **Livros, obras e músicas:** dentro de cada sessão, numa estante separada, depois como venda de produtos
  de terceiros e, mais adiante, dos livros da própria autora.
- **Conteúdo:** revisado pela dona do produto. Depois, um login de **preceptor** (revisar, comentar, aprovar,
  anexar imagens e texto) cujo envio vira entrada para a IA rascunhar a versão final.
- **Comunidade de trocas:** só depois do lançamento.
- **Assinatura: a revisitar.** Ideia atual: 7 dias grátis com restrição de materiais (ex.: Tesouro de Marina), depois
  R$ 39,90 por mês por família + R$ 10 por criança. Conflita com o ADR 0010 (ver "Riscos" abaixo).

### Etapas (substituem a tabela de fases; os detalhes das Fases 0 a 6 abaixo seguem valendo como referência)

| Etapa | O que fecha | Estórias |
|---|---|---|
| A · Arrumar a casa | Roteiro e GitHub fiéis ao código; PRs de conteúdo e Dependabot mergeados | auditar #31 #33 #36 #38 #39 #41 #42; PRs #55 #64 a #67 |
| B · Ciclo da sessão (sessão de 30 min) | Preparar → imprimir → aplicar → registrar → jornada sugere | #11 #13 #2 (parte 1) |
| C · Faixa de 2 a 8 anos e emoções | Spec e conteúdo para 2 anos; domínio Formação e regulação emocional | novas: faixa 2–8, domínio emocional |
| D · Rotina de afterschooling | Plano e impressão da semana | #8 #9 #2 (parte 2) |
| E · Estante e indicações | Livro, obra ou música em cada sessão; estante filtrável | #12 · novas: tipo obra e música, indicação por sessão, ADR de links de terceiros |
| F · Conteúdo para o lançamento | Lotes revisados pela dona; status de revisão no conteúdo | #21 #22 #23 #24 |
| G · Pronto para abrir | Domínio, CSP, guia das vertentes, sondagem curta, termos/LGPD | #34 #32 #30 #17 #25 |
| H · Conta e cobrança | Primeiro servidor: conta, teste, assinatura, restrição de materiais | #26 #3 #6 #5 · nova: revisão do modelo de preço (ADR 0010) |
| I · Lançamento | Landing page e abertura ao público (v1.0) | #4 |
| Depois | Portfólio e homeschooling, irmãos, sincronização, portal do preceptor, comunidade, livros próprios | #10 #18 #19 #20 #27 #29 · novas: portal do preceptor, comunidade |

Rebaixadas para "Depois" porque o afterschooling não precisa delas no dia 1: portfólio jurídico (#20, #29), ressondagem (#18),
fotos de evidências (#10), sessão de irmãos (#19). Sincronização (#27) sai do caminho do lançamento.

### Riscos e perguntas abertas

1. **Cobrança por criança contradiz o ADR 0010.** Com dados só no aparelho, o servidor não sabe quantas crianças a
   família tem; cobrar por criança ou exige guardar essa contagem no servidor (muda a regra de privacidade) ou depende de
   declaração do pai na compra. Decidir antes da etapa H.
2. **Restringir o Tesouro de Marina não funciona hoje.** Os PDFs são servidos pelo site estático (ADR 0015), então quem
   sabe o endereço baixa tudo. Restringir de verdade exige servidor com link assinado (etapa H) ou um recorte do que fica
   livre. Até lá, o Tesouro completo fica disponível a todos.
3. **O que acontece depois dos 7 dias?** Volta ao plano Livre (ADR 0010) ou bloqueia? O ADR 0010 diz que dados e histórico nunca ficam reféns.
4. **Links de afiliado e venda de terceiros** exigem ADR (privacidade e ECA Digital: sem anúncios nem perfilamento).
   Proposta: só na estante, nunca na folha da criança, sem rastreio no app, com aviso de afiliado.
5. **Crianças de 2 anos:** o pacote precisa de atenção a materiais pequenos (engasgo) e a sessões de 30 min que sejam
   várias atividades curtas; o texto da especificação (§1, decisão 2) e os marcos precisam de revisão pedagógica.
6. **Portal do preceptor** é um segundo produto (login, upload de imagens, fila de revisão, integração com a IA). Até
   existir, o fluxo de revisão é o PR no GitHub, e cada marco ou atividade ganha um campo `revisao` (rascunho, revisado, aprovado).

---

## Fase 0 · Base para testar (v0.2)

**Objetivo:** deixar o site publicado fácil de testar e transparente sobre o que está no ar.

| Estória | O que entrega |
|---|---|
| #38 Versão publicada e novidades | Versão + data no topo e em Configurações; página "Novidades" com o que mudou em cada versão |
| #39 Família de exemplo | Botão "Explorar com uma família de exemplo": cria 2 crianças posicionadas e sessões no histórico; "Apagar exemplo" remove só o que é do exemplo (famílias reais ficam intactas) |
| #33 Ficha em 1 página | A ficha de registro cabe numa folha A4 com até 2 atividades |
| #36 Actions por SHA | Segurança da publicação (sem efeito visível) |
| #31 Arquivar site antigo | Repositório limpo (sem efeito visível) |

**Roteiro de teste (celular e computador):**
1. Abra o site numa janela anônima. A versão `v0.2` aparece no topo.
2. Toque em "Explorar com uma família de exemplo". Em segundos, aparecem Ana (5 anos) e Theo (7 anos), já posicionados.
3. Prepare uma sessão de 40 min para a Ana com 2 atividades, imprima e salve em PDF: a ficha ocupa **uma** página.
4. Abra "Novidades" e confira o que mudou na v0.2.
5. Em Configurações, toque em "Apagar exemplo": o exemplo some e o app volta ao estado anterior; num navegador sem outros dados, mostra a tela de boas-vindas.

**Testes automáticos novos:** unitário da família de exemplo (idades a partir de hoje, posições válidas) e da versão; integração "exemplo + família real: só o exemplo some";
integração de carregar/apagar o exemplo; e2e boas-vindas → exemplo → sessão → apagar; e2e que conta as páginas da ficha no PDF.

---

## Fase 1 · Visual novo, moderno e clássico (v0.3)

**Objetivo:** trocar a identidade visual do app e das folhas, sem mudar os fluxos.
**Direção a escolher na #14**, entre as duas candidatas do protótipo: **A · Caderno de botânica** (marfim, verde-musgo e ocre; Fraunces + Inter) e **B · Biblioteca clássica** (creme, azul-tinta e dourado; Libre Caslon + Source Sans). A escolha vira um ADR.
Protótipo: `prototipos/design/direcoes-visuais.html`.

| Estória | O que entrega |
|---|---|
| #14 Look and feel | Escolha da direção (registrada em ADR), `docs/DESIGN.md` com as regras e os tokens (cores, fontes, espaços) |
| #41 Aplicar o visual ao app | Todas as telas no estilo novo; navegação inferior no celular; ícones de linha no lugar dos emojis da interface |
| #42 Aplicar o visual às folhas | Roteiro, folhas e ficha no estilo novo, em preto e branco, economizando tinta |
| #2 Página principal (parte 1) | Cartão da criança com a próxima sessão sugerida e o progresso por domínio |
| #15 Jornada do usuário | Documento do caminho do educador; vira o roteiro dos testes e2e |

**Roteiro de teste:**
1. Com a família de exemplo, passe por todas as telas no celular: início, jornada, preparar sessão, sessão, família e configurações.
2. A navegação inferior (Início, Jornada, Sessões, Família; Configurações fica dentro de Família, e a Estante entra só na Fase 4) leva às seções principais com um toque; nada fica cortado nem precisa de rolagem para o lado.
3. Imprima uma sessão em preto e branco: títulos legíveis, ilustrações em traço e nenhum fundo colorido grande.
4. Compare com o protótipo da direção escolhida.

**Testes automáticos:** os e2e existentes continuam verdes (os fluxos não mudam) e uma verificação de contraste (AA) roda nas telas principais.

---

## Fase 2 · Ciclo completo da sessão (v0.4)

**Objetivo:** depois de aplicar a sessão, o educador registra o que observou; a jornada só sugere ("parece pronto") e o pai confirma no mapa, porque o avanço é manual (decisão 9).

| Estória | O que entrega |
|---|---|
| #11 Informar progresso | "Registrar sessão" pelo código impresso, em cerca de 2 minutos no celular; selo "parece pronto" (ícone de broto + texto, conforme o `DESIGN.md`) |
| #13 Atividades avulsas | Buscar ("rimas", "contar") e imprimir uma atividade só |
| #21 + #22 (conteúdo) | Pipeline de conteúdo e as linhas LG.FON e MA.SEN completas, com BNCC |

**Roteiro de teste:**
1. Família de exemplo → prepare e imprima uma sessão para a Ana.
2. Em "Registrar sessão", digite o código impresso (ex.: `S-1014-A1`) e marque os marcos. As observações ficam no histórico da Ana; a jornada ainda não muda.
3. Na ficha da primeira sessão, marque um marco como *Consolidado* (o marco continua *Em desenvolvimento* no mapa). Prepare e registre uma
   segunda sessão com esse mesmo marco, também como *Consolidado*: aparece o selo "parece pronto". Confirme o marco no mapa: o selo some.
4. Busque "sílaba" (sem acento) e imprima a atividade encontrada.

**Testes automáticos novos:** unitário do registro e do selo "parece pronto" e da busca sem acento; integração do
registro (com migração do banco e backup); importação de backup recusando estados fora de *Não observado / Em desenvolvimento / Consolidado* e contando uma só vez a mesma sessão duplicada; e2e "gerar → registrar" e "buscar → imprimir".

---

## Fase 3 · Rotina da semana (v0.5)

| Estória | O que entrega |
|---|---|
| #8 Plano semanal | Escolher dias e duração; o app distribui as atividades pela semana; calendário por criança |
| #9 Imprimir a semana | Um arquivo com todas as sessões, separadores por dia e a lista de materiais consolidada |
| #2 Página principal (parte 2) | Sessões feitas na semana e a próxima ação sugerida |

**Roteiro de teste:** planeje seg/qua/sex de 40 min para a Ana, imprima a semana (um PDF só, com a lista de materiais no começo), registre a sessão de segunda e veja o dia marcado como feito no início.

**Testes automáticos novos:** unitário do distribuidor semanal e da lista de materiais consolidada; integração do
plano no banco e no backup; e2e "planejar → imprimir a semana".

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

**Antes de começar:** o domínio próprio (#34) é uma decisão estrutural (muda a origem onde os dados ficam) e precisa de ADR aprovado.

**Roteiro de teste:** crie uma família nova no endereço próprio, aplique a sondagem impressa, lance os resultados e confira a posição; abra o guia pelo cadastro e um livro da estante.

---

## Fase 5 · Evidências e portfólio (v0.7)

#10 fotos dos trabalhos (só no aparelho, no backup) · #18 ressondagem a cada 8 semanas · #19 sessão de irmãos ·
#29 validação jurídica → #20 portfólio trimestral em PDF com anexo BNCC.

**Antes de começar:** a validação jurídica (#29) vem **antes** do código do portfólio (#20), porque pode mudar o que o
relatório precisa conter. As fotos (#10) ficam só no aparelho e entram no backup: a importação valida cada arquivo
(tipo, tamanho e vínculo com sessões existentes), como manda o `CLAUDE.md` para todo dado vindo de fora, e o ADR 0002
é atualizado.

**Roteiro de teste:** fotografe 2 trabalhos, gere o portfólio do trimestre, confira frequência, marcos, fotos e o anexo BNCC no PDF; exporte e importe o backup com as fotos.

---

## Fase 6 · Abrir ao público (v1.0)

#25 termos e LGPD (bloqueia o resto) · #26 backend de contas · #3 login · #6 logout · #5 pagamento por família ·
#4 landing page · #27 sincronização entre aparelhos.

**Antes de começar (privacidade é inegociável, `CLAUDE.md`):** hoje nenhum dado sai do aparelho. Esta fase cria o primeiro
servidor, então nada de #26, #3 ou #27 começa sem um **ADR aprovado** que diga o que vai para o servidor (só conta
e assinatura; o servidor não sabe quantas crianças existem, §9.4 "Arquitetura que isso exige"), como os dados da sincronização são criptografados de ponta a ponta, por
quanto tempo ficam guardados e onde. O `CLAUDE.md` (seção Privacidade) e o ADR 0002 são atualizados no mesmo PR.

**Roteiro de teste:** do anúncio à assinatura: landing → uso no plano Livre, sem conta → cadastro por e-mail → teste gratuito → fim do teste volta ao Livre → assinatura em ambiente de teste do gateway → cancelamento → exportação dos dados.

---

## Trilha de conteúdo (contínua, a partir da Fase 2)

#21 pipeline de produção (IA rascunha, pessoa revisa) → #22 Linguagem e Matemática com BNCC → #23 Línguas
(inglês, francês, latim) → #24 banco de ilustrações (substitui os emojis das folhas; segue o visual da Fase 1).
Cada lote de conteúdo é um PR próprio e entra no ar sem esperar as fases de software.
