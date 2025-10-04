// components/explorer.js
import { AppStorage } from '../storage.js';
import DataLoader from '../data-loader.js';

class Explorer {
  constructor(router) {
    this.router = router;
    this.dataLoader = new DataLoader();
    this.resources = null;
    this.values = null;
    this.filters = {
      type: '',
      ageRange: '',
      values: [],
      styles: [],
      format: ''
    };
  }

  async render() {
    const profile = AppStorage.getProfile();
    
    if (!profile) {
      this.router.navigate('/onboarding');
      return;
    }

    this.resources = await this.dataLoader.getResources();
    this.values = await this.dataLoader.getValues();

    const app = document.getElementById('app');
    app.innerHTML = `
      <div class="explorer-container">
        <div class="explorer-header">
          <h1>🔍 Explorar Recursos</h1>
          <p>Descubra atividades, histórias, rituais e mais</p>
        </div>

        <div class="explorer-filters">
          ${this.renderFilters()}
        </div>

        <div class="explorer-results">
          ${this.renderResults()}
        </div>
      </div>
    `;

    this.attachEventListeners();
  }

  renderFilters() {
    const types = ['activity', 'story', 'ritual', 'song', 'book'];
    const typeNames = {
      'activity': 'Atividades',
      'story': 'Histórias',
      'ritual': 'Rituais',
      'song': 'Músicas',
      'book': 'Livros'
    };

    const ageRanges = ['0-2', '3-6', '7-10', '10+'];
    const styles = ['Montessori', 'Waldorf', 'Clássico', 'Religioso'];

    return `
      <div class="filters-grid">
        <div class="filter-group">
          <label>Tipo</label>
          <select id="filterType" class="form-select">
            <option value="">Todos</option>
            ${types.map(t => `
              <option value="${t}" ${this.filters.type === t ? 'selected' : ''}>
                ${typeNames[t]}
              </option>
            `).join('')}
          </select>
        </div>

        <div class="filter-group">
          <label>Idade</label>
          <select id="filterAge" class="form-select">
            <option value="">Todas</option>
            ${ageRanges.map(a => `
              <option value="${a}" ${this.filters.ageRange === a ? 'selected' : ''}>
                ${a} anos
              </option>
            `).join('')}
          </select>
        </div>

        <div class="filter-group">
          <label>Valores</label>
          <div class="filter-chips">
            ${this.values.map(v => `
              <label class="chip ${this.filters.values.includes(v.id) ? 'selected' : ''}">
                <input type="checkbox" value="${v.id}" class="filter-value">
                ${v.name}
              </label>
            `).join('')}
          </div>
        </div>

        <div class="filter-group">
          <label>Estilos</label>
          <div class="filter-chips">
            ${styles.map(s => `
              <label class="chip ${this.filters.styles.includes(s) ? 'selected' : ''}">
                <input type="checkbox" value="${s}" class="filter-style">
                ${s}
              </label>
            `).join('')}
          </div>
        </div>

        <div class="filter-actions">
          <button class="btn btn-secondary btn-small" id="clearFilters">Limpar Filtros</button>
        </div>
      </div>
    `;
  }

  renderResults() {
    const filtered = this.dataLoader.filterResources(this.resources, this.filters);

    if (filtered.length === 0) {
      return `
        <div class="no-results">
          <p>😔 Nenhum recurso encontrado com esses filtros</p>
          <button class="btn btn-primary" id="clearFiltersBtn">Limpar Filtros</button>
        </div>
      `;
    }

    return `
      <div class="results-header">
        <p>${filtered.length} recurso(s) encontrado(s)</p>
      </div>
      <div class="resources-grid">
        ${filtered.map(r => this.renderResourceCard(r)).join('')}
      </div>
    `;
  }

  renderResourceCard(resource) {
    const typeIcons = {
      'activity': '🎨',
      'story': '📖',
      'ritual': '🕯️',
      'song': '🎵',
      'book': '📚'
    };

    const typeNames = {
      'activity': 'Atividade',
      'story': 'História',
      'ritual': 'Ritual',
      'song': 'Música',
      'book': 'Livro'
    };

    const valueNames = resource.values
      .map(vId => this.values.find(v => v.id === vId)?.name)
      .filter(Boolean)
      .join(', ');

    return `
      <div class="resource-card-compact" data-resource-id="${resource.id}">
        <div class="card-header">
          <span class="card-icon">${typeIcons[resource.type]}</span>
          <div>
            <span class="card-type">${typeNames[resource.type]}</span>
            <h3>${resource.title}</h3>
            ${resource.author ? `<p class="card-author">${resource.author}</p>` : ''}
          </div>
        </div>
        
        <p class="card-cultural">${resource.culturalNotes}</p>
        
        <div class="card-tags">
          ${resource.values.slice(0, 2).map(vId => {
            const val = this.values.find(v => v.id === vId);
            return val ? `<span class="tag">${val.name}</span>` : '';
          }).join('')}
        </div>
        
        <div class="card-meta">
          <span>⏱️ ${resource.durationMin} min</span>
          <span>👶 ${resource.ageRange} anos</span>
          <span>📐 ${resource.styles.join(', ')}</span>
        </div>
        
        <button class="btn btn-primary btn-small view-details-btn" data-resource-id="${resource.id}">
          Ver Detalhes
        </button>
      </div>
    `;
  }

