import { escolherAtividade } from './proposta';
import { expect, test, type Page } from '@playwright/test';

// Estórias #142 e #143: "Hoje com X" no Início (D19), "Tudo foi bem" (D10), resumo e Desfazer (D20),
// próximo passo depois de cadastrar (D21), linhas "em breve" recolhidas e caixas próprias no lugar do confirm().

const HOSTS_PERMITIDOS = ['fonts.googleapis.com', 'fonts.gstatic.com'];

async function explorar(page: Page) {
  await page.goto('./');
  await page.getByRole('button', { name: 'Explorar com uma família de exemplo' }).click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
}

const cartaoDeHoje = (page: Page) => page.locator('.crianca-cartao.hoje');

/** Gera uma sessão da Ana (a criança de hoje no exemplo) só com consciência fonológica. */
async function gerarSessaoDaAna(page: Page): Promise<string> {
  await cartaoDeHoje(page)
    .getByRole('link', { name: /^Mudar a sessão de Ana/ })
    .click();
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

test.describe('Início: "Hoje com X" (D19)', () => {
  test('prepara e abre a sessão em 2 toques, com a prévia antes de imprimir', async ({ page }) => {
    await explorar(page);
    const hoje = cartaoDeHoje(page);
    await expect(hoje.getByRole('heading', { name: 'Hoje com Ana' })).toBeVisible();
    // A sugestão já vem pronta e nada foi guardado: as 3 sessões do exemplo continuam 3.
    await expect(hoje.locator('.hoje-sugestao li').first()).toBeVisible();
    await expect(page.locator('.lista-sessoes li')).toHaveCount(3);
    // "Registrar" continua à vista no mesmo cartão; as outras crianças ficam abaixo.
    await expect(hoje.getByRole('link', { name: 'Registrar sessão de Ana' })).toBeVisible();
    await expect(page.locator('.crianca-cartao').nth(1)).toContainText('Theo');

    // Toque 1: já cai na página da sessão, com a prévia. Toque 2 (imprimir) fica à vista.
    await hoje.getByRole('button', { name: 'Preparar sessão de hoje' }).click();
    await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();
    await expect(page.locator('#previa')).toBeVisible();
    await expect(page.getByRole('button', { name: /Imprimir/ })).toBeVisible();

    await page.getByRole('link', { name: 'Início' }).click();
    await expect(page.locator('.lista-sessoes li')).toHaveCount(4);
  });

  test('a criança de hoje é a da sessão mais recente, não a mais velha', async ({ page }) => {
    await explorar(page);
    await expect(cartaoDeHoje(page)).toContainText('Ana'); // a sessão mais recente do exemplo é da Ana
    // O Theo (mais velho) ganha uma sessão nova: passa a ser a criança de hoje.
    await page.getByRole('link', { name: 'Preparar sessão de Theo' }).click();
    await page.getByRole('button', { name: 'Sugerir atividades' }).click();
    await page.getByRole('button', { name: 'Gerar pacote' }).click();
    await expect(page.getByRole('heading', { name: /Sessão S-/ })).toBeVisible();
    await page.getByRole('link', { name: 'Início' }).click();
    await expect(cartaoDeHoje(page).getByRole('heading', { name: 'Hoje com Theo' })).toBeVisible();
    await expect(page.locator('.crianca-cartao').nth(1)).toContainText('Ana');
  });
});

test.describe('Registro rápido: "Tudo foi bem" (D10)', () => {
  test('só preenche "Em desenvolvimento" como sugestão: não salva sozinho e respeita o que já foi marcado', async ({
    page,
  }) => {
    await explorar(page);
    const codigo = await gerarSessaoDaAna(page);
    await page.getByRole('link', { name: 'Registrar', exact: true }).click();
    await expect(page.locator('#contador-marcos')).toContainText('0 de 2 marcos marcados');

    // Uma resposta da pessoa vale mais que a sugestão.
    await grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }).check();
    await page.getByRole('button', { name: 'Tudo foi bem' }).click();
    await expect(page.locator('#contador-marcos')).toContainText('2 de 2 marcos marcados');
    await expect(
      grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }),
    ).toBeChecked();
    await expect(grupoDoMarco(page, 'LG.FON.03').getByLabel('Em desenvolvimento')).toBeChecked();
    // Nunca "Consolidado" em silêncio: só o que a pessoa marcou.
    await expect(page.locator('fieldset.reg-marco input[value=consolidado]:checked')).toHaveCount(
      1,
    );
    await expect(page.locator('#ajuda-tudo-bem')).toContainText('Preenchi');

    // Nada foi salvo: sair sem "Salvar" deixa a sessão por registrar.
    await page.getByRole('link', { name: 'Cancelar' }).click();
    await expect(page.locator('.lista-sessoes li', { hasText: codigo })).not.toContainText(
      'Feita ✓',
    );
  });

  test('sem nenhuma resposta, preenche todos e ainda dá para mudar cada um antes de salvar', async ({
    page,
  }) => {
    await explorar(page);
    await gerarSessaoDaAna(page);
    await page.getByRole('link', { name: 'Registrar', exact: true }).click();
    await page.getByRole('button', { name: 'Tudo foi bem' }).click();
    await expect(
      page.locator('fieldset.reg-marco input[value=em-desenvolvimento]:checked'),
    ).toHaveCount(2);
    await grupoDoMarco(page, 'LG.FON.03').getByLabel('Não observado', { exact: true }).check();
    await expect(page.locator('#contador-marcos')).toContainText('2 de 2 marcos marcados');
    await page.getByRole('button', { name: 'Salvar registro' }).click();
    await expect(page.getByRole('heading', { name: 'Sessão registrada' })).toBeVisible();
    await expect(page.locator('#resumo-observados')).toHaveText('2 marcos observados');
  });
});

