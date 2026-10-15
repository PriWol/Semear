# O Grande Tesouro de Marina

> **Onde estão os PDFs:** na Release [`tesouro-marina`](https://github.com/PriWol/Semear/releases/tag/tesouro-marina), atualizada automaticamente a cada merge no `main` que altere esta pasta (workflow `publicar-tesouro.yml`, ADR 0011). Os PDFs e as páginas de inspeção não ficam no Git; as tabelas abaixo citam os nomes dos arquivos.

Currículo clássico ilustrado para a infância: 8 volumes, 563 páginas planejadas (4 volumes produzidos), em A4 imprimível.

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

## Rede e privacidade
O único acesso externo do pipeline é o download de páginas digitalizadas do Internet Archive (`editorial/fontes_v1.py`), feito só no build dos PDFs, fora do app. Nenhum dado de família é enviado. Cada página baixada é conferida pelo SHA-256 registrado em `editorial/dominio_publico/paginas.sha256.json`; página sem hash é recusada (para catalogar uma nova, confira a imagem e rode `python3 fontes_v1.py registrar`). Decisão registrada no ADR 0011.

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
```
Requer também `pdftoppm` (poppler) para as páginas de inspeção. As ilustrações de domínio público já recortadas estão em `editorial/dominio_publico/`; só é preciso baixar páginas do Internet Archive para refazer recortes (`fontes_v1.py`).
