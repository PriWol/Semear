# 0016. Reproduções de obras de arte do Wikimedia Commons no Volume 5

- **Status:** Aceito
- **Data:** 2026-10-16

## Contexto
O Volume 5 da coleção *O Grande Tesouro de Marina* (ADR 0011) é sobre artes e precisa mostrar obras reais de Dürer, Kandinsky, Monet,
Van Gogh e Mary Cassatt. O Internet Archive, fonte dos volumes anteriores, tem livros ilustrados, mas não boas reproduções
dessas pinturas. Os grandes acervos de acesso aberto (Met, Art Institute, Rijksmuseum, National Gallery) não estão acessíveis a partir do ambiente de produção.

## Opções consideradas
1. **Só ilustrações próprias (aquarela procedural):** sem risco de direitos, mas o volume deixaria de mostrar as obras que é a razão de existir.
2. **Obras do Wikimedia Commons, só de autores mortos há mais de 70 anos, com licença conferida e SHA-256 registrado:** mesmo padrão do ADR 0011.
3. **Obras de acervos de museus diretamente:** melhor qualidade em alguns casos, mas hosts bloqueados e termos de uso diferentes a cada acervo.

## Decisão
Opção 2.

- **Quais obras:** só autores mortos há mais de 70 anos (teste automático em `test_fontes_v5.py`) e imagens que o Commons marca como domínio público ou CC0. Obra ainda sob direitos autorais (por exemplo, as colagens de Matisse) é citada no texto, nunca reproduzida.
- **Rede:** o download do Commons acontece só ao catalogar uma obra (`python3 fontes_v5.py registrar`), fora do app e fora do build dos PDFs. O build usa o JPEG já tratado, versionado em `dominio_publico/v5/`. Nada da família é enviado.
- **Integridade:** o SHA-256 do arquivo de origem fica em `dominio_publico/obras.sha256.json`; arquivo sem hash ou com hash diferente é recusado (falha fechada), como no ADR 0011. O CI roda `python3 fontes_v5.py verificar`.
- **Crédito:** cada obra tem legenda com autor, título, ano, acervo, licença e o nome do arquivo no Commons, e o volume avisa que a cor de uma reprodução nunca é a do original.
- **Direitos da fotografia:** o Commons pode marcar a fotografia de uma obra com regra própria; só entram arquivos marcados como domínio público ou CC0.

## Consequências
- O Commons limita o ritmo de pedidos (erro 429) e pode recusar downloads por um tempo; por isso o download tem espera e nova tentativa, e as imagens tratadas ficam no Git (cerca de 1 MB cada).
- A licença é a que o Commons registrava na data da catalogação; uma mudança posterior no Commons não altera o que já foi catalogado.
- Mantemos a revisão humana: a dona do produto confere cada reprodução antes de a coleção ser impressa ou vendida.
