# DESIGN: identidade visual do Semear

Referência **obrigatória** para telas do app e folhas impressas. Direção escolhida pela dona do produto:
**A · Caderno de botânica** (estória #14; decisão no [ADR 0013](adr/0013-direcao-visual-caderno-de-botanica.md)).
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

## Ilustrações
- **Clássicas:** gravuras botânicas e naturalistas de **domínio público**, com fonte, licença e SHA-256
  registrados (mesmo cuidado do ADR 0011). Nada de ilustração gerada que imite artista vivo.
- **No app:** versão em cor suave sobre `--s-papel`, como ornamento (cabeçalhos, estados vazios, cartões).
  Nunca no lugar de um texto necessário.
- **Nas folhas:** só traço em preto e branco, sem preenchimento chapado, e fora da área de escrita da criança.
- Substituem os emojis da interface. Exceção: emoji que a atividade usa como **conteúdo** (contar, circular).

## Ícones e tom de voz
- Ícones de linha fina (1,5 px), cor `--s-principal` ou `--s-suave`.
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
Fora do escopo por ora (opcional, depois). Os tokens já permitem: bastaria um segundo conjunto de valores.
