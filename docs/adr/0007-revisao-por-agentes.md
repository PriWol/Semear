# 0007. Revisão por dois agentes + aprovação humana; PR único da v1

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto
A dona do produto é gerente de projetos e não revisa código linha a linha. O app lida com dados de crianças.

## Decisão
- Cada PR é revisado por **dois agentes** (`.github/workflows/revisao-agentes.yml`):
  1. **Correção**: bugs, regras da especificação, testes faltando.
  2. **Segurança e privacidade**: injeção de HTML, dados da criança saindo do aparelho, dependências.
- PRs abertos pelo Dependabot **não passam pelos agentes**: o job é pulado, porque esses PRs não recebem os segredos do repositório e a ação recusa atores bot. Ficam só com CI e aprovação humana.
- O merge exige **CI verde + aprovação da dona do produto**.
- A v1 vai num **único PR**, organizado em commits temáticos para facilitar a revisão.

## Consequências
- Os agentes precisam de um segredo no repositório (`CLAUDE_CODE_OAUTH_TOKEN` ou `ANTHROPIC_API_KEY`).
- PR grande = revisão mais difícil. Mitigação: commits pequenos e descrição do PR com roteiro de leitura.
  Depois da v1, voltar a PRs menores por funcionalidade.
