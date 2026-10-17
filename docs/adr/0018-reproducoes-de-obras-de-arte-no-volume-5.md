# 0018. Reproduções de obras de arte no Volume 5 (Commons e acervos abertos)

- **Status:** Aceito
- **Data:** 2026-10-16

## Contexto
O Volume 5 da coleção *O Grande Tesouro de Marina* (ADR 0011) é sobre artes e precisa mostrar obras reais de Dürer, Kandinsky, Monet,
Van Gogh e Mary Cassatt. O Internet Archive, fonte dos volumes anteriores, tem livros ilustrados, mas não boas reproduções
dessas pinturas. Dos grandes acervos de acesso aberto, só o Instituto de Arte de Chicago e a National Gallery of Art puderam ser liberados no ambiente de produção (Met e Rijksmuseum, não). O Wikimedia Commons limita o ritmo de pedidos e chegou a recusar todos os downloads por mais de uma hora.

## Opções consideradas
1. **Só ilustrações próprias (aquarela procedural):** sem risco de direitos, mas o volume deixaria de mostrar as obras que é a razão de existir.
2. **Obras do Wikimedia Commons, só de autores mortos há mais de 70 anos, com licença conferida e SHA-256 registrado:** mesmo padrão do ADR 0011.
3. **Obras de acervos de museus diretamente:** melhor qualidade em alguns casos, mas, como regra geral, hosts bloqueados e termos de uso diferentes a cada acervo. Só dois acervos preenchiam os requisitos (acesso aberto declarado e host liberado no ambiente); os demais ficam de fora.

## Decisão
Combinação das opções 2 e 3: o Commons segue como fonte principal e, onde ele falhou ou o museu tem a melhor imagem, entram os dois acervos que declaram acesso aberto (6 das 10 obras vêm do AIC e da NGA, por causa do limite de pedidos do Commons). Duas ressalvas: o Instituto de Arte de Chicago e a National Gallery of Art (acesso aberto, CC0 para obras em domínio público) são aceitos porque publicam as obras em domínio público sob a política de acesso aberto do próprio museu (AIC: Open Access; NGA: CC0), sem exigir cadastro nem contornar limite de uso, e valem como o Commons: e um arquivo entregue pela dona do produto também vale, desde que o hash seja registrado e o crédito diga que a origem foi o envio da editora.

- **Quais obras:** só autores mortos há mais de 70 anos (teste automático em `test_fontes_v5.py`) e imagens que o Commons marca como domínio público ou CC0. Obra ainda sob direitos autorais (por exemplo, as colagens de Matisse) é citada no texto, nunca reproduzida.
- **Rede:** o download acontece só ao catalogar uma obra (`python3 fontes_v5.py registrar`), fora do app e fora do build dos PDFs. O build usa o JPEG já tratado, versionado em `dominio_publico/v5/`. Nada da família é enviado.
- **Integridade:** o SHA-256 do arquivo de origem e o do JPEG tratado (o que entra no PDF, em `v5/`) ficam em `dominio_publico/obras.sha256.json`; uma troca de JPEG aparece como linha alterada no manifesto e `verificar` a acusa; arquivo sem hash ou com hash diferente é recusado (falha fechada), como no ADR 0011. O CI roda `python3 fontes_v5.py verificar`.
- **Crédito:** cada obra tem legenda com autor, título, ano, acervo, licença e a origem (arquivo no Commons, número de inventário e página no acervo do museu, ou "arquivo fornecido pela editora"), e o volume avisa que a cor de uma reprodução nunca é a do original.
- **Direitos da fotografia:** o Commons pode marcar a fotografia de uma obra com regra própria; só entram arquivos marcados como domínio público ou CC0.

## Consequências
- Commons e museus limitam o ritmo de pedidos (erro 429, com `Retry-After`); o download respeita o tempo pedido, e as imagens tratadas ficam no Git (cerca de 1 MB cada).
- Arquivo entregue à mão (`envio:`) só vale com acervo e endereço de origem: `verificar` falha sem isso. Os *Girassóis* chegaram assim, sem origem; a imagem enviada era da mesma pintura (Neue Pinakothek), mas a fonte não pôde ser comprovada, então o volume usa a reprodução do Projeto Yorck no Commons, marcada como domínio público.
- O site do Instituto de Arte de Chicago só atende pedidos com um `User-Agent` de aparência de navegador (e o cabeçalho `AIC-User-Agent`); `fontes_v5.py` usa esse formato apenas no download manual de obras de acesso aberto, identificando o projeto, sem contornar nenhum login ou limite de uso.
- Se um acervo reprocessar a imagem (as URLs IIIF do AIC e da NGA pedem um tamanho, e o arquivo servido pode mudar), `baixar` recusa o arquivo novo porque o SHA-256 da origem não bate (falha fechada). Para aceitar a mudança, confira a imagem, apague a linha da origem em `dominio_publico/obras.sha256.json`, rode `python3 fontes_v5.py registrar <obra>` e revise o diff do manifesto e do JPEG em `v5/`.
- A licença é a que o Commons registrava na data da catalogação; uma mudança posterior no Commons não altera o que já foi catalogado.
- Mantemos a revisão humana: a dona do produto confere cada reprodução antes de a coleção ser impressa ou vendida.
