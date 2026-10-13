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

## Gerar de novo
```
pip install numpy scipy pillow matplotlib
cd editorial && python3 build_amostra.py
```
Requer Node com Playwright (Chromium) e `pdftoppm` (poppler).
