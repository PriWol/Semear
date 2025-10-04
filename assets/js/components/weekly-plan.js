// components/weekly-plan.js
import { AppStorage } from '../storage.js';
import DataLoader from '../data-loader.js';

class WeeklyPlan {
  constructor(router) {
    this.router = router;
    this.dataLoader = new DataLoader();
    this.currentPlan = null;
    this.resources = null;
  }

  async render() {
    const profile = AppStorage.getProfile();
    
    if (!profile) {
      this.router.navigate('/onboarding');
      return;
    }

    this.resources = await this.dataLoader.getResources();
    const child = profile.children[0];
    
    // Buscar ou criar plano da semana atual
    this.currentPlan = AppStorage.getCurrentWeekPlan(child.id);
    
    if (!this.currentPlan) {
      this.currentPlan = await this.generateWeeklyPlan(profile, child);
      AppStorage.saveWeeklyPlan(this.currentPlan);
    }

    const app = document.getElementById('app');
    app.innerHTML = `
      <div class="weekly-plan-container">
        <div class="plan-header">
          <h1>📅 Plano da Semana</h1>
          <p class="child-name">Para ${child.name}</p>
          <p class="week-date">Semana de ${this.formatWeekDate(this.currentPlan.weekStartISO)}</p>
        </div>

        <div class="plan-content">
          ${await this.renderPlanCards()}
        </div>

        <div class="plan-checklist">
          <h2>✓ Checklist da Semana</h2>
          ${this.renderChecklist()}
        </div>

        <div class="plan-actions">
          <button class="btn btn-secondary" id="regenerateBtn">🔄 Gerar Novo Plano</button>
          <button class="btn btn-primary" id="savePlanBtn">💾 Salvar Progresso</button>
        </div>
      </div>
    `;

    this.attachEventListeners();
  }

  async generateWeeklyPlan(profile, child) {
    const ageRange = this.dataLoader.getAgeRange(child.ageYears);
    
    // Filtrar recursos baseado no perfil
    const filters = {
      ageRange,
      values: profile.valuesPriority,
      styles: profile.stylePreferences
    };

    // Selecionar recursos aleatórios de cada tipo
    const activity = this.selectRandom(
      this.dataLoader.filterResources(this.resources, { ...filters, type: 'activity' })
    );
    
    const story = this.selectRandom(
      this.dataLoader.filterResources(this.resources, { ...filters, type: 'story' })
    );
    
    const ritual = this.selectRandom(
      this.dataLoader.filterResources(this.resources, { ...filters, type: 'ritual' })
    );
    
    const song = this.selectRandom(
      this.dataLoader.filterResources(this.resources, { ...filters, type: 'song' })
    );
    
    const book = this.selectRandom(
      this.dataLoader.filterResources(this.resources, { ...filters, type: 'book' })
    );

    return {
      id: AppStorage.generateId('plano'),
      weekStartISO: AppStorage.getWeekStart(),
      childId: child.id,
      selections: {
        activityId: activity?.id || null,
        storyId: story?.id || null,
        ritualId: ritual?.id || null,
        songId: song?.id || null,
        bookId: book?.id || null
      },
      checklist: [
        { id: 'chk-atividade', label: 'Realizou a atividade', done: false },
        { id: 'chk-historia', label: 'Leu/contou a história', done: false },
        { id: 'chk-ritual', label: 'Fez o ritual', done: false },
        { id: 'chk-musica', label: 'Ouviu a música', done: false },
        { id: 'chk-livro', label: 'Leu o livro', done: false }
      ],
      notes: '',
      createdAt: new Date().toISOString()
    };
  }

  selectRandom(array) {
    if (!array || array.length === 0) return null;
    return array[Math.floor(Math.random() * array.length)];
  }

  async renderPlanCards() {
    const { selections } = this.currentPlan;
    const cards = [];

    // Atividade
    if (selections.activityId) {
      const activity = this.dataLoader.getResourceById(this.resources, selections.activityId);
      cards.push(this.renderResourceCard(activity, 'Atividade', '🎨'));
    }

    // História
    if (selections.storyId) {
      const story = this.dataLoader.getResourceById(this.resources, selections.storyId);
      cards.push(this.renderResourceCard(story, 'História', '📖'));
    }

    // Ritual
    if (selections.ritualId) {
      const ritual = this.dataLoader.getResourceById(this.resources, selections.ritualId);
      cards.push(this.renderResourceCard(ritual, 'Ritual', '🕯️'));
    }

    // Música
    if (selections.songId) {
      const song = this.dataLoader.getResourceById(this.resources, selections.songId);
      cards.push(this.renderResourceCard(song, 'Música', '🎵'));
    }

    // Livro
    if (selections.bookId) {
      const book = this.dataLoader.getResourceById(this.resources, selections.bookId);
      cards.push(this.renderResourceCard(book, 'Livro', '📚'));
    }

    return cards.join('');
  }

