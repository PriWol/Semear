# Decisões pendentes (registro acumulado)

Este arquivo junta as decisões que **dependem da dona do produto** e que travam estórias. Ele não decide nada:
cada item traz as opções, uma recomendação e o que a decisão destrava. Quando uma decisão for tomada, ela vira
um ADR em `docs/adr/` e o item sai daqui (ou fica marcado como decidido, com o número do ADR).

Última atualização: 20/11/2026. Preços e condições de serviços externos **não foram pesquisados**: onde aparecem
como "a pesquisar", confirme antes de decidir.

## Resumo

| # | Decisão | Estórias | Decidir antes de | Já existe |
|---|---|---|---|---|
| D1 | Hospedagem e domínio próprio | #34, #4 | Piloto (Fase 4) | ADR 0009 (GitHub Pages) |
| D2 | Servidor de contas e sincronização | #26, #3, #6, #27 | Fase 6 | Regra de privacidade do `CLAUDE.md` |
| D3 | Modelo de assinatura e cobrança | #75, #76, #5 | Fase 6 | ADR 0010; rascunho no ADR 0027 (PR #96) |
| D4 | App de celular e contas nas lojas | #95 | Publicar nas lojas | ADR 0028 (PR #96) |
| D5 | Termos, LGPD e validação jurídica | #25, #29 | Abrir ao público e portfólio (#20) | nenhum |
| D6 | Links de terceiros e afiliados na estante | #74 | Estante com links externos | nenhum |
| D7 | Quem revisa o conteúdo e o que só aparece aprovado | #77, #78, #21 | Divulgar para outras famílias | campo `revisao` (#77, `app/content/README.md`) |
| D8 | Comunidade de trocas entre famílias | #79 | Depois da Fase 6 | nenhum |

A ordem importa: **D1 vem primeiro** (muda a origem onde os dados ficam), D5 antes de D2 e D3 (o jurídico pode
mudar o que o servidor pode guardar), e D2 antes de D3 (cobrança precisa de conta).

---

## D1. Hospedagem e domínio próprio (#34, #4)

**Hoje:** GitHub Pages em `priwol.github.io/Semear`, publicado por GitHub Actions a cada merge que altera `app/`
(ADR 0009). O ADR registra o risco: todos os sites da conta compartilham a origem `priwol.github.io`, e um script de
outro projeto da conta poderia ler o IndexedDB do Semear. Regra provisória: **não publicar outro projeto nessa conta**.

