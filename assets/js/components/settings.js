// components/settings.js
import { AppStorage, Storage } from '../storage.js';
import Exporter from '../export.js';

class Settings {
  constructor(router) {
    this.router = router;
  }

  async render() {
    const profile = AppStorage.getProfile();
    
    const app = document.getElementById('app');
    app.innerHTML = `
      <div class="settings-container">
        <div class="settings-header">
          <h1>⚙️ Configurações</h1>
        </div>

        <div class="settings-content">
          ${profile ? this.renderProfileSettings(profile) : '<p>Nenhum perfil encontrado</p>'}
          ${this.renderDataManagement()}
          ${this.renderAbout()}
        </div>
      </div>
    `;

    this.attachEventListeners();
  }

  renderProfileSettings(profile) {
    return `
      <div class="settings-section">
        <h2>👨‍👩‍👧 Perfil da Família</h2>
        
        <div class="profile-info">
          <p><strong>Pais/Responsáveis:</strong> ${profile.parents.join(', ')}</p>
          <p><strong>Crianças:</strong></p>
          <ul>
            ${profile.children.map(c => `
              <li>${c.name} - ${c.ageYears} anos</li>
            `).join('')}
          </ul>
          <p><strong>Valores prioritários:</strong> ${profile.valuesPriority.length} selecionados</p>
          <p><strong>Estilos pedagógicos:</strong> ${profile.stylePreferences.join(', ')}</p>
          <p><strong>Tempo disponível:</strong> ${profile.timePerWeekMin} min/semana</p>
        </div>
        
        <button class="btn btn-secondary" id="editProfileBtn">✏️ Editar Perfil</button>
      </div>
    `;
  }

  renderDataManagement() {
    const metrics = AppStorage.getMetrics();
    const plans = AppStorage.getWeeklyPlans();
    const diaries = AppStorage.getDiaries();

    return `
      <div class="settings-section">
        <h2>💾 Gerenciamento de Dados</h2>
        
        <div class="data-stats">
          <p>📊 <strong>${metrics.length}</strong> eventos registrados</p>
          <p>📅 <strong>${plans.length}</strong> planos semanais</p>
          <p>📔 <strong>${diaries.length}</strong> diários</p>
        </div>
        
        <div class="data-actions">
          <button class="btn btn-primary" id="exportJSONBtn">📥 Exportar Dados (JSON)</button>
          <button class="btn btn-primary" id="exportCSVBtn">📊 Exportar Métricas (CSV)</button>
          <button class="btn btn-secondary" id="importJSONBtn">📤 Importar Dados (JSON)</button>
          <input type="file" id="importFileInput" accept=".json" style="display: none;">
        </div>
        
        <div class="data-warning">
          <h3>⚠️ Dados Locais</h3>
          <p>Todos os seus dados estão armazenados localmente no navegador. Faça backup regularmente!</p>
          <button class="btn btn-danger" id="clearDataBtn">🗑️ Limpar Todos os Dados</button>
        </div>
      </div>
    `;
  }

  renderAbout() {
    return `
      <div class="settings-section">
        <h2>ℹ️ Sobre o Semear</h2>
        
        <div class="about-content">
          <p><strong>Versão:</strong> 1.0.0 (MVP)</p>
          <p><strong>Missão:</strong> Empoderar famílias brasileiras a serem protagonistas na educação de seus filhos, com base em valores universais e cultura local.</p>
          
          <h3>🌱 Como funciona</h3>
          <ul>
            <li>100% gratuito e local (sem custos)</li>
            <li>Dados armazenados no seu navegador</li>
            <li>Conteúdo brasileiro + referências globais</li>
            <li>Personalizável para sua família</li>
          </ul>
          
          <h3>🤝 Contribua</h3>
          <p>O Semear é um projeto comunitário. Compartilhe recursos, participe dos encontros e ajude outras famílias!</p>
          
          <div class="about-links">
            <a href="https://github.com/semear-educacao" target="_blank" class="btn btn-secondary btn-small">
              GitHub
            </a>
            <a href="mailto:contato@semear.com.br" class="btn btn-secondary btn-small">
              Contato
            </a>
          </div>
        </div>
      </div>
    `;
  }

  attachEventListeners() {
    // Editar perfil
    const editProfileBtn = document.getElementById('editProfileBtn');
    if (editProfileBtn) {
      editProfileBtn.addEventListener('click', () => {
        if (confirm('Deseja refazer o onboarding? Seus dados atuais serão mantidos.')) {
          this.router.navigate('/onboarding');
        }
      });
    }

    // Exportar JSON
    const exportJSONBtn = document.getElementById('exportJSONBtn');
    if (exportJSONBtn) {
      exportJSONBtn.addEventListener('click', () => {
        const data = Storage.exportAll();
        Exporter.exportJSON(data, `semear-backup-${new Date().toISOString().split('T')[0]}.json`);
        AppStorage.logMetric('settings.exportJSON', {});
      });
    }

    // Exportar CSV
    const exportCSVBtn = document.getElementById('exportCSVBtn');
    if (exportCSVBtn) {
      exportCSVBtn.addEventListener('click', () => {
        const metrics = AppStorage.getMetrics();
        Exporter.exportMetricsCSV(metrics, `semear-metrics-${new Date().toISOString().split('T')[0]}.csv`);
        AppStorage.logMetric('settings.exportCSV', {});
      });
    }

    // Importar JSON
    const importJSONBtn = document.getElementById('importJSONBtn');
    const importFileInput = document.getElementById('importFileInput');
    
    if (importJSONBtn && importFileInput) {
      importJSONBtn.addEventListener('click', () => {
        importFileInput.click();
      });

      importFileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        try {
          const data = await Exporter.importJSON(file);
          if (confirm('Deseja importar estes dados? Os dados atuais serão substituídos.')) {
            Storage.importAll(data);
            AppStorage.logMetric('settings.importJSON', {});
            alert('✅ Dados importados com sucesso!');
            this.render();
          }
        } catch (error) {
          alert('❌ Erro ao importar dados: ' + error.message);
        }
      });
    }

    // Limpar dados
    const clearDataBtn = document.getElementById('clearDataBtn');
    if (clearDataBtn) {
      clearDataBtn.addEventListener('click', () => {
        if (confirm('⚠️ ATENÇÃO: Isso irá apagar TODOS os seus dados permanentemente. Deseja continuar?')) {
          if (confirm('Tem certeza? Esta ação não pode ser desfeita!')) {
            Storage.clear();
            AppStorage.logMetric('settings.clearData', {});
            alert('Dados limpos. Você será redirecionado para o início.');
            this.router.navigate('/');
          }
        }
      });
    }

    AppStorage.logMetric('settings.viewed', {});
  }
}

export default Settings;
