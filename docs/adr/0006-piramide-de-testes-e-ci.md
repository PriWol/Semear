# 0006. Pirâmide de testes e CI obrigatória

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto
Queremos um software robusto, construído em boa parte com IA. Código gerado por IA precisa de uma
rede de segurança automática que verifique o comportamento, não só a aparência.

## Decisão
**Pirâmide de testes:**
- **Base: unitários** (Vitest) nas regras do domínio e no gerador de pacote. Muitos e rápidos.
- **Meio: integração** (Vitest + `fake-indexeddb`) no repositório de dados.
- **Topo: ponta a ponta** (Playwright, desktop e celular) nos fluxos principais: cadastrar família,
  posicionar criança, gerar e baixar pacote. Poucos e mais lentos.

**CI obrigatória** (`.github/workflows/app-ci.yml`): em todo push e PR que toque `app/`, roda typecheck,
lint, formatação, testes, build e e2e. Nada entra no `main` com CI vermelha.

## Consequências
- Não usamos meta de cobertura em %: o critério é "toda regra de negócio tem teste".
- O CI leva alguns minutos por PR.
- Para ser obrigatória de fato, a proteção do branch `main` precisa ser ligada nas configurações do GitHub.
