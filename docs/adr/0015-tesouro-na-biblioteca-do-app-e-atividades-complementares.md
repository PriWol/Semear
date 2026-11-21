# 0015. Tesouro na biblioteca do app e atividades complementares

- **Status:** Aceito (piloto com o Volume 4). Complementa o ADR 0011.
- **Data:** 2026-10-15

## Contexto

O ADR 0011 manteve _O Grande Tesouro de Marina_ fora do app. Agora a dona do produto quer que o material
alimente a jornada Clássica (piloto: Volume 4, música). Os domínios AR, NM e DI não têm marcos
(especificação §3.0); suas atividades devem entrar nas sessões como "complementares", mas o gerador de sessão
(§5.6) e a validação (ADR 0005) só conheciam atividades com marco.

## Opções consideradas

1. **PDFs no Git / no app:** pesa o repositório e o cache offline (cerca de 29 MB por volume).
2. **Link para o arquivo na Release:** a Release entrega o PDF como download, sem abrir no navegador nem na página.
3. **Baixar os PDFs da Release no deploy do site e servi-los na mesma origem:** abre inline, aceita `#page=N`,
   não envia nada para fora e não aumenta o Git.

## Decisão

Opção 3, mais as mudanças de modelo abaixo.

- **Complementar** é uma atividade com `marcos: []`, `dominio` (domínio sem jornada) e `categoria` (uma das
  categorias do domínio). A validação recusa atividade sem marco que não cumpra isso.
- **`materialImpresso`** (`volume`, `unidade`, `paginas`) liga a atividade ao trecho do volume. A ficha e o
  roteiro mostram o trecho; a Biblioteca abre o PDF direto na unidade.
- **Gerador de sessão:** depois de preencher a duração com a jornada, entra **no máximo uma** complementar,
  só se couber na duração, adequada à idade, publicada e pontuada como as demais (vertente, inspiração, novidade).
  Só no modo "equilibrado": com linhas de foco escolhidas à mão, nada é acrescentado. O "Trocar" percorre as outras complementares.
- **Catálogo** `app/content/tesouro.json`: volumes (e, desde o adendo de 2026-11-20, cadernos), arquivo e unidades com páginas. Um teste confere que cada
  `materialImpresso` aponta para uma unidade do catálogo.
- **Biblioteca com os volumes 1 a 8:** todos aparecem na Biblioteca e são baixados no deploy (cerca de 237 MB de PDFs `*-tela`, somando os cadernos; ver o adendo de 2026-11-20; o Volume 5 entrou depois do piloto, com 20 MB). Só o Volume 4 tem atividades ligadas (piloto); os demais ficam disponíveis para consulta.
- **Site:** o workflow `publicar-site.yml` baixa, para `dist/tesouro/`, os PDFs `*-tela` listados no catálogo (volumes e, desde o adendo, cadernos),
  a partir da Release pública `tesouro-marina`, e confere o cabeçalho `%PDF-`. O service worker não os guarda
  no cache offline nem responde por eles (`navigateFallbackDenylist`). É preciso estar online ou ter baixado o arquivo.
- **Rascunho:** as 8 atividades do Volume 4 entram como `rascunho` (origem `ia`). Só aparecem para as famílias
  quando a dona do produto revisar e publicar.

## Direção futura: jornada livre

A dona do produto quer, mais adiante, dar à educadora autonomia para montar a jornada sem que o app decida.
A Biblioteca e as atividades complementares são o primeiro passo: acervo navegável e atividades que não
dependem de marcos. Ficam para uma fase própria, com ADR próprio: navegar por domínio e categoria,
"adicionar à sessão" à mão e jornadas com marcos e ordem definidos pela educadora (hoje vêm do conteúdo curado).

## Consequências

- O site depende da Release existir no momento do deploy; sem ela o deploy falha (melhor que publicar link quebrado).
- Privacidade inalterada: nenhum dado da família sai do aparelho, e o PDF vem do mesmo domínio do app.
- O site só republica quando `app/` muda: se um PDF mudar na Release (paginação, conteúdo), rode o workflow "Publicar site" à mão (`workflow_dispatch`) e atualize o catálogo.
- O catálogo é mantido à mão neste piloto; se os volumes mudarem de paginação, atualize o catálogo e rode `npm run check`.
- Se a criança não tem atividade da jornada disponível, a sessão pode ser só a complementar (a educadora continua podendo trocar ou remover). Atividade com `idioma` nunca é complementar.
- Atividades complementares ainda não têm "tema"; a escolha usa idade, vertente e novidade.

