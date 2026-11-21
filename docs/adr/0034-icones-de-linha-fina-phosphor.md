# 0034. Ícones de linha fina: Phosphor (MIT), SVG copiados sem dependência

- **Status:** Aceito (decisão da dona do produto, estória #130)
- **Data:** 2026-11-21

## Contexto
A interface usava emojis como ícones (menu, botões "Imprimir" e "Baixar", avisos, domínios). Emoji muda de
desenho em cada sistema, não herda a cor do texto (o modo escuro não o alcança) e destoa do "Caderno de
botânica" (ADR 0014, `docs/DESIGN.md`), que pede ícones de linha fina de 1,5 px. A dona do produto decidiu
trocá-los por um conjunto de linha fina.

## Opções consideradas
1. **Phosphor Icons, peso "regular"** (`phosphor-icons/core` 2.1.1, MIT, "Copyright (c) 2023 Phosphor Icons"):
   traço de 16/256 (1,5 px a 24 px), pontas arredondadas, formas orgânicas (planta, folha, livros) que combinam
   com a identidade; SVG pronto com `fill="currentColor"`; cobre todos os nomes de que precisamos. Escolhida.
2. **Lucide** (ISC): bom, mas o desenho é mais geométrico e, na versão avaliada, faltavam `music`, `smile` e `trash-2`
   (renomeados); parte dos ícones herdados do Feather exige um segundo aviso (MIT).
3. **Tabler** (MIT): muito grande e mais frio; traço de 2 px por padrão.
4. **Pacote npm** de qualquer um deles: descartado. Traria milhares de ícones para usar ~26 e uma dependência
   nova (CLAUDE.md pede justificativa). Copiar só os usados custa ~13 KB.

## Decisão
- Os SVG usados ficam copiados, sem alteração, em `app/src/ui/icones.ts` (mapa nome → `<path>`). `icone(nome, { rotulo?, tamanho? })`
  monta o `<svg>` e devolve `HtmlSeguro`: `fill="currentColor"`, `focusable="false"`, `aria-hidden="true"` por padrão,
  ou `role="img"` + `aria-label` (escapado) quando há rótulo. Nome desconhecido devolve vazio, nunca lança erro.
- A lista de nomes vive em `app/src/domain/icones.ts` (`NOMES_ICONE`, `ehNomeDeIcone`), porque `domain/` não importa `ui/`.
- `app/content/dominios.json` guarda o **nome** do ícone (`"icone": "chat-circle-text"`), não mais um emoji.
  `validarConteudo` recusa nome fora do conjunto (dado de fora é validado antes de usar, CLAUDE.md), e a tela
  mostra nada em vez de quebrar se um nome ruim chegar até ela.
- Tamanhos por token (`--s-icone` 1.25rem, `--s-icone-g` 2rem) e classes `.icone` / `.icone-g` em `estilos.css`.
- **Licença (MIT):** o aviso de copyright e o texto completo ficam em `app/public/LICENCAS-TERCEIROS.md`, publicado na
  raiz do site junto com o app; `tests/icones.test.ts` confere que continuam lá.
- **Ficam como emoji (conteúdo, não interface):** os rostinhos da ficha "circule", os emojis dentro das atividades e folhas
  (`app/content/`) e tudo o que está em `src/pacote/` (o documento impresso tem as próprias regras: preto e branco, ADR 0004).
  Também ficam os caracteres de texto `☐`, `✓` e `○`.

### Regra de uso
- Ícone **ao lado de texto** é decorativo: `icone('printer')`, sem rótulo (vira `aria-hidden`).
- Ícone **sozinho** precisa de nome: `icone('printer', { rotulo: 'Imprimir' })`, ou `aria-labelledby`/`aria-label` no botão.
- O alvo de toque continua sendo do botão (`--s-alvo-toque`), não do desenho. Nunca só o ícone como pista (sempre há texto ou rótulo).
- Cor herdada (`currentColor`); nada de cor própria no SVG.
- Emoji de interface é proibido em `pages/`, `ui/` e `index.html`; `tests/icones.test.ts` acusa.

### Como adicionar um ícone novo
1. Procure o nome em phosphoricons.com e pegue `assets/regular/<nome>.svg` do repositório `phosphor-icons/core` (mesma versão ou mais nova).
2. Acrescente o nome em `NOMES_ICONE` (`domain/icones.ts`) e o conteúdo dos `<path>` em `ICONES` (`ui/icones.ts`), sem o `<svg>` de fora.
3. Use `icone('nome')`. O teste confere que todo nome usado existe e que todo ícone do mapa é usado.
4. Atualize a versão/commit e a contagem em `LICENCAS-TERCEIROS.md` se mudar de versão.

## Consequências
- Sem dependência nova e sem chamada de rede (privacidade intacta); o app já cacheia o JS, os ícones vão junto.
- Ícones herdam a cor do texto, o que prepara o modo escuro (outro PR).
- Os brotos do engajamento (`icone-broto`, desenhados à mão no projeto) continuam como estão.
- Trocar de conjunto no futuro é mexer em um arquivo (`ui/icones.ts`) e nos nomes de `dominios.json`.
