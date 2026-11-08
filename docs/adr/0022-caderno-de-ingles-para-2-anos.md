# 0022. Caderno de inglês para crianças de 2 anos

- **Status:** Aceito (em produção: abertura e unidade 1)
- **Data:** 2026-11-08

## Contexto
A língua materna da Marina é o português, e a família quer apresentar o inglês a ela, aos 2 anos, só com quem fala inglês em casa. O pedido foi seguir metodologias conhecidas, com atividades que não sejam só de papel (rimas, conversa, objetos, o corpo),
e levar em conta que ela está na fase do “não” e tem dificuldade de se concentrar por muito tempo (ver ADR 0021).

## Opções consideradas
1. **Cartões e vocabulário em lista:** exige que a criança repita palavras soltas; pouco compatível com a idade.
2. **Um caderno de rotinas, rimas e leitura, com métodos descritos:** o inglês entra em momentos fixos do dia, com objeto, gesto e rima.
3. **Só indicar vídeos e aplicativos:** descartado: a coleção não usa tela com crianças dessa idade.

## Decisão
Opção 2. O *Caderno de inglês da Marina* (`editorial/caderno_ingles.py`) tem 8 unidades de rotina e mundo (acordar, banho, refeições, brincar, ao ar livre, bichos, família e sentimentos, hora de dormir), cada uma com quatro atividades, duas páginas de rimas, duas atividades de acalmar e um livro para ler juntos.
O texto de apoio é em português; as falas são em inglês e marcadas com `lang="en"`. Os blocos de página são os do caderno de atividades (`caderno.py`).

- **Métodos em que se apoia** (ficam explicados na carta ao adulto): entrada compreensível (Krashen e Terrell, *Natural Approach*), Resposta Física Total (Asher), língua por hora e lugar (Grosjean) com um falante de inglês, leitura dialogada (Whitehurst) e rimas e cantigas. As buscas trouxeram sobretudo manuais, trabalhos de curso, resumos e páginas de divulgação, não os textos originais, e quase nada específico sobre crianças de 2 anos: são boas práticas, não garantia de resultado.
- **O que não é usado:** a cifra “30% das horas acordada” e a taxa de sucesso de “uma pessoa, uma língua” aparecem só em blogs; não foram confirmadas e o caderno diz isso. O caderno não promete fluência.
- **Rimas e cantigas:** só as tradicionais inglesas de autoria desconhecida, de domínio público ou escritas pela coleção (*Good Morning to All*, de Patty e Mildred Hill, 1893; *Open, shut them*; *This little piggy*; entre outras). Melodia não é impressa.
- **Livros:** indicados só pelo título e autoria (*Brown Bear, Brown Bear, What Do You See?*; *Goodnight Moon*; *Hands Are Not for Hitting* e outros), com a nota de que estão sob direitos autorais. O caderno não reproduz o texto nem as imagens deles e diz como conversar sobre cada um.
- **Fase do “não” e atenção curta:** o inglês nunca é imposto (“se ela recusar, volte ao português”), as escolhas são entre duas coisas, e há atividades de acalmar em inglês em todas as unidades.
- **Visual:** motivos em aquarela da coleção, os mesmos dos outros cadernos.

## Consequências
- O caderno de inglês depende dos blocos de `caderno.py` (PR do caderno de atividades): deve ser mergeado depois dele.
- Sem áudio: para a pronúncia, o adulto usa um dicionário com áudio ou uma gravação de falante nativo.
- O caderno não substitui o pediatra nem uma fonoaudióloga que acompanhe crianças bilíngues.
