# 0021. Caderno de atividades para crianças de 2 anos

- **Status:** Aceito
- **Data:** 2026-11-07

## Contexto
Os volumes de *O Grande Tesouro de Marina* são para crianças de 3 a 8 anos, mas a Marina tem 2. Nessa idade a aprendizagem não passa por papel e lápis: passa por conversar, cantar, tocar, nomear, sair e mexer o corpo.
Foi pedido um caderno que acompanhe os oito volumes com atividades dessa idade, de tipos variados.

## Opções consideradas
1. **Adaptar as páginas dos volumes** (recortar, colar, desenhar): exige habilidades que ela ainda não tem.
2. **Um caderno separado, com uma unidade por volume e atividades de vários tipos.**
3. **Só um guia de texto para o adulto, sem ilustração:** menos útil e sem o visual da coleção.

## Decisão
Opção 2. O *Caderno de atividades da Marina* (`editorial/caderno.py`) tem uma unidade para cada volume, com atividades de seis tipos: cantar e rimar, conversar, mostrar o mundo, fazer com as mãos, mexer o corpo e nomear.
Cada atividade traz o tempo, o material de casa, o que fazer, o que dizer, perguntas simples, variações, um quadro de registro e uma nota para o adulto sobre o porquê. O caderno não usa tela.

- **Fontes consultadas** (inspiração, não regra): Charlotte Mason (hábitos, ar livre e cinco sentidos até os 6 anos), pedagogia Waldorf (imitação, ritmo, jogos de dedos), Montessori em casa (vida prática e nomear objetos reais), a Sociedade Brasileira de Pediatria (sem telas antes dos 2 anos) e a BNCC (campos de experiência da educação infantil). As buscas trouxeram sobretudo páginas de editoras, escolas e blogs, e não os textos originais nem o documento oficial da SBP: as faixas de idade e as recomendações devem ser conferidas antes da publicação.
- **Rimas e cantigas:** só as tradicionais de autoria desconhecida (a letra varia de região, e a página diz isso) e as escritas pela coleção. Melodia só entra se for conferida.
- **Ilustração:** motivos em aquarela da coleção, os mesmos dos volumes.
- **Segurança:** nenhuma atividade usa peça que caiba na boca nem deixa a criança sozinha com água; cada página traz o aviso quando for o caso.

## Consequências
- O caderno não substitui o pediatra: a carta à família manda procurar um profissional em caso de dúvida sobre fala, audição ou desenvolvimento.
- O vídeo de referência do canal indicado pela dona do produto não pôde ser lido (o acesso ao YouTube falhou); o conteúdo dele não foi usado. Se a transcrição for enviada, as atividades devem ser revistas com ela.
- O PDF sai junto com os dos volumes na Release `tesouro-marina` (workflow `publicar-tesouro.yml`).
