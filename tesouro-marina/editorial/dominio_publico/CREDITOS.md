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

Observações: os dois quadros de Kandinsky foram baixados do Commons depois que o limite de pedidos liberou (o do *Estudo de cores* é idêntico, byte a byte, ao arquivo que a editora tinha enviado). Os *Girassóis* vêm do Commons, em reprodução do Projeto Yorck (2002), marcada como domínio público (PD-Art); a imagem que a editora tinha enviado é da mesma pintura (Neue Pinakothek, Munique), mas tem outra origem (provavelmente fotografia licenciada em CC BY 4.0), por isso não foi usada. Os arquivos de origem têm SHA-256 em `obras.sha256.json`.

## Volume 6: pranchas de naturalistas (`v6/`)

Gravuras e litografias antigas baixadas do Wikimedia Commons (arquivo e página citados na coluna "Fonte"). Foram reduzidas a no máximo 2000 px no maior lado (JPEG, cores fiéis à origem em sRGB, sem retoque). O SHA-256 do arquivo de origem de cada uma está em `obras.sha256.json`, e o do JPEG tratado também. A licença é a que o Commons registrava ao catalogar (outubro de 2026).

| Arquivo | Prancha e autoria | Acervo | Fonte | Situação |
|---|---|---|---|---|
| `v6/sabia.jpg` | *Turdus rufiventer* e *Coracina scutata*, autoria desconhecida, século XIX (data a confirmar) | Brasiliana Iconográfica | Wikimedia Commons, `File:Turdus rufiventer - Coracina scutata, da Coleção Brasiliana Iconográfica.jpg` | domínio público (marcação do Commons; autoria desconhecida) |
| `v6/bemtevi.jpg` | *Bienteveo Tyrant* (*Pitangus bolivianus*), de *Birds of La Plata*, Henrik Grönvold (1858–1940), em W. H. Hudson (1841–1922), 1920 | Biodiversity Heritage Library | Wikimedia Commons, `File:Birds of La Plata (Plate) (7788867022).jpg` | domínio público |
| `v6/beijaflor.jpg` | *Heliothrix phaïnolæma*, de *A Monograph of the Trochilidae*, vol. 4, John Gould (1804–1881) e Henry C. Richter (1821–1902), 1861 | livro digitalizado, via Wikimedia Commons | Wikimedia Commons, `File:Heliothrix phaïnolæma + Till. bulbosa - Gould -Humm.jpg` | domínio público |
| `v6/merian_frangipani.jpg` | *Metamorphosis insectorum Surinamensium*, prancha 8, Maria Sibylla Merian (1647–1717), 1705 | Biodiversity Heritage Library | Wikimedia Commons, `File:Metamorphosis insectorum surinamensium (Pl. 8) BHL41398729.jpg` | domínio público |

Observações: a prancha do sabiá é de autoria desconhecida (coleção Brasiliana Iconográfica); entra pela marcação "domínio público" do Commons e por ser uma gravura do século XIX, e deve ser reconferida antes da venda. A legenda da prancha do bem-te-vi diz *Pitangus bolivianus*; o livro mantém o nome da prancha. Os arquivos de origem foram conferidos, byte a byte, contra o tamanho e o SHA-1 que o Commons informa.