  attachEventListeners() {
    // Filtro tipo
    const filterType = document.getElementById('filterType');
    if (filterType) {
      filterType.addEventListener('change', async (e) => {
        this.filters.type = e.target.value;
        await this.render();
      });
    }

    // Filtro idade
    const filterAge = document.getElementById('filterAge');
    if (filterAge) {
      filterAge.addEventListener('change', async (e) => {
        this.filters.ageRange = e.target.value;
        await this.render();
      });
    }

    // Filtro valores
    document.querySelectorAll('.filter-value').forEach(checkbox => {
      checkbox.addEventListener('change', async (e) => {
        const value = e.target.value;
        if (e.target.checked) {
          this.filters.values.push(value);
        } else {
          this.filters.values = this.filters.values.filter(v => v !== value);
        }
        await this.render();
      });
    });

    // Filtro estilos
    document.querySelectorAll('.filter-style').forEach(checkbox => {
      checkbox.addEventListener('change', async (e) => {
        const style = e.target.value;
        if (e.target.checked) {
          this.filters.styles.push(style);
        } else {
          this.filters.styles = this.filters.styles.filter(s => s !== style);
        }
        await this.render();
      });
    });

    // Limpar filtros
    const clearBtn = document.getElementById('clearFilters') || document.getElementById('clearFiltersBtn');
    if (clearBtn) {
      clearBtn.addEventListener('click', async () => {
        this.filters = {
          type: '',
          ageRange: '',
          values: [],
          styles: [],
          format: ''
        };
        await this.render();
      });
    }

    // Ver detalhes
    document.querySelectorAll('.view-details-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const resourceId = e.target.dataset.resourceId;
        this.showResourceDetails(resourceId);
      });
    });
  }

  showResourceDetails(resourceId) {
    const resource = this.dataLoader.getResourceById(this.resources, resourceId);
    if (!resource) return;

    const typeIcons = {
      'activity': '🎨',
      'story': '📖',
      'ritual': '🕯️',
      'song': '🎵',
      'book': '📚'
    };

    const instructions = resource.instructions ? 
      `<div class="detail-section">
        <h4>Como fazer:</h4>
        <ol>
          ${resource.instructions.map(i => `<li>${i}</li>`).join('')}
        </ol>
      </div>` : '';

    const materials = resource.materials ?
      `<div class="detail-section">
        <h4>Materiais necessários:</h4>
        <ul>
          ${resource.materials.map(m => `<li>${m}</li>`).join('')}
        </ul>
      </div>` : '';

    const summary = resource.summary ?
      `<div class="detail-section">
        <p>${resource.summary}</p>
      </div>` : '';

    const lyrics = resource.lyrics ?
      `<div class="detail-section">
        <h4>Letra:</h4>
        <p class="lyrics">${resource.lyrics}</p>
      </div>` : '';

    const spotifyLink = resource.spotifyUrl ?
      `<a href="${resource.spotifyUrl}" target="_blank" class="btn btn-primary">
        🎧 Ouvir no Spotify
      </a>` : '';

    // Criar modal
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <span class="modal-icon">${typeIcons[resource.type]}</span>
          <h2>${resource.title}</h2>
          <button class="modal-close">&times;</button>
        </div>
        
        <div class="modal-body">
          ${resource.author ? `<p class="modal-author">Por ${resource.author}</p>` : ''}
          
          <p class="modal-cultural"><strong>Contexto cultural:</strong> ${resource.culturalNotes}</p>
          
          ${summary}
          ${lyrics}
          ${instructions}
          ${materials}
          
          <div class="modal-meta">
            <span>⏱️ Duração: ${resource.durationMin} minutos</span>
            <span>👶 Idade: ${resource.ageRange} anos</span>
            <span>📐 Estilos: ${resource.styles.join(', ')}</span>
          </div>
          
          <div class="modal-values">
            <strong>Valores trabalhados:</strong>
            ${resource.values.map(vId => {
              const val = this.values.find(v => v.id === vId);
              return val ? `<span class="tag">${val.name}</span>` : '';
            }).join('')}
          </div>
          
          ${spotifyLink}
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    // Fechar modal
    const closeBtn = modal.querySelector('.modal-close');
    closeBtn.addEventListener('click', () => {
      document.body.removeChild(modal);
    });

    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        document.body.removeChild(modal);
      }
    });

    AppStorage.logMetric('resource.viewed', { resourceId });
  }
}

export default Explorer;
