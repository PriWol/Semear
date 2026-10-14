# 0010. Coleção editorial impressa em `tesouro-marina/`, fora do app

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto
A dona do produto pediu uma coleção de livros de atividades impressos (*O Grande Tesouro de Marina*, 8 volumes,
mais de 500 páginas A4) com currículo clássico para 2 a 6 anos. É um produto editorial: textos, ilustrações de
domínio público, cartões e jogos recortáveis em PDF. Não é uma funcionalidade do app e não usa dados de família.

## Opções consideradas
1. **Diretório próprio na raiz (`tesouro-marina/`), com pipeline Python + Playwright:** isolado do `app/`,
   sem dependência nova no app, reproduzível a partir de `editorial/`. Exige Python (numpy, scipy, pillow) e o
   Chromium do Playwright para gerar os PDFs.
2. **Dentro de `app/content/`:** misturaria um produto impresso de centenas de páginas com o conteúdo curado em
   JSON que o app valida (ADR 0005), sem que o app use esse material.
3. **Repositório separado:** isolamento total, mas perde a relação com a jornada por domínios.

## Decisão
Opção 1. A coleção fica em `tesouro-marina/` e não é importada pelo app nem publicada no Pages.

- **Rede:** o único acesso externo é o download, no build editorial, de páginas digitalizadas do Internet Archive
  (`editorial/fontes_v1.py`). Nada da família é enviado. Cada página é conferida por SHA-256
  (`editorial/dominio_publico/paginas.sha256.json`), com limite de tamanho e verificação de imagem.
- **Relação com a jornada:** os domínios da coleção (linguagem, raciocínio, matemática, música, artes, natureza,
  línguas, vida prática) podem mais tarde alimentar marcos e atividades em `app/content/`. Quando isso acontecer,
  a especificação (`docs/JORNADA_SPEC.md`) será atualizada e o conteúdo passará pela validação do ADR 0005.

### Arquivos gerados fora do Git
Os PDFs finais e as páginas de inspeção (`*/inspecao/`) são reproduzíveis a partir de `editorial/` e somariam
centenas de MB no histórico. Opções consideradas: manter no Git, Git LFS ou Release do GitHub. A dona do produto
escolheu a **Release**: o workflow `.github/workflows/publicar-tesouro.yml` gera os PDFs a cada merge no `main` que
altere `tesouro-marina/` e atualiza os anexos da Release `tesouro-marina`. Em PRs, o mesmo workflow só gera os PDFs
(artefato do workflow, para conferência), sem publicar. O Git guarda apenas as fontes: `editorial/`, `docs/` e as
ilustrações de domínio público já recortadas (`editorial/dominio_publico/`).

## Consequências
- O app continua sem dependências novas; quem trabalha só no `app/` não precisa de Python.
- Os PDFs precisam ser regenerados (`python3 volumeN.py`) quando o texto ou o estilo mudar.
- Para baixar os PDFs: página de Releases do repositório, Release `tesouro-marina`.
- O workflow precisa de Python, Node (Playwright/Chromium) e poppler no runner; leva alguns minutos.