test.describe('Resumo depois de registrar e Desfazer (D20)', () => {
  const marcoNaJornada = (page: Page, id: string) => page.locator(`li.marco[data-marco="${id}"]`);

  test('mostra "observados" (nunca "avançou"), não muda o estado e oferece Ver jornada e a próxima sessão', async ({
    page,
  }) => {
    await explorar(page);
    await gerarSessaoDaAna(page);
    await page.getByRole('link', { name: 'Registrar', exact: true }).click();
    await grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }).check();
    await page.getByRole('button', { name: 'Salvar registro' }).click();

    const resumo = page.locator('.resumo-registro');
    await expect(resumo.getByRole('heading', { name: 'Sessão registrada' })).toBeVisible();
    await expect(page.locator('#resumo-observados')).toHaveText('1 marco observado');
    await expect(resumo).not.toContainText(/avan/i);
    await expect(resumo).toContainText('O estado dos marcos na jornada não mudou');
    await expect(resumo.getByRole('link', { name: 'Preparar a próxima sessão' })).toBeVisible();

    await resumo.getByRole('link', { name: 'Ver jornada' }).click();
    await expect(
      marcoNaJornada(page, 'LG.FON.04').getByRole('button', { name: /Em desenvolvimento/ }),
    ).toHaveAttribute('aria-pressed', 'true');
  });

  test('Desfazer dentro da janela devolve a sessão a "por registrar" e some o registro', async ({
    page,
  }) => {
    await explorar(page);
    const codigo = await gerarSessaoDaAna(page);
    await page.getByRole('link', { name: 'Registrar', exact: true }).click();
    await grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }).check();
    await page.getByRole('button', { name: 'Salvar registro' }).click();
    await expect(page.getByRole('heading', { name: 'Sessão registrada' })).toBeVisible();

    await page.getByRole('button', { name: /Desfazer este registro/ }).click();
    // Volta à ficha, sem nada marcado, e a sessão continua sem registro.
    await expect(page.getByRole('heading', { name: 'Como foi a sessão?' })).toBeVisible();
    await expect(page.locator('fieldset.reg-marco input[type=radio]:checked')).toHaveCount(0);
    await expect(page.locator('.reg-aviso')).toHaveCount(0);
    await page.getByRole('link', { name: 'Cancelar' }).click();
    await expect(page.locator('.lista-sessoes li', { hasText: codigo })).not.toContainText(
      'Feita ✓',
    );
  });

  test('passados 10 s o Desfazer some e o registro vale', async ({ page }) => {
    await page.clock.install();
    await explorar(page);
    const codigo = await gerarSessaoDaAna(page);
    await page.getByRole('link', { name: 'Registrar', exact: true }).click();
    await grupoDoMarco(page, 'LG.FON.04').getByLabel('Consolidado', { exact: true }).check();
    await page.getByRole('button', { name: 'Salvar registro' }).click();
    await expect(page.getByRole('button', { name: /Desfazer este registro/ })).toBeVisible();
    await page.getByRole('button', { name: /Desfazer este registro/ }).focus();
    await page.clock.fastForward(11_000);
    await expect(page.getByRole('button', { name: /Desfazer este registro/ })).toHaveCount(0);
    // quem estava no botão não perde o foco: vai para o título, e o fim do prazo é anunciado
    await expect(page.locator('#titulo-resumo')).toBeFocused();
    await expect(page.locator('#aviso-texto')).toContainText('O prazo para desfazer terminou');
    await page.getByRole('link', { name: 'Voltar ao início' }).click();
    await expect(page.locator('.lista-sessoes li', { hasText: codigo })).toContainText('Feita ✓');
  });
});

