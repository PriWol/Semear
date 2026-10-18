# Imagens em domínio público usadas na coleção

| Arquivo | Obra e ilustrador | Edição | Fonte | Situação |
|---|---|---|---|---|
| `brooke_cachinhos_tigelas.png` | *The Story of the Three Bears*, prancha "Goldilocks e as tigelas", L. Leslie Brooke (1862–1940) | *The Golden Goose Book*, Londres e Nova York: Frederick Warne, 1905 | Internet Archive, item `goldengoosebookb00broo`, página n40 | domínio público (ilustrador morto em 1940; obra de 1905) |
| `potter_pedro_porteira.png` | *The Tale of Peter Rabbit*, Pedro passando por baixo da porteira, Beatrix Potter (1866–1943) | *Histoire de Pierre Lapin*, Londres e Nova York: Frederick Warne, 1921 | Internet Archive, item `histoiredepierre00pott`, página n26 | domínio público (autora morta em 1943); só a imagem é usada, o texto é tradução da coleção |
| `v1/opera_*` (11 páginas) e `clave_sol.png` | Gravuras, partituras e clave de sol de *The Baby's Opera: a book of old rhymes, with new dresses*, Walter Crane (1845–1915) | Londres: George Routledge and Sons, 1900 (1.ª ed. 1877) | Internet Archive, item `babysoperabookof00cran`, páginas n7, n13–n15, n22, n23, n38, n45, n57–n59 | domínio público (ilustrador morto em 1915; obra de 1877); a clave é o recorte da página n13, com as linhas da pauta removidas |

Tratamento: recorte das margens (`recorte_pd.py`) e conversão do papel amarelado da digitalização em transparência, para a imagem se assentar no papel da coleção. A prancha de Brooke foi reduzida a 1400 px de largura (300 dpi no tamanho usado, 112 mm). Nenhum retoque nas pinturas.

## Volume 5: reproduções de obras de arte (`v5/`)

As imagens vêm do Wikimedia Commons, de acervos de acesso aberto (Instituto de Arte de Chicago e National Gallery of Art) ou de arquivo fornecido pela editora, conforme a coluna "Fonte". Foram reduzidas a no máximo 2000 px no maior lado (JPEG, cores intactas, sem retoque). O SHA-256 do arquivo de origem de cada uma está em `obras.sha256.json`. A licença é a que a fonte registrava ao catalogar (outubro de 2026).

