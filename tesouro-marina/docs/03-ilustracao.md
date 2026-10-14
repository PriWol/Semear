# Ilustração: o que foi possível, o que não foi, e como resolver

Este documento explica uma limitação técnica **antes** de qualquer promessa de entrega, como pedido no projeto.

## O que eu consigo produzir neste ambiente

Não tenho aqui um gerador de imagens nem um pintor. Para não trocar a aquarela por clipart sem avisar, escrevi um **motor de aquarela procedural** (`editorial/aquarela.py`). Ele pinta por velaturas transparentes, com borda irregular, acúmulo de pigmento na orla, mistura molhado sobre molhado, granulação do papel prensado a frio e contorno a lápis sépia com falhas. Cada motivo é desenhado à mão, em código, para a sua função.

**Funciona bem para:** frutas, flores, folhas, sementes, cogumelos, cesta, nuvens, gotas, sinais de som (musicogramas), guirlandas e vinhetas. É o que está na amostra: cartões, memória, traçado, musicograma e capa.

**Não alcança a qualidade pedida para:**
- **cenas narrativas** (paisagens, interiores, luz, profundidade);
- **personagens** com expressão e anatomia convincentes (a Marina, o Lobo, a Chapeuzinho, o Patinho, animais em ação);
- o nível de pintura de Beatrix Potter ou das imagens de referência.

O ratinho da amostra é o limite do que dá para fazer: reconhecível e simpático, mas simples. **Não usarei esse motor para cenas nem para personagens principais.** A página-modelo de *Cachinhos Dourados e o Lobo* mostra o espaço da cena marcado como **ilustração pendente**, com a especificação da imagem.

## Três rotas para as cenas pintadas (podem ser combinadas)

### Rota A — Acervos em domínio público (recomendada para arte, botânica e contos clássicos)
Existem aquarelas e gravuras de altíssima qualidade, e livres:
- **Beatrix Potter** (morta em 1943): *O Coelho Pedro* e outros contos, com as aquarelas originais.
- **L. Leslie Brooke** (morto em 1940): *Os Três Porquinhos* e *Cachinhos Dourados* (*The Story of the Three Bears*, 1904).
- **Randolph Caldecott**, **Walter Crane**, **Arthur Rackham** (Grimm, Esopo), **Edmund Dulac** (Andersen; morto em 1953, livre no Brasil desde 2024).
- **Pranchas botânicas e de animais:** Redouté, Audubon, gravuras de história natural.
- **Obras de arte:** Dürer, Vermeer, Monet, Van Gogh, Cassatt, além de retratos de Vivaldi, Bach e Mozart.

**Bloqueio atual:** a rede deste ambiente recusa `commons.wikimedia.org`, `upload.wikimedia.org` e `www.gutenberg.org`, com erro 403 do proxy. Para liberar, edite o ambiente (menu do ambiente na barra de título da sessão → *Edit* → *Network access*) e acrescente esses domínios em *Allowed domains*. Instruções: https://code.claude.com/docs/en/cloud-environments#network-access

Limite desta rota: os personagens variam de um ilustrador para outro, e a Marina e o ratinho não existem nesses livros.

### Rota B — Ilustrações geradas por você a partir das minhas fichas (recomendada para cenas com a Marina, o ratinho e o Lobo)
As imagens de referência que você enviou parecem feitas com um gerador de imagens. Se você tiver acesso a um, eu entrego para cada cena:
1. uma **ficha de estilo** fixa (técnica, paleta, luz, traço);
2. **fichas de personagem** (Marina aos 2–3 anos, o ratinho, o Lobo), para usar como referência em todas as cenas;
3. a **descrição da cena** com proporção e resolução exatas (veja a página-modelo).

Você salva cada arquivo em `ilustracoes/` com o nome indicado. O montador encaixa a imagem, confere a resolução (300 dpi no tamanho de uso), recusa imagens com texto ou deformadas, e eu inspeciono cada página.

### Rota C — Ilustrador(a) humano(a)
É a melhor consistência artística possível, com custo e prazo maiores. As mesmas fichas da Rota B servem como encomenda.

## Situação atual (atualizado)
- **Rede liberada** para `archive.org`, `*.us.archive.org`, `www.gutenberg.org` e Wikimedia. A Wikimedia ainda recusa a maioria das consultas por excesso de pedidos (limite do lado dela).
- **Fontes confirmadas no Internet Archive**, com digitalização nítida:
  - L. Leslie Brooke, *The Golden Goose Book* (Warne, 1905): pranchas coloridas de *Cachinhos Dourados e os três ursos* e de *Os Três Porquinhos*, com cerca de 2000 × 2550 px (até ~17 cm de largura a 300 dpi).
  - Beatrix Potter, *Histoire de Pierre Lapin* (Warne, 1921): aquarelas originais de *O Coelho Pedro*, com 1150 a 1600 px de largura (de 10 a 14 cm, o tamanho original das pranchas).
  - Arthur Rackham, *The Fairy Tales of the Brothers Grimm* (Doubleday, 1916): localizado, ainda não inspecionado.
- **Descartadas:** uma edição americana de 1917 de *Peter Rabbit* (não tem as aquarelas de Potter) e as "Gunston Classics" (procedência das imagens incerta).
- Já em uso na amostra: ver `editorial/dominio_publico/CREDITOS.md`.
- A família aprovou usar a versão tradicional com os **três ursos**; a versão com o Lobo segue como variação oral ("Criar").

## Recomendação
- **Rota A** para obras de arte, botânica, retratos de compositores e contos clássicos (Potter, Brooke, Rackham).
- **Rota B** para as cenas próprias da coleção (a Marina, o ratinho, *A cesta do pomar*, *Cachinhos Dourados e o Lobo*).
- **Motor procedural** para cartões, jogos, traçados, musicogramas e ornamentos, como na amostra.

Até essa decisão, sigo com o que não depende dela: textos, guias, cartões, jogos e diagramação dos Volumes 1 e 2.
