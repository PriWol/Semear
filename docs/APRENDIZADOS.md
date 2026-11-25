# Aprendizados do time

Todos os agentes leem este arquivo ao começar. Entram aqui só regras que a dona do produto aprovou na retro (`/retro`)
ou que já provaram valor. Erro que se repete 2 vezes vira teste ou regra de lint, e a linha aqui aponta para ele.

## Testes
- Antes do e2e, encerre qualquer `vite preview` ainda rodando (`pkill -f "vite preview"`): com a porta 4173 ocupada o
  teste roda contra a build errada. Use `--workers=3`.
- Teste e2e que preenche o cadastro precisa esperar o título "Adicionar criança". Depois de salvar uma criança nova, a tela
  é o próximo passo (`e2e/cadastro.ts`, `irParaJornadaDepoisDeCadastrar`).
- Nunca pular, desligar ou apagar teste para ficar verde.

## Git e PR
- Squash-merge: não reutilize uma branch cujos commits já foram mesclados; abra outra a partir do `origin/main`.
- `Closes #N` só quando o PR entrega a estória; `Refs #N` quando só avança. "Fecha" ou "Entrega" não fecham no GitHub.
- PR que toca conteúdo, dados, CSP, workflows ou ADRs: só a dona mescla.

## Texto e conteúdo
- Texto neutro de gênero ("com sono?", "O cadastro de X está pronto"); guia em `docs/` e decisão D8 da #138.
- Conteúdo de saúde ou desenvolvimento: sinalizar "conferência profissional pendente" (ADR 0037).