**Em aberto**
- Qual domínio (ex.: `app.semear.com.br`) e quem registra e paga.
- Onde hospedar depois do domínio: continuar no GitHub Pages com domínio próprio ou migrar de serviço.
- Onde fica a landing page (#4): no mesmo domínio raiz ou separada do app.

**Opções**
1. **Domínio próprio apontando para o GitHub Pages.** Sem mudar o fluxo de publicação, isola a origem, custo só do
   domínio. Sem prévias por PR.
2. **Cloudflare Pages ou Netlify com domínio próprio.** Dá prévia por PR (útil para testar com famílias), mas exige
   conta e configuração externas (ADR 0009, opção 3). Custo a pesquisar.
3. **Ficar como está até o piloto.** Zero custo, mas o risco de origem compartilhada continua.

**Recomendação:** opção 1, com `app.` para o app e a raiz reservada para a landing. Revisitar a opção 2 só se as
prévias por PR fizerem falta no piloto.

**Atenção (consequência técnica):** o IndexedDB é guardado **por origem**. Ao mudar de endereço, as famílias que já
usam o app em `priwol.github.io` **não levam os dados automaticamente**. Duas saídas: decidir isto **antes** de ter
famílias reais (por isso o prazo é "antes do piloto"), ou entregar um aviso com "exportar backup no endereço antigo,
importar no novo" no próprio app. O ADR precisa dizer qual.

**Destrava:** #34 (e o isolamento exigido pela revisão de segurança), #4 (landing) e o endereço fixo para os termos (D5).
**Registro:** novo ADR substituindo a seção "Riscos de privacidade" do ADR 0009.

## D2. Servidor de contas e sincronização (#26, #3, #6, #27)

**Hoje:** nenhum dado sai do aparelho (`CLAUDE.md`, ADR 0002). Esta é a primeira vez que existiria um servidor.

**Em aberto**
- Provedor de contas (e-mail e senha, link mágico, login social) e onde ele guarda dados (região; LGPD).
- O que vai para o servidor. Regra já posta no roteiro: **só conta e assinatura**; o servidor não sabe quantas crianças existem.
- Sincronização entre aparelhos e com o outro responsável (#27): criptografia de ponta a ponta, por quanto tempo
  guardar e como recuperar se a família perder a chave.

**Opções**
1. **Serviço pronto de autenticação (backend como serviço).** Rápido, menos código; atenção ao país onde ficam os dados
   e à dependência do fornecedor. Custos a pesquisar.
2. **Servidor próprio mínimo.** Controle total, mais trabalho de manutenção e segurança para uma equipe pequena.
3. **Sem conta e sem sincronização**, só backup manual (como hoje). Mantém a privacidade total, mas não permite
   cobrança por assinatura verificável nem uso em dois aparelhos.

**Recomendação:** decidir D5 antes. Se o jurídico aceitar, opção 1 só para conta e assinatura, sem dados de crianças;
sincronização (#27) fica para depois, como estória separada com ADR próprio.
**Destrava:** #3, #6, #5, #27. **Registro:** ADR aprovado antes de qualquer código (exigência do roteiro, Fase 6),
junto com a atualização da seção Privacidade do `CLAUDE.md` e do ADR 0002.

## D3. Modelo de assinatura e cobrança (#75, #76, #5)

**Hoje:** o ADR 0010 define Livre grátis + Família (R$ 29,90 por mês ou R$ 239 por ano, a testar), com teste sem cartão.
O PR #96 propõe, em rascunho (ADR 0027 depois da renumeração), R$ 49,90 por mês para uma criança e R$ 69,90 para duas ou mais,
teste de 7 dias e volta a um plano Livre **reduzido**.

**Em aberto (listadas no próprio PR #96)**
- Aprovar ou não o novo modelo. Ele **contradiz o ADR 0010**: o Livre perde jornada, marcos e sondagem, e o ADR 0010
  prometia que o histórico nunca fica refém.
- A lista exata do que fica no Livre, e se o portfólio completo continua nele.
- Preço por faixa (uma criança, duas ou mais) conflita com a regra do ADR 0010 de que o servidor não sabe quantas
  crianças existem: cobrar por faixa exige informar a quantidade no cadastro da assinatura.
- Cobrança dentro do app nas lojas (comissão) e provedor de cobrança.
- Pix Automático exige CNPJ ativo há mais de 6 meses (ADR 0010).

**Recomendação:** manter o princípio do ADR 0010 (dados e portfólio nunca ficam reféns) e decidir o resto depois do
piloto, com dados reais de uso. Até lá, o ADR 0027 permanece "aprovação pendente".
**Destrava:** #76 (restringir o Tesouro de Marina por assinatura), #5 (página de pagamento).

## D4. App de celular e contas nas lojas (#95)

**Hoje:** o PR #96 entrega a regra pura de lembretes, a preferência validada no backup e um adaptador que não faz nada
no navegador. O projeto Capacitor (Android e iPhone) e o teste em aparelho real **não existem**.

**Em aberto**
- Abrir contas de desenvolvedor nas lojas (custos anuais a pesquisar; a da Apple exige aparelho Apple para o build).
- Se a assinatura é cobrada dentro do app (comissão das lojas; ver D3).
- Quem testa em aparelho real e em quais modelos.

**Recomendação:** só começar depois de D1 (endereço fixo) e D3 (se a cobrança entra no app). Enquanto isso, o lembrete
fica disponível como recurso do aplicativo instalado e não afeta quem usa só o navegador.

## D5. Termos, LGPD e validação jurídica (#25, #29)

**Em aberto**
- Termos de uso e política de privacidade para dados de crianças (LGPD, ECA Digital, Lei 15.211/2025).
- Validação jurídica do modelo de portfólio (#29), que o roteiro põe **antes** do código do portfólio (#20).
- Quem redige e quem valida (advogada ou advogado de proteção de dados).
- Nome da empresa responsável (CNPJ) e endereço de contato, que dependem de D1 e D3.

**Recomendação:** contratar uma revisão única do texto antes de abrir ao público. Hoje, como nada sai do aparelho, o risco
é baixo; ele sobe no dia em que D2 existir.
**Destrava:** abrir ao público (Fase 6), #20 e a escolha do provedor em D2.

## D6. Links de terceiros e afiliados na estante (#74)

**Em aberto:** se a estante pode ter links de compra (afiliados) e se eles alteram a recomendação de livros. O ECA Digital
e o ADR 0010 vetam anúncios e perfilamento; links de afiliado não são anúncios, mas podem enviar dado de quem clica
(a página de destino vê o visitante) e exigem aviso claro.
**Recomendação:** sem afiliados no piloto. Se entrar, só link simples, rotulado, sem rastreio no app e com ADR de segurança.

## D7. Quem revisa o conteúdo (#77, #78, #21)

**Hoje:** `revisao` (rascunho, revisado, aprovado, quem e quando) existe em marcos, atividades e livros. **Só o `aprovado`
aparece no app**; item sem o campo é o conteúdo anterior e continua aparecendo (`app/content/README.md`).

**Em aberto**
- Conferência do **Caderno de inglês** (PR #97) por pediatra ou fonoaudióloga que acompanhe crianças bilíngues: fase do
  "não", atenção curta, quando procurar ajuda. O PDF não vai para a Release até lá (ADR 0021 e ADR 0026).
- Conferência das orientações do domínio emocional (ADR 0024) e do conteúdo de 2 anos (ADR 0023).
- Prazo para o conteúdo antigo sem `revisao` também passar por revisão, em vez de aparecer para sempre sem ela.
- Portal do preceptor (#78): só depois de haver preceptores.

**Recomendação:** definir uma pessoa revisora para a saúde da primeira infância e anotar o nome no campo `revisao.por`.

## D8. Comunidade de trocas entre famílias (#79)

Exige conta (D2) e moderação, e levanta o risco de contato entre adultos que não se conhecem, com dados de crianças
por perto. **Recomendação:** não começar antes de D2 e D5; tratar como produto à parte, com revisão de segurança própria.

---

## Como fechar um item deste arquivo
1. Escreva o ADR (copie `docs/adr/0000-modelo.md`) com a decisão e as consequências.
2. Troque o item aqui por uma linha "Decidido: ADR NNNN".
3. Comente na estória ligada e, se tinha o rótulo `decisao`, registre a decisão nela antes de fechar (`CLAUDE.md`).
