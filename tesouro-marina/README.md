# O Grande Tesouro de Marina

> **Onde estão os PDFs:** na Release [`tesouro-marina`](https://github.com/PriWol/Semear/releases/tag/tesouro-marina), atualizada automaticamente a cada merge no `main` que altere esta pasta (workflow `publicar-tesouro.yml`, ADR 0011). Os PDFs e as páginas de inspeção não ficam no Git; as tabelas abaixo citam os nomes dos arquivos.

Currículo clássico ilustrado para a infância: 8 volumes, 592 páginas planejadas (7 volumes produzidos), em A4 imprimível.

## Primeira entrega (para aprovação)
| Arquivo | O que é |
|---|---|
| `docs/01-arquitetura-curricular.md` | Fundamentação, progressão Descobrir → Relacionar → Criar, mapa dos 8 volumes e Volumes 1 e 2 em detalhe |
| `docs/02-padrao-editorial.md` | Formato, grade, tipografia, paleta, cartões, regras de ilustração e verificação |
| `docs/03-ilustracao.md` | O que foi possível ilustrar aqui, o que não foi, e as rotas para as cenas pintadas |
| `amostra/amostra-v1-impressao.pdf` | 12 páginas reais, incluindo duas com aquarelas originais em domínio público (Brooke e Potter): fundo branco, para imprimir em papel creme |
| `amostra/amostra-v1-tela.pdf` | as mesmas páginas com fundo creme, para ver na tela |
| `editorial/dominio_publico/` | ilustrações de domínio público usadas e seus créditos |
| `amostra/inspecao/` | cada página renderizada a partir do PDF, usada na inspeção visual |

## Volume 1 — O mundo ao meu redor (73 páginas)
| Arquivo | O que é |
|---|---|
| `volume1/volume1-impressao.pdf` | fundo branco, para imprimir em papel creme ou marfim |
| `volume1/volume1-tela.pdf` | fundo creme, para ver na tela |
| `volume1/inspecao/` | as 73 páginas renderizadas a partir do PDF, usadas na revisão visual |
| `editorial/volume1.py` | todo o conteúdo do volume (textos, guias, atividades) |
| `editorial/fontes_v1.py` | ilustrações de domínio público: origem, recorte e crédito |

## Volume 2 — Histórias, memória e imaginação (71 páginas)
| Arquivo | O que é |
|---|---|
| `volume2/volume2-impressao.pdf` | fundo branco, para imprimir em papel creme ou marfim |
| `volume2/volume2-tela.pdf` | fundo creme, para ver na tela |
| `volume2/inspecao/` | as 71 páginas renderizadas, usadas na revisão visual |
| `editorial/volume2.py` | todo o conteúdo do volume |

## Volume 3 — Números, formas e raciocínio (68 páginas)
`volume3/volume3-impressao.pdf`, `volume3/volume3-tela.pdf`, `volume3/inspecao/`, conteúdo em `editorial/volume3.py`.

## Volume 4 — O mundo da música (75 páginas)
`volume4/volume4-impressao.pdf`, `volume4/volume4-tela.pdf`, `volume4/inspecao/`, conteúdo em `editorial/volume4.py`. A notação (pauta, ritmo, musicograma) vem de `editorial/musica.py`, com testes em `editorial/test_musica.py`; instrumentos e bichos são motivos de `editorial/motivos5.py`. As cantigas e partituras de Walter Crane (*The Baby's Opera*) estão registradas em `fontes_v1.py`.

## Volume 5 — O mundo das artes (67 páginas)
`volume5/volume5-impressao.pdf`, `volume5/volume5-tela.pdf`, `volume5/inspecao/`, conteúdo em `editorial/volume5.py`. As reproduções de obras (Dürer, Kandinsky, Monet, Van Gogh e Mary Cassatt) vêm de acervos de acesso aberto (Instituto de Arte de Chicago e National Gallery of Art), ou do Wikimedia Commons, e estão registradas em `editorial/fontes_v5.py`, com testes em `editorial/test_fontes_v5.py`; potes, pincel, argila, papéis e demais desenhos são motivos de `editorial/motivos6.py`. Obras sem reprodução de acesso aberto (por exemplo, as colagens de Matisse, ainda protegidas nos Estados Unidos) são citadas no texto, mas não reproduzidas.

## Volume 6 — O livro da natureza (90 páginas)
`volume6/volume6-impressao.pdf`, `volume6/volume6-tela.pdf`, `volume6/inspecao/`, conteúdo em `editorial/volume6.py`. Nove unidades (diário da natureza, aves, insetos, árvores, sementes, água, céu, corpo humano e estações), com quatro pranchas antigas de naturalistas (sabiá-laranjeira, bem-te-vi, beija-flor e Merian) registradas em `editorial/fontes_v6.py` e testadas em `editorial/test_fontes_v6.py`. O resto é aquarela da coleção (`editorial/motivos7.py`, cerca de 70 motivos novos: bichos, folhas, fases da lua, corpo, estações), com a mesma abordagem dos volumes anteriores (ADR 0019).

## Volume 7 — Primeiras línguas (64 páginas)
`volume7/volume7-impressao.pdf`, `volume7/volume7-tela.pdf`, `volume7/inspecao/`, conteúdo em `editorial/volume7.py`. Inglês e francês em oito unidades paralelas (cumprimentos, família, casa, comida, animais, cores, corpo e natureza), com latim só como cultura (uma seção de 6 páginas com lemas, números romanos e palavras-mãe, e a linha de latim no verso dos cartões). Cada unidade tem 6 páginas: guia do adulto, uma rima inglesa de Kate Greenaway (*Under the Window*, 1878) ou de Walter Crane, uma canção francesa de *Vieilles chansons pour les petits enfants* (1883) com a partitura original na página, cartões em frente e verso e um jogo com rotina. Cada página e cada cartão traz um idioma por vez, sempre com etiqueta. As gravuras de domínio público estão registradas em `editorial/fontes_v1.py` (Greenaway, Boutet de Monvel e as de Crane, Brooke, Caldecott e Potter que já eram do catálogo); o resto é aquarela da coleção (`editorial/motivos8.py`, 19 motivos novos), com testes em `test_motivos8.py` e `test_volume7.py`. Decisões no ADR 0020.

## Rede e privacidade
Os únicos acessos externos do pipeline são o download de páginas digitalizadas do Internet Archive (`editorial/fontes_v1.py`) e o de reproduções de obras do Wikimedia Commons e de acervos de museus (`editorial/fontes_v5.py`; `editorial/fontes_v6.py` baixa só do Commons, pelas mesmas regras, ADR 0019), feitos só ao catalogar imagens, fora do app e fora do build dos PDFs (que usa as imagens já tratadas e versionadas). Nenhum dado de família é enviado. Cada página baixada é conferida pelo SHA-256 registrado em `editorial/dominio_publico/paginas.sha256.json` (Internet Archive) ou `obras.sha256.json` (Commons); arquivo sem hash é recusado (para catalogar um novo, confira a imagem e rode `python3 fontes_v1.py registrar` ou `python3 fontes_v5.py registrar`). O download de `fontes_v5.py` respeita o `Retry-After` da fonte (até 1 h por pedido e 2 h no total); com o Commons limitando o ritmo, `baixar`/`registrar` podem demorar horas. O hash dos JPEGs tratados depende da versão do Pillow/libjpeg: ao regenerar em outra máquina, rode `python3 fontes_v5.py jpegs` e revise o diff do manifesto. Decisão registrada nos ADRs 0011 e 0018.

## Gerar de novo
```
cd tesouro-marina/editorial
pip install -r requirements.txt
npm ci && npx playwright install chromium
python3 build_amostra.py   # amostra
python3 volume1.py         # Volume 1
python3 volume2.py         # Volume 2
python3 volume3.py         # Volume 3
python3 volume4.py         # Volume 4
python3 volume5.py         # Volume 5
python3 volume6.py         # Volume 6
python3 volume7.py         # Volume 7
```
Requer também `pdftoppm` (poppler) para as páginas de inspeção. As ilustrações de domínio público já recortadas estão em `editorial/dominio_publico/`; só é preciso baixar páginas do Internet Archive para refazer recortes (`fontes_v1.py`).
