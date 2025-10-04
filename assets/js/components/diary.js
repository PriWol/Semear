// components/diary.js
import { AppStorage } from '../storage.js';
import DataLoader from '../data-loader.js';

class Diary {
  constructor(router) {
    this.router = router;
    this.dataLoader = new DataLoader();
    this.currentDiary = null;
  }

  async render() {
    const profile = AppStorage.getProfile();
    
    if (!profile) {
      this.router.navigate('/onboarding');
      return;
    }

    const child = profile.children[0];
    
    // Buscar ou criar diário da semana atual
    this.currentDiary = AppStorage.getCurrentWeekDiary(child.id);
    
    if (!this.currentDiary) {
      this.currentDiary = {
        id: AppStorage.generateId('diario'),
        weekStartISO: AppStorage.getWeekStart(),
        childId: child.id,
        moments: [],
        reflection: '',
        nextWeekFocus: '',
        createdAt: new Date().toISOString()
      };
      AppStorage.saveDiary(this.currentDiary);
    }

    const app = document.getElementById('app');
    app.innerHTML = `
      <div class="diary-container">
        <div class="diary-header">
          <h1>📔 Diário de Memórias</h1>
          <p class="child-name">Momentos especiais com ${child.name}</p>
          <p class="week-date">Semana de ${this.formatWeekDate(this.currentDiary.weekStartISO)}</p>
        </div>

        <div class="diary-content">
          ${this.renderProgress()}
          ${this.renderMoments()}
          ${this.renderReflection()}
        </div>

        <div class="diary-actions">
          <button class="btn btn-primary" id="addMomentBtn">➕ Adicionar Momento</button>
          <button class="btn btn-secondary" id="saveDiaryBtn">💾 Salvar Diário</button>
          <button class="btn btn-secondary" id="viewHistoryBtn">📚 Ver Histórico</button>
        </div>
      </div>
    `;

    this.attachEventListeners();
  }

