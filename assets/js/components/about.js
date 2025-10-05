// components/about.js - Página Institucional
class About {
  constructor(router) {
    this.router = router;
  }

  render() {
    const app = document.getElementById('app');
    
    app.innerHTML = `
      <div class="about-container">
        <div class="about-hero">
          <h1>🌱 Sobre o Semear</h1>
          <p class="about-tagline">Cultivando valores, colhendo memórias</p>
        </div>

        <div class="about-content">
          <section class="about-section">
            <h2>🎯 Nosso Objetivo</h2>
            <p>O Semear nasceu da necessidade de criar um espaço onde famílias brasileiras possam ser protagonistas na educação de seus filhos, integrando valores universais com a rica cultura do nosso país.</p>
            <p>Acreditamos que momentos de qualidade, intencionais e alinhados aos valores familiares, são a base para formar crianças felizes, conscientes e conectadas com suas raízes.</p>
          </section>

          <section class="about-section highlight">
            <h2>💚 Nossa Missão</h2>
            <p>Democratizar o acesso a uma educação de qualidade, oferecendo ferramentas práticas e gratuitas para que pais e mães ocupados possam:</p>
            <ul>
              <li>Criar momentos significativos com seus filhos (10-30 min/dia)</li>
              <li>Integrar valores universais no dia a dia</li>
              <li>Valorizar a cultura e identidade brasileira</li>
              <li>Aplicar pedagogias de qualidade (Montessori, Waldorf, Clássico, Religioso)</li>
              <li>Construir memórias afetivas duradouras</li>
            </ul>
          </section>

          <section class="about-section">
            <h2>👩‍👧‍👦 Quem Idealizou</h2>
            <div class="founder-card">
              <div class="founder-content">
                <h3>Priscila Wollmann</h3>
                <p class="founder-title">Idealizadora e Desenvolvedora</p>
                <p>Sou mãe, profissional e, acima de tudo, uma mulher que acredita que a educação dos filhos é uma das maiores responsabilidades e privilégios que temos.</p>
                <p>Como muitas mães brasileiras, vivo a realidade de equilibrar carreira, casa e o desejo profundo de estar presente na formação dos meus filhos. Sei o quanto é desafiador encontrar tempo e recursos para criar momentos educativos significativos.</p>
                <p>O Semear nasceu dessa vivência: da necessidade de ter um apoio prático, acessível e alinhado com nossos valores e cultura. Criei esta ferramenta pensando em você, que assim como eu, quer ser protagonista na educação dos seus filhos, mas precisa de um caminho mais claro e acessível.</p>
                <blockquote>
                  "Não precisamos ser perfeitas. Precisamos estar presentes, intencionais e conectadas com o que realmente importa: formar seres humanos íntegros, felizes e orgulhosos de suas raízes."
                </blockquote>
              </div>
            </div>
          </section>

          <section class="about-section">
            <h2>🇧🇷 Por Que Cultura Brasileira?</h2>
            <p>Vivemos em um mundo globalizado, mas nossas raízes são únicas e preciosas. O Semear valoriza:</p>
            <div class="culture-grid">
              <div class="culture-item">
                <span class="culture-icon">📖</span>
                <h4>Folclore</h4>
                <p>Saci, Iara, Curupira - histórias que formam nossa identidade</p>
              </div>
              <div class="culture-item">
                <span class="culture-icon">🎵</span>
                <h4>Música</h4>
                <p>Cantigas de roda que atravessam gerações</p>
              </div>
              <div class="culture-item">
                <span class="culture-icon">🎨</span>
                <h4>Arte</h4>
                <p>Expressões artísticas genuinamente brasileiras</p>
              </div>
              <div class="culture-item">
                <span class="culture-icon">🌿</span>
                <h4>Natureza</h4>
                <p>Conexão com nossa fauna e flora únicas</p>
              </div>
            </div>
          </section>

          <section class="about-section highlight">
            <h2>💡 Nossos Princípios</h2>
            <div class="principles-list">
              <div class="principle-item">
                <span class="principle-icon">🆓</span>
                <div>
                  <h4>100% Gratuito</h4>
                  <p>Educação de qualidade não deve ser privilégio. Sempre será gratuito.</p>
                </div>
              </div>
              <div class="principle-item">
                <span class="principle-icon">🔒</span>
                <div>
                  <h4>Privacidade Total</h4>
                  <p>Seus dados ficam no seu dispositivo. Sem rastreamento, sem venda de dados.</p>
                </div>
              </div>
              <div class="principle-item">
                <span class="principle-icon">🤝</span>
                <div>
                  <h4>Comunidade</h4>
                  <p>Crescemos juntos, compartilhando experiências e aprendizados.</p>
                </div>
              </div>
              <div class="principle-item">
                <span class="principle-icon">🌱</span>
                <div>
                  <h4>Simplicidade</h4>
                  <p>Ferramentas práticas para o dia a dia de famílias ocupadas.</p>
                </div>
              </div>
            </div>
          </section>

          <section class="about-section">
            <h2>🚀 Como Funciona</h2>
            <div class="how-it-works">
              <div class="step-card">
                <span class="step-number">1</span>
                <h4>Configure seu Perfil</h4>
                <p>Conte sobre sua família, valores e tempo disponível</p>
              </div>
              <div class="step-card">
                <span class="step-number">2</span>
                <h4>Receba seu Plano</h4>
                <p>Sugestões personalizadas de atividades, histórias e rituais</p>
              </div>
              <div class="step-card">
                <span class="step-number">3</span>
                <h4>Viva os Momentos</h4>
                <p>Dedique 10-30 min/dia para criar memórias</p>
              </div>
              <div class="step-card">
                <span class="step-number">4</span>
                <h4>Registre e Celebre</h4>
                <p>Documente momentos especiais no diário</p>
              </div>
            </div>
          </section>

          <section class="about-section cta-section">
            <h2>Junte-se a Nós!</h2>
            <p>Faça parte de uma comunidade de famílias que acreditam na educação com valores e identidade brasileira.</p>
            <div class="cta-buttons">
              <a href="/" class="btn btn-primary" data-link>Começar Agora</a>
              <a href="/community" class="btn btn-secondary" data-link>Conhecer a Comunidade</a>
            </div>
          </section>
        </div>
      </div>
    `;

    // Adicionar navegação aos links
    document.querySelectorAll('[data-link]').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        this.router.navigate(link.getAttribute('href'));
      });
    });
  }
}

export default About;
