import { abrirAjustes, apagarTudoPelosAjustes, confirmarTrazerCopia } from './ajustes-ajuda';
import { escolherAtividade } from './proposta';
import { expect, test, type Page } from '@playwright/test';
import { readFile } from 'node:fs/promises';

// #11 "informar progresso": registrar a sessão pela ficha, sem mudar o estado do marco (§5.2),
// e o selo "parece pronto" quando a observação Consolidado se repete em 2 sessões diferentes.
// Todos os testes começam em "Explorar com uma família de exemplo" (Ana e Theo, ADR 0013).

const HOSTS_PERMITIDOS = ['fonts.googleapis.com', 'fonts.gstatic.com'];

async function explorar(page: Page) {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
}

const anaCartao = (page: Page) => page.locator('.crianca-cartao', { hasText: /\bAna\b/ });

/** Prepara uma sessão da Ana só com a linha de consciência fonológica (a atividade "Caça às sílabas"). */
async function gerarSessaoDaAna(page: Page): Promise<string> {
  await anaCartao(page).getByRole('link', { name: 'Preparar sessão' }).click();
  await page.getByRole('radio', { name: /Escolher linhas/ }).check();
  await page.getByRole('checkbox', { name: /Consciência fonológica/ }).check();
  await page.getByRole('button', { name: 'Sugerir atividades' }).click();
  await escolherAtividade(page, 'Caça às sílabas');
  await page.getByRole('button', { name: 'Gerar pacote' }).click();
  const titulo = page.getByRole('heading', { name: /Sessão S-/ });
  await expect(titulo).toBeVisible();
  return ((await titulo.innerText()).match(/S-\d{4}-[A-Z]\d+/) ?? [''])[0]!;
}

const grupoDoMarco = (page: Page, marco: string) =>
  page.getByRole('group', { name: new RegExp(marco.replaceAll('.', '\\.')) });

const marcoNaJornada = (page: Page, id: string) => page.locator(`li.marco[data-marco="${id}"]`);

async function abrirJornadaDaAna(page: Page) {
  await page.getByRole('link', { name: 'Início' }).click();
  await anaCartao(page).getByRole('link', { name: 'Ver jornada' }).click();
  await expect(page.getByRole('heading', { name: /Jornada de Ana/ })).toBeVisible();
}

test.beforeEach(async ({ page }) => {
  page.on('dialog', (d) => void d.accept());
});

