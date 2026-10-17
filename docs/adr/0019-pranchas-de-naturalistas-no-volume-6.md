# 0019. Pranchas de naturalistas e motivos novos no Volume 6

- **Status:** Aceito
- **Data:** 2026-10-17

## Contexto
O Volume 6 da coleção *O Grande Tesouro de Marina* (*O livro da natureza*) precisa mostrar aves, insetos e plantas. O ADR 0018
(Volume 5) já definiu como reproduzir obras reais com proveniência verificável. Aqui as imagens são pranchas científicas antigas,
e nem toda unidade tem uma prancha boa e livre: não se achou prancha utilizável de folhas, de germinação nem do corpo humano. Uma primeira versão do volume (71 páginas) preencheu essa falta só com motivos que já existiam, e ficou pouco ilustrada perto dos volumes 1 a 5; a dona do produto pediu o volume "bem ilustrado na medida dos outros".

## Opções consideradas
1. **Tudo em aquarela própria da coleção:** sem risco de direitos, mas sem as pranchas históricas de Merian, Gould e Hudson, que são parte do interesse do volume.
2. **Só pranchas antigas:** o volume ficaria incompleto onde não há prancha livre adequada.
3. **Pranchas antigas onde houver; no resto, motivos novos pintados pela coleção** (`motivos7.py`, mesma aquarela procedural dos volumes anteriores).

## Decisão
Opção 3. Entram quatro pranchas do Wikimedia Commons, todas de autores mortos há mais de 70 anos: sabiá-laranjeira (Descourtilz, *Ornithologie brésilienne*, 1854–1856, via Brasiliana Iconográfica; a autoria vem do número e dos nomes impressos na prancha), bem-te-vi (Hudson e Grönvold, 1920), beija-flor (Gould e Richter, 1861) e a prancha 8 de Merian (1705). Para folhas, sementes, água, céu, corpo humano e estações a coleção **pinta cerca de 70 motivos novos** (`motivos7.py`): bichos pequenos, folhas e árvores, as oito fases da lua e o Cruzeiro do Sul, partes do corpo, roupas e símbolos das estações. Plantas, objetos e astros são o que o motor de aquarela faz bem (`docs/03-ilustracao.md`); aves e cenas narrativas continuam só nas pranchas antigas.

- **Proveniência:** as mesmas regras do ADR 0018, no mesmo manifesto (`obras.sha256.json`): SHA-256 da origem e do JPEG tratado, falha fechada, build dos PDFs sem rede. `fontes_v6.py` reaproveita de `fontes_v5.py` o download com espera, a conversão de cor e o manifesto, e aceita só arquivos do Commons.
- **Conferência da origem:** os arquivos de origem foram comparados com o tamanho e o SHA-1 que o Commons informa para o arquivo original. Na conversa, uma imagem colada chega reduzida a 2000 px; por isso os originais maiores foram enviados num `.zip`.
- **Crédito:** cada prancha traz autoria, título, ano, acervo ou digitalização, licença e o arquivo do Commons, e o volume avisa que a cor de uma reprodução nunca é a do original.

## Consequências
- A autoria da prancha do sabiá é atribuída pelo número e pelos nomes impressos nela; o Commons a marca como domínio público. Deve ser reconferida antes da venda.
- O volume passa de 71 para 90 páginas; o mapa da coleção e o total (573 → 592) foram atualizados.
- A legenda da prancha do bem-te-vi diz *Pitangus bolivianus* (nome de 1920); o livro mantém o nome da prancha e a conferência do nome atual fica pendente.
- `fontes_v6.py` repete parte da estrutura de `fontes_v5.py` (`verificar`, `baixar`, `processar`), porque aquele módulo guarda o catálogo em variáveis do módulo. Unificar os dois num módulo único é uma melhoria futura.
