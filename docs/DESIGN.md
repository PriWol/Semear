# DESIGN: identidade visual do Semear

Referência **obrigatória** para telas do app e folhas impressas. Direção escolhida pela dona do produto:
**A · Caderno de botânica** (estória #14; decisão no [ADR 0014](adr/0014-direcao-visual-caderno-de-botanica.md)).
Protótipo de referência: `prototipos/design/direcoes-visuais.html`. Aplicação nas telas: #41. Nas folhas: #42.
Ilustrações: #24.

## Princípios
1. **Moderno e clássico:** papel marfim, serifa de livro nos títulos, gravura botânica como ornamento.
2. **Calmo:** pouca cor, muito respiro, nenhum elemento que dispute a atenção com a atividade.
3. **Imprimível:** o que vai para a folha da criança é preto e branco e gasta pouca tinta (§5.8).
4. **Acessível:** todo texto passa no contraste AA (≥ 4,5:1), conferido por `app/tests/tokens.test.ts`.

## Tokens
Fonte única: [`app/src/tokens.css`](../app/src/tokens.css), carregada pelo app e embutida no pacote impresso,
com os mesmos nomes. Nunca escreva cor, fonte ou medida solta no CSS: use `var(--s-…)`. Para mudar um valor,
mude o token e o teste de contraste.

| Token | Valor | Uso |
|---|---|---|
| `--s-fundo` | `#f8f5ee` | fundo da página (marfim) |
| `--s-papel` | `#fffdf8` | cartões e folhas |
| `--s-tinta` | `#1e2b23` | texto principal |
| `--s-suave` | `#5d6a61` | texto secundário |
| `--s-linha` | `#e4ddcd` | filetes e bordas (decorativo, não carrega informação sozinho) |
| `--s-principal` / `-claro` | `#355e45` / `#e3ece3` | verde-musgo: botões, links, títulos |
| `--s-destaque` | `#b8862f` | ocre, **só decorativo** (contraste 3,2:1 sobre papel) |
| `--s-destaque-texto` / `-claro` | `#7a5a1e` / `#f6ecd8` | ocre escuro para **texto** e selos |
| `--s-alerta` / `-claro` | `#9c4a33` / `#f7e4dc` | terracota: avisos e erros |
| `--s-fonte-titulo` | Fraunces, Georgia, serif | títulos (h1 a h3) |
| `--s-fonte-texto` | Inter, system-ui, sans-serif | texto corrido e interface |
| `--s-raio` / `--s-raio-p` | 14 px / 10 px | cartões / botões e campos |
| `--s-espaco-1` a `-6` | 0,25 a 2 rem | espaçamento (escala de 4 pt) |
| `--s-sombra` | sombra suave | só em cartões elevados |

Na folha da criança a letra **não** muda: Andika (bastão e script) e Playwrite BR (cursiva), §5.8.

## Contraste conferido (WCAG 2.1 AA)
| Texto | Fundo | Razão |
|---|---|---|
| tinta | fundo / papel | 13,5 / 14,5 |
| suave | fundo / papel | 5,2 / 5,6 |
| principal | fundo / principal-claro | 6,8 / 6,1 |
| papel (botão primário) | principal | 7,3 |
| destaque-texto | destaque-claro / papel | 5,4 / 6,2 |
| alerta | alerta-claro / papel | 5,0 / 6,0 |

O ocre `--s-destaque` e a linha `--s-linha` **nunca** são cor de texto.

## Tipografia
- Títulos em Fraunces (peso 400 a 600); texto em Inter 400, 500 e 600. Corpo mínimo de 16 px no app.
- Entrelinha de 1,5 no texto corrido; 1,25 nos títulos.
- Texto em português com no máximo ~65 caracteres por linha.

## Largura e medida de leitura (#176)
- **Conteúdo:** ocupa a largura da janela até o teto `--s-largura-app` (100rem, 1600 px); acima disso fica centralizado.
  A margem lateral é `--s-margem-pagina` (16 px no celular, até 32 px em janela larga) e vale também para o topo, para o menu
  e o conteúdo começarem na mesma linha. Em telas de até 400 px a margem continua a do celular (12 px no conteúdo, 8 px no topo).
- **Medida de leitura:** texto corrido, descrições e campos de formulário não passam de `--s-medida-leitura` (65ch), por mais larga
  que seja a janela. É a largura do bloco de texto que se limita, não a do cartão.
- **Listas longas** (Atividades, Acervo, sessões, dias da semana) viram grade: colunas de no mínimo `--s-largura-cartao-min`
  que se repartem sozinhas conforme a janela (1 coluna no celular).
- **Filtros** de Atividades: campos em linha, de no mínimo `--s-largura-filtro-min`; a busca ocupa a linha toda.
- **Botão principal** do cartão "hoje" e **tabela** de conteúdo têm limite de largura (`--s-medida-leitura` e `--s-largura-tabela`),
  para não virarem faixas de 1.500 px.
- O pacote de sessão e a impressão têm largura própria (A4) e não seguem estas regras.

## Ilustrações
- **Clássicas:** gravuras botânicas e naturalistas de **domínio público**, com fonte, licença e SHA-256
  registrados (mesmo cuidado do ADR 0011). Nada de ilustração gerada que imite artista vivo.
- **No app:** versão em cor suave sobre `--s-papel`, como ornamento (cabeçalhos, estados vazios, cartões).
  Nunca no lugar de um texto necessário.
- **Nas folhas:** só traço em preto e branco, sem preenchimento chapado, e fora da área de escrita da criança.
- **Em uso (ADR 0035):** girassol (boas-vindas), gladíolo (início sem criança) e tulipas (Biblioteca), em `app/public/gravuras/`, com
  variante de tinta clara para o tema escuro. Registro, SHA-256 e crédito em `app/src/gravuras.ts`; `alt=""` (ornamento).
- Substituem os emojis da interface. Exceção: emoji que a atividade usa como **conteúdo** (contar, circular).

## Ícones e tom de voz
- Ícones de linha fina **Phosphor, peso regular** (1,5 px a 24 px), copiados como SVG (ADR 0034): use `icone('nome')` de `app/src/ui/icones.ts`, nunca um emoji.
- Cor herdada do texto (`currentColor`), em geral `--s-principal` ou `--s-suave`. Tamanho só pelos tokens `--s-icone` (1,25 rem, junto ao texto) e `--s-icone-g` (2 rem, destaque).
- Ícone ao lado de texto é decorativo (`aria-hidden`); ícone **sozinho** leva `aria-label` (`icone('x', { rotulo })`). O alvo de toque é do botão (ao menos `--s-alvo-toque`), não do desenho. Nunca só o ícone como pista.
- Na folha impressa: só preto, sem preenchimento chapado, fora da área de escrita. Emoji que é conteúdo (rostinhos do "circule", atividades) fica.
- Voz acolhedora e direta, sem infantilizar o educador nem exigir termos técnicos. A criança nunca usa o app.

## Faça e não faça
| Faça | Não faça |
|---|---|
| `color: var(--s-tinta)` | `color: #222` |
| Ocre escuro (`--s-destaque-texto`) em selos de texto | Texto em `--s-destaque` |
| Folha da criança em preto e branco | Fundo colorido ou sombra na folha |
| Uma ilustração por tela, como respiro | Ilustração atrás de texto |
| Margem de impressão ≥ 8 mm | Conteúdo encostado na borda |

## Modo escuro
Automático, segue o aparelho (`prefers-color-scheme: dark`), sem botão (ADR 0033). Segundo conjunto dos mesmos tokens em `app/src/tokens-escuro.css`:
fundo grafite-esverdeado `#1b201c`, papel `#242a25`, tinta marfim `#ebe6d9`, verde-musgo clareado `#8fbf9f`, ocre `#d4a547`, terracota `#eb9a82`; sem preto nem branco puros.
Contraste AA conferido em `tests/tokens.test.ts` para os dois temas. A **folha** (prévia do pacote, impressão e arquivo baixado) é sempre clara: papel não escurece.
