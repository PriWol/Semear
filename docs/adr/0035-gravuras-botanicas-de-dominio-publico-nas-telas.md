# 0035. Gravuras botânicas de domínio público nas telas

- **Status:** Aceito (escolha da dona do produto, estória #130 e #24)
- **Data:** 2026-11-21

## Contexto
`docs/DESIGN.md` (ADR 0014) pede gravura botânica como ornamento, com fonte, licença e SHA-256 registrados, "uma ilustração por tela, como respiro". O ADR 0019 e o ADR 0021 já fixaram o padrão para imagens de domínio público na coleção impressa: origem verificável, SHA-256 do original e do arquivo tratado, falha fechada. Faltava levar o mesmo cuidado ao app. O Designer propôs três candidatas por tela (todas do Internet Archive, por ser o único host de imagens liberado na rede de trabalho) e a dona do produto escolheu a combinação recomendada.

## Decisão
**Escolhas** (a página é o `n<N>` do Internet Archive; o SHA-256 é do JPEG original baixado):

| Tela | Obra | Item, página | SHA-256 do original |
|---|---|---|---|
| Boas-vindas (`#/`, sem família) | Besler, *Flos Solis prolifer* (girassol), *Hortus Eystettensis*, 1640 | `mobot31753003651095`, n222 | `f02a39e3267a85dd057e53e8168064ba4700ad5bfc90c7f0abf6e4f27f726952` |
| Início sem criança (família cadastrada, nenhuma criança) | Redouté, *Gladiolus gracilis*, *Les Liliacées*, 1802–1816 | `mobot31753002806732`, n36 | `934fe988dc0f65c8a60e88a55173642e74a25c1727d3db22d6427adf26d63e04` |
| Topo da Biblioteca | Besler, *Tulipa* (cinco tulipas com bulbo), 1640 | `mobot31753003651095`, n78 | `9e42bd675444ec7beef20a9153f0df423d8c8d5919085b68a2336418c9f61580` |

- **Origem:** `https://archive.org/download/<item>/page/n<N>.jpg` (mesmo método do `fontes_v1.py`), exemplares digitalizados pela Missouri Botanical Garden (Biodiversity Heritage Library). Besler morreu em 1629 e Redouté em 1840: obras de domínio público.
- **Arquivos locais:** `app/public/gravuras/{girassol,gladiolo,tulipas}.webp` e as variantes `*-escuro.webp`. O app nunca chama o archive.org (CSP e privacidade inalteradas: `img-src 'self'`). Os endereços de origem existem só como registro em `src/gravuras.ts`, e um teste garante que nenhum outro arquivo de `src/` os cita.
- **Tratamento** (`app/scripts/gravuras.py`, Pillow e NumPy, roda só na máquina de quem mantém, nunca no build): baixa a página, **confere o SHA-256 do original e para se divergir**, recorta só a planta, apaga legendas e numerais de prancha (máscaras retangulares, listadas no script), divide pelo papel estimado (some o tom do papel, as manchas e a sombra da página) e converte a tinta em **canal alfa** (fundo transparente). A tinta é uma cor chapada: `--s-principal` do tema claro (`#355e45`) e `--s-principal` do tema escuro (`#8fbf9f`, ADR 0033), mesma origem. Resultado: WebP com alfa, de 9 a 58 KB cada (total de ~240 KB das seis, todas no cache offline do PWA). Como a tinta vem do canal alfa, a gravura fica boa sobre `--s-papel` e sobre `--s-fundo`, nos dois temas.
- **Variante escura:** `<picture>` com `<source media="(prefers-color-scheme: dark)">`, o mesmo gatilho do tema escuro (ADR 0033). Se um dia o tema virar escolha manual, a troca do gatilho precisa chegar também a este `<source>` (o `media` não enxerga um atributo do `<html>`).
- **Registro e falha fechada:** `src/gravuras.ts` guarda, por imagem, título, autor, ano, livro, item, página, URL de origem e da página, licença, SHA-256 do original e dos dois WebP, tamanho e crédito. `tests/gravuras.test.ts` calcula o SHA-256 dos arquivos de `public/gravuras/` e falha se algum divergir, se faltar crédito, se a origem não for archive.org, se o arquivo passar de 60 KB ou se sobrar arquivo sem registro. `ui/gravura.ts` só desenha imagem registrada: id desconhecido não mostra nada.
- **Acessibilidade:** `alt=""`. A gravura é ornamento (DESIGN.md: "nunca no lugar de um texto necessário"); o sentido da tela está no título ao lado, e ler "gravura botânica: girassol" a cada visita só atrapalha quem usa leitor de tela. O crédito aparece em Ajustes, em "Sobre o Semear" (`<details>` "Créditos das gravuras").
- **Layout:** altura por tokens (`--s-gravura-g/-m/-p`), `max-width: 100%`, `width`/`height` no `<img>` para não saltar. Nenhuma está abaixo da dobra hoje, então carregam logo; `figuraGravura(id, { abaixoDaDobra: true })` liga `loading="lazy"` para uso futuro.

**A nota "Permission to digitize granted by rights holder".** Os metadados dos dois itens do Internet Archive trazem esse texto no campo de direitos. É um aviso da digitalizadora sobre o acesso ao **livro físico** (a biblioteca autorizou o escaneamento do exemplar), não um direito autoral sobre a imagem: a prancha em si é uma gravura de 1640 e de 1802–1816, e uma reprodução fiel de obra bidimensional em domínio público não cria direito novo. Registramos a nota aqui para que ninguém a redescubra e se assuste. Risco zero, se algum dia for exigido: pedir o mesmo arquivo ao Wikimedia Commons (a série Besler de 1613 do Seminário de Eichstätt está marcada "Public domain" lá), o que depende de a rede de trabalho liberar o download.

**Cópias evitadas.** Há no Internet Archive exemplares italianos desses livros marcados CC BY-NC-ND (`IT-FI0098...`). Não os usamos: a licença proíbe uso comercial e obra derivada (o recorte e a tinta em cor própria seriam), e o Semear tem plano pago (ADR 0027).

## Consequências
- Para **acrescentar uma gravura**: ver a página de origem à mão e anotar item, página e SHA-256 do JPEG; incluir no `GRAVURAS` do script (caixa de recorte, máscaras, pontos de preto e branco) e rodar; olhar o resultado; copiar os SHA-256 dos WebP para `src/gravuras.ts`; ficar abaixo de 60 KB; usar `figuraGravura('id')` na tela; conferir 320 e 390 px nos dois temas.
- O SHA-256 do **WebP** pode mudar entre versões do Pillow/libwebp. O do original nunca muda. Se o script gerar outro hash do WebP, olha-se a imagem e atualiza-se o registro; o teste existe para pegar alteração acidental do arquivo, não para exigir bits idênticos em outra máquina.
- Até o modo escuro (ADR 0033) entrar na mesma base, a variante escura (tinta clara) aparece sobre um fundo ainda claro num aparelho em modo escuro. Os dois PRs devem ser mesclados em sequência.
- Nas folhas impressas as gravuras não entram (o pacote tem CSP e CSS próprios e a folha da criança é preto e branco); uma versão em limiar preto e branco para a folha fica para outra estória.
- O app pesa ~240 KB a mais no cache offline.
