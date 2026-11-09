# 0026. Modelo de assinatura revisado: preço por faixa e plano Livre reduzido

- **Status:** Aceito (substitui a parte de preços e de plano do ADR 0010; falta a dona do produto aprovar o texto)
- **Data:** 2026-11-09
- **Relacionado:** 0010, 0002 (dados no aparelho), #75, #4

## Contexto
O ADR 0010 propunha um plano Livre amplo (jornada, sondagem, histórico e portfólio completos) e uma assinatura **por família** de R$ 29,90 por mês, com 14 a 30 dias de teste. Em 09/11/2026 a dona do produto definiu outro modelo.

## Decisão
- **Assinatura mensal por faixa:** **R$ 49,90** para **uma criança** e **R$ 69,90** para **duas ou mais**.
- **Teste grátis de 7 dias.** Depois dele a família **volta ao plano Livre** (nunca fica bloqueada).
- **Plano Livre:** alguns acessos gratuitos, **sem acompanhamento de percurso** (sem jornada por domínios, marcos e sondagem), com **alguns materiais da biblioteca** e **uma sugestão de atividade por fim de semana**.
- **Como o servidor sabe a faixa:** os dados das crianças ficam no aparelho (ADR 0002), então o servidor **não conta crianças**. A família escolhe a faixa na compra e pode trocá-la; o app não envia nenhum dado das crianças. A cobrança confia na declaração, como a maioria das assinaturas por faixa.
- Continua valendo do ADR 0010: **nunca bloquear o acesso aos dados da família** (backup e exportação funcionam em qualquer plano) e **sem anúncios nem telemetria**.

## O que muda em relação ao ADR 0010
- O preço sobe de R$ 29,90 para R$ 49,90 e passa a ter duas faixas.
- O plano Livre **perde** a jornada, a sondagem e o histórico de marcos. Isso reduz o valor do plano gratuito para empurrar a assinatura e **contradiz** a promessa do ADR 0010 de que o histórico não fica refém. Mitigação: quem volta ao Livre **mantém os dados já registrados e pode exportá-los** (backup e portfólio), mas **não os atualiza** nem vê a jornada.
- O teste cai de 14–30 para 7 dias.

## Pontos em aberto
- Definir a lista exata do que fica no Livre: quais materiais da biblioteca e quais funções.
- O portfólio completo (ADR 0010) continua em qualquer plano?
- Cobrança dentro do aplicativo de celular: as lojas costumam exigir a compra na loja, com comissão (ADR 0027). O preço de R$ 49,90 pode precisar de ajuste por plataforma.
- Provedor de contas e de cobrança (escolha pendente) e o ADR de backend e privacidade, que continua exigido antes de qualquer código de conta ou assinatura.

## Consequências
- Nada muda no app de hoje: o plano Livre reduzido e a assinatura só entram com o código de conta e assinatura.
- O domínio ganhará regras puras e testadas para o plano efetivo (teste, Livre, assinatura de uma criança ou de várias).
