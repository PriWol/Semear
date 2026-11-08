# 0023. Faixa etária de 2 a 8 anos

- **Status:** Aceito (conteúdo para 2 anos pendente de revisão da dona do produto)
- **Data:** 2026-11-08

## Contexto

Em 16/10/2026 o público passou a incluir crianças de 2 anos (creche e maternal), com foco em afterschooling (estória #71). A especificação dizia 3 a 8 anos. O código não tinha um piso de idade: o cadastro só pedia uma data no passado.

## Decisão

- A faixa do produto é **2 a 8 anos** (`src/domain/faixa.ts`). O cadastro e o backup **não bloqueiam** por idade: a tela só avisa quando a criança está fora da faixa, para um irmão mais novo ou mais velho poder usar o app. O backup passa a recusar apenas datas que não existem (antes, `2026-02-30` passava).
- **Sessão padrão de 30 minutos** de atividade (`DURACAO_PADRAO`). A **preparação do adulto** é um campo à parte da atividade (`preparoMin`) e o pacote a mostra separada da duração.
- Atividade que começa **antes dos 3 anos** é validada com regras próprias: precisa de `cuidados` (aviso de materiais pequenos, engasgo, água), impresso junto dos materiais, e deve durar **até 10 minutos**, para a sessão ser feita de várias atividades curtas.
- Marcos e atividades para 2 anos entram como `rascunho` (#77) e só aparecem para as famílias depois de revisados e aprovados.

## Consequências

- Documentos atualizados: `CLAUDE.md`, `README.md` e `docs/JORNADA_SPEC.md` (decisão 2).
- Não há ainda conteúdo para 2 anos: a estrutura está pronta; os marcos vêm com o domínio emocional (#72) e o caderno do ADR 0021.
- A pontuação de atividades já usa a faixa de idade de cada atividade, então não mudou.
