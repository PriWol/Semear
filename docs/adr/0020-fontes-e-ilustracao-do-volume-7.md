# 0020. Fontes de letra, melodia e ilustração do Volume 7 (Primeiras línguas)

- **Status:** Aceito
- **Data:** 2026-10-18

## Contexto
O Volume 7 da coleção *O Grande Tesouro de Marina* (*Primeiras línguas*) traz inglês e francês em oito unidades paralelas, com o latim só como cultura (`tesouro-marina/docs/01-arquitetura-curricular.md`, §4). Cada unidade tem uma rima ou canção, cartões, um jogo e uma rotina. Isso levanta três questões que os volumes anteriores resolveram só em parte: de onde vêm letras que se possa publicar, de onde vem uma melodia que se possa garantir, e como ilustrar as línguas com a mesma riqueza dos volumes 1 a 6 (a dona do produto pediu o volume "bem ilustrado, na medida dos outros").

Regras que já valiam e continuam: ilustrações só de domínio público com fonte registrada, ou motivos próprios em aquarela; letras só se forem de domínio público; melodia só se for conferida; latim como cultura; nunca misturar idiomas num cartão sem rótulo.

## Opções consideradas
1. **Letras e melodias de memória, com ilustração só em aquarela própria:** rápido, mas a melodia não seria conferida, e as cenas e os personagens não cabem no motor de aquarela (`docs/03-ilustracao.md`).
2. **Só reaproveitar o que o catálogo já tem** (Crane, Greenaway, Potter): sem download novo, mas não há nada em francês, e o volume ficaria com um idioma só ilustrado.
3. **Fontes antigas conferidas por idioma, e aquarela própria para o que é objeto ou gesto.**

## Decisão
Opção 3.

- **Inglês:** rima das *Miss Pelicoes*, de Kate Greenaway (1846–1901), em *Under the Window* (1878), que já era fonte do catálogo (prancha n59 do item `underwindowpictv00greerich`). Os versos que ensinam "if you please", "many thanks", "good morning" e "good night" vêm da própria prancha. Como o livro não traz melodia, a página diz que é uma rima **para dizer**, e a coleção não inventa melodia.
- **Francês:** *La Polichinelle* (*Pan ! qu'est-c' qu'est là ?*), canção tradicional, em *Vieilles chansons pour les petits enfants* (Plon, 1883), com os acompanhamentos de Charles-Marie Widor (1844–1937) e as ilustrações de Louis-Maurice Boutet de Monvel (1850–1913), ambos mortos há mais de 70 anos. A fonte é o exemplar digitalizado pela Biblioteca da Universidade McGill no Internet Archive. **A melodia é a que está impressa na partitura reproduzida na página**, e isso é a conferência: o livro mostra a imagem da partitura em vez de reescrevê-la. A linha de piano de Widor fica na imagem, e o texto diz para o adulto ignorá-la.
- **Catálogo e proveniência:** as três páginas novas entram em `fontes_v1.py` (mesmo fluxo do Volume 1: SHA-256 da página de origem em `paginas.sha256.json`, falha fechada, build dos PDFs sem rede). As páginas do exemplar da McGill são fotografias do livro (fundo escuro, papel com sombra), então não há papel limpo para virar transparência: o conjunto `FIEL` as trata como retângulos recortados e reduzidos, iguais nas versões de impressão e de tela, como as reproduções de obras dos volumes 5 e 6.
- **Aquarela própria (`motivos8.py`):** nove motivos novos, só mãos, objetos e astros: mão acenando, mãos juntas, polegar para cima, dedo de "não", carinha feliz, porta, porta aberta, janela com sol e cama. Pessoas inteiras e cenas continuam só nas gravuras antigas.
- **Latim:** só como curiosidade, em linha rotulada no verso dos cartões (*salvē*, *valē*, *quaesō*, *grātiās*, *ita*, *nōn*, *quid agis?*). Onde não há fórmula clássica fixa (*boa noite*), o cartão diz "sem fórmula fixa" em vez de inventar uma, e o rodapé do verso avisa que ninguém precisa decorar (parâmetro `nota_latim` de `cartoes()`).
- **Idiomas:** cada página e cada cartão traz um idioma por vez, com etiqueta (`rotulo()` em `volume7.py`); a frente dos cartões só tem o português, e o texto em outra língua leva `lang` para leitores de tela.

## Consequências
- O volume cresce por unidades: esta decisão vale para as oito, e cada nova gravura segue o mesmo fluxo de catálogo e hash. A canção francesa de cada unidade seguinte pode vir do mesmo livro de 1883 (*Frère Jacques*, *Fais dodo, Colas* e outras, na unidade da família) e a inglesa do *Under the Window* ou do *Baby's Opera*.
- A conferência da melodia é visual (a partitura é a página impressa). Se um dia a melodia for reescrita com a notação da coleção (`musica.py`), ela precisará de teste contra uma fonte, como as do Volume 4.
- As duas páginas de Boutet de Monvel são fotografias de um livro: a cor depende da luz da foto e do tom do papel antigo, e esse tom fica nas versões de impressão e de tela. Os créditos do volume dizem que nenhuma imagem foi retocada.
- A tradução das letras é da coleção e precisa de revisão por uma pessoa que fale as línguas antes da venda, como a conferência da licença de cada página.
- `volume7.py` importa `cena` e `tira` de `volume6.py`, em vez de copiá-las; se o Volume 6 mudar essas funções, o 7 muda junto.
- As mãos juntas (*por favor*) e o dedo de "não" são estilizados: o motor de aquarela não desenha mão com naturalidade. Se a dona do produto achar que não funcionam como cartão, a alternativa é uma gravura antiga (por exemplo, um gesto de pedir em Greenaway) em vez de mais aquarela.
