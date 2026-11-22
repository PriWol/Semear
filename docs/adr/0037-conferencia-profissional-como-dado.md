# 0037. Conferência profissional como dado, com selo único na tela

- **Status:** Aceito (decisão D2 da #138, aprovada pela dona do produto); parte de código da #147. A migração do conteúdo é uma leva à parte.
- **Data:** 2026-11-22

## Contexto

Cerca de 230 itens (149 atividades e 81 marcos) trazem, dentro do texto de `cuidados` ou `sinaisDeAtencao`, a nota interna "conferência por profissional pendente" ou "Orientação ainda sem conferência por profissional de saúde; não substitui o pediatra". Ela aparece para a família em cada item, assusta e cansa, e o estado da conferência não existe como dado: não há como o app saber quando ela acontece, e na Caderneta o registro de revisão diz "validado por especialista" enquanto o texto diz "pendente" (QA3-01, QA3-15; #138 D1 e D2).

## Opções consideradas

1. **Manter a frase em cada texto.** Honesto, mas repetido e fora do dado; o texto precisaria ser editado à mão item a item quando a conferência acontecesse.
2. **Mostrar só "não substitui o pediatra".** Diz menos que a verdade; não recomendada pelo time.
3. **Campo no registro de revisão + um selo por tela.** Escolhida.

## Decisão

- `Revisao` ganha o campo opcional `conferenciaProfissional?: { estado: 'pendente' | 'conferida'; por?: string; em?: string }`. Ausente = sem aviso de conferência (retrocompatível: nenhum conteúdo existente muda de formato, nenhuma migração de IndexedDB, pois é conteúdo e não dado da família).
- Validação (`validarRevisao`): estado fora do conjunto é recusado; `conferida` exige `por` e `em` (AAAA-MM-DD); valem também para itens em `rascunho`.
- `precisaAvisoDeConferencia(itens)` (domínio, pura): verdadeira se algum item da tela está `pendente`.
- **Selo único por tela** (`src/ui/selo.ts`, `role="note"`, ícone Phosphor `heart`, tokens `--s-destaque-*`): "Orientação em conferência por profissional de saúde. Não substitui o pediatra." Telas: atividade, jornada (por domínio, acima das linhas) e Biblioteca (atividades com material impresso). Some sozinho quando a conferência acontece (`conferida`). O pacote impresso mostra a mesma frase uma vez no topo do roteiro quando há item pendente.
- **"Não substitui o pediatra" nunca sai.** Sem pendência, os cuidados concretos de cada atividade continuam e a frase fixa permanece em "Para os pais" dos marcos da Caderneta (`DI.CAD`), com ou sem pendência. O aviso fixo no topo da linha Caderneta é a C1-6, fora desta entrega.
- **Teste de estilo** (`tests/estilo-conteudo.test.ts`): a frase interna dentro do texto vira aviso (`console.warn`) enquanto a migração não acontece, e vira erro depois dela; já falha se um item que tem `conferenciaProfissional` repete a frase.

## Plano de migração do conteúdo (leva separada, do Curador)

1. `node app/scripts/migrar-conferencia.mjs` lista os itens e arquivos com a frase (só lê).
2. Para cada item: tirar a frase do texto (preservando o cuidado concreto) e acrescentar `conferenciaProfissional: { estado: 'pendente' }` ao `revisao`. Na Caderneta, só depois de a dona dizer o que a especialista validou (#138 D1).
3. Trocar o aviso do teste de estilo por erro.
4. Quando um profissional conferir, mudar para `conferida` com `por` e `em`; o selo some da tela sem mexer em código.
   O conteúdo de saúde não afirma certeza clínica; o aviso de saúde nunca é removido, só muda como aparece.

## Consequências

- A frase deixa de se repetir em ~230 textos e o estado passa a ser auditável e testável.
- O selo pode passar sensação de produto inacabado (risco apontado pelo Designer); a alternativa honesta é a escolhida, em linha com os ADR 0021 e 0026 (a conferência é um controle da dona antes da venda).
- Até a migração, itens antigos ainda trazem a frase no texto (e nenhum selo): o comportamento atual é preservado.
- A Biblioteca ainda mantém o aviso próprio dos cadernos de 2 anos (`AVISO_SAUDE`, vem do catálogo); sai quando o catálogo ganhar o estado de conferência.
