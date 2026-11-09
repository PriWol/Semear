# 0027. Aplicativo nativo para celular e lembretes agendados no aparelho

- **Status:** Aceito (a publicação nas lojas e a cobrança dentro do app seguem em aberto)
- **Data:** 2026-11-09
- **Relacionado:** 0002 (dados no aparelho), 0009 (publicação), 0025 (plano semanal), 0026, #95

## Contexto
A dona do produto quer o Semear como aplicativo de celular e que a família receba, todo dia, uma notificação com as atividades do dia (#95). O app já é um PWA instalável, e o plano da semana já fica no aparelho.

## Opções consideradas
1. **PWA com notificação por servidor (Web Push):** exige um servidor e guardar o endereço de cada aparelho; no iPhone só vale com o app na tela inicial.
2. **Aplicativo nativo empacotado (Capacitor) com notificação local agendada no aparelho.**

## Decisão
Opção 2. O mesmo código web é empacotado com o Capacitor para Android e iPhone. Os lembretes são **notificações locais**, calculadas a partir do plano semanal que já está no aparelho: **sem servidor e sem enviar dado da criança**.

- **Regra pura** (`domain/lembretes.ts`): recebe o plano, a configuração e "agora", e devolve a lista de lembretes. Só entram dias com atividade, ainda não feitos e no futuro; um dia marcado como feito cancela o lembrete.
- **Preferência da família** (`Familia.lembrete`): ligado ou desligado, horário e se inclui o nome da criança. **O nome fica de fora por padrão**, porque a notificação aparece na tela bloqueada.
- **Adaptador** (`nativo/lembretes.ts`): fala com a ponte do Capacitor só quando o app roda dentro do aplicativo (`window.Capacitor`); no navegador não faz nada. Cada sincronização cancela os lembretes antigos e agenda de novo.
- A permissão de notificação é pedida **depois de explicar o motivo**, e dá para desligar nas configurações.

## Consequências
- **Dependências novas (quando o empacotamento entrar):** `@capacitor/core`, `@capacitor/cli`, `@capacitor/android`, `@capacitor/ios` e `@capacitor/local-notifications`. Só o empacotamento usa; o app web continua sem elas.
- **Lojas:** conta de desenvolvedor na Apple (cerca de US$ 99 por ano) e no Google (cerca de US$ 25, uma vez); valores a confirmar. Compilar para iPhone exige um Mac com Xcode.
- **Cobrança:** as lojas costumam exigir que assinaturas digitais sejam compradas dentro do app, com comissão; isso afeta o preço (ADR 0026) e o provedor de cobrança.
- **Privacidade:** nada novo sai do aparelho. Se um dia houver notificação enviada por servidor, é outro ADR.
- Nesta etapa entram a regra pura, a preferência na configuração e o adaptador. O projeto Capacitor (Android e iOS) e a publicação nas lojas ficam para a etapa seguinte.
