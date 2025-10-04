// router.js - SPA Router simples
class Router {
  constructor() {
    this.routes = {};
    this.currentRoute = null;
    this.init();
  }

  init() {
    window.addEventListener('popstate', () => this.handleRoute());
    document.addEventListener('DOMContentLoaded', () => this.handleRoute());
    
    // Interceptar cliques em links internos
    document.addEventListener('click', (e) => {
      if (e.target.matches('[data-link]')) {
        e.preventDefault();
        this.navigate(e.target.getAttribute('href'));
      }
    });
  }

  register(path, handler) {
    this.routes[path] = handler;
  }

  navigate(path) {
    window.history.pushState({}, '', path);
    this.handleRoute();
  }

  handleRoute() {
    const path = window.location.pathname;
    this.currentRoute = path;

    // Encontrar rota correspondente
    const handler = this.routes[path] || this.routes['/'];
    
    if (handler) {
      handler();
    } else {
      this.show404();
    }

    // Atualizar navegação ativa
    this.updateActiveNav();
  }

  updateActiveNav() {
    document.querySelectorAll('[data-link]').forEach(link => {
      const href = link.getAttribute('href');
      if (href === this.currentRoute) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }

  show404() {
    const app = document.getElementById('app');
    if (app) {
      app.innerHTML = `
        <div class="error-page">
          <h1>404</h1>
          <p>Página não encontrada</p>
          <a href="/" data-link>Voltar ao início</a>
        </div>
      `;
    }
  }
}

export default Router;
