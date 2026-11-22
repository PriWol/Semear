# 📘 Guia de aprendizado: decisões técnicas explicadas para gestão

Este guia cresce junto com o projeto. Cada conceito técnico que usamos entra aqui, em linguagem de
gestão, com o **porquê** e um paralelo com o dia a dia de projetos. As decisões formais ficam nos
ADRs (`docs/adr/`); aqui fica o entendimento.

---

## 1. Como o software é organizado

### Camadas e "núcleo funcional"
**O que é:** separar o código em partes com responsabilidades diferentes. No Semear:
- **Domínio** (`src/domain/`): as regras do negócio (onde a criança está na jornada, que atividades sugerir).
- **Dados** (`src/dados/`): guardar e buscar informações no banco.
- **Telas** (`src/pages/`): o que o educador vê e clica.
- **Pacote** (`src/pacote/`): gerar os arquivos para imprimir.

**Paralelo de gestão:** é como separar *política* (regras da empresa) de *operação* (sistemas e pessoas
que executam). Mudar o sistema de RH não deveria mudar a política de férias.

**Por que importa:** as regras do domínio são **funções puras**: dada a mesma entrada, sempre a mesma
saída, sem efeitos colaterais. Isso as torna fáceis de testar, como uma planilha que, com os mesmos
números, sempre dá o mesmo resultado. (ADR 0003)

### Repositório (padrão de projeto)
**O que é:** um "balcão de atendimento" único para os dados. As telas pedem "me dê os marcos da Ana"
sem saber onde ou como isso está guardado.

**Por que importa:** se um dia trocarmos o banco (ou somarmos sincronização com servidor), só o balcão muda. (ADR 0002)

### Regra pura derivada: o selo "parece pronto"
**O que é:** o selo não é um dado guardado; é **calculado** a cada vez que a jornada abre, por uma função pura
(`pareceProntoPara`, em `src/domain/registro.ts`) que olha o histórico: o marco ainda não está *Consolidado* e foi
observado como *Consolidado* em **2 sessões diferentes**. De cada sessão vale só o último registro; um "Está aqui"
zera o que veio antes dele.

**Por que importa:** como é calculado e não guardado, a regra pode mudar (de 2 para 3 sessões, por exemplo) sem
converter nenhum dado, e é testada sem abrir tela nenhuma: só entrega uma lista e recebe um sim ou não. O selo é
uma **dica**: quem confirma o marco é o pai, no mapa. (ADR 0030)

---

## 2. Onde ficam os dados

### Banco de dados local: IndexedDB
**O que é:** um banco de dados que **todo navegador já tem**, dentro do próprio celular ou computador.
Usamos uma pequena biblioteca (`idb`) para facilitar o uso.

**Por que não um servidor agora:** princípio do produto: os dados da criança ficam no aparelho.
Também funciona sem internet e não tem custo de servidor.

**Risco e mitigação:** se a família limpar os dados do navegador ou perder o aparelho, perde os dados.
Por isso existe o **backup** (exportar/importar arquivo).

**Futuro:** quando houver contas e assinatura, entra um banco **no servidor** (planejado: Supabase,
que usa PostgreSQL) só para conta e assinatura. O plano Livre continua sem conta e sem servidor.
A sincronização dos dados da criança, se houver, será criptografada. (ADR 0002 e 0010, especificação §9.4)

### Licença offline ("data de validade")
**O que é:** quando a família assina, o servidor entrega ao app um **comprovante assinado
digitalmente** dizendo "esta conta tem o plano Família até tal data". O app guarda esse comprovante e
confere a assinatura digital sem precisar de internet.

**Por que usamos:** o app funciona offline e o servidor nunca precisa saber quantas crianças existem nem
o que elas aprenderam: só que a licença vale até uma data. Quando ela vence (para quem assina, depois de 7 dias de
tolerância), o app volta aos limites do plano Livre, sem apagar nem esconder nenhum dado. (ADR 0010)

### Migração de dados
**O que é:** quando mudamos o formato dos dados guardados, escrevemos um passo que converte os dados
antigos para o formato novo, para ninguém perder nada ao atualizar o app.

**Paralelo:** como migrar uma planilha para um novo modelo de colunas sem perder as linhas antigas.

