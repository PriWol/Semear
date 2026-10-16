# 0010. Modelo de negócio: plano Livre + assinatura por família

- **Status:** Aceito
- **Data:** 2026-10-14
- **Relacionado:** 0002 (dados no aparelho), 0003 (domínio puro)

## Contexto

A especificação (§9, decisões 29 a 33) previa teste de 30 dias com cartão no cadastro, assinatura
**por criança** e **bloqueio total** depois do teste. A revisão de out/2026 encontrou problemas:

- **Mercado:** o homeschooling no Brasil tem cerca de 75 mil famílias (estimativa da ANED, 2026). A
  escala está no afterschooling, que precisa de uma porta de entrada sem atrito.
- **Regulação:** o PL 1338/2022 segue parado no Senado. O histórico e o portfólio (§8) protegem a
  família, e o bloqueio total tirava isso dela justamente quando ela poderia precisar.
- **Arquitetura:** com dados só no aparelho (ADR 0002), o servidor não tem como conferir o número de
  crianças sem violar o princípio de privacidade. Cobrar por criança fica impossível de verificar.
- **Comunidade:** o Semear antigo era 100% gratuito, e as famílias educadoras divulgam boca a boca.
- **ECA Digital (Lei 15.211/2025):** reforça que a receita não pode vir de anúncios ou de perfilamento.
- **Pagamento:** o Pix Automático exige CNPJ ativo há mais de 6 meses.

## Opções consideradas

1. **Manter o modelo anterior** (teste com cartão, por criança, bloqueio total): receita mais rápida por
   usuário, mas com cadastro difícil, risco de má fama e uma cobrança que não pode ser verificada. A variante "cobrar por criança contando
   só no aparelho" também foi descartada: o número fica fácil de burlar e conferi-lo no servidor
   violaria a privacidade.
2. **Gratuito com anúncios ou patrocínio:** fere a privacidade e o ECA Digital. Descartada.
3. **Plano Livre permanente + assinatura por família** (anual como padrão): a família paga pelo
   conteúdo novo toda semana, e o histórico nunca fica refém.

## Decisão

Opção 3, detalhada na especificação §9:

- **Semear Livre**, grátis para sempre e sem conta: jornada, sondagem, histórico, backup, **portfólio
  completo** e um número limitado de pacotes.
- **Semear Família**, por família e com crianças ilimitadas: pacotes ilimitados e conteúdo
  completo. Preço inicial a testar: R$ 29,90 por mês ou R$ 239 por ano (Pix à vista ou cartão
  em até 12x), com o preço de "família fundadora" para o piloto.
- **Teste sem cartão**, um por e-mail verificado, de 14 a 30 dias (30 no piloto; a duração final é
  questão aberta no §11), que volta para o Livre ao terminar.
- **Nunca** bloquear o acesso aos dados da família. O portfólio completo (evidências + anexo BNCC) sai
  em qualquer plano e para qualquer período: ele protege a família e não pode depender de pagamento.

## Consequências

- Nada muda no app de hoje: o limite do Livre e o plano Família só entram com o código de conta e
  assinatura (§12.3).
- O backend fica menor: o servidor guarda só a conta e a data de validade da licença, nunca dados ou
  contagem de crianças (§9.4). O app confere offline um comprovante assinado.
- O **limite do Livre** e o plano efetivo viram regras de domínio puras e testadas:
  `planoEfetivo(comprovantesVerificados, agora, maiorDataVista, contaIdAtual)` (ADR 0003); a conferência da
  assinatura (WebCrypto) fica em `dados/`. O app usa a
  maior data já vista para que voltar o relógio não estenda a licença, e os planos pagos têm 7
  dias de tolerância depois do fim; o teste não tem (§9.4).
- O portfólio não depende de comprovante de licença. Isso dispensa regras de cobertura de período,
  tira os comprovantes do backup e elimina o incentivo a repetir o teste para gerar portfólio.
- O limite do Livre entra no domínio como parâmetro injetado de `podeGerarPacote(plano, limiteLivre,
pacotesNaSemana)`, sem valor fixo, até o piloto decidir.
- **Privacidade:** os comprovantes levam o `contaId`, então ficam só no store de licença e nunca vão
  no backup; ao entrar na conta, o app baixa os comprovantes de novo.
- **Antes de qualquer código de conta ou assinatura**, um ADR próprio de backend e privacidade
  (dados enviados ao gateway e ao Supabase, retenção, base legal, CSP). O sync fica fora dessa fase.
  Até lá, continua valendo a regra do `CLAUDE.md` de que as Fontes do Google são a única chamada
  externa do app.
- **Pré-venda da família fundadora:** só abre depois das travas do §9.3 (gateway com contrato de
  operador, termos e política de privacidade publicados, página sem dados da criança, link nunca
  embutido no app). O `inicio` do comprovante é a data de ativação, não a do pagamento.
- **Sem telemetria:** as métricas do piloto vêm de entrevistas, de questionário voluntário e do
  gateway de pagamento. Telemetria exige ADR próprio.
- Licença anual primeiro: a cobrança recorrente mensal pode esperar o CNPJ cumprir o prazo do Pix Automático.
- A receita por família é menor no curto prazo. O piloto precisa medir a conversão e o uso para
  calibrar o limite do Livre e o preço (§9.5).
- Esta decisão revisa as decisões 23, 24 e 29 a 33 da especificação e o §8 (item 9).