test('gerar, registrar e ver na jornada: o selo só aparece com 2 sessões diferentes e o estado não muda', async ({
  page,
}) => {
  const externos: string[] = [];
  page.on('request', (r) => {
    const url = new URL(r.url());
    const interno =
      url.origin === 'http://localhost:4173' || ['data:', 'blob:'].includes(url.protocol);
    if (!interno && !HOSTS_PERMITIDOS.includes(url.hostname)) externos.push(r.url());
  });

  await explorar(page);
  // A Ana já tem UMA sessão registrada com Consolidado em LG.FON.04: sozinha, não acende o selo.
  await abrirJornadaDaAna(page);
  await expect(marcoNaJornada(page, 'LG.FON.04')).not.toContainText('parece pronto');
  await expect(
    marcoNaJornada(page, 'LG.FON.04').getByRole('button', { name: /Em desenvolvimento/ }),
  ).toHaveAttribute('aria-pressed', 'true');

  // Gera uma segunda sessão e registra: a ficha de registro do app é a do pacote.
  await page.getByRole('link', { name: 'Início' }).click();
  const codigo = await gerarSessaoDaAna(page);
  await page.getByRole('link', { name: 'Registrar', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Como foi a sessão?' })).toBeVisible();
  await expect(page.locator('.reg-contexto')).toContainText(codigo);
  await expect(page.locator('.reg-contexto')).toContainText('Ana');
  await expect(page.locator('#contador-marcos')).toContainText('0 de 2 marcos marcados');

  // Nenhum rádio vem marcado.
  await expect(page.locator('fieldset.reg-marco input[type=radio]:checked')).toHaveCount(0);
  await grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }).check();
  await expect(page.locator('#contador-marcos')).toContainText('1 de 2 marcos marcados');
  await grupoDoMarco(page, 'LG.FON.03').getByLabel('Em desenvolvimento').check();
  await page.getByLabel('Duração real (minutos)').fill('25');
  await page.getByLabel('Animado').check();
  await page.getByLabel(/Anotações/).fill('Pediu para brincar de novo.');
  await page.getByRole('button', { name: 'Salvar registro' }).click();

  // Volta ao início, avisa e mostra "Feita ✓" na lista.
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await expect(page.locator('#aviso')).toContainText(`Sessão ${codigo} registrada.`);
  await expect(page.locator('.lista-sessoes li', { hasText: codigo })).toContainText('Feita ✓');

  // Agora são 2 sessões diferentes com Consolidado: o selo aparece, e o estado continua "Em desenvolvimento".
  await abrirJornadaDaAna(page);
  const marco = marcoNaJornada(page, 'LG.FON.04');
  await expect(marco).toContainText('parece pronto');
  await expect(marco.getByRole('button', { name: /Em desenvolvimento/ })).toHaveAttribute(
    'aria-pressed',
    'true',
  );
  await expect(marco.getByRole('button', { name: /Consolidado/ })).toHaveAttribute(
    'aria-pressed',
    'false',
  );
  // O selo é só uma dica (sem botão). O pai confirma no mapa e o selo some.
  await expect(marco.locator('.selo-pronto').getByRole('button')).toHaveCount(0);
  await marco.getByRole('button', { name: /Consolidado/ }).click();
  await expect(marcoNaJornada(page, 'LG.FON.04')).not.toContainText('parece pronto');

  expect(externos).toEqual([]);
});

test('corrigir um registro: a sessão volta preenchida e conta como uma só', async ({ page }) => {
  await explorar(page);
  const codigo = await gerarSessaoDaAna(page);
  await page.getByRole('link', { name: 'Registrar', exact: true }).click();
  await grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }).check();
  await page.getByRole('button', { name: 'Salvar registro' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();

  // Reabre pela lista: aviso, campos preenchidos e botão "Salvar alterações".
  await page.locator('.lista-sessoes li', { hasText: codigo }).getByRole('link').click();
  await page.getByRole('link', { name: 'Corrigir registro' }).click();
  await expect(page.locator('.reg-aviso')).toContainText('Esta sessão já foi registrada em');
  await expect(
    grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }),
  ).toBeChecked();
  await expect(page.getByRole('button', { name: 'Salvar alterações' })).toBeVisible();
  await page.getByRole('button', { name: 'Salvar alterações' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
});

test('salvar uma sessão já registrada pede confirmação; cancelar não grava', async ({ page }) => {
  await explorar(page);
  const codigo = await gerarSessaoDaAna(page);
  await page.getByRole('link', { name: 'Registrar', exact: true }).click();
  await grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }).check();
  await page.getByRole('button', { name: 'Salvar registro' }).click(); // primeira vez: sem pergunta
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();

  await page.locator('.lista-sessoes li', { hasText: codigo }).getByRole('link').click();
  await page.getByRole('link', { name: 'Corrigir registro' }).click();
  await page.getByLabel(/Anotações/).fill('nota nova');
  const perguntas: string[] = [];
  page.removeAllListeners('dialog');
  page.on('dialog', (d) => {
    perguntas.push(d.message());
    void d.dismiss();
  });
  await page.getByRole('button', { name: 'Salvar alterações' }).click();
  await expect.poll(() => perguntas.length).toBe(1);
  expect(perguntas[0]).toMatch(
    /Esta sessão já foi registrada em \d{2}\/\d{2}\. Substituir o registro anterior\?/,
  );
  // Cancelou: continua na ficha, com o texto na tela, e nada foi gravado.
  await expect(page.getByRole('heading', { name: 'Como foi a sessão?' })).toBeVisible();
  await expect(page.getByLabel(/Anotações/)).toHaveValue('nota nova');
  await expect(page.getByRole('button', { name: 'Salvar alterações' })).toBeEnabled();

  page.removeAllListeners('dialog');
  page.on('dialog', (d) => void d.accept());
  await page.getByRole('button', { name: 'Salvar alterações' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await page.locator('.lista-sessoes li', { hasText: codigo }).getByRole('link').click();
  await expect(page.locator('.reg-anotacoes')).toHaveText('nota nova');
});

