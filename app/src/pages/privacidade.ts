import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';

/**
 * Política de privacidade do app como ele é hoje (CLAUDE.md, "Privacidade"). É um rascunho sem
 * revisão jurídica (#25): precisa de advogado(a) antes de abrir cadastro e cobrança. Se o
 * comportamento do app mudar (conta, servidor, analytics), este texto muda junto.
 */
export const paginaPrivacidade: FabricaPagina = async () => ({
  titulo: 'Privacidade',
  conteudo: html`
    <h1>Política de privacidade</h1>
    <p class="alerta" role="note">
      Rascunho, ainda sem revisão jurídica. Descreve o que o app faz hoje.
    </p>
    <section class="cartao">
      <h2>O que fica no seu aparelho</h2>
      <p>
        O nome do educador, os nomes e as datas de nascimento das crianças, as posições na jornada,
        as sessões geradas e os backups ficam <b>somente neste aparelho</b>, no armazenamento do
        navegador. Nós não recebemos esses dados e não os enviamos a nenhum servidor.
      </p>
    </section>
    <section class="cartao">
      <h2>O que sai do aparelho</h2>
      <p>
        Só o carregamento das <b>fontes do Google</b> (Google Fonts), que não leva dados da sua
        família. Não usamos anúncios, análise de uso, rastreamento nem perfis.
      </p>
    </section>
    <section class="cartao">
      <h2>Seus direitos</h2>
      <ul>
        <li>
          <b>Exportar</b>: em <a href="#/config">Config.</a> você baixa um backup com tudo.
        </li>
        <li>
          <b>Apagar</b>: em <a href="#/config">Config.</a> você apaga todos os dados do aparelho
          com um toque. Sem os dados no nosso servidor, não há nada a apagar do nosso lado.
        </li>
        <li>
          <b>Crianças</b>: o cadastro é feito pelo responsável, que decide o que registrar. Os
          dados da criança nunca saem do aparelho.
        </li>
      </ul>
    </section>
    <section class="cartao">
      <h2>Cuidado com o aparelho e o backup</h2>
      <p>
        Como os dados ficam no aparelho, limpar os dados do navegador ou trocar de aparelho apaga
        tudo. Faça backup com frequência e guarde o arquivo em local seguro: ele contém os nomes e
        as datas de nascimento das crianças.
      </p>
    </section>
    <section class="cartao">
      <h2>Mudanças</h2>
      <p>
        Quando houver conta e assinatura, este texto será atualizado antes, dizendo o que passa a
        ser guardado e por quê.
      </p>
    </section>
  `,
});