**Quando não precisa migrar:** um campo **opcional** novo (como a duração real da sessão, #11) não exige
migração: os registros antigos simplesmente não o têm e continuam valendo. Por isso o registro de sessão não
subiu a versão do banco nem a do arquivo de backup (ADR 0030).

### Histórico que só acrescenta ("append-only")
**O que é:** em vez de editar uma linha, guardamos uma nova linha por acontecimento ("em 15/10, na sessão S-1014-A1,
o marco foi observado como Consolidado"). Nada é apagado nem reescrito. O estado atual do marco é uma coisa; a
história do que foi observado é outra.

**Por que usamos:** a observação da sessão não muda o estado do marco (só o pai muda, no mapa). Guardar cada
observação como um fato novo deixa o app calcular dicas, como o selo "parece pronto", sem mexer no que o pai decidiu.
Ao corrigir um registro, só entra linha nova para o marco que **mudou**; repetir tudo poria observações velhas depois de um "Está aqui". O que vale é a **ordem de gravação**, não a data: uma data pode estar errada, a ordem não. (ADR 0030, especificação §5.2)

### Transação (tudo ou nada)
**O que é:** um grupo de gravações que o banco trata como uma só: ou todas acontecem, ou nenhuma. É como um
cheque: ou o dinheiro sai de uma conta e entra na outra, ou nada acontece.

**Por que usamos:** registrar uma sessão grava a sessão **e** as observações. Se a energia acaba no meio, o banco
não pode ficar com a sessão marcada como feita e sem as observações. O repositório faz as duas gravações na
mesma transação (`registrarSessao`) e desfaz tudo se uma falhar. A transação também nem abre o lugar dos estados dos
marcos, o que garante, no próprio código, que a ficha não muda o estado.

### Gravar só o que mudou (duas abas abertas)
**O que é:** em vez de ler a família ao abrir a tela e depois gravar a cópia inteira por cima, a tela manda ao
repositório só os campos que o formulário alterou, e o repositório lê e grava na mesma transação
(`atualizarFamilia`, `atualizarCrianca`).

**Por que usamos:** com duas abas abertas, a que ficou parada tinha uma cópia velha da família. Ao salvar, desfazia o
que a outra mudou (por exemplo, o aviso diário). Mexendo só nos campos alterados, uma aba não apaga o trabalho da
outra. A função pura `camposAlterados` calcula essa diferença.

### Dado de fora: limites e coerência
**O que é:** a cópia de segurança importada é um arquivo que qualquer um pode ter editado. Antes de apagar os dados do
aparelho, `validarBackup` confere a forma, o tamanho (10 MB, checado por `File.size` antes de ler), a quantidade de
registros, se cada `criancaId` existe no arquivo e se a data de nascimento é possível (`nascimentoPlausivel`).

**Por que usamos:** um arquivo errado não pode zerar o app nem deixar registros órfãos (crianças sem família,
sessões de uma criança que não existe). As regras são puras e moram em `domain/`; o relógio entra por parâmetro.

### Rodízio por domínio, teto de duração e semente do dia (gerador de sessão v2)
**O que é:** o gerador de sessão (`proporSessao`, em `src/domain/sessao.ts`) escolhe atividades em **rodadas**:
em cada rodada entra no máximo uma atividade por **domínio** (Linguagem, Matemática, Artes...), e a próxima é a
melhor pontuada que **caiba no tempo que resta** e no **teto de duração da idade** (2 anos até 10 min ... 7 a 8
anos até 25 min). Quando várias linhas empatam, quem abre a sessão é decidido por uma **semente**: um número
calculado a partir da data e do id da linha (um "embaralhar" que não sorteia).

**Por que importa:** antes, a ordem do arquivo decidia o empate e a primeira atividade entrava mesmo sendo
longa, então a mesma atividade de 35 min abria toda sessão. A semente muda o resultado de um dia para o outro,
mas **a mesma entrada dá sempre a mesma saída**, o que mantém a regra testável (sorteio de verdade quebraria o
teste). O **teste de propriedades** (`tests/sugestor-conteudo.test.ts`) roda a regra com o conteúdo real em 280
combinações e confere afirmações que valem sempre ("a soma fica em até 110% do tempo"), em vez de comparar uma
lista de ids que mudaria a cada atividade nova. (ADR 0036)

### Estado como dado, aviso como selo único (conferência profissional)
**O que é:** em vez de copiar a frase "conferência por profissional pendente" dentro do texto de 230 itens, o
estado vira um **campo** (`revisao.conferenciaProfissional`) e a tela decide sozinha: se algum item da tela está
`pendente`, mostra **um selo** (`seloDeConferencia`, em `src/ui/selo.ts`); se não, não mostra. A decisão de "precisa
avisar?" é uma função pura do domínio (`precisaAvisoDeConferencia`), testada sem abrir navegador.

**Por que importa:** texto é para a pessoa ler; **estado é para o programa decidir**. Misturar os dois obriga a
editar centenas de textos à mão quando a situação muda e deixa o app sem saber o que já foi conferido. O selo
usa `role="note"` para o leitor de tela anunciá-lo, e "Não substitui o pediatra" é uma regra de segurança que
nunca sai da tela. Um teste de estilo impede que a frase volte para dentro dos textos. (ADR 0037)

---

## 3. Qualidade: testes e automação

### Pirâmide de testes
| Nível | O que testa | Quantos | Velocidade | Ferramenta |
|---|---|---|---|---|
| **Unitário** | uma regra isolada ("a fronteira é o primeiro marco não consolidado") | muitos | milissegundos | Vitest |
| **Integração** | partes juntas ("salvar e ler a família no banco") | alguns | segundos | Vitest + banco simulado |
| **Ponta a ponta (e2e)** | o fluxo do usuário no navegador ("cadastrar família e baixar um pacote") | poucos | minutos | Playwright |

**Paralelo de gestão:** unitário = conferir cada item do checklist; integração = conferir que as
equipes se entendem na passagem de bastão; e2e = o teste de aceite com o cliente.

**Por que não meta de cobertura (%):** um número alto pode esconder testes que não protegem nada.
Nosso critério é qualitativo: **toda regra de negócio tem teste**. (ADR 0006)

### CI (Integração Contínua)
**O que é:** um robô (GitHub Actions) que, a cada envio de código, roda automaticamente todos os
testes e verificações. Se algo falhar, o PR fica vermelho e não deve entrar.

**Paralelo:** um *quality gate* automático em cada entrega, sem depender de alguém lembrar de conferir.

### Teste de regra editorial (aviso por página)
**O que é:** um teste que lê as páginas geradas e confere uma regra de conteúdo, em vez de uma função. No caderno de atividades, por exemplo, toda página que cita água precisa trazer o aviso de supervisão **na própria página**: checar só que a frase existe “em algum lugar” do livro deixaria uma página sem o aviso passar.

**Paralelo:** um checklist de conformidade em que cada documento é conferido, não só o conjunto.

### Lint, formatação e tipos
- **TypeScript** (tipos): o código declara o "formato" de cada dado. Erros como "esqueci um campo" são
  apontados **antes** de o app rodar. É um corretor ortográfico de lógica.
- **ESLint** (lint): verifica más práticas e as regras da arquitetura (ex.: o domínio não pode acessar a tela).
- **Prettier** (formatação): padroniza a aparência do código, e as revisões focam no que importa.

---

### Modo escuro com tokens
O navegador informa se o aparelho prefere tema escuro (`@media (prefers-color-scheme: dark)`). Como todo estilo usa variáveis (`--s-fundo`, `--s-tinta`), basta redefinir os **mesmos nomes** nesse bloco e o app inteiro troca de cor, sem tocar nos estilos das telas. O contraste dos dois temas é testado em `tests/tokens.test.ts`. A folha impressa fica de fora de propósito: papel é sempre claro (ADR 0033).

## 4. Como trabalhamos com IA (vibe coding com disciplina)

### O fluxo: spec → plano → testes → código → revisão
1. **Spec**: o que e por quê (você escreve ou aponta a especificação).
2. **Plano**: a IA propõe como fazer; você aprova.
3. **Testes**: escritos antes ou junto do código; viram a "especificação executável".
4. **Código**: a IA implementa até os testes passarem.
5. **Revisão**: CI + dois agentes revisores + sua aprovação.

**Por que funciona:** a IA é rápida, mas tende a "inventar" decisões. Os testes e o CLAUDE.md
são os **trilhos**: definem o que é certo, e a IA não pode sair deles sem que algo fique vermelho.

### CLAUDE.md
Arquivo na raiz que a IA lê no começo de toda sessão: comandos, arquitetura, convenções e
**definição de pronto**. É o "manual de onboarding" da IA. Quanto melhor ele estiver, mais coerente
é o trabalho entre sessões diferentes.

### Tokens de design
Cores, fontes e medidas guardadas como variáveis CSS (`--s-tinta`, `--s-principal`…) num arquivo só,
`app/src/tokens.css`. Em vez de escrever `#355e45` em cem lugares, escreve-se `var(--s-principal)`. Trocar a
identidade visual vira editar um arquivo, e app e folhas impressas nunca divergem. Um teste confere o contraste
das cores (acessibilidade AA).

### ADR (registro de decisão)
Uma página por decisão técnica importante: contexto, opções, escolha, consequências.
**Paralelo:** a ata de decisão de um comitê. Responde, meses depois, "por que fizemos assim?".

### PR (Pull Request) e revisão
**O que é:** um pedido para juntar mudanças ao código principal (`main`). É onde acontecem a revisão,
os comentários e a aprovação. No Semear: dois agentes revisam (correção; segurança e privacidade) e
você aprova o merge. (ADR 0007)

---

## 5. Publicação

### PWA (Progressive Web App)
Um site que se comporta como aplicativo: **instala** no celular e no computador, abre em tela cheia e
**funciona offline**. Um só código para todas as plataformas, sem passar pelas lojas (e sem a taxa delas). (ADR 0001)

### Service worker
Um "assistente" que o navegador roda por trás do app, guardando os arquivos em cache para funcionar
sem internet e atualizando-os quando sai uma versão nova.

### Publicação contínua (deploy automático)
**O que é:** a cada merge no `main`, um robô (GitHub Actions) verifica o código, gera a versão final
do app (o *build*) e publica no GitHub Pages. Ninguém precisa "subir arquivos" à mão. (ADR 0009)

**Paralelo de gestão:** é uma linha de produção com controle de qualidade embutido: se a inspeção
(`npm run check`) reprovar, o produto não sai da fábrica.

### Conferir o que se baixa (SHA-256 e "falha fechada")
**O que é:** o SHA-256 é uma "impressão digital" de um arquivo: qualquer mudança, mesmo de um pixel, gera outra
impressão. Antes de usar uma imagem baixada, o pipeline da coleção impressa (`tesouro-marina/`) compara a impressão
dela com a que foi registrada quando a imagem foi conferida a olho. **Falha fechada** significa que, na dúvida
(hash diferente ou ausente), o processo para em vez de seguir adiante. (ADR 0011)

**Paralelo de gestão:** é o recebimento de mercadoria com nota fiscal: o que chega sem nota ou com nota que não
bate não entra no estoque.

### Recortar uma prancha sem mexer no original
**O que é:** uma prancha antiga às vezes traz mais de uma figura (o sabiá e outra ave, por exemplo). Em vez de baixar outra
imagem, o pipeline do Volume 6 guarda o arquivo de origem inteiro, conferido por SHA-256, e grava um JPEG só com o trecho
indicado (`RECORTES` em `fontes_v6.py`), sem retoque de cor. O crédito do livro diz que é um recorte. O recorte também pode
ser só visual (um quadro do estilo que mostra um pedaço da mesma imagem), como nos cartões da lagarta e da borboleta. (ADR 0019)

**Paralelo de gestão:** é citar um trecho de um relatório: o relatório inteiro continua guardado, e a citação diz de onde veio.

### Imagem com fundo transparente e `<picture>` para o tema escuro
**O que é:** as gravuras das telas (ADR 0035) são WebP com **canal alfa**: cada pixel guarda a cor da tinta e *quanto* dela
aparece (transparência). Assim o papel amarelado do livro some e a gravura assenta sobre qualquer fundo do app. Para o tema
escuro há um segundo arquivo, com a mesma gravura em tinta clara; o `<picture>` com `<source media="(prefers-color-scheme: dark)">`
faz o navegador escolher sozinho, sem JavaScript. O registro em `src/gravuras.ts` e o teste de SHA-256 repetem a "falha fechada" do
Tesouro: arquivo que não bate com o registro derruba o teste.

**Paralelo de gestão:** é ter o logotipo da empresa em duas versões (colorida e em branco) e deixar o sistema usar a certa conforme o
fundo do documento, com uma planilha dizendo de onde veio cada arquivo.

### Versionamento (números de versão)
**O que é:** cada publicação tem um número, como `0.2.0`. O primeiro número muda nas grandes viradas
(o `1.0` será a abertura ao público), o do meio a cada fase do roteiro, e o último em correções
pequenas. O app mostra a versão no topo e conta o que mudou em "Novidades". Quando sai uma versão
nova, aparece "Nova versão disponível · Atualizar". (ADR 0012)

**Paralelo de gestão:** é o número da revisão de um documento ("v3 do contrato"). Quando alguém
relata um problema, a primeira pergunta é "em qual versão?".

### Roteamento por hash
Os endereços das telas ficam como `…/#/jornada/ana`. Isso permite publicar o app em qualquer
hospedagem simples (como o GitHub Pages) sem erros ao recarregar. (ADR 0008)

### Termos de uso e política de privacidade
São duas páginas curtas, ligadas no rodapé de todas as telas e na boas-vindas, que dizem à família o
que o app faz com os dados dela e em que condições é oferecido. Elas só valem se **cada afirmação for
verdadeira frente ao código**: "nada vai a servidor" depende de não haver `fetch` nem analytics;
"apagar tudo" depende de `apagarTudo` limpar mesmo todas as lojas do banco; "as letras ficam
guardadas" depende do cache do service worker. Por isso, mudou o comportamento (conta, servidor,
nova loja de dados, nova chamada externa), muda o texto no mesmo PR. A versão atual é inicial e não
teve revisão jurídica; não promete preço, plano nem prazo, só diz que haverá aviso antes de
qualquer cobrança. (#25)

### Caixa de confirmação com `<dialog>`
`confirm()` e `alert()` do navegador aparecem diferentes em cada celular e não deixam oferecer um botão
como "Guardar uma cópia primeiro". O elemento HTML `<dialog>`, aberto com `showModal()`, já traz o que
precisamos: prende o foco dentro da caixa, fecha com Esc e devolve o foco ao botão que a abriu. Em
`src/ui/dialogo.ts` ele recebe título, texto e botões; para a ação sem volta ("Apagar todos os dados")
a caixa pede a palavra APAGAR (regra pura em `domain/confirmacao.ts`) antes de liberar o botão. Do mesmo
modo, a hora do aviso usa dois campos (hora e minutos) porque o `input type=time` segue o idioma do
aparelho (AM/PM) e não dá para forçar 24 h; a validação fica em `horaDe24h`. A tela de Ajustes
(rota `#/config`) mostra a "última cópia" por `resumoUltimaCopia`, com alerta a partir de 30 dias.

---

## 6. Glossário rápido

| Termo | Significado |
|---|---|
| **Domínio** (produto) | Grande área do conhecimento: Linguagem, Matemática, Línguas. |
| **Linha** | Sequência de aprendizagem dentro de um domínio (ex.: Consciência fonológica). |
| **Marco** | Uma conquista observável numa linha (ex.: identifica a sílaba inicial). |
| **Orientação para os pais** | Texto pedagógico de um marco, recolhido na jornada ("Para os pais"): por que importa, como participar, sinais de atenção e o que a vertente da família acrescenta. |
| **Conferência profissional** | Estado (`pendente` ou `conferida`) guardado em `revisao.conferenciaProfissional`; faz a tela mostrar um selo único de aviso, que some quando vira conferida (ADR 0037). |
| **Referência** | Obra do catálogo bibliográfico (`referencias.json`) citada nos marcos, exibida em ABNT. |
| **Fronteira** | O primeiro marco da linha que a criança ainda não consolidou. |
| **Marcos ativos** | Os marcos sendo trabalhados agora (fronteira + o seguinte, no máx. 2). |
| **Pista** | Uma linha, ou uma linha num idioma (no domínio de Línguas). |
| **Sessão** | Um encontro de estudo planejado: atividades + livro. |
| **Teto de duração** | Limite suave, por idade, para uma atividade da sessão (2 anos: 10 min; 7 a 8 anos: 25 min). Acima dele só entra se for a única possível (ADR 0036). |
| **Pacote** | Os arquivos da sessão: roteiro, materiais, folhas da criança e ficha de registro. |
| **Plano Livre / Família** | Plano gratuito permanente e plano pago por família (especificação §9). |
| **Lacuna** | Linha com marco ativo mas sem atividade publicada: sinal para a curadoria. |
| **SHA-256** | Impressão digital de um arquivo, usada para ter certeza de que ele não mudou. |
| **Pulso** (música) | A batida regular que não muda, como os passos de quem caminha; o ritmo é o desenho das batidas sobre o pulso. |
| **Musicograma** | A música desenhada como formas e cores, para acompanhar com o dedo enquanto se escuta. |
| **Domínio público** | Obra cujos direitos autorais acabaram (no Brasil, 70 anos após a morte do autor) e que pode ser reproduzida livremente; vale para a obra, não para uma foto dela com direitos próprios. |
| **Reprodução de obra** | Foto ou digitalização de um quadro; nunca tem exatamente a cor do original, e o volume 5 avisa isso. |
| **SVG** | Desenho feito de linhas e formas descritas em texto; a pauta e as notas do Volume 4 são geradas assim, em `musica.py`. |
| **Domínio** (código) | A camada do código com as regras de negócio (`src/domain/`). |
| **Função pura** | Função sem efeitos colaterais: mesma entrada, mesma saída. |
| **Repositório** | Ponto único de acesso aos dados guardados. |
| **IndexedDB** | Banco de dados embutido no navegador. |
| **CI** | Robô que roda testes e verificações a cada envio de código. |
| **E2E** | Teste "ponta a ponta", que usa o app como uma pessoa usaria. |
| **Lint** | Verificador automático de más práticas no código. |
| **PR** | Pull Request: pedido de revisão e merge de mudanças. |
| **ADR** | Registro de uma decisão técnica e do seu porquê. |
| **PWA** | Site instalável que funciona offline. |
| **Build** | O processo que transforma o código em arquivos prontos para publicar. |
| **Dependência** | Biblioteca de terceiros usada pelo projeto (ex.: `idb`). |
| **Atividade complementar** | Atividade de um domínio sem jornada (música, artes…): não tem marcos e entra em no máximo uma por sessão (ADR 0015). |
| **Material impresso** | Trecho de um volume d'O Grande Tesouro de Marina ligado a uma atividade; a Biblioteca abre o PDF na página certa. |
| **Service worker** | Programa do navegador que guarda arquivos do app para uso offline; precisa ser instruído a não interceptar os PDFs. |
| **CSP** | Content Security Policy: lista que diz ao navegador de onde scripts, estilos e conexões podem vir; bloqueia código injetado (ADR 0022). |
| **Iframe sandbox** | Quadro isolado da página: sem a origem do app, só com o que for liberado. Um `srcdoc` herda a CSP do app; por isso a prévia usa `previa.html` (ADR 0022). A "tela cheia" é um painel (`<dialog>` modal) com esse mesmo iframe, não uma nova aba `blob:`, que seria da origem do app. |
| **Faixa etária** | Idades que o produto atende (2 a 8 anos). O app avisa, mas não bloqueia, quem está fora (ADR 0023). |
| **Preparo** | Tempo do adulto para separar materiais; fica fora dos 30 minutos de atividade da sessão (ADR 0023). |
| **Regulação emocional** | Capacidade de perceber o que sente e voltar à calma. Aos 2 anos depende do adulto (“coregulação”); depois a criança assume aos poucos (ADR 0024). |
| **Sondagem** | Folha curta aplicada no papel para descobrir onde a criança está em cada linha. Começa perto da idade, sobe se acertou, desce se não observou, e grava a posição com origem “sondagem” (#17, §5.4). |
| **Migração de banco** | Mudança na estrutura do IndexedDB que roda ao abrir o app (aqui, v1 → v2 para criar os planos); precisa de teste e não volta atrás (ADR 0025). |
| **Ressondagem** | Mini-sondagem só das linhas “paradas” (marco em desenvolvimento sem mudar há 8 semanas) ou “sem observação” (nenhum registro). Reaproveita a folha da sondagem inicial (#18). |
| **Observação (da sessão)** | O que o educador viu em cada marco depois da sessão (*Não observado*, *Em desenvolvimento*, *Consolidado*). Fica no histórico e **não muda** o estado do marco (#11, §5.2). |
| **Selo "parece pronto"** | Dica na jornada: marco ainda não consolidado e observado como *Consolidado* em 2 sessões diferentes. Calculado, nunca guardado (ADR 0030). |
| **Histórico "só acrescenta"** | Cada acontecimento vira uma linha nova; nada é editado nem apagado (exceto quando a sessão ou a criança é excluída). |
| **Transação** | Grupo de gravações do banco que acontece inteiro ou não acontece. |
| **Ícone SVG inline** | Desenho vetorial escrito dentro do HTML; com `fill="currentColor"` herda a cor do texto. O app copia só os ~26 ícones Phosphor (MIT) que usa em `ui/icones.ts`, sem pacote nem rede; decorativo leva `aria-hidden`, sozinho leva `aria-label` (ADR 0034). |
| **Notificação local** | Aviso agendado pelo próprio aplicativo no aparelho, sem servidor. Usado no lembrete diário das atividades de hoje (ADR 0028). |
