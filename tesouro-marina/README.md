# O Grande Tesouro de Marina

Currículo clássico ilustrado para a infância: 8 volumes, 544 páginas planejadas, em A4 imprimível.

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

## Gerar de novo
```
pip install numpy scipy pillow matplotlib
cd editorial && python3 build_amostra.py   # amostra
cd editorial && python3 volume1.py         # Volume 1 (baixa do Internet Archive as páginas que faltarem)
```
Requer Node com Playwright (Chromium) e `pdftoppm` (poppler).
