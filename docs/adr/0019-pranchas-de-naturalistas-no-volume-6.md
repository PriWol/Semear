# 0019. Pranchas de naturalistas no Volume 6 (Commons e motivos já existentes)

- **Status:** Aceito
- **Data:** 2026-10-17

## Contexto
O Volume 6 da coleção *O Grande Tesouro de Marina* (*O livro da natureza*) precisa mostrar aves, insetos e plantas. O ADR 0018
(Volume 5) já definiu como reproduzir obras reais com proveniência verificável. Aqui as imagens são pranchas científicas antigas,
e nem toda unidade tem uma prancha boa e livre: não se achou prancha utilizável de folhas, de germinação nem do corpo humano, e não se quis preencher essa falta com desenhos novos.

## Opções consideradas
1. **Tudo em aquarela própria da coleção:** sem risco de direitos, mas sem as pranchas históricas de Merian, Gould e Hudson, que são parte do interesse do volume.
2. **Só pranchas antigas:** o volume ficaria incompleto onde não há prancha livre adequada.
3. **Pranchas antigas onde houver; no resto, motivos que a coleção já tem e quadros em branco para a criança desenhar.**

## Decisão
Opção 3. Entram quatro pranchas do Wikimedia Commons, todas de autores mortos há mais de 70 anos (ou, no caso do sabiá, de autoria desconhecida e marcada como domínio público pelo Commons): sabiá (Brasiliana Iconográfica), bem-te-vi (Hudson e Grönvold, 1920), beija-flor (Gould e Richter, 1861) e a prancha 8 de Merian (1705). Para folhas, sementes, água, céu e corpo humano a coleção **não desenha motivos novos**: usa os que já existem (folha, gota, nuvem, sol, lua, estrela, lupa, galho e outros), recortes das próprias pranchas e quadros em branco para a criança desenhar. Foi pedido de quem encomenda o livro: pouco desenho procedural, mais espaço para a criança.

- **Proveniência:** as mesmas regras do ADR 0018, no mesmo manifesto (`obras.sha256.json`): SHA-256 da origem e do JPEG tratado, falha fechada, build dos PDFs sem rede. `fontes_v6.py` reaproveita de `fontes_v5.py` o download com espera, a conversão de cor e o manifesto, e aceita só arquivos do Commons.
- **Conferência da origem:** os arquivos de origem foram comparados com o tamanho e o SHA-1 que o Commons informa para o arquivo original. Na conversa, uma imagem colada chega reduzida a 2000 px; por isso os originais maiores foram enviados num `.zip`.
- **Crédito:** cada prancha traz autoria, título, ano, acervo ou digitalização, licença e o arquivo do Commons, e o volume avisa que a cor de uma reprodução nunca é a do original.

## Consequências
- A prancha do sabiá tem autoria desconhecida: o teste dos 70 anos não se aplica a ela, e a licença depende da marcação do Commons. Deve ser reconferida antes da venda.
- A legenda da prancha do bem-te-vi diz *Pitangus bolivianus* (nome de 1920); o livro mantém o nome da prancha e a conferência do nome atual fica pendente.
- `fontes_v6.py` repete parte da estrutura de `fontes_v5.py` (`verificar`, `baixar`, `processar`), porque aquele módulo guarda o catálogo em variáveis do módulo. Unificar os dois num módulo único é uma melhoria futura.
