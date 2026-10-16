# 0003. Camadas com núcleo funcional (domínio puro)

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto

As regras da jornada e do gerador de sessão são o coração do produto e vão mudar muito com o piloto.
Precisamos testá-las de forma rápida e confiável, sem depender de navegador, banco ou data do sistema.

## Decisão

Padrão "núcleo funcional, casca imperativa":

- `src/domain/`: funções **puras** (mesma entrada → mesma saída, sem efeitos colaterais).
  Recebem a data atual e os dados por parâmetro.
- Casca: `src/dados/` (banco), `src/pacote/` (gera HTML), `src/pages/` e `src/ui/` (telas) chamam o domínio.
  O `src/pacote/` também usa o helper de escape `src/ui/html.ts`, para que todo HTML gerado passe pela mesma proteção.
- O ESLint impede o domínio de importar a casca ou usar APIs do navegador (`window`, `document`,
  `location`, `navigator`, `fetch`, `indexedDB`…).

## Consequências

- A maior parte dos testes é unitária e roda em milissegundos.
- O gerador de sessão é determinístico: o mesmo pedido gera a mesma sugestão (fácil de testar e explicar).
- Um pouco mais de "encanamento": as telas precisam buscar os dados e passá-los ao domínio.