test.describe('Cadastro: próximo passo (D21)', () => {
  async function cadastrarBia(page: Page) {
    await explorar(page);
    await page.goto('./#/crianca/nova');
    await page.getByLabel('Nome').fill('Bia');
    await page.getByLabel('Data de nascimento').fill(`${new Date().getFullYear() - 5}-03-15`);
    await page.getByRole('button', { name: 'Salvar' }).click();
  }

  test('depois de salvar, "Pronto, Bia está cadastrada" com três caminhos', async ({ page }) => {
    await cadastrarBia(page);
    await expect(page.getByRole('heading', { name: 'Pronto, Bia está cadastrada' })).toBeVisible();
    const alturas = await page.evaluate(() => document.documentElement.scrollHeight);
    expect(alturas).toBeLessThan(1400); // curta: nada de jornada de 9.700 px
    await expect(page.getByRole('link', { name: 'Preparar a primeira sessão' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Onde Bia está hoje (10 min)' })).toHaveAttribute(
      'href',
      /#\/sondagem\//,
    );
    await expect(page.getByRole('link', { name: 'Ver jornada' })).toHaveAttribute(
      'href',
      /#\/jornada\//,
    );
    await page.getByRole('link', { name: 'Preparar a primeira sessão' }).click();
    await expect(page.getByRole('heading', { name: 'Preparar sessão' })).toBeVisible();
    await expect(page.locator('select[name=crianca]')).toHaveValue(/.+/);
    await expect(page.locator('select[name=crianca] option:checked')).toHaveText('Bia');
  });

  test('"Onde Bia está hoje" leva à sondagem', async ({ page }) => {
    await cadastrarBia(page);
    await page.getByRole('link', { name: 'Onde Bia está hoje (10 min)' }).click();
    await expect(page.getByRole('heading', { name: /Sondagem/ })).toBeVisible();
  });
});

test('jornada: as linhas "em breve" ficam recolhidas, com a contagem, e não são apagadas', async ({
  page,
}) => {
  await explorar(page);
  await page.goto('./#/jornada/exemplo-ana');
  const bloco = page.locator('details.linhas-em-breve');
  await expect(bloco).toHaveCount(1);
  await expect(bloco.locator('summary')).toHaveText(/^\s*\d+ linhas? em breve\s*$/);
  await expect(bloco).not.toHaveAttribute('open', '');
  const emBreve = bloco.locator('section.linha');
  expect(await emBreve.count()).toBeGreaterThan(0);
  await expect(emBreve.first()).toBeHidden();
  // Fora do bloco só ficam linhas com marcos.
  await expect(page.locator('section.linha:not(details *)').first()).toBeVisible();
  await expect(page.locator('section.linha:not(details *)', { hasText: 'em breve' })).toHaveCount(
    0,
  );
  await bloco.locator('summary').click();
  await expect(emBreve.first()).toBeVisible();
  await expect(emBreve.first()).toContainText('Conteúdo desta linha em breve');
});

test('Remover criança: caixa própria com "Guardar uma cópia antes", sem confirm() nativo', async ({
  page,
}) => {
  const nativos: string[] = [];
  page.on('dialog', (d) => {
    nativos.push(d.message());
    void d.dismiss();
  });
  await explorar(page);
  await page.getByRole('link', { name: 'Editar Theo', exact: true }).click();
  await page.getByRole('button', { name: 'Remover criança' }).click();
  const caixa = page.getByRole('dialog', { name: 'Remover Theo?' });
  await expect(caixa).toBeVisible();
  await expect(caixa).toContainText('Isso não pode ser desfeito');

  // Guardar a cópia mantém a caixa aberta.
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    caixa.getByRole('button', { name: 'Guardar uma cópia antes' }).click(),
  ]);
  expect(download.suggestedFilename()).toMatch(/^semear-backup-\d{4}-\d{2}-\d{2}\.json$/);
  await expect(caixa).toContainText('Cópia guardada');

  // "Manter" não remove nada.
  await caixa.getByRole('button', { name: 'Manter Theo' }).click();
  await expect(caixa).toHaveCount(0);
  await page.goto('./#/');
  await expect(page.locator('.crianca-cartao')).toHaveCount(2);

  // Remover de verdade.
  await page.getByRole('link', { name: 'Editar Theo', exact: true }).click();
  await page.getByRole('button', { name: 'Remover criança' }).click();
  await page
    .getByRole('dialog', { name: 'Remover Theo?' })
    .getByRole('button', { name: 'Remover Theo' })
    .click();
  await expect(page.getByRole('heading', { name: 'Olá, Marina!' })).toBeVisible();
  await expect(page.locator('.crianca-cartao')).toHaveCount(1);
  expect(nativos).toEqual([]);
});

