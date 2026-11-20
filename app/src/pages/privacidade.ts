import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';

/**
 * Política de privacidade do app como ele é hoje (CLAUDE.md, "Privacidade"; #25). Versão inicial,
 * sem revisão jurídica: precisa de advogado(a) antes de abrir cadastro e cobrança. Cada afirmação
 * aqui tem de ser verdadeira frente ao código (ver docs/GUIA_APRENDIZADO.md); se o app mudar
 * (conta, servidor, analytics, nova loja de dados), este texto muda junto. As seções de contato
 * ("Dúvidas") ficam de fora até a dona do produto definir um canal.
 */
export const paginaPrivacidade: FabricaPagina = async () => ({
  titulo: 'Privacidade',
  conteudo: html`
    <h1>Política de privacidade</h1>
    <p class="alerta" role="note">
      Versão inicial, ainda sem revisão jurídica. Escrevemos o que o app faz hoje, com as palavras
      mais simples que encontramos. Atualizada em novembro de 2026.
    </p>
    <section class="cartao">
      <h2>Em resumo</h2>
      <ul>
        <li>Tudo o que você cadastra e registra no Semear fica só no seu aparelho.</li>
        <li>
          Nós não temos servidor que receba esses dados. Não enviamos nada sobre a sua família para
          ninguém.
        </li>
        <li>O app não tem anúncios, análise de uso, rastreamento nem perfis.</li>
        <li>Você pode baixar tudo em um backup ou apagar tudo, quando quiser.</li>
      </ul>
    </section>
    <section class="cartao">
      <h2>O que fica no seu aparelho</h2>
      <p>
        Tudo o que você cadastra e registra no app fica guardado no armazenamento do navegador,
        <b>somente neste aparelho</b>. Por exemplo:
      </p>
      <ul>
        <li>seu nome como educador, as pedagogias de inspiração e os idiomas que você escolheu;</li>
        <li>
          o nome, a data de nascimento, a letra, a rotina (dias e duração) e as línguas de cada
          criança;
        </li>
        <li>em que ponto cada criança está na jornada, e o histórico dessas mudanças;</li>
        <li>
          as sessões que você gerou e os planos da semana, com o que você registra sobre elas: a
          duração, como a criança reagiu e as <b>anotações de texto livre</b> que você escrever;
        </li>
        <li>a preferência de lembrete diário (ativo, hora, se mostra o nome da criança);</li>
        <li>a data do seu último backup.</li>
      </ul>
      <p>
        Os dados ficam só neste navegador deste aparelho. Quem usa este aparelho e este navegador
        consegue abri-los: o app não tem senha. A família de exemplo traz dados fictícios, não de
        pessoas reais.
      </p>
    </section>
    <section class="cartao">
      <h2>O que não fazemos</h2>
      <ul>
        <li>Não enviamos os dados da sua família a servidor.</li>
        <li>Não usamos anúncios.</li>
        <li>Não usamos análise de uso nem rastreadores.</li>
        <li>Não montamos perfis de uso nem de pessoas para publicidade ou análise.</li>
        <li>Não pedimos conta, e-mail nem senha.</li>
      </ul>
    </section>
    <section class="cartao">
      <h2>O que sai do seu aparelho</h2>
      <p>
        O Semear é um site. Para ele abrir e funcionar, o aparelho precisa fazer alguns pedidos pela
        internet. Nenhum deles leva os dados da sua família.
      </p>
      <ul>
        <li>
          <b>Fontes de letra do Google (Google Fonts).</b> O app e o pacote de sessão pedem as
          letras ao Google. Como em qualquer site, o Google recebe o endereço de internet do
          aparelho, o tipo de navegador e o endereço do site que pediu as letras. Ele não recebe
          nomes, datas nem nada do que você cadastrou. O Google tem a própria política de
          privacidade.
        </li>
        <li>
          <b>Entrega do app.</b> O app é publicado no GitHub Pages. Como em qualquer site, quem
          hospeda pode registrar que o aparelho abriu a página. Nada do que você cadastrou vai
          junto.
        </li>
        <li>
          <b>Atualizações.</b> De tempos em tempos, o app confere se há uma versão nova. Esse pedido
          não leva dados seus.
        </li>
        <li>
          <b>Links que você toca.</b> Alguns botões, como os do Acervo gratuito, abrem sites de
          terceiros (por exemplo, bibliotecas digitais). Isso só acontece quando você toca. Aí você
          está no site deles, com as regras deles.
        </li>
      </ul>
      <p>Fora isso, o app não faz outras chamadas pela internet.</p>
    </section>
    <section class="cartao">
      <h2>Lembrete diário</h2>
      <p>
        É uma notificação gerada no próprio aparelho. Se você marcar “Mostrar o nome da criança no
        aviso”, o nome aparece na tela bloqueada. Desmarque se outras pessoas veem a tela.
      </p>
    </section>
    <section class="cartao">
      <h2>Pacote de sessão e impressão</h2>
      <p>
        O pacote é montado no seu aparelho. Ele foi configurado para não enviar nada para fora: ele
        carrega as letras do Google, mas bloqueia conexões, imagens e formulários externos. Se você
        imprimir ou salvar em PDF, o arquivo passa a ser seu. Guarde-o como guardaria qualquer papel
        com o nome da criança.
      </p>
      <p>
        O nome da criança aparece nas folhas e também no nome do arquivo baixado (por exemplo,
        semear-s01-ana.html). Guarde e compartilhe o arquivo com cuidado.
      </p>
    </section>
    <section class="cartao">
      <h2>Funcionar sem internet</h2>
      <p>
        O navegador guarda no aparelho uma cópia do app e da letra principal do app, para ele abrir
        sem internet. O pacote de sessão usa outras letras do Google. Sem internet, o pacote pode
        aparecer com as letras que o aparelho já tem. Essa cópia não tem os dados da sua família.
      </p>
    </section>
    <section class="cartao">
      <h2>Backup</h2>
      <p>
        Em <a href="#/config">Config.</a>, “Baixar backup” cria um arquivo com tudo o que você
        cadastrou e registrou. Atenção:
      </p>
      <ul>
        <li>
          o arquivo <b>não é criptografado</b>: ele mostra, em texto aberto, nomes, datas de
          nascimento, a jornada das crianças e as anotações que você escreveu nas sessões. Evite
          escrever nas anotações dados que você não quer ver no arquivo;
        </li>
        <li>quem guarda esse arquivo é você, no lugar que escolher. Nós não temos cópia;</li>
        <li>guarde em lugar seguro e não compartilhe com quem você não conhece;</li>
        <li>
          se você enviar o arquivo por e-mail ou guardar em nuvem, passa a valer a política desse
          serviço;
        </li>
        <li>
          “Restaurar backup” troca os dados do aparelho pelos do arquivo, depois de você confirmar.
        </li>
      </ul>
    </section>
    <section class="cartao">
      <h2>Apagar tudo</h2>
      <p>
        Em <a href="#/config">Config.</a>, no cartão “Apagar dados”, toque em “Apagar tudo” e
        confirme.
      </p>
      <ul>
        <li>
          O app apaga deste aparelho tudo o que você cadastrou e registrou: família, crianças,
          jornada e histórico, sessões, planos da semana e a data do último backup. Depois disso, o
          app volta à tela de boas-vindas.
        </li>
        <li>Não dá para desfazer. Baixe um backup antes, se quiser guardar.</li>
        <li>
          <b>Não</b> apaga: arquivos de backup que você já baixou, pacotes que você imprimiu ou
          salvou, e a cópia do app que o navegador guarda (ela não tem dados da sua família).
        </li>
        <li>
          Não apaga dados que estejam em outro aparelho ou em outro navegador. Em cada um, é preciso
          apagar separadamente.
        </li>
        <li>Como nunca recebemos os seus dados, não há nada guardado por nós para apagar.</li>
      </ul>
    </section>
    <section class="cartao">
      <h2>Seus dados, suas escolhas</h2>
      <ul>
        <li><b>Ver e levar com você:</b> baixe o backup quando quiser.</li>
        <li><b>Corrigir:</b> edite a família e as crianças no próprio app.</li>
        <li>
          <b>Apagar:</b> use “Apagar tudo”, ou toque em “Remover criança” na tela dela.
        </li>
      </ul>
    </section>
    <section class="cartao">
      <h2>Crianças</h2>
      <p>
        O Semear é para adultos que educam. A criança nunca usa o app. Quem cadastra, e decide o que
        registrar, é você. Os dados da criança não saem do aparelho.
      </p>
    </section>
    <section class="cartao">
      <h2>Cuidado com o aparelho</h2>
      <p>
        Como tudo fica no aparelho, limpar os dados do navegador, perder ou trocar de aparelho apaga
        tudo. Faça backup de vez em quando. O app avisa quando faz tempo.
      </p>
    </section>
    <section class="cartao">
      <h2>Se algo mudar</h2>
      <p>
        Se um dia o app passar a guardar dados fora do seu aparelho, esta página será atualizada
        antes disso e avisaremos aqui no app. Veja também os <a href="#/termos">Termos de uso</a>.
      </p>
    </section>
  `,
});