for (const largura of [320, 390]) {
  test(`com um estado marcado, nada transborda em ${largura} px`, async ({ page }) => {
    await page.setViewportSize({ width: largura, height: 800 });
    await explorar(page);
    await gerarSessaoDaAna(page);
    await page.getByRole('link', { name: 'Registrar', exact: true }).click();
    for (const est of ['Não observado', 'Em desenvolvimento', 'Consolidado']) {
      await grupoDoMarco(page, 'LG.FON.04').getByLabel(est, { exact: true }).check();
      const medidas = await page.evaluate(() => {
        const cartao = document.querySelector('fieldset.reg-marco')!.getBoundingClientRect();
        const botoes = [...document.querySelectorAll('fieldset.reg-marco .reg-rotulo')].map((b) =>
          b.getBoundingClientRect(),
        );
        return {
          rolagem: [document.documentElement.scrollWidth, document.documentElement.clientWidth],
          sobra: Math.max(...botoes.map((b) => b.right - cartao.right)),
          larguras: botoes.map((b) => Math.round(b.width)),
        };
      });
      expect(medidas.rolagem[0]).toBeLessThanOrEqual(medidas.rolagem[1]!);
      expect(medidas.sobra).toBeLessThanOrEqual(0);
      // sem deslocamento: as três colunas têm a mesma largura marcado ou não
      expect(new Set(medidas.larguras).size).toBe(1);
    }
  });
}

