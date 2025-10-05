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
    // Adicionar base path se necessário para GitHub Pages
    const basePath = window.location.pathname.includes('/Semear/') ? '/Semear' : '';
    const fullPath = basePath + path;
    window.history.pushState({}, '', fullPath);
    this.handleRoute();
  }

  handleRoute() {
    let path = window.location.pathname;
    
    // Remover /Semear/ do path se existir (GitHub Pages)
    const basePath = '/Semear';
    if (path.startsWith(basePath)) {
      path = path.substring(basePath.length) || '/';
    }
    
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
