# 0021. Caderno de atividades para crianças de 2 anos

- **Status:** Aceito, com a conferência pediátrica das fontes pendente (ver Pendências)
- **Data:** 2026-11-07

## Contexto
Os volumes de *O Grande Tesouro de Marina* são para crianças de 3 a 8 anos, mas a Marina tem 2. Nessa idade a aprendizagem não passa por papel e lápis: passa por conversar, cantar, tocar, nomear, sair e mexer o corpo.
Foi pedido um caderno que acompanhe os oito volumes com atividades dessa idade, de tipos variados.

## Opções consideradas
1. **Adaptar as páginas dos volumes** (recortar, colar, desenhar): exige habilidades que ela ainda não tem.
2. **Um caderno separado, com uma unidade por volume e atividades de vários tipos.**
3. **Só um guia de texto para o adulto, sem ilustração:** menos útil e sem o visual da coleção.

## Decisão
Opção 2. O *Caderno de atividades da Marina* (`editorial/caderno.py`) tem uma unidade para cada volume, com atividades de sete tipos: cantar e rimar, conversar, mostrar o mundo, fazer com as mãos, mexer o corpo, nomear e **acalmar**.
Cada atividade traz o tempo, o material de casa, o que fazer, o que dizer, perguntas simples, variações, um quadro de registro e uma nota para o adulto sobre o porquê. O caderno não usa tela.

**Segunda versão (pedido da família):** a criança já fala bastante, mas tem dificuldade de concentração por muito tempo e está na fase do “não”, com birras. Por isso:
- cada unidade tem **duas páginas de rimas e parlendas** (quatro ou mais por unidade) e **pelo menos duas atividades de acalmar** (respiração brincada, bolhas, balançar, massagem nas mãos, corrida de lesma, garrafa da calma etc.), com a regra de brincar nos momentos tranquilos para ela já conhecer o caminho na hora difícil;
- a abertura traz duas páginas para o adulto sobre a fase do “não” (o que ajuda no dia a dia, o que fazer durante a birra, atenção curta e quando conversar com o pediatra), uma página sobre o cantinho da calma e uma semana de exemplo;
- as atividades são curtas (2 a 10 minutos), com “versão de 2 minutos” e “para variar”, e cada página traz um quadro para anotar o que ajudou;
- há um registro de calma no fim, para levar ao pediatra, se for o caso.

- **Fontes consultadas** (inspiração, não regra; sobre birra e atenção: programa “Crise dos dois anos”, da SBP, cujo conteúdo foi lido só pela descrição, entrevista do dr. Daniel Becker, material da Sociedade Portuguesa de Pediatria, AACAP e páginas de pediatras e de educação infantil): Charlotte Mason (hábitos, ar livre e cinco sentidos até os 6 anos), pedagogia Waldorf (imitação, ritmo, jogos de dedos), Montessori em casa (vida prática e nomear objetos reais), a Sociedade Brasileira de Pediatria (sem telas antes dos 2 anos) e a BNCC (campos de experiência da educação infantil). As buscas trouxeram sobretudo páginas de editoras, escolas e blogs, e não os textos originais nem o documento oficial da SBP: as faixas de idade e as recomendações devem ser conferidas antes da publicação.
- **Rimas e cantigas:** só as tradicionais de autoria desconhecida (a letra varia de região, e a página diz isso), as de domínio público em inglês e francês (*Twinkle, twinkle*, de Jane Taylor, 1806; *Frère Jacques*; *Row, row, row your boat*, letra de 1852; *Pat-a-cake*) e as escritas pela coleção. Melodia não é impressa. Ficaram de fora cantigas com violência ou medo (*Atirei o pau no gato*, *Boi da cara preta*, *Dorme, nenê, que a Cuca vem pegar*) e as que ainda estão sob direitos autorais (*Parabéns a você*).
- **Ilustração:** motivos em aquarela da coleção, os mesmos dos volumes.
- **Segurança:** nenhuma atividade usa peça solta que caiba na boca nem deixa a criança sozinha com água; o chocalho e a garrafa da calma só são feitos com tampa selada pelo adulto. Cada página traz o aviso quando for o caso. A página não promete efeito terapêutico: as atividades de acalmar são brincadeiras de apoio.

## Consequências
- O caderno não faz diagnóstico nem substitui o pediatra, e as indicações de quando procurar ajuda (birras muito longas, frequentes ou intensas; se ela se machuca ou machuca outros; perda de habilidades) vêm de fontes que divergem nas faixas de tempo, por isso ficam sem números. A carta à família e a página “Na hora da crise” mandam procurar o pediatra em caso de dúvida sobre fala, audição, comportamento ou desenvolvimento.
- O vídeo de referência do canal indicado pela dona do produto não pôde ser lido (o acesso ao YouTube falhou); o conteúdo dele não foi usado. Se a transcrição for enviada, as atividades devem ser revistas com ela.
- O PDF sai junto com os dos volumes na Release `tesouro-marina` (workflow `publicar-tesouro.yml`).

## Pendências
- [ ] **Conferência por um pediatra** das orientações sobre a fase do “não”, atenção curta e quando procurar ajuda, antes de divulgar o caderno para outras famílias. Até lá, o PDF na Release é para uso da família da Marina. Quem decidir sobre a divulgação registra a decisão aqui.
- [ ] Conferir a letra das parlendas tradicionais com a versão que a família usa.
- O caderno não faz parte do app: `docs/JORNADA_SPEC.md` não é alterada.

## Regras verificadas por teste
`test_caderno.py` confere, página a página: o aviso de supervisão em toda atividade que usa água, quatro ou mais rimas e duas atividades de acalmar em cada unidade, o total de 84 páginas (par) e que cada montagem tem o seu sumário.