| Arquivo | Obra e artista | Acervo | Fonte | Situação |
|---|---|---|---|---|
| `v5/durer_lebre.jpg` | *A lebre jovem* (Feldhase), Albrecht Dürer (1471–1528), 1502 | Albertina, Viena | Wikimedia Commons, `File:Albrecht Dürer - Hare, 1502 - Google Art Project.jpg` | domínio público |
| `v5/durer_primulas.jpg` | *Tufo de prímulas* (Tuft of Cowslips), Albrecht Dürer (1471–1528), 1526 | National Gallery of Art, Washington | National Gallery of Art, Washington, inv. 1991.217.1, https://www.nga.gov/artworks/74162 | CC0 (acesso aberto do acervo) |
| `v5/kandinsky_quadrados.jpg` | *Estudo de cores: quadrados com círculos concêntricos*, Wassily Kandinsky (1866–1944), 1913 | Städtische Galerie im Lenbachhaus, Munique | Wikimedia Commons, `File:Vassily Kandinsky, 1913 - Color Study, Squares with Concentric Circles.jpg` | domínio público |
| `v5/kandinsky_circulos.jpg` | *Vários círculos* (Several Circles), Wassily Kandinsky (1866–1944), 1926 | Museu Solomon R. Guggenheim, Nova York | Wikimedia Commons, `File:Vassily Kandinsky, 1926 - Several Circles, Gugg 0910 25.jpg` | domínio público |
| `v5/monet_medas.jpg` | *Medas de trigo (fim do verão)* (Stacks of Wheat, End of Summer), Claude Monet (1840–1926), 1890–91 | Instituto de Arte de Chicago | Instituto de Arte de Chicago, inv. 1985.1103, https://www.artic.edu/artworks/64818 | domínio público (acesso aberto do acervo) |
| `v5/monet_ninfeias.jpg` | *Ninfeias* (Water Lilies), Claude Monet (1840–1926), 1906 | Instituto de Arte de Chicago | Instituto de Arte de Chicago, inv. 1933.1157, https://www.artic.edu/artworks/16568 | domínio público (acesso aberto do acervo) |
| `v5/vangogh_girassois.jpg` | *Girassóis* (Vase with Twelve Sunflowers), Vincent van Gogh (1853–1890), Arles, agosto de 1888 | Neue Pinakothek, Munique | Wikimedia Commons, `File:Vincent Willem van Gogh 128.jpg` | domínio público (PD-Art, reprodução do Projeto Yorck) |
| `v5/cassatt_banho.jpg` | *O banho da criança* (The Child's Bath), Mary Cassatt (1844–1926), 1893 | Instituto de Arte de Chicago | Instituto de Arte de Chicago, inv. 1910.2, https://www.artic.edu/artworks/111442 | domínio público (acesso aberto do acervo) |
| `v5/cassatt_poltrona.jpg` | *Menina na poltrona azul* (Little Girl in a Blue Armchair), Mary Cassatt (1844–1926), 1878 | National Gallery of Art, Washington | National Gallery of Art, Washington, inv. 1983.1.18, https://www.nga.gov/artworks/61368 | CC0 (acesso aberto do acervo) |
| `v5/cassatt_praia.jpg` | *Crianças brincando na praia* (Children Playing on the Beach), Mary Cassatt (1844–1926), 1884 | National Gallery of Art, Washington | National Gallery of Art, Washington, inv. 1970.17.19, https://www.nga.gov/artworks/52163 | CC0 (acesso aberto do acervo) |

Observações: os dois quadros de Kandinsky foram baixados do Commons depois que o limite de pedidos liberou (o do *Estudo de cores* é idêntico, byte a byte, ao arquivo que a editora tinha enviado). Os *Girassóis* vêm do Commons, em reprodução do Projeto Yorck (2002), marcada como domínio público (PD-Art); a imagem que a editora tinha enviado é da mesma pintura (Neue Pinakothek, Munique), mas tem outra origem (provavelmente fotografia licenciada em CC BY 4.0), por isso não foi usada. Os arquivos de origem têm SHA-256 em `obras.sha256.json`. Inventário, título, autoria e data das seis obras de museu foram conferidos em 17/10/2026 nas bases abertas dos acervos: na API do Instituto de Arte de Chicago (`main_reference_number` igual ao inventário e `is_public_domain` verdadeiro para as três) e nos arquivos `objects.csv` e `published_images.csv` da National Gallery of Art (inventário igual e `openaccess` = 1 para as três imagens). A conferência da licença em cada página, antes da venda, continua sendo humana.

## Volume 6: pranchas de naturalistas (`v6/`)

Gravuras e litografias antigas baixadas do Wikimedia Commons (arquivo e página citados na coluna "Fonte"). Foram reduzidas a no máximo 2000 px no maior lado (JPEG, cores fiéis à origem em sRGB, sem retoque). O SHA-256 do arquivo de origem de cada uma está em `obras.sha256.json`, e o do JPEG tratado também. A licença é a que o Commons registrava ao catalogar (outubro de 2026).

| Arquivo | Prancha e autoria | Acervo | Fonte | Situação |
|---|---|---|---|---|
| `v6/sabia.jpg` | *Turdus rufiventer* (figura 1 da prancha 26), de *Ornithologie brésilienne*, Jean-Théodore Descourtilz (1796–1855), 1854–1856 | Brasiliana Iconográfica | Wikimedia Commons, `File:Turdus rufiventer - Coracina scutata, da Coleção Brasiliana Iconográfica.jpg` | domínio público (marcação do Commons; autoria atribuída pelo número e pelos nomes impressos na prancha) |
| `v6/bemtevi.jpg` | *Bienteveo Tyrant* (*Pitangus bolivianus*), de *Birds of La Plata*, Henrik Grönvold (1858–1940), em W. H. Hudson (1841–1922), 1920 | Biodiversity Heritage Library | Wikimedia Commons, `File:Birds of La Plata (Plate) (7788867022).jpg` | domínio público |
| `v6/beijaflor.jpg` | *Heliothrix phaïnolæma*, de *A Monograph of the Trochilidae*, vol. 4, John Gould (1804–1881) e Henry C. Richter (1821–1902), 1861 | livro digitalizado, via Wikimedia Commons | Wikimedia Commons, `File:Heliothrix phaïnolæma + Till. bulbosa - Gould -Humm.jpg` | domínio público |
| `v6/merian_frangipani.jpg` | *Metamorphosis insectorum Surinamensium*, prancha 8, Maria Sibylla Merian (1647–1717), 1705 | Biodiversity Heritage Library | Wikimedia Commons, `File:Metamorphosis insectorum surinamensium (Pl. 8) BHL41398729.jpg` | domínio público |

Observações: a prancha do sabiá é a de número 26 da *Ornithologie brésilienne* (Descourtilz, 1854–1856), em que a figura 1 é o *Turdus rufiventer* ("Sabiá Larangerra") e a figura 2 é a *Coracina scutata* ("Pavão"); a atribuição vem do número e dos nomes impressos na prancha e do texto do livro (Internet Archive, item `OrnithologieBre00Desc`), porque o Commons registra a autoria como desconhecida. O livro usa só um recorte da figura 1, sem retoque (`RECORTES` em `fontes_v6.py`). Deve ser reconferida antes da venda. A legenda da prancha do bem-te-vi diz *Pitangus bolivianus*; o livro mantém o nome da prancha. Os arquivos de origem foram conferidos, byte a byte, contra o tamanho e o SHA-1 que o Commons informa.

## Volume 7: gravuras de rimas e canções (`v1/`)

Mesmo catálogo e mesmas regras do Volume 1 (`fontes_v1.py`, SHA-256 de cada página de origem em `paginas.sha256.json`). Nenhuma imagem foi retocada; as fotografias do exemplar da McGill só foram recortadas dentro da moldura impressa e reduzidas a 2200 px, sem conversão do papel em transparência.

| Arquivo | Obra e ilustrador | Edição | Fonte | Situação |
|---|---|---|---|---|
| `v1/greenaway_pelicoes_*.jpg` | *The twelve Miss Pelicoes*, Kate Greenaway (1846–1901) | *Under the Window*, Londres: George Routledge and Sons, 1878 | Internet Archive, item `underwindowpictv00greerich`, página n59 | domínio público (ilustradora morta em 1901; obra de 1878) |
| `v1/monvel_polichinelle_*.jpg` | *La Polichinelle* (partitura), Louis-Maurice Boutet de Monvel (1850–1913), com acompanhamento de Charles-Marie Widor (1844–1937) | *Vieilles chansons pour les petits enfants*, Paris: E. Plon, Nourrit et Cie, 1883; exemplar digitalizado pela Biblioteca da Universidade McGill | Internet Archive, item `McGillLibrary-rbsc_vieilles-chansons-petits-enfants_M1993W53V51900z-25297`, folha n11 (página impressa 8) | domínio público (ilustrador morto em 1913, compositor em 1937; obra de 1883) |
| `v1/monvel_polichinelle_cena_*.jpg` | *La Polichinelle* (cena com a letra), Boutet de Monvel | idem | mesmo item, folha n12 (página impressa 9) | domínio público |

### Volume 7, unidades 2 a 8 (rimas de Greenaway, canções de Boutet de Monvel e recortes de cartões)

Mesmas regras. As páginas de *Under the Window* e do exemplar da McGill de *Vieilles chansons pour les petits enfants* têm o SHA-256 da página de origem em `paginas.sha256.json`; nenhuma imagem foi retocada, e os recortes de cartões (`cartao_*`, `monvel_abraco`) são só caixas dentro das mesmas páginas.

| Arquivos | Obra e ilustrador | Fonte (Internet Archive) | Situação |
|---|---|---|---|
| `v1/greenaway_carrinho_*`, `greenaway_casa_vermelha_*`, `greenaway_tres_meninos_*`, `greenaway_gansos_prancha_*`, `greenaway_marias_cores_*`, `greenaway_ventinho_*`, `greenaway_procissao_*`; recortes `cartao_irmao_*`, `cartao_irma_*`, `cartao_bebe_*`, `cartao_familia_*` | rimas e gravuras de Kate Greenaway (1846–1901), *Under the Window*, Londres: George Routledge and Sons, 1878 | item `underwindowpictv00greerich`, folhas n32, n64, n46, n33, n31, n26, n48 | domínio público (ilustradora morta em 1901; obra de 1878) |
| `v1/monvel_fais_dodo_*`, `monvel_clair_de_lune_*`, `monvel_boulangere_*`, `monvel_mere_michel_*`, `monvel_bois_*`, `monvel_choux_*`, `monvel_coucou_*`, `monvel_frere_jacques_*`; recorte `monvel_abraco_*` | partituras e gravuras de Louis-Maurice Boutet de Monvel (1850–1913), com acompanhamento de Charles-Marie Widor (1844–1937), *Vieilles chansons pour les petits enfants*, Paris: E. Plon, Nourrit et Cie, 1883, exemplar da Biblioteca da Universidade McGill | item `McGillLibrary-rbsc_vieilles-chansons-petits-enfants_M1993W53V51900z-25297`, folhas n41, n9, n16, n48, n28, n47, n39, n21 (página impressa = n − 3) | domínio público (ilustrador morto em 1913, compositor em 1937; obra de 1883) |

As gravuras de Crane (*This Little Pig*, *Little Red Riding Hood*), de Brooke e de Caldecott, que também aparecem nos cartões e nas rimas deste volume, já estavam registradas nas seções anteriores.
