// app.js - Aplicação principal
import Router from './router.js';
import { AppStorage } from './storage.js';
import Onboarding from './components/onboarding.js';
import WeeklyPlan from './components/weekly-plan.js';
import Explorer from './components/explorer.js';
import Guide from './components/guide.js';
import Community from './components/community.js';
import Diary from './components/diary.js';
import Settings from './components/settings.js';
import About from './components/about.js';

class App {
  constructor() {
    this.router = new Router();
    this.initRoutes();
    this.checkFirstAccess();
  }

  initRoutes() {
    // Home
    this.router.register('/', () => this.renderHome());
    
    // Onboarding
    this.router.register('/onboarding', () => {
      const onboarding = new Onboarding(this.router);
      onboarding.render();
    });

    // Plano Semanal
    this.router.register('/weekly-plan', () => {
      const weeklyPlan = new WeeklyPlan(this.router);
      weeklyPlan.render();
    });

    // Explorar
    this.router.register('/explorer', () => {
      const explorer = new Explorer(this.router);
      explorer.render();
    });

    // Guia
    this.router.register('/guide', () => {
      const guide = new Guide(this.router);
      guide.render();
    });

    // Comunidade
    this.router.register('/community', () => {
      const community = new Community(this.router);
      community.render();
    });

    // Diário
    this.router.register('/diary', () => {
      const diary = new Diary(this.router);
      diary.render();
    });

    // Configurações
    this.router.register('/settings', () => {
      const settings = new Settings(this.router);
      settings.render();
    });

    // Sobre
    this.router.register('/about', () => {
      const about = new About(this.router);
      about.render();
    });
  }

  checkFirstAccess() {
    const profile = AppStorage.getProfile();
    
    // Se não tem perfil e não está na página de onboarding, redirecionar
    if (!profile && window.location.pathname !== '/onboarding') {
      this.router.navigate('/onboarding');
    }
  }

  renderHome() {
    const profile = AppStorage.getProfile();
    
    if (!profile) {
      this.router.navigate('/onboarding');
      return;
    }

    const app = document.getElementById('app');
    const child = profile.children[0];
    const currentPlan = AppStorage.getCurrentWeekPlan(child.id);
    const currentDiary = AppStorage.getCurrentWeekDiary(child.id);

    const planProgress = currentPlan ? 
      currentPlan.checklist.filter(c => c.done).length / currentPlan.checklist.length * 100 : 0;

    app.innerHTML = `
      <div class="home-container">
        <div class="hero-section">
          <div class="hero-image">
            <img src="https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=1200&h=600&fit=crop" 
                 alt="Mãe e criança aprendendo juntos" 
                 onerror="this.style.display='none'">
          </div>
          <div class="hero-overlay"></div>
          <div class="hero-content">
            <h1 class="hero-title">Momentos de Qualidade que Formam Valores</h1>
            <p class="hero-subtitle">Atividades intencionais formadoras de valores que estejam alinhados aos da sua família, com identidade brasileira e pedagogia de qualidade.</p>
            <div class="hero-badges">
              <span class="badge">❤️ Baseado em Valores</span>
              <span class="badge">📖 Cultura Brasileira</span>
              <span class="badge">⏱️ 10-30 min/dia</span>
            </div>
          </div>
        </div>
        
        <div class="home-welcome">
          <p class="home-greeting">Olá, ${profile.parents[0]}! Vamos cultivar momentos especiais com ${child.name}? 🌱</p>
        </div>

        <div class="home-cards">
          <div class="home-card" data-link="/weekly-plan">
            <div class="card-icon">📅</div>
            <h2>Plano da Semana</h2>
            <p>Atividades personalizadas para esta semana</p>
            ${currentPlan ? `
              <div class="card-progress">
                <div class="progress-bar-small">
                  <div class="progress-fill" style="width: ${planProgress}%"></div>
                </div>
                <p>${Math.round(planProgress)}% completo</p>
              </div>
            ` : '<p class="card-cta">Criar primeiro plano →</p>'}
          </div>

          <div class="home-card" data-link="/explorer">
            <div class="card-icon">🔍</div>
            <h2>Explorar</h2>
            <p>Descubra atividades, histórias e rituais brasileiros</p>
          </div>

          <div class="home-card" data-link="/diary">
            <div class="card-icon">📔</div>
            <h2>Diário</h2>
            <p>Registre momentos especiais e progresso</p>
            ${currentDiary && currentDiary.moments.length > 0 ? `
              <p class="card-stat">✨ ${currentDiary.moments.length} momento(s) esta semana</p>
            ` : ''}
          </div>

          <div class="home-card" data-link="/guide">
            <div class="card-icon">📚</div>
            <h2>Guia Pedagógico</h2>
            <p>Entenda os estilos educacionais</p>
          </div>

          <div class="home-card" data-link="/community">
            <div class="card-icon">🤝</div>
            <h2>Comunidade</h2>
            <p>Conecte-se com outras famílias</p>
          </div>

          <div class="home-card" data-link="/settings">
            <div class="card-icon">⚙️</div>
            <h2>Configurações</h2>
            <p>Gerencie seu perfil e dados</p>
          </div>
        </div>

        <div class="home-tips">
          <h3>💡 Dica da Semana</h3>
          <p>Comece com pequenos rituais diários de 5-10 minutos. A consistência é mais importante que a duração!</p>
        </div>
      </div>
    `;

    // Adicionar navegação aos cards
    document.querySelectorAll('.home-card[data-link]').forEach(card => {
      card.addEventListener('click', () => {
        const link = card.getAttribute('data-link');
        this.router.navigate(link);
      });
    });

    AppStorage.logMetric('home.viewed', {});
  }
}

// Inicializar app quando DOM estiver pronto
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new App();
  });
} else {
  new App();
}

export default App;
