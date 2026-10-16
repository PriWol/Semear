# 0013. Família de exemplo com marcador por registro

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto
Para testar e demonstrar o app sem cadastrar nada, ele oferece uma **família de exemplo** (#39). O app
guarda uma família só, e os dados ficam apenas no aparelho, sem servidor (ADR 0002). Quem explora o exemplo
pode, sem querer, cadastrar uma criança de verdade ali dentro. Apagar o exemplo **não pode** levar esses dados
reais junto: não há cópia em nuvem para recuperar.

## Opções consideradas
1. **`clear()` em todas as lojas ao apagar o exemplo:** simples, mas apaga também o que a pessoa cadastrou.
2. **Um banco separado só para o exemplo:** isola bem, mas duplica o repositório, as telas e os testes, e o app
   teria de saber em qual banco está.
3. **Marcador `exemplo: true` em cada registro criado pelo exemplo** (família, crianças e sessões; os estados e o
   histórico saem junto com a criança). "Apagar exemplo" remove só o que tem o marcador.

## Decisão
Opção 3. Regras:
- O marcador é um campo opcional (`exemplo?: true`) em `Familia`, `Crianca` e `Sessao`. Não há mudança de versão do
  banco: registros antigos simplesmente não têm o campo.
- `apagarExemplo` nunca usa `clear()`: filtra pelo marcador, numa única transação.
- **Família mantida:** se sobrar criança sem o marcador, a família fica, **sem o marcador**, para a criança real
  não ficar órfã (invisível na tela). A tela leva a pessoa a conferir os dados dela, porque a família ainda traz o
  nome e as vertentes fictícios.
- O exemplo só carrega quando não existe família, e a checagem fica dentro da transação (dois toques seguidos não
  duplicam).
- **Backup:** o `validarBackup` aceita o campo só como `true` ou ausente, e recusa registros de exemplo quando a
  família não é de exemplo (senão Ana e Theo ficariam misturados aos dados reais, sem como apagá-los em bloco).
  O caso inverso (família de exemplo com criança real) é aceito: é o que acontece quando a pessoa cadastra durante o
  exemplo.
- **Lembrete de backup:** o exemplo não grava data de backup. O lembrete (`domain/backup.ts`) só olha crianças sem
  o marcador, então uma criança real cadastrada durante o exemplo já pede backup.

## Consequências
- Mais fácil: apagar o exemplo com segurança, sem tocar no que é da pessoa, e sem código duplicado.
- Mais difícil: todo registro novo criado pelo exemplo precisa lembrar de levar o marcador. Os testes de
  integração cobrem isso (um registro real sobrevive ao "Apagar exemplo" e nada do exemplo fica para trás).
- Se um dia houver mais de uma família no aparelho (ex.: sincronização, #27), o marcador continua valendo, mas a
  regra de "família mantida" precisa ser revista.