  renderResourceCard(resource, type, icon) {
    if (!resource) return '';

    const instructions = resource.instructions ? 
      `<div class="resource-instructions">
        <h4>Como fazer:</h4>
        <ol>
          ${resource.instructions.map(i => `<li>${i}</li>`).join('')}
        </ol>
      </div>` : '';

    const materials = resource.materials ?
      `<div class="resource-materials">
        <h4>Materiais:</h4>
        <ul>
          ${resource.materials.map(m => `<li>${m}</li>`).join('')}
        </ul>
      </div>` : '';

    const spotifyLink = resource.spotifyUrl ?
      `<a href="${resource.spotifyUrl}" target="_blank" class="btn btn-small">🎧 Ouvir no Spotify</a>` : '';

    const author = resource.author ? `<p class="resource-author">Por ${resource.author}</p>` : '';

    return `
      <div class="resource-card" data-resource-id="${resource.id}">
        <div class="resource-header">
          <span class="resource-icon">${icon}</span>
          <div>
            <span class="resource-type">${type}</span>
            <h3>${resource.title}</h3>
            ${author}
          </div>
        </div>
        
        <p class="resource-cultural">${resource.culturalNotes}</p>
        
        ${resource.summary ? `<p class="resource-summary">${resource.summary}</p>` : ''}
        ${resource.lyrics ? `<p class="resource-lyrics"><em>${resource.lyrics}</em></p>` : ''}
        
        ${instructions}
        ${materials}
        
        <div class="resource-meta">
          <span>⏱️ ${resource.durationMin} min</span>
          <span>👶 ${resource.ageRange} anos</span>
        </div>
        
        ${spotifyLink}
        
        <button class="btn btn-secondary btn-small swap-btn" data-type="${resource.type}">
          🔄 Trocar ${type}
        </button>
      </div>
    `;
  }

  renderChecklist() {
    return `
      <div class="checklist">
        ${this.currentPlan.checklist.map(item => `
          <label class="checklist-item">
            <input type="checkbox" 
                   data-check-id="${item.id}" 
                   ${item.done ? 'checked' : ''}>
            <span>${item.label}</span>
          </label>
        `).join('')}
      </div>
      
      <div class="plan-notes">
        <label>Notas da semana:</label>
        <textarea id="planNotes" class="form-textarea" 
                  placeholder="Como foi a semana? O que funcionou bem?">${this.currentPlan.notes || ''}</textarea>
      </div>
    `;
  }

  formatWeekDate(isoDate) {
    const date = new Date(isoDate);
    const options = { day: 'numeric', month: 'long' };
    return date.toLocaleDateString('pt-BR', options);
  }

  attachEventListeners() {
    // Checklist
    document.querySelectorAll('[data-check-id]').forEach(checkbox => {
      checkbox.addEventListener('change', (e) => {
        const checkId = e.target.dataset.checkId;
        const item = this.currentPlan.checklist.find(c => c.id === checkId);
        if (item) {
          item.done = e.target.checked;
          AppStorage.logMetric('checklist.toggle', { 
            checkId, 
            done: item.done 
          });
        }
      });
    });

    // Notas
    const notesTextarea = document.getElementById('planNotes');
    if (notesTextarea) {
      notesTextarea.addEventListener('change', (e) => {
        this.currentPlan.notes = e.target.value;
      });
    }

    // Salvar
    const saveBtn = document.getElementById('savePlanBtn');
    if (saveBtn) {
      saveBtn.addEventListener('click', () => {
        AppStorage.saveWeeklyPlan(this.currentPlan);
        AppStorage.logMetric('plan.saved', { planId: this.currentPlan.id });
        alert('✅ Progresso salvo!');
      });
    }

    // Regenerar
    const regenerateBtn = document.getElementById('regenerateBtn');
    if (regenerateBtn) {
      regenerateBtn.addEventListener('click', async () => {
        if (confirm('Deseja gerar um novo plano? O atual será substituído.')) {
          const profile = AppStorage.getProfile();
          const child = profile.children[0];
          this.currentPlan = await this.generateWeeklyPlan(profile, child);
          AppStorage.saveWeeklyPlan(this.currentPlan);
          AppStorage.logMetric('plan.regenerated', { planId: this.currentPlan.id });
          await this.render();
        }
      });
    }

    // Trocar recurso
    document.querySelectorAll('.swap-btn').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const type = e.target.dataset.type;
        await this.swapResource(type);
      });
    });
  }

  async swapResource(type) {
    const profile = AppStorage.getProfile();
    const child = profile.children[0];
    const ageRange = this.dataLoader.getAgeRange(child.ageYears);
    
    const filters = {
      type,
      ageRange,
      values: profile.valuesPriority,
      styles: profile.stylePreferences
    };

    const options = this.dataLoader.filterResources(this.resources, filters);
    const currentId = this.currentPlan.selections[`${type}Id`];
    
    // Filtrar opção atual
    const filtered = options.filter(r => r.id !== currentId);
    
    if (filtered.length === 0) {
      alert('Não há outras opções disponíveis para este tipo');
      return;
    }

    const newResource = this.selectRandom(filtered);
    const oldId = this.currentPlan.selections[`${type}Id`];
    this.currentPlan.selections[`${type}Id`] = newResource.id;
    
    AppStorage.saveWeeklyPlan(this.currentPlan);
    AppStorage.logMetric('plan.swapResource', { 
      type, 
      from: oldId, 
      to: newResource.id 
    });
    
    await this.render();
  }
}

export default WeeklyPlan;
