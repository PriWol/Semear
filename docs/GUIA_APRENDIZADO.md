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

### Lint, formatação e tipos
- **TypeScript** (tipos): o código declara o "formato" de cada dado. Erros como "esqueci um campo" são
  apontados **antes** de o app rodar. É um corretor ortográfico de lógica.
- **ESLint** (lint): verifica más práticas e as regras da arquitetura (ex.: o domínio não pode acessar a tela).
- **Prettier** (formatação): padroniza a aparência do código, e as revisões focam no que importa.

---

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

### Roteamento por hash
Os endereços das telas ficam como `…/#/jornada/ana`. Isso permite publicar o app em qualquer
hospedagem simples (como o GitHub Pages) sem erros ao recarregar. (ADR 0008)

---

## 6. Glossário rápido

| Termo | Significado |
|---|---|
| **Domínio** (produto) | Grande área do conhecimento: Linguagem, Matemática, Línguas. |
| **Linha** | Sequência de aprendizagem dentro de um domínio (ex.: Consciência fonológica). |
| **Marco** | Uma conquista observável numa linha (ex.: identifica a sílaba inicial). |
| **Fronteira** | O primeiro marco da linha que a criança ainda não consolidou. |
| **Marcos ativos** | Os marcos sendo trabalhados agora (fronteira + o seguinte, no máx. 2). |
| **Pista** | Uma linha, ou uma linha num idioma (no domínio de Línguas). |
| **Sessão** | Um encontro de estudo planejado: atividades + livro. |
| **Pacote** | Os arquivos da sessão: roteiro, materiais, folhas da criança e ficha de registro. |
| **Plano Livre / Família** | Plano gratuito permanente e plano pago por família (especificação §9). |
| **Lacuna** | Linha com marco ativo mas sem atividade publicada: sinal para a curadoria. |
| **SHA-256** | Impressão digital de um arquivo, usada para ter certeza de que ele não mudou. |
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