test('"Marcar como feito" no plano da semana é só um atalho: não conta para o selo', async ({
  page,
}) => {
  await explorar(page);
  await anaCartao(page).getByRole('link', { name: 'Planejar semana' }).click();
  await page.getByRole('button', { name: 'Planejar semana' }).click();
  const dias = page.locator('section.dia-plano');
  await expect(dias).toHaveCount(3);
  await dias.first().getByRole('button', { name: 'Marcar como feito' }).click();
  await expect(page.locator('section.dia-plano').first()).toContainText('Feita ✓');

  // A sessão criada pelo atalho não está registrada: continua sem "Feita ✓" no início e sem selo.
  await page.getByRole('link', { name: 'Início' }).click();
  await expect(page.locator('.lista-sessoes li').first()).not.toContainText('Feita ✓');
  await abrirJornadaDaAna(page);
  await expect(page.locator('.selo-pronto')).toHaveCount(0);

  // Registrando a sessão do dia, o plano continua mostrando "Feita ✓" e não oferece mais "Desmarcar"
  // (desmarcar apagaria a sessão e a observação dela).
  await page.getByRole('link', { name: 'Início' }).click();
  await page.locator('.lista-sessoes li').first().getByRole('link').click();
  await page.getByRole('link', { name: 'Registrar', exact: true }).click();
  await page.getByRole('button', { name: 'Salvar registro' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await anaCartao(page).getByRole('link', { name: 'Planejar semana' }).click();
  await expect(page.locator('section.dia-plano').first()).toContainText('Feita ✓');
  await expect(
    page.locator('section.dia-plano').first().getByRole('button', { name: 'Desmarcar' }),
  ).toHaveCount(0);
});

test('achar a sessão pelo código, com minúsculas e espaços', async ({ page }) => {
  await explorar(page);
  const codigo = (await page.locator('.lista-sessoes li').first().locator('b').innerText()).trim();
  const digitado = codigo.toLowerCase().replaceAll('-', ' '); // "s 1104 a1"

  await anaCartao(page).getByRole('link', { name: 'Registrar sessão' }).click();
  await expect(page.getByRole('heading', { name: 'Registrar sessão', level: 1 })).toBeVisible();
  await page.getByLabel('Código da sessão').fill(digitado);
  await page.getByRole('button', { name: 'Encontrar sessão' }).click();
  await expect(page.getByRole('heading', { name: 'Como foi a sessão?' })).toBeVisible();
  await expect(page.locator('.reg-contexto')).toContainText(codigo);
});

test('código inexistente ou vazio mostra a mensagem, devolve o foco e mantém a lista', async ({
  page,
}) => {
  await explorar(page);
  await page.goto('./#/sessao/registrar');
  const campo = page.getByLabel('Código da sessão');
  await campo.fill('S-0000-Z9');
  await page.getByRole('button', { name: 'Encontrar sessão' }).click();
  const alerta = page.getByRole('alert');
  await expect(alerta).toContainText('Não achamos a sessão “S-0000-Z9”.');
  await expect(alerta).toContainText('Confira o código impresso no alto da folha');
  await expect(campo).toBeFocused();
  await expect(campo).toHaveAttribute('aria-invalid', 'true');
  await expect(
    page.getByRole('heading', { name: 'Ou escolha uma das últimas sessões' }),
  ).toBeVisible();

  await campo.fill('   ');
  await page.getByRole('button', { name: 'Encontrar sessão' }).click();
  await expect(alerta).toContainText('Digite o código da sessão.');

  // Texto hostil aparece como texto, nunca vira HTML.
  await campo.fill('<img src=x onerror=alert(1)>');
  await page.getByRole('button', { name: 'Encontrar sessão' }).click();
  await expect(alerta).toContainText('<img src=x onerror=alert(1)>');
  await expect(alerta.locator('img')).toHaveCount(0);

  // E dá para escolher na lista (até 6 sessões, as mais recentes primeiro).
  const itens = page.locator('.reg-lista-sessoes a');
  await expect(itens).toHaveCount(3);
  await itens.first().click();
  await expect(page.getByRole('heading', { name: 'Como foi a sessão?' })).toBeVisible();
});

test('a anotação aparece como texto literal e só o obrigatório já salva', async ({ page }) => {
  await explorar(page);
  const codigo = await gerarSessaoDaAna(page);
  await page.getByRole('link', { name: 'Registrar', exact: true }).click();
  // Só um marco marcado; duração, engajamento e anotação ficam de fora.
  await grupoDoMarco(page, 'LG.FON.04').getByLabel('Em desenvolvimento').check();
  await page.getByRole('button', { name: 'Salvar registro' }).click();
  await expect(page.locator('.lista-sessoes li', { hasText: codigo })).toContainText('Feita ✓');

  // Corrige com uma anotação que parece HTML.
  await page.locator('.lista-sessoes li', { hasText: codigo }).getByRole('link').click();
  await page.getByRole('link', { name: 'Corrigir registro' }).click();
  await page.getByLabel(/Anotações/).fill('<b>x</b>');
  await page.getByRole('button', { name: 'Salvar alterações' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();

  await page.locator('.lista-sessoes li', { hasText: codigo }).getByRole('link').click();
  const anotacao = page.locator('.reg-anotacoes');
  await expect(anotacao).toHaveText('<b>x</b>');
  await expect(anotacao.locator('b')).toHaveCount(0);
});

test('detalhes inválidos mostram o erro e não perdem o que foi marcado', async ({ page }) => {
  await explorar(page);
  await gerarSessaoDaAna(page);
  await page.getByRole('link', { name: 'Registrar', exact: true }).click();
  await grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }).check();
  await page.getByLabel('Duração real (minutos)').fill('999');
  await page.getByRole('button', { name: 'Salvar registro' }).click();
  await expect(page.getByRole('alert')).toContainText('de 1 a 240');
  await expect(
    grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }),
  ).toBeChecked();
  await expect(page.getByRole('button', { name: 'Salvar registro' })).toBeEnabled();
});