for (const largura of [320, 390]) {
  test(`${largura} px: Início, registro, resumo e próximo passo sem rolagem lateral e sem rede externa`, async ({
    page,
  }) => {
    const externos: string[] = [];
    page.on('request', (r) => {
      const url = new URL(r.url());
      const interno =
        url.origin === 'http://localhost:4173' || ['data:', 'blob:'].includes(url.protocol);
      if (!interno && !HOSTS_PERMITIDOS.includes(url.hostname)) externos.push(r.url());
    });
    await page.setViewportSize({ width: largura, height: 800 });
    const semRolagem = async (tela: string) => {
      const [rolagem, visivel] = await page.evaluate(() => [
        document.documentElement.scrollWidth,
        document.documentElement.clientWidth,
      ]);
      expect(rolagem, `${tela} em ${largura} px`).toBeLessThanOrEqual(visivel!);
    };

    await explorar(page);
    await semRolagem('Início');
    await gerarSessaoDaAna(page);
    await page.getByRole('link', { name: 'Registrar', exact: true }).click();
    await page.getByRole('button', { name: 'Tudo foi bem' }).click();
    await semRolagem('Registro');
    await page.getByRole('button', { name: 'Salvar registro' }).click();
    await expect(page.getByRole('heading', { name: 'Sessão registrada' })).toBeVisible();
    await semRolagem('Resumo');

    await page.goto('./#/crianca/nova');
    await page.getByLabel('Nome').fill('Bia');
    await page.getByLabel('Data de nascimento').fill(`${new Date().getFullYear() - 5}-03-15`);
    await page.getByRole('button', { name: 'Salvar' }).click();
    await expect(page.getByRole('heading', { name: 'Pronto, Bia está cadastrada' })).toBeVisible();
    await semRolagem('Próximo passo');
    await page.getByRole('link', { name: 'Ver jornada' }).click();
    await semRolagem('Jornada');
    expect(externos).toEqual([]);
  });
}