## Adendo (2026-11-20): volumes 6 e 7 e cadernos para 2 anos (estória #109)

- **Catálogo:** `app/content/tesouro.json` passa a ter `volumes` (1 a 7) e `cadernos` (`atividades-2-anos` e
  `ingles-2-anos`). Os cadernos **não são volumes da coleção**: têm `id`, `titulo`, `subtitulo`, `aviso` (o aviso de
  saúde do cartão), `arquivo`, `paginas` e `unidades`; no caderno de atividades cada unidade traz `volume` (1 a 8), o
  volume que acompanha. O Volume 8 está planejado, mas ainda não foi produzido: a Biblioteca mostra "acompanha o
  Volume 8 (ainda não disponível no app)" para volume fora do catálogo.
  `MaterialImpresso` não muda e `enderecoDoMaterial` continua só para volumes. No Volume 7, a seção
  "Latim · De onde vêm as palavras" entra como unidade 9 (decisão provisória; a dona do produto confirma no PR).
- **Peso:** a soma dos PDFs `*-tela` sobe para cerca de 237 MB (volumes 1 a 5, ~129 MB, mais os volumes 6 e 7 e os dois cadernos, ~108 MB).
  Continuam fora do precache do service worker.
- **Deploy:** o passo "Baixar os PDFs do Tesouro" de `publicar-site.yml` lê volumes e cadernos do catálogo, mantém a regra
  de nome (que agora falha o job quando o nome é inválido) e a checagem `%PDF-`, garante o `pdfinfo` (instala `poppler-utils`
  se faltar e falha com mensagem clara se não conseguir) e confere que o total de páginas de cada PDF bate com o catálogo.
- **Biblioteca:** depois dos volumes, a seção "Cadernos para 2 anos" tem um aviso de saúde (orientações ainda não
  conferidas por profissional; não substituem o pediatra) em destaque acima dos cartões e, vindo do catálogo, dentro de cada caderno. Sem tela nova e sem mostrar o tamanho dos arquivos.
- **Decisão da dona do produto (2026-11-20):** expor os cadernos no app antes da conferência pediátrica (ADR 0021 e 0026).
  A conferência continua sendo controle manual dela, **antes de vender ou divulgar** os cadernos.
- **`pdfinfo` no deploy:** se o runner não tiver `pdfinfo`, o passo faz `sudo apt-get install poppler-utils` (pacote do
  repositório oficial do Ubuntu, em runner descartável do GitHub). Preferimos isso a falhar o deploy por falta da
  ferramenta; reavaliar se o runner passar a trazer o poppler.
- **Integridade (estória #111, resolvida; ADR 0031):** o deploy baixa o manifesto `SHA256SUMS` da Release e exige que
  o sha256 de cada PDF baixado bata com a entrada dele, além de nome, `%PDF-` e páginas. Limite: o manifesto não
  protege contra quem escreve na Release (troca PDF e manifesto juntos).

## Adendo (2026-11-21): Volume 8 na Biblioteca (estória #112)

- **Catálogo:** `app/content/tesouro.json` passa a ter os volumes 1 a 8. O Volume 8, "Jogos e descobertas" (32 páginas, 5 unidades: os quatro blocos de jogos e o diário), entra como os volumes 6 e 7 e é publicado na Release e no manifesto `SHA256SUMS` (ADR 0031).
- **Rótulo:** "acompanha o Volume 8" aparece normalmente na unidade 8 do caderno de 2 anos. O texto "(ainda não disponível no app)" continua só para número de volume fora do catálogo.
- **Peso:** o PDF de tela do Volume 8 soma ao total de PDFs baixados no deploy (ver o tamanho real na Release).

## Adendo (2026-11-21): `materialImpresso` pode apontar para um caderno (estória #118)

- **Decisão:** `materialImpresso` é uma união: `{ volume, unidade, paginas }` ou `{ caderno, unidade, paginas }`, em que `caderno` é o `id` de um caderno de `tesouro.json`. Os dois juntos, ou nenhum, são recusados.
- **Validação:** `domain/` é puro e não lê o catálogo; `validarConteudo` recebe a lista de ids de cadernos por parâmetro (sem ela, nenhum caderno é aceito). O rótulo (`rotuloDoMaterial`) e o pacote recebem os títulos do catálogo da mesma forma, e o endereço sai de `enderecoDoMaterial` (`tesouro/<arquivo>#page=P`; id desconhecido dá `null`). Nenhuma dependência nova nem chamada externa.