test('guardar e trazer a cópia mantém o registro; um arquivo inválido mostra o erro e mantém os dados', async ({
  page,
}) => {
  const mensagens: string[] = [];
  page.removeAllListeners('dialog');
  page.on('dialog', (d) => {
    mensagens.push(d.message());
    void d.accept();
  });
  await explorar(page);
  const codigo = await gerarSessaoDaAna(page);
  await page.getByRole('link', { name: 'Registrar', exact: true }).click();
  await grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }).check();
  await page.getByLabel(/Anotações/).fill('Anotação do backup');
  await page.getByRole('button', { name: 'Salvar registro' }).click();
  await expect(page.locator('.lista-sessoes li', { hasText: codigo })).toContainText('Feita ✓');

  await abrirAjustes(page);
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Guardar uma cópia dos meus dados' }).click(),
  ]);
  const arquivo = (await download.path())!;
  const texto = await readFile(arquivo, 'utf-8');
  expect(texto).toContain('Anotação do backup');
  // Espera a tela se atualizar com a data da cópia antes de escolher arquivo (ela se redesenha depois do download).
  await expect(page.getByText(/Última cópia: hoje/)).toBeVisible();

  // Um backup adulterado (observação de uma sessão que não existe) é recusado sem apagar nada.
  const adulterado = JSON.parse(texto) as { historico: Record<string, unknown>[] };
  adulterado.historico.push({
    criancaId: 'exemplo-ana',
    chave: 'LG.FON.04',
    sessaoId: 'sessao-que-nao-existe',
    registro: { estado: 'consolidado', atualizadoEm: new Date().toISOString(), origem: 'sessao' },
  });
  await page.locator('#importar').setInputFiles({
    name: 'adulterado.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify(adulterado)),
  });
  await expect(page.locator('#erro-copia')).toContainText('Arquivo de backup inválido');
  expect(mensagens).toEqual([]); // nada de alert() do navegador
  await page.getByRole('link', { name: 'Início' }).click();
  await expect(page.locator('.lista-sessoes li', { hasText: codigo })).toContainText('Feita ✓');

  // Restaurar o backup bom: apaga tudo e importa; o registro continua lá.
  await abrirAjustes(page);
  await apagarTudoPelosAjustes(page);
  await expect(page.getByRole('heading', { name: 'Bem-vindo ao Semear' })).toBeVisible();
  await abrirAjustes(page);
  await page.locator('#importar').setInputFiles(arquivo);
  await confirmarTrazerCopia(page);
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await expect(page.locator('.lista-sessoes li', { hasText: codigo })).toContainText('Feita ✓');
  await page.locator('.lista-sessoes li', { hasText: codigo }).getByRole('link').click();
  await expect(page.locator('.reg-anotacoes')).toHaveText('Anotação do backup');
});

test('no celular, os controles do registro têm pelo menos 44 px', async ({ page }, info) => {
  test.skip(info.project.name !== 'celular', 'medida do celular');
  await explorar(page);
  await gerarSessaoDaAna(page);
  await page.getByRole('link', { name: 'Registrar', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Como foi a sessão?' })).toBeVisible();

  const alvos = page.locator(
    '.reg-opcao, .reg-engajamento label, .reg-acoes .botao, .reg-acoes button, #duracao',
  );
  const quantidade = await alvos.count();
  expect(quantidade).toBeGreaterThanOrEqual(10);
  for (let i = 0; i < quantidade; i++) {
    const caixa = await alvos.nth(i).boundingBox();
    expect(caixa, `alvo ${i}`).not.toBeNull();
    expect(caixa!.height, `altura do alvo ${i}`).toBeGreaterThanOrEqual(44);
  }
  // Sem rolagem horizontal na página.
  const largura = await page.evaluate(() => [
    document.documentElement.scrollWidth,
    document.documentElement.clientWidth,
  ]);
  expect(largura[0]).toBeLessThanOrEqual(largura[1]!);
});
