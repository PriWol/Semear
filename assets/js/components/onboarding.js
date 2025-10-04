// components/onboarding.js
import { AppStorage } from '../storage.js';
import DataLoader from '../data-loader.js';

class Onboarding {
  constructor(router) {
    this.router = router;
    this.dataLoader = new DataLoader();
    this.currentStep = 1;
    this.totalSteps = 4;
    this.formData = {
      parents: [],
      children: [],
      stylePreferences: [],
      valuesPriority: [],
      timePerWeekMin: 60
    };
  }

  async render() {
    const app = document.getElementById('app');
    
    app.innerHTML = `
      <div class="onboarding-container">
        <div class="onboarding-header">
          <h1>🌱 Bem-vindo ao Semear</h1>
          <div class="progress-bar">
            <div class="progress-fill" style="width: ${(this.currentStep / this.totalSteps) * 100}%"></div>
          </div>
          <p class="step-indicator">Passo ${this.currentStep} de ${this.totalSteps}</p>
        </div>
        
        <div class="onboarding-content" id="onboarding-step">
          ${await this.renderStep()}
        </div>
      </div>
    `;

    this.attachEventListeners();
  }

  async renderStep() {
    switch (this.currentStep) {
      case 1:
        return this.renderStep1();
      case 2:
        return await this.renderStep2();
      case 3:
        return await this.renderStep3();
      case 4:
        return this.renderStep4();
      default:
        return '';
    }
  }

  renderStep1() {
    return `
      <div class="step-content">
        <h2>Sobre sua família</h2>
        <p>Vamos começar conhecendo vocês!</p>
        
        <div class="form-group">
          <label>Nome dos pais/responsáveis (separe por vírgula)</label>
          <input type="text" id="parents" class="form-input" 
                 placeholder="Ex: Maria, João" 
                 value="${this.formData.parents.join(', ')}">
        </div>

        <div class="form-group">
          <label>Nome da criança</label>
          <input type="text" id="childName" class="form-input" 
                 placeholder="Ex: Ana" 
                 value="${this.formData.children[0]?.name || ''}">
        </div>

        <div class="form-group">
          <label>Data de nascimento da criança</label>
          <input type="date" id="childBirthdate" class="form-input" 
                 value="${this.formData.children[0]?.birthdate || ''}">
        </div>

        <div class="button-group">
          <button class="btn btn-primary" id="nextBtn">Próximo</button>
        </div>
      </div>
    `;
  }

  async renderStep2() {
    const values = await this.dataLoader.getValues();
    
    return `
      <div class="step-content">
        <h2>Valores que guiam sua família</h2>
        <p>Escolha até 3 valores prioritários para você</p>
        
        <div class="values-grid">
          ${values.map(v => `
            <div class="value-card ${this.formData.valuesPriority.includes(v.id) ? 'selected' : ''}" 
                 data-value="${v.id}">
              <h3>${v.name}</h3>
              <p>${v.description}</p>
            </div>
          `).join('')}
        </div>

        <div class="button-group">
          <button class="btn btn-secondary" id="backBtn">Voltar</button>
          <button class="btn btn-primary" id="nextBtn">Próximo</button>
        </div>
      </div>
    `;
  }

  async renderStep3() {
    const styles = ['Montessori', 'Waldorf', 'Clássico', 'Religioso'];
    const stylesInfo = {
      'Montessori': 'Autonomia, ambiente preparado, aprender fazendo',
      'Waldorf': 'Arte, ritmo, conexão com natureza e imaginação',
      'Clássico': 'Virtudes, grandes obras, tradição e excelência',
      'Religioso': 'Fé, valores espirituais, comunidade'
    };

    return `
      <div class="step-content">
        <h2>Estilo pedagógico</h2>
        <p>Escolha os estilos que mais ressoam com você (pode escolher vários)</p>
        
        <div class="styles-grid">
          ${styles.map(s => `
            <div class="style-card ${this.formData.stylePreferences.includes(s) ? 'selected' : ''}" 
                 data-style="${s}">
              <h3>${s}</h3>
              <p>${stylesInfo[s]}</p>
            </div>
          `).join('')}
        </div>

        <div class="form-group">
          <label>Quanto tempo você tem por semana? (minutos)</label>
          <input type="range" id="timeRange" class="form-range" 
                 min="30" max="300" step="15" 
                 value="${this.formData.timePerWeekMin}">
          <div class="range-value">${this.formData.timePerWeekMin} minutos</div>
        </div>

        <div class="button-group">
          <button class="btn btn-secondary" id="backBtn">Voltar</button>
          <button class="btn btn-primary" id="nextBtn">Próximo</button>
        </div>
      </div>
    `;
  }

  renderStep4() {
    return `
      <div class="step-content">
        <h2>Tudo pronto! 🎉</h2>
        <p>Vamos criar seu primeiro plano semanal personalizado</p>
        
        <div class="summary-card">
          <h3>Resumo do seu perfil</h3>
          <ul>
            <li><strong>Família:</strong> ${this.formData.parents.join(', ')}</li>
            <li><strong>Criança:</strong> ${this.formData.children[0]?.name}, ${this.dataLoader.calculateAge(this.formData.children[0]?.birthdate)} anos</li>
            <li><strong>Valores:</strong> ${this.formData.valuesPriority.length} selecionados</li>
            <li><strong>Estilos:</strong> ${this.formData.stylePreferences.join(', ')}</li>
            <li><strong>Tempo disponível:</strong> ${this.formData.timePerWeekMin} min/semana</li>
          </ul>
        </div>

        <div class="button-group">
          <button class="btn btn-secondary" id="backBtn">Voltar</button>
          <button class="btn btn-primary" id="finishBtn">Começar!</button>
        </div>
      </div>
    `;
  }

