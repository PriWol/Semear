# Conteúdo do Semear

Todo o conteúdo que as famílias veem (marcos, atividades, folhas e livros) fica nesta pasta, em JSON.
O app lê estes arquivos no build (ADR 0005). Para publicar conteúdo novo: edite, rode `npm run check`
dentro de `app/` e abra um PR.

## Arquivos

| Arquivo                 | O que contém                                                            |
| ----------------------- | ----------------------------------------------------------------------- |
| `dominios.json`         | Domínios, linhas, trilhas de língua e vertentes. Muda pouco.            |
| `marcos/<DOMÍNIO>.json` | Marcos de cada domínio, ex.: `marcos/LG.json`.                          |
| `referencias.json`      | Catálogo de referências bibliográficas (ABNT) citadas nos marcos.       |
| `atividades/<id>.json`  | Uma atividade por arquivo, com roteiro, ficha e folhas da criança.      |
| `livros.json`           | Curadoria de livros (`editora` e `linkCompra` são opcionais; só https). |
| `acervo.json`           | Acervo gratuito (domínio público/licença aberta), ADR 0016.             |
| `tesouro.json`          | Catálogo d'O Grande Tesouro de Marina (volumes e unidades; ADR 0015).   |

## Marco

```jsonc
{
  "id": "LG.FON.04", // <linha>.<número com 2 dígitos>
  "linha": "LG.FON",
  "ordem": 4, // posição na linha (sem repetir); o `id` é estável e não precisa seguir a ordem
  "titulo": "Identifica a sílaba inicial",
  "descricaoPais": "Percebe que BOLA e BOTA começam com o mesmo pedaço.",
  "evidencias": ["Separa figuras pela sílaba inicial"],
  "idadeTipica": 5,
  "idadeIntroducao": { "Waldorf": 6.5 }, // só gera aviso, nunca bloqueia
  "preRequisitos": ["LG.FON.03"], // pode citar marcos de outras linhas
  "bncc": [], // obrigatório em LG e MA antes do lançamento (portfólio)
  "orientacaoPais": {}, // obrigatório em todo marco, ver abaixo
}
```

### Orientação para os pais

Texto de apoio que a família lê **se quiser**: na jornada ele fica num bloco recolhido, "📖 Para os pais".
**É obrigatório em todo marco** (ADR 0017): marco sem `orientacaoPais` é erro de validação e o CI falha. Só `porVertente` é opcional.

```jsonc
"orientacaoPais": {
  "porQueImporta": "O que o marco desenvolve e por que isso conta.",
  "comoParticipar": "Uma ou duas atividades simples para fazer em casa.",
  "sinaisDeAtencao": "Quando vale conversar com a escola ou um profissional. Não é diagnóstico.",
  "referencias": ["morais-consciencia-fonologica"], // ids de referencias.json
  "porVertente": {
    // só as vertentes com algo a acrescentar; as demais veem apenas o texto geral
    "Waldorf": { "comoParticipar": "Como essa pedagogia trata o marco.", "referencias": ["steiner-educacao-crianca"] },
  },
}
```

- A família vê o texto geral, depois o da **vertente principal** ("Na pedagogia X") e o das **inspirações**.
- O texto por vertente precisa concordar com `idadeIntroducao`: se o marco só entra aos 7 anos naquela
  pedagogia, o texto diz isso e não propõe a tarefa antes.
- Só cite obras que você conferiu (autor, título, editora e ano). Livros não levam link; fontes oficiais
  de acesso livre podem levar, sempre `https://`.

## Referência (`referencias.json`)

```jsonc
{
  "id": "morais-consciencia-fonologica", // usado em "referencias" dos marcos
  "autores": "MORAIS, Artur Gomes de", // já no formato ABNT
  "titulo": "Consciência fonológica na educação infantil e no ciclo de alfabetização",
  "ano": 2019,
  "veiculo": "Belo Horizonte: Autêntica", // local: editora
  "link": "https://…", // opcional
}
```

Na tela a referência sai em ABNT: `AUTORES. *Título*. Veículo, ano.` Cada obra é escrita uma única vez aqui.

## Atividade

Veja `atividades/atv-caca-silabas.json` (Linguagem) e `atividades/atv-feira-numeros.json` (Matemática)
como modelos completos. Campos principais:

- `marcos` (trabalhados; vazio = atividade **complementar**, que exige `dominio` sem jornada, ex.: `AR`, e `categoria`; pode trazer `materialImpresso` com `volume`, `unidade` e `paginas`, conferido contra `tesouro.json`) e `revisa` (aparecem como revisão na ficha);
- `vertentes`, `idade` `[mín, máx]` e `duracaoMin`: usados pelo gerador de sessão para pontuar;
- `objetivo`, `passos`, `observar`, `ajustes`, `materiais`, `toqueVertente`: viram o roteiro do educador;
- `evidencias` e `perguntaFicha`: viram a ficha de registro;
- `folhas`: as páginas da criança (tipos abaixo);
- `autoria.status`: só `"publicado"` aparece para as famílias.

Nos textos, `**negrito**` e `*itálico*` funcionam. HTML não funciona (é escapado, por segurança).

## Tipos de folha

| `tipo`       | Para quê                                                  | Campos                                                                       |
| ------------ | --------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `ligar`      | ligar pares (duas colunas)                                | `titulo`, `esquerda[]`, `direita[]` com `{ emoji, texto }`                   |
| `marcar`     | pintar o quadradinho dos itens que combinam com um modelo | `titulo`, `grupos[]` com `modelo` e `itens[]`                                |
| `cartas`     | até 12 cartas para recortar                               | `titulo`, `cartas[]` com `{ emoji, texto }`, `{ numero }` ou `{ quadroDez }` |
| `desenho`    | desenho livre com linha para escrever                     | `titulo`, `legenda?`                                                         |
| `contar`     | contar itens e circular o número                          | `titulo`, `itens[]` com `{ emoji, quantidade, opcoes[] }`                    |
| `quadro-dez` | representar números (até 20) em quadros de dez            | `titulo`, `dica?`, `numeros[]`                                               |
| `comparar`   | circular onde tem mais                                    | `titulo`, `dica?`, `pares[]` com `a` e `b` `{ emoji, quantidade }`           |

Precisa de um tipo novo? É uma mudança de código (`src/domain/tipos.ts`, `src/pacote/folhas.ts`,
validação e testes).

## Validação

`tests/conteudo.test.ts` valida tudo a cada `npm test` e no CI:

- **erros** (marco inexistente, ordem repetida, resposta fora das opções…) fazem o CI falhar;
- **avisos** (pré-requisito ainda não escrito, atividade em rascunho…) aparecem na tela
  **Configurações → Ver cobertura do conteúdo**.

## Acervo gratuito

`acervo.json` lista obras de acesso gratuito em português, inglês, latim e francês (2 a 8 anos). Cada item tem
`idioma`, `idade`, `fonte`, `licenca`, `url` (só https) e `tipoLink`: `obra` abre o livro; `busca` abre a busca da
própria fonte pelo título. A busca na tela roda no aparelho. Confira a licença antes de incluir uma obra nova.
