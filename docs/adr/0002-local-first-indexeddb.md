# 0002. Dados no aparelho com IndexedDB (`idb`) atrás de um repositório

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto

Princípio do produto: dados da criança ficam no aparelho (especificação §1 e §9.4). O app precisa
funcionar offline, guardar histórico e, no futuro, fotos do portfólio. O app antigo usava `localStorage`.

## Opções consideradas

1. **localStorage**: simples, mas ~5 MB, síncrono (trava a tela), sem migrações.
2. **IndexedDB com `idb`**: banco nativo do navegador, assíncrono, grande, com versões de esquema;
   `idb` é uma camada de ~1 KB que troca a API antiga de eventos por `async/await`.
3. **Dexie**: IndexedDB com mais recursos (~25 KB) e sincronização paga própria, que concorreria
   com o backend planejado (Supabase).

## Decisão

Opção 2. Todo acesso passa por `src/dados/repositorio.ts`, uma interface com operações do negócio
(`salvarFamilia`, `estadosDaCrianca`, `salvarSessao`…). As telas nunca falam com o banco diretamente.

## Consequências

- Trocar ou somar um banco (ex.: sincronizar com Supabase) exige mudar só a implementação do repositório.
- Testes de integração rodam o repositório contra um IndexedDB simulado (`fake-indexeddb`).
- Mudanças de esquema exigem uma **migração** na função `upgrade` do banco, com teste.
- Se a família limpar os dados do navegador, perde tudo: por isso existe exportar/importar backup.
