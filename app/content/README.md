# Conteúdo do Semear

Todo o conteúdo que as famílias veem (marcos, atividades, folhas e livros) fica nesta pasta, em JSON.
O app lê estes arquivos no build (ADR 0005). Para publicar conteúdo novo: edite, rode `npm run check`
dentro de `app/` e abra um PR.

## Arquivos

| Arquivo                 | O que contém                                                                                         |
| ----------------------- | ---------------------------------------------------------------------------------------------------- |
| `dominios.json`         | Domínios, linhas, trilhas de língua e vertentes. Muda pouco.                                         |
| `marcos/<DOMÍNIO>.json` | Marcos de cada domínio, ex.: `marcos/LG.json`.                                                       |
| `referencias.json`      | Catálogo de referências bibliográficas (ABNT) citadas nos marcos.                                    |
| `atividades/<id>.json`  | Uma atividade por arquivo, com roteiro, ficha e folhas da criança.                                   |
| `guia.json`             | Guia das vertentes (#30): uma seção por vertente e como combiná-las.                                 |
| `sondagem.json`         | Itens da sondagem impressa (#17): um por marco de LG.FON e MA.SEN.                                   |
| `livros.json`           | Curadoria de livros, obras e músicas (ver abaixo). `editora` e `linkCompra` são opcionais; só https. |
| `acervo.json`           | Acervo gratuito (domínio público/licença aberta), ADR 0016.                                          |
| `tesouro.json`          | Catálogo d'O Grande Tesouro de Marina (volumes, cadernos para 2 anos e unidades; ADR 0015).          |

## Revisão do conteúdo

Marcos, atividades e livros aceitam o campo opcional `revisao` (#77):

```jsonc
"revisao": { "estado": "aprovado", "por": "Nome de quem revisou", "em": "2026-11-08" }
```

- `estado`: `rascunho` (escrito pela IA, ainda sem revisão), `revisado` (alguém leu) ou `aprovado` (pode ir para as famílias).
  Valor fora desse conjunto é erro de validação. A partir de `revisado`, `por` e `em` (AAAA-MM-DD) são obrigatórios.
- **Só o `aprovado` aparece no app.** Item sem `revisao` é o conteúdo anterior a este campo e continua aparecendo.
  Conteúdo novo deve entrar com `revisao`.
- **Conferência por profissional de saúde** (ADR 0037): campo opcional dentro de `revisao`, no lugar da frase "conferência
  por profissional pendente" dentro do texto:

  ```jsonc
  "revisao": { "estado": "aprovado", "por": "…", "em": "2026-11-08",
               "conferenciaProfissional": { "estado": "pendente" } }
  // depois da conferência:
  "conferenciaProfissional": { "estado": "conferida", "por": "Nome e registro", "em": "2026-12-01" }
  ```

  `estado`: `pendente` ou `conferida` (fora disso é erro); `conferida` exige `por` e `em` (AAAA-MM-DD). Sem o campo, a tela
  não mostra aviso de conferência. Com `pendente`, a tela mostra **um selo por tela** ("Orientação em conferência por
  profissional de saúde. Não substitui o pediatra."), que some quando vira `conferida`. **Não escreva a frase de conferência
  no texto** (`tests/estilo-conteudo.test.ts`); "não substitui o pediatra" e os cuidados concretos de segurança continuam
  nos textos que precisam deles. `node scripts/migrar-conferencia.mjs` lista o que ainda traz a frase.

- Atividade aprovada que cita marco ainda em `rascunho` é válida, mas o app ignora esse marco em todo lugar
  (pacote, ficha, proposta, busca) via `marcosVisiveis` (`src/domain/conteudo.ts`); ele passa a valer ao ser aprovado.
- Rascunhos e revisados continuam sendo validados (`carregarConteudoBruto`), mesmo escondidos.
- **Fluxo:** a IA abre um PR com os itens em `rascunho`; quem revisa comenta no PR, e o último commit
  troca o estado para `revisado`/`aprovado` com `por` e `em`. O merge é a aprovação registrada.
- Nas atividades, `autoria.status` segue valendo até a regra ser confirmada; para aparecer, a atividade precisa estar
  `publicado` **e** sem revisão ou `aprovada`.

## Livros, obras e músicas (indicação da sessão)

Cada item de `livros.json` é uma indicação que o pacote traz junto da sessão (#73). `tipo` é `livro` (o padrão), `obra` ou `musica`:

- `obra` e `musica` exigem `fonte` (de onde vem: domínio público, acervo) e usam `uso` `observar-e-conversar` ou `ouvir-e-cantar`;
- liga-se a `marcos` e/ou a `linhas` (ex.: `LG.NAR`): a sessão sugere a indicação cujo marco ou linha ela trabalha;
- `linkGratuito` (opcional, só https) leva a uma versão gratuita ou de domínio público e aparece **só como texto** no pacote impresso;
- a criança nunca abre o app: a indicação é para o adulto ou vai impressa.

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

- `marcos` (trabalhados; vazio = atividade **complementar**, que exige `dominio` sem jornada, ex.: `AR`, e `categoria`; pode trazer `materialImpresso` com `volume` **ou** `caderno` (id do caderno em `tesouro.json`, nunca os dois), `unidade` e `paginas`, conferido contra `tesouro.json`) e `revisa` (aparecem como revisão na ficha);
- `vertentes`, `idade` `[mín, máx]` e `duracaoMin`: usados pelo gerador de sessão para pontuar;
- `objetivo`, `passos`, `observar`, `ajustes`, `materiais`, `toqueVertente`: viram o roteiro do educador;
- `evidencias` e `perguntaFicha`: viram a ficha de registro;
- `folhas`: as páginas da criança (tipos abaixo);
- `palavrasChave` (opcional): palavras que ajudam a achar a atividade na tela **Atividades** (#13), além do título, do objetivo e dos marcos. A busca ignora acento e maiúsculas;
- `preparoMin` (opcional) e `cuidados`: o preparo do adulto, à parte da duração, e o aviso de segurança. `cuidados` é obrigatório (e a duração, de até 10 min) quando `idade` começa antes dos 3 anos;
- **A idade da atividade não precisa coincidir com a idade típica do marco** (decisão de 2026-11-21). Uma mesma atividade pode servir a várias idades, com exigência e pontos de trabalho diferentes: ligue-a a todo marco que ela de fato trabalha (o mais novo é a versão simples, o mais velho, a versão mais exigente), amplie `idade` até onde o conteúdo realmente vai e registre em `ajustes` o que muda por idade (`dificil` = o que se pede à criança menor; `facil` = o que se pede à maior). Use o que o texto da atividade já diz, sem inventar passos; só ligue o que a atividade de fato trabalha. Quem começa antes dos 3 anos continua exigindo `cuidados` e duração de até 10 min (e, se ligar a marco de EM, `cuidados` cita "peça pequena" ou "boca").
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
