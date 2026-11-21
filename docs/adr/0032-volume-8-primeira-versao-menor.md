# 0032. Volume 8 "Jogos e descobertas": primeira versão menor, em dois PRs

- **Status:** Aceito (decisão da dona do produto, estória #112)
- **Data:** 2026-11-20

## Contexto
O roteiro (`tesouro-marina/docs/01-arquitetura-curricular.md`) prevê o Volume 8 com 84 páginas e 6 blocos: conjuntos recortáveis completos, bonecos de vara, cenários dobráveis,
projetos integradores e o diário de observação. Os cadernos de 2 anos já apontam para esse volume (unidade 8, *Brincar junto*) e o app só mostra o aviso "ainda não disponível" enquanto ele não existe.

## Opções consideradas
1. Volume completo de 84 páginas: fiel ao roteiro, mas grande demais para uma estória só e com muito conteúdo pedagógico novo para aprovar de uma vez.
2. Primeira versão menor, só com o que os cadernos de 2 anos citam e o diário: entrega depressa o que as famílias já esperam, e o restante evolui em estória à parte.

## Decisão
Opção 2, em dois PRs. O **PR A** (rótulo `conteudo`, mesclado pela dona do produto) traz o volume em `tesouro-marina/`: 32 páginas A4 (múltiplo de 4), título e subtítulo "Jogos e descobertas",
quatro blocos de jogos com níveis de 2, 3 e 4 anos, dois jogos de cartões, memória, dominó, loto, fichas da vez, rimas de roda (só tradicionais ou da coleção, ADR 0021) e duas páginas de diário.
O **PR B** (código) põe o volume no catálogo do app (`app/content/tesouro.json`), ajusta a Biblioteca e o e2e e tira o aviso, usando o número de páginas conferido com `pdfinfo`.
Ilustração: cinco motivos novos em aquarela da coleção (`editorial/motivos9.py`), como nos volumes 6 e 7 (ADR 0019); nenhuma gravura de domínio público nem fonte externa nova.
O PDF **não vai à Release** no PR A: o workflow `publicar-tesouro.yml` passa a copiar só `volume[1-7]`, e o Volume 8 fica como artefato do workflow para revisão. A publicação acontece depois da aprovação da dona do produto, invertendo essa linha.

## Consequências
- Fora desta versão: conjuntos recortáveis completos e sequências, bonecos de vara, cenários dobráveis e projetos integradores; seguem como evolução do volume, em estória própria.
- O sumário e os testes (`test_volume8.py`) recusam prometer o que não está no arquivo.
- Precisa de revisão do Curador e aprovação da dona do produto (jogos para 2 anos, rimas, diário sem avaliação).
- Depois da aprovação: inverter o glob do workflow e abrir o PR B.

## Atualização (2026-11-21): PR B entregue
A dona do produto aprovou o conteúdo e a publicação. O PR B inverte o glob do workflow (`volume[1-8]`, sem o artefato de rascunho), põe o Volume 8 no catálogo (32 páginas e 5 unidades conferidas no sumário do PDF com `pdfinfo`) e tira o aviso "ainda não disponível" da Biblioteca. Ordem de merge: o workflow Publicar tesouro roda no main antes do deploy do site; se o deploy correr junto e falhar por falta do PDF e do manifesto, basta reexecutá-lo.
