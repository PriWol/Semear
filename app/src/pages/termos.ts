import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';

/**
 * Termos de uso do app gratuito, local e sem conta (#25). Versão inicial, sem revisão jurídica.
 * Não promete preço, plano nem prazo; só diz que haverá aviso prévio antes de qualquer cobrança.
 * Ficam de fora, até a dona do produto decidir com apoio jurídico: garantias, responsável pelo
 * serviço, contato, lei e foro.
 */
export const paginaTermos: FabricaPagina = async () => ({
  titulo: 'Termos de uso',
  conteudo: html`
    <h1>Termos de uso</h1>
    <p class="alerta" role="note">
      Versão inicial, ainda sem revisão jurídica. Estes termos são curtos de propósito. Atualizados
      em novembro de 2026.
    </p>
    <section class="cartao">
      <h2>O que é o Semear</h2>
      <p>
        O Semear é um app para famílias que educam em casa (homeschooling e afterschooling). Ele
        ajuda você a acompanhar a jornada de aprendizado de crianças de 2 a 8 anos e a gerar pacotes
        de sessão, para imprimir ou abrir no tablet.
      </p>
    </section>
    <section class="cartao">
      <h2>Para quem é</h2>
      <p>Para adultos: pais, mães e outros educadores. <b>A criança nunca usa o app.</b></p>
    </section>
    <section class="cartao">
      <h2>Gratuito por ora</h2>
      <p>
        Hoje o Semear é gratuito e não pede conta. Isso pode mudar no futuro. Se algum dia houver
        cobrança, avisaremos antes, aqui no app. Você decide se quer continuar. Nada será cobrado
        sem esse aviso.
      </p>
    </section>
    <section class="cartao">
      <h2>Seus dados ficam com você</h2>
      <p>
        Tudo o que você cadastra e registra fica só no seu aparelho. Não temos servidor que receba
        esses dados. Os detalhes estão na <a href="#/privacidade">Política de privacidade</a>.
      </p>
    </section>
    <section class="cartao">
      <h2>Backup e guarda do aparelho</h2>
      <p>
        Como os dados ficam no seu aparelho, a guarda deles é sua. Se você limpar o navegador,
        perder o aparelho ou trocar de aparelho sem backup, os dados somem e não temos como
        recuperar. Baixe um backup de vez em quando e guarde em lugar seguro. O arquivo não é
        criptografado e mostra nomes e datas de nascimento das crianças.
      </p>
    </section>
    <section class="cartao">
      <h2>Fontes do Google e links</h2>
      <p>
        O app só chama a internet para entregar o próprio app (GitHub Pages) e para carregar as
        letras do Google. Isso não leva os dados da sua família. Alguns botões (como os do Acervo
        gratuito) abrem sites de terceiros quando você toca. Esses sites têm regras próprias, e não
        respondemos por eles.
      </p>
    </section>
    <section class="cartao">
      <h2>O conteúdo é apoio</h2>
      <p>
        As atividades, os marcos da jornada, o acervo e <i>O Grande Tesouro de Marina</i> são
        material de apoio para a sua família. Cada criança tem o seu ritmo. Eles
        <b>não substituem</b> orientação profissional: pedagógica, médica ou jurídica. Se algo na
        criança preocupar você (fala, movimento, atenção, emoções, comportamento), procure um
        profissional. As indicações de “sinais de atenção” no app são lembretes, não diagnóstico.
      </p>
    </section>
    <section class="cartao">
      <h2>O app não é aconselhamento jurídico</h2>
      <p>
        As regras sobre educação domiciliar variam e podem mudar. O Semear não dá orientação
        jurídica sobre isso. Para saber o que vale no seu caso, consulte um(a) advogado(a) ou uma
        associação de educação domiciliar.
      </p>
    </section>
    <section class="cartao">
      <h2>Como apagar tudo</h2>
      <p>
        Em <a href="#/config">Config.</a>, no cartão “Apagar dados”, toque em “Apagar tudo” e
        confirme. Isso apaga deste aparelho tudo o que você cadastrou e registrou, e não dá para
        desfazer. Os detalhes estão na <a href="#/privacidade">Política de privacidade</a>.
      </p>
    </section>
    <section class="cartao">
      <h2>Mudanças nestes termos</h2>
      <p>
        Podemos atualizar estes termos. Quando mudar algo que afete você, avisaremos aqui no app.
      </p>
    </section>
  `,
});
