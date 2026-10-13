# Padrão editorial — Etapa 2

Sistema visual e técnico aplicado a todas as páginas da coleção. Implementação: `editorial/estilo.css` e `editorial/build_amostra.py`.

## Formato e impressão
- **A4 (210 × 297 mm)**, sem sangria. Impressoras domésticas não imprimem até a borda, então nada importante fica a menos de **9 mm** da borda. O verificador automático (`editorial/pdf.js`) recusa qualquer bloco a menos de 8 mm.
- **Duas saídas por volume.**
  - **Impressão:** fundo branco, para imprimir em papel **creme, marfim ou pólen** (90–120 g nas páginas, **180–240 g** nos cartões). O tom creme vem do papel, sem gastar tinta.
  - **Tela:** fundo creme `#fbf6ea`, para ver no tablet ou no computador.
- **Frente e verso.** Nas folhas recortáveis, o verso tem as colunas espelhadas para coincidir com a frente ao virar a folha pela borda longa. Fica indicado no topo da folha.
- **Imagens:** 300 dpi no tamanho de uso (um motivo de 50 mm tem 600 px), PNG com transparência.

## Grade e componentes
| Elemento | Medida |
|---|---|
| Moldura dupla (páginas de leitura) | a 9 mm da borda; filetes de 0,6 pt e 0,3 pt em `#bfae8f` |
| Mancha de texto | 18 mm de margem lateral; topo em 20 mm; base em 20 mm |
| Cabeçalho | versalete de 7,6 pt: volume e unidade |
| Rodapé | número em estilo antigo entre florões ❧ |
| Aba de domínio | 3,2 × 26 mm na borda externa, na cor do domínio |
| Faixa "Para o adulto" | separada por um filete, 9,2 pt, sempre na base da página, fora da área da criança |
| Folhas recortáveis | sem moldura (ela cruzaria os cortes); linhas tracejadas e marcas de corte externas |
| Cartões de vocabulário | **60 × 78 mm**, 9 por folha |
| Cartas de memória | **52 × 52 mm**, 12 por folha (6 pares) |
| Cartões de sequência (Vol. 2) | 85 × 60 mm, 8 por folha |

## Tipografia (fontes livres, licença OFL, embutidas em `editorial/fonts`)
| Uso | Fonte | Corpo |
|---|---|---|
| Títulos | EB Garamond 500–600 | 26–34 pt |
| Subtítulos | EB Garamond itálico | 14 pt |
| Texto de história (lido em voz alta, a criança acompanha as imagens) | EB Garamond | 17,5 pt, entrelinha 1,45 |
| Palavra do cartão | EB Garamond 500 | 21 pt, minúsculas (como ela vai encontrar nos livros) |
| Guia do adulto | EB Garamond | 9,6 pt |

Uma só família tipográfica (EB Garamond). A Cormorant Garamond foi testada e descartada: o acento circunflexo dela (â, ê, ô) tem um desenho pontiagudo que parece defeito de impressão em português. Algarismos de estilo antigo; latim com mácrons (ā, ū) para indicar as vogais longas.

## Paleta
| Papel | Tinta | Sépia | Musgo | Oliva | Rosa antigo | Azul-acinzentado | Ocre |
|---|---|---|---|---|---|---|---|
| `#fbf6ea` | `#3d3127` | `#6b5440` | `#4f6b3a` | `#7f9a52` | `#c0716b` | `#5f7f9c` | `#b8863a` |

**Cores dos domínios** (abas e sumário): histórias `#c0716b` · memória `#7f9a52` · matemática `#5f8f8a` · música `#8a6f9e` · artes `#c9963f` · natureza `#4f6b3a` · inglês `#5f7f9c` · francês `#7a86b8` · latim `#a0805a` · vida prática `#b07a5a` · jogos `#9a6a7a`.

## Regras de ilustração
1. **Função antes de ornamento.** Cartão: objeto isolado, fundo limpo, silhueta reconhecível. Narrativa: cena rica, com espaço calmo para o texto. Traçado: linhas nítidas, nada de imagem por trás do percurso.
2. **Uma técnica só:** aquarela transparente com contorno fino em sépia, como nas pranchas botânicas e nos livros ingleses do início do século XX.
3. **Consistência:** cada personagem tem ficha de referência (docs/03). O mesmo motivo (por exemplo, a maçã) é **o mesmo arquivo** em todo lugar onde aparece.
4. **Nada de texto dentro das imagens.** Todo texto é tipografia, revisável.
5. **Proibido:** clipart, ícone vetorial como ilustração principal, recorte de painéis prontos, imagem esticada ou abaixo de 300 dpi.

## Verificação antes de entregar
1. Geração do PDF com checagem automática de área segura e de texto cortado.
2. Renderização de todas as páginas em PNG (`amostra/inspecao/`).
3. Inspeção visual página a página: cortes, sobreposições, colisões com marcas de corte, alinhamento frente/verso, legibilidade.
4. Revisão de ortografia em português e de cada palavra em inglês, francês e latim.
