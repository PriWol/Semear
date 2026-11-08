# 0024. Domínio de formação e regulação emocional

- **Status:** Aceito, com a revisão pedagógica e a conferência das referências pendentes
- **Data:** 2026-11-08

## Contexto
A estória #72 pede uma linha de formação e regulação emocional de 2 a 8 anos. A especificação só tinha o esboço DI.SOC, dentro de Desenvolvimento Integral, que é um domínio **sem jornada** (só atividades).

## Opções consideradas
1. **Dar jornada ao DI.** Mistura motor, vida prática e espiritualidade com emoções, e muda um domínio inteiro.
2. **Domínio novo `EM` com jornada.** A criança é posicionada em cada linha e o plano de sessão usa o domínio como os demais.

## Decisão
Opção 2: domínio `EM` (💛) com quatro linhas: `EM.NOM` (reconhecer e nomear emoções), `EM.REG` (autorregulação), `EM.CON` (convivência e resolução de conflitos) e `EM.VAL` (valores e cuidado). Cada linha tem 4 marcos, do 2º ao 7º ano de idade. O DI.SOC fica só para as atividades antigas.

- Todos os 16 marcos entram como **`rascunho`** (ADR do status de revisão, #77): ficam fora do app até a dona do produto revisar e aprovar. A tela da jornada mostra “Conteúdo desta linha em breve”.
- Cada marco traz o texto “Para os pais” (por que importa, como participar, sinais de atenção) e diz que **não é diagnóstico**. O texto evita rotular a criança.
- Referências: BNCC e *O cérebro da criança* (Siegel e Bryson, nVersos, 2015), em `referencias.json`. **Conferir** autor, título e ano da edição brasileira antes de aprovar. Os textos gerais não citam outras obras.
- Os textos por vertente (Montessori, Waldorf etc.) ficaram de fora desta primeira versão.

## Consequências
- Há 5 atividades em rascunho (`atv-em-*`): caras no espelho, soprar a vela, brincar lado a lado, roda de história e cuidar da planta. As de 2 anos têm até 10 min e `cuidados` (ADR 0023). Elas não têm folhas para a criança, por escolha (aos 2 anos o caderno do ADR 0021 não usa papel). A escolha da sessão passa a usá-las quando forem aprovadas.
- Quando os marcos forem aprovados, o domínio aparece sozinho para as famílias: não há mais nada a ligar.
- O cache do Vitest não percebe arquivos novos em `content/marcos/`; se um teste não enxergar o arquivo, apague `node_modules/.vitest-cache`.
