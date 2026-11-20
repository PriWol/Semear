# 0030. Registro de sessão grava observação e nunca muda o estado do marco

- **Status:** Aceito
- **Data:** 2026-11-20

## Contexto
A estória #11 ("informar progresso") leva a ficha de registro impressa (§5.7) para dentro do app: depois da
sessão, o educador digita o código impresso, marca o que observou em cada marco e anota como foi. A decisão 9
do produto diz que o avanço na jornada é **manual**: só o pai muda o estado, no mapa (§5.2). Se a ficha mudasse o
estado sozinha, uma observação num dia ruim faria a criança "regredir" ou "avançar" sem o pai perceber.
Também é preciso decidir como o app sugere que um marco "parece pronto" sem decidir por ele, e como guardar os
campos novos sem quebrar bancos e backups que já existem.

## Opções consideradas
1. **A ficha muda o estado:** simples, mas tira a decisão do pai e contraria §5.2.
2. **Guardar a observação num lugar novo (nova loja do IndexedDB):** exige subir a versão do banco e migrar;
   duplica o que o histórico já faz.
3. **Observação como evento no histórico que já existe (`historico`), com o id da sessão, mais campos opcionais
   na `Sessao`:** nada de migração; o histórico já é "só acrescenta".

## Decisão
Opção 3, com estas regras:
- **A ficha grava a observação e não muda `estados`.** `registrarSessao(sessao, eventos)` (repositório) grava a
  sessão e acrescenta os eventos numa **única transação**: se qualquer gravação falha, nada é gravado. A
  transação nem abre a loja `estados`. Sessão inexistente e evento de outra sessão ou de outra criança são
  recusados com erro claro.
- **Eventos com `origem: 'sessao'` e `sessaoId`.** Marco sem escolha na ficha não gera evento. Registrar a mesma
  sessão de novo **acrescenta** eventos (o histórico nunca é apagado, §4.2) e **substitui** os campos da `Sessao`
  (data do registro, duração real, engajamento, anotações): quem corrige pode apagar um detalhe.
- **Selo "parece pronto" é derivado, nunca gravado** (`pareceProntoPara`, função pura em `domain/registro.ts`): o
  marco ainda não está *Consolidado* e teve a observação *Consolidado* em **2 sessões diferentes**. De cada sessão
  vale só o último registro do marco; um "Está aqui" (evento `posicionamento`) zera o que veio **antes dele, pela
  ordem do histórico** (a ordem de gravação, não a data, que pode estar errada); evento sem `sessaoId` nunca
  conta. O selo conta sessões com *Consolidado*, não só a mais recente. É só uma dica, sem botão.
  - O "Está aqui" só grava eventos dos marcos que mudam de estado, então ele zera só esses marcos. Um marco
    mais adiante, sem registro, mantém as observações anteriores.
  - Não existe "não observado regride o estado" nem "o selo some após retrocesso": o estado é do pai.
- **A ficha do app e a ficha impressa listam os mesmos marcos**, na mesma ordem (`observacoesDaSessao`, usada
  pelo pacote e pela tela). Em Línguas a chave é `id@idioma`, como a jornada grava. Se um marco é principal numa
  atividade e revisão em outra, vale como principal.
- **Sem subir versões.** Os campos novos são opcionais: registros antigos simplesmente não os têm. A versão do
  IndexedDB continua 2 e `VERSAO_BACKUP` continua 1; um backup antigo importa sem mudança, e um app antigo que
  receba um backup novo apenas ignora os campos que não conhece.
- **`validarBackup` valida tudo o que veio de fora:** `registradaEm` (instante ISO), `duracaoReal` (inteiro de 1
  a 240), `engajamento` (um dos quatro valores), `anotacoes` (texto de até 500 caracteres), `sessaoId` (texto).
  Recusa evento cujo `sessaoId` não existe nas sessões do backup, ou pertence a sessão de outra criança, ou tem
  origem diferente de `sessao`, e as chaves `__proto__`, `constructor` e `prototype`. Tudo é conferido antes de
  qualquer gravação: a importação inválida não apaga os dados atuais.
- **Excluir uma sessão leva junto as observações dela** (`removerSessao`), senão o backup exportado depois teria
  eventos órfãos e seria recusado. No plano semanal, uma sessão já registrada não pode ser "desmarcada".
- **Família de exemplo (ADR 0013):** passa a trazer sessões registradas (para mostrar o selo) e uma por registrar.
  `apagarExemplo` remove os eventos delas, nunca os de sessões reais.
- **Engajamento:** guardamos o texto (`baixo`, `ok`, `bom`, `alto`); emojis e rótulos são só da tela.

## Consequências
- Fica mais fácil: o selo é recalculável e testável sem tela; a ficha não pode estragar a jornada; nada de
  migração para quem já usa o app.
- **Privacidade:** o backup agora leva **anotações de texto livre** sobre a criança, que podem conter dados
  sensíveis que a pessoa escrever. A tela de privacidade e a de configurações avisam isso; as anotações
  continuam só no aparelho e só saem no arquivo que a pessoa baixa. A anotação é sempre exibida como texto
  (o helper `html` escapa; o campo de texto recebe o conteúdo escapado).
- Fica mais difícil: ordenar por data o histórico passa a ser arriscado (a ordem de gravação é o que vale); uma
  futura loja de índice por `sessaoId` só será necessária se o histórico ficar muito grande (hoje o repositório
  percorre o histórico para apagar as observações de uma sessão).
- Se um dia a regra do selo mudar (por exemplo, 3 sessões), muda uma constante e o teste; nenhum dado precisa ser
  convertido.