  attachEventListeners() {
    const nextBtn = document.getElementById('nextBtn');
    const backBtn = document.getElementById('backBtn');
    const finishBtn = document.getElementById('finishBtn');

    if (nextBtn) {
      nextBtn.addEventListener('click', () => this.handleNext());
    }

    if (backBtn) {
      backBtn.addEventListener('click', () => this.handleBack());
    }

    if (finishBtn) {
      finishBtn.addEventListener('click', () => this.handleFinish());
    }

    // Step 1 listeners
    const parentsInput = document.getElementById('parents');
    const childNameInput = document.getElementById('childName');
    const childBirthdateInput = document.getElementById('childBirthdate');

    if (parentsInput) {
      parentsInput.addEventListener('change', (e) => {
        this.formData.parents = e.target.value.split(',').map(p => p.trim()).filter(p => p);
      });
    }

    if (childNameInput) {
      childNameInput.addEventListener('change', (e) => {
        if (!this.formData.children[0]) {
          this.formData.children[0] = {};
        }
        this.formData.children[0].name = e.target.value;
      });
    }

    if (childBirthdateInput) {
      childBirthdateInput.addEventListener('change', (e) => {
        if (!this.formData.children[0]) {
          this.formData.children[0] = {};
        }
        this.formData.children[0].birthdate = e.target.value;
      });
    }

    // Step 2 listeners (values)
    document.querySelectorAll('.value-card').forEach(card => {
      card.addEventListener('click', () => {
        const valueId = card.dataset.value;
        const index = this.formData.valuesPriority.indexOf(valueId);
        
        if (index >= 0) {
          this.formData.valuesPriority.splice(index, 1);
          card.classList.remove('selected');
        } else if (this.formData.valuesPriority.length < 3) {
          this.formData.valuesPriority.push(valueId);
          card.classList.add('selected');
        } else {
          alert('Você pode escolher no máximo 3 valores');
        }
      });
    });

    // Step 3 listeners (styles)
    document.querySelectorAll('.style-card').forEach(card => {
      card.addEventListener('click', () => {
        const style = card.dataset.style;
        const index = this.formData.stylePreferences.indexOf(style);
        
        if (index >= 0) {
          this.formData.stylePreferences.splice(index, 1);
          card.classList.remove('selected');
        } else {
          this.formData.stylePreferences.push(style);
          card.classList.add('selected');
        }
      });
    });

    const timeRange = document.getElementById('timeRange');
    if (timeRange) {
      timeRange.addEventListener('input', (e) => {
        this.formData.timePerWeekMin = parseInt(e.target.value);
        document.querySelector('.range-value').textContent = `${this.formData.timePerWeekMin} minutos`;
      });
    }
  }

  async handleNext() {
    if (this.validateStep()) {
      this.currentStep++;
      await this.render();
    }
  }

  async handleBack() {
    this.currentStep--;
    await this.render();
  }

  validateStep() {
    switch (this.currentStep) {
      case 1:
        if (!this.formData.parents.length) {
          alert('Por favor, informe o nome dos pais/responsáveis');
          return false;
        }
        if (!this.formData.children[0]?.name) {
          alert('Por favor, informe o nome da criança');
          return false;
        }
        if (!this.formData.children[0]?.birthdate) {
          alert('Por favor, informe a data de nascimento da criança');
          return false;
        }
        // Calcular idade
        this.formData.children[0].ageYears = this.dataLoader.calculateAge(this.formData.children[0].birthdate);
        this.formData.children[0].id = AppStorage.generateId('crianca');
        return true;

      case 2:
        if (this.formData.valuesPriority.length === 0) {
          alert('Por favor, escolha pelo menos 1 valor');
          return false;
        }
        return true;

      case 3:
        if (this.formData.stylePreferences.length === 0) {
          alert('Por favor, escolha pelo menos 1 estilo pedagógico');
          return false;
        }
        return true;

      default:
        return true;
    }
  }

  handleFinish() {
    // Criar perfil completo
    const profile = {
      id: AppStorage.generateId('familia'),
      parents: this.formData.parents,
      children: this.formData.children,
      stylePreferences: this.formData.stylePreferences,
      valuesPriority: this.formData.valuesPriority,
      timePerWeekMin: this.formData.timePerWeekMin,
      communityLinks: {
        whatsapp: '',
        telegram: '',
        meetMonthly: ''
      },
      consents: {
        localStorage: true,
        metricsLocal: true
      },
      createdAt: new Date().toISOString()
    };

    // Salvar perfil
    AppStorage.setProfile(profile);

    // Log métrica
    AppStorage.logMetric('onboarding.completed', { profileId: profile.id });

    // Navegar para plano semanal
    this.router.navigate('/weekly-plan');
  }
}

export default Onboarding;