  renderProgress() {
    const currentPlan = AppStorage.getCurrentWeekPlan(this.currentDiary.childId);
    
    if (!currentPlan) {
      return '<div class="progress-section"><p>Nenhum plano semanal encontrado</p></div>';
    }

    const completed = currentPlan.checklist.filter(c => c.done).length;
    const total = currentPlan.checklist.length;
    const percentage = total > 0 ? (completed / total) * 100 : 0;

    return `
      <div class="progress-section">
        <h2>📊 Progresso da Semana</h2>
        <div class="progress-bar-large">
          <div class="progress-fill" style="width: ${percentage}%"></div>
        </div>
        <p class="progress-text">${completed} de ${total} atividades completadas (${Math.round(percentage)}%)</p>
        
        <div class="progress-checklist">
          ${currentPlan.checklist.map(item => `
            <div class="progress-item ${item.done ? 'done' : ''}">
              <span>${item.done ? '✅' : '⬜'}</span>
              <span>${item.label}</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  renderMoments() {
    if (this.currentDiary.moments.length === 0) {
      return `
        <div class="moments-section">
          <h2>✨ Momentos Especiais</h2>
          <div class="no-moments">
            <p>Ainda não há momentos registrados esta semana</p>
            <p>Clique em "Adicionar Momento" para começar!</p>
          </div>
        </div>
      `;
    }

    return `
      <div class="moments-section">
        <h2>✨ Momentos Especiais</h2>
        <div class="moments-grid">
          ${this.currentDiary.moments.map(m => this.renderMomentCard(m)).join('')}
        </div>
      </div>
    `;
  }

  renderMomentCard(moment) {
    const stars = '⭐'.repeat(moment.rating);
    const tags = moment.tags.map(t => `<span class="tag">${t}</span>`).join('');

    return `
      <div class="moment-card" data-moment-id="${moment.id}">
        <div class="moment-header">
          <div class="moment-rating">${stars}</div>
          <button class="moment-delete" data-moment-id="${moment.id}">🗑️</button>
        </div>
        <p class="moment-text">${moment.text}</p>
        <div class="moment-tags">${tags}</div>
        <p class="moment-date">${this.formatDate(moment.createdAt)}</p>
      </div>
    `;
  }

  renderReflection() {
    return `
      <div class="reflection-section">
        <h2>💭 Reflexão da Semana</h2>
        
        <div class="form-group">
          <label>Como foi o ritmo da semana?</label>
          <textarea id="reflectionText" class="form-textarea" 
                    placeholder="O que funcionou bem? O que pode melhorar?">${this.currentDiary.reflection || ''}</textarea>
        </div>
        
        <div class="form-group">
          <label>Foco para a próxima semana</label>
          <textarea id="nextWeekText" class="form-textarea" 
                    placeholder="O que você quer explorar ou praticar mais?">${this.currentDiary.nextWeekFocus || ''}</textarea>
        </div>
      </div>
    `;
  }

  formatWeekDate(isoDate) {
    const date = new Date(isoDate);
    const options = { day: 'numeric', month: 'long' };
    return date.toLocaleDateString('pt-BR', options);
  }

  formatDate(isoDate) {
    const date = new Date(isoDate);
    const options = { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' };
    return date.toLocaleDateString('pt-BR', options);
  }

  attachEventListeners() {
    // Adicionar momento
    const addMomentBtn = document.getElementById('addMomentBtn');
    if (addMomentBtn) {
      addMomentBtn.addEventListener('click', () => {
        this.showAddMomentModal();
      });
    }

    // Salvar diário
    const saveDiaryBtn = document.getElementById('saveDiaryBtn');
    if (saveDiaryBtn) {
      saveDiaryBtn.addEventListener('click', () => {
        this.saveDiary();
      });
    }

    // Ver histórico
    const viewHistoryBtn = document.getElementById('viewHistoryBtn');
    if (viewHistoryBtn) {
      viewHistoryBtn.addEventListener('click', () => {
        this.showHistoryModal();
      });
    }

    // Deletar momento
    document.querySelectorAll('.moment-delete').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const momentId = e.target.dataset.momentId;
        if (confirm('Deseja remover este momento?')) {
          this.deleteMoment(momentId);
        }
      });
    });

    // Reflexão
    const reflectionText = document.getElementById('reflectionText');
    if (reflectionText) {
      reflectionText.addEventListener('change', (e) => {
        this.currentDiary.reflection = e.target.value;
      });
    }

    const nextWeekText = document.getElementById('nextWeekText');
    if (nextWeekText) {
      nextWeekText.addEventListener('change', (e) => {
        this.currentDiary.nextWeekFocus = e.target.value;
      });
    }
  }

  showAddMomentModal() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h2>✨ Adicionar Momento Especial</h2>
          <button class="modal-close">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label>Descreva o momento</label>
            <textarea id="momentText" class="form-textarea" 
                      placeholder="O que aconteceu? Como a criança reagiu?"
                      rows="4"></textarea>
          </div>
          
          <div class="form-group">
            <label>Avaliação (1-5 estrelas)</label>
            <div class="rating-input">
              ${[1, 2, 3, 4, 5].map(n => `
                <button class="star-btn" data-rating="${n}">⭐</button>
              `).join('')}
            </div>
            <input type="hidden" id="momentRating" value="5">
          </div>
          
          <div class="form-group">
            <label>Tags (separe por vírgula)</label>
            <input type="text" id="momentTags" class="form-input" 
                   placeholder="Ex: natureza, criatividade, paciência">
          </div>
          
          <button class="btn btn-primary" id="saveMomentBtn">Salvar Momento</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    // Rating interativo
    let selectedRating = 5;
    modal.querySelectorAll('.star-btn').forEach((btn, index) => {
      btn.addEventListener('click', () => {
        selectedRating = parseInt(btn.dataset.rating);
        document.getElementById('momentRating').value = selectedRating;
        
        // Atualizar visual
        modal.querySelectorAll('.star-btn').forEach((b, i) => {
          if (i < selectedRating) {
            b.classList.add('selected');
          } else {
            b.classList.remove('selected');
          }
        });
      });
    });

    // Inicializar com 5 estrelas
    modal.querySelectorAll('.star-btn').forEach(b => b.classList.add('selected'));

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

    // Salvar momento
    const saveMomentBtn = document.getElementById('saveMomentBtn');
    saveMomentBtn.addEventListener('click', () => {
      const text = document.getElementById('momentText').value;
      const rating = parseInt(document.getElementById('momentRating').value);
      const tagsInput = document.getElementById('momentTags').value;
      const tags = tagsInput.split(',').map(t => t.trim()).filter(t => t);

      if (!text) {
        alert('Por favor, descreva o momento');
        return;
      }

      const moment = {
        id: AppStorage.generateId('mom'),
        text,
        rating,
        tags,
        photoRef: '',
        createdAt: new Date().toISOString()
      };

      this.currentDiary.moments.push(moment);
      AppStorage.saveDiary(this.currentDiary);
      AppStorage.logMetric('diary.momentAdded', { momentId: moment.id, rating });

      document.body.removeChild(modal);
      this.render();
    });
  }

  deleteMoment(momentId) {
    this.currentDiary.moments = this.currentDiary.moments.filter(m => m.id !== momentId);
    AppStorage.saveDiary(this.currentDiary);
    AppStorage.logMetric('diary.momentDeleted', { momentId });
    this.render();
  }

  saveDiary() {
    AppStorage.saveDiary(this.currentDiary);
    AppStorage.logMetric('diary.saved', { diaryId: this.currentDiary.id });
    alert('✅ Diário salvo com sucesso!');
  }

  showHistoryModal() {
    const allDiaries = AppStorage.getDiaries();
    const childDiaries = allDiaries
      .filter(d => d.childId === this.currentDiary.childId)
      .sort((a, b) => new Date(b.weekStartISO) - new Date(a.weekStartISO));

    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
      <div class="modal-content modal-large">
        <div class="modal-header">
          <h2>📚 Histórico de Diários</h2>
          <button class="modal-close">&times;</button>
        </div>
        
        <div class="modal-body">
          ${childDiaries.length === 0 ? `
            <p>Nenhum diário anterior encontrado</p>
          ` : `
            <div class="history-list">
              ${childDiaries.map(d => `
                <div class="history-item">
                  <h3>Semana de ${this.formatWeekDate(d.weekStartISO)}</h3>
                  <p><strong>${d.moments.length}</strong> momento(s) registrado(s)</p>
                  ${d.reflection ? `<p class="history-reflection">${d.reflection}</p>` : ''}
                  <button class="btn btn-small btn-secondary view-diary-btn" data-diary-id="${d.id}">
                    Ver Detalhes
                  </button>
                </div>
              `).join('')}
            </div>
          `}
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

    // Ver detalhes de diário específico
    modal.querySelectorAll('.view-diary-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const diaryId = e.target.dataset.diaryId;
        const diary = allDiaries.find(d => d.id === diaryId);
        if (diary) {
          this.showDiaryDetails(diary);
        }
      });
    });

    AppStorage.logMetric('diary.historyViewed', {});
  }

  showDiaryDetails(diary) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h2>📔 Semana de ${this.formatWeekDate(diary.weekStartISO)}</h2>
          <button class="modal-close">&times;</button>
        </div>
        
        <div class="modal-body">
          <h3>✨ Momentos</h3>
          ${diary.moments.length === 0 ? '<p>Nenhum momento registrado</p>' : `
            <div class="moments-list">
              ${diary.moments.map(m => `
                <div class="moment-detail">
                  <div class="moment-rating">${'⭐'.repeat(m.rating)}</div>
                  <p>${m.text}</p>
                  <div class="moment-tags">
                    ${m.tags.map(t => `<span class="tag">${t}</span>`).join('')}
                  </div>
                </div>
              `).join('')}
            </div>
          `}
          
          ${diary.reflection ? `
            <h3>💭 Reflexão</h3>
            <p>${diary.reflection}</p>
          ` : ''}
          
          ${diary.nextWeekFocus ? `
            <h3>🎯 Foco para próxima semana</h3>
            <p>${diary.nextWeekFocus}</p>
          ` : ''}
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
  }
}

export default Diary;
