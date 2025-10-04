// components/community.js
import { AppStorage } from '../storage.js';

class Community {
  constructor(router) {
    this.router = router;
  }

  async render() {
    const profile = AppStorage.getProfile();
    
    const app = document.getElementById('app');
    app.innerHTML = `
      <div class="community-container">
        <div class="community-header">
          <h1>🤝 Comunidade Semear</h1>
          <p>Conecte-se com outras famílias e participe dos encontros</p>
        </div>

        <div class="community-content">
          ${this.renderCommunityLinks(profile)}
          ${this.renderMonthlyMeet()}
          ${this.renderResources()}
        </div>
      </div>
    `;

    this.attachEventListeners();
  }

  renderCommunityLinks(profile) {
    const hasLinks = profile?.communityLinks?.whatsapp || profile?.communityLinks?.telegram;

    return `
      <div class="community-section">
        <h2>💬 Grupos de Conversa</h2>
        <p>Participe dos grupos para trocar experiências, tirar dúvidas e compartilhar momentos especiais.</p>
        
        ${hasLinks ? `
          <div class="community-links">
            ${profile.communityLinks.whatsapp ? `
              <a href="${profile.communityLinks.whatsapp}" target="_blank" class="btn btn-primary">
                <span>📱</span> Grupo WhatsApp
              </a>
            ` : ''}
            
            ${profile.communityLinks.telegram ? `
              <a href="${profile.communityLinks.telegram}" target="_blank" class="btn btn-primary">
                <span>✈️</span> Grupo Telegram
              </a>
            ` : ''}
          </div>
        ` : `
          <div class="community-placeholder">
            <p>🚧 Em breve você poderá se conectar com outras famílias!</p>
            <p>Por enquanto, você pode criar seu próprio grupo e adicionar o link nas configurações.</p>
            <button class="btn btn-secondary" id="addLinksBtn">Adicionar Links</button>
          </div>
        `}
        
        <div class="community-guidelines">
          <h3>📋 Diretrizes da Comunidade</h3>
          <ul>
            <li><strong>Respeito:</strong> Acolha diferentes estilos e escolhas familiares</li>
            <li><strong>Partilha:</strong> Compartilhe experiências, dúvidas e aprendizados</li>
            <li><strong>Apoio mútuo:</strong> Ajude outras famílias com dicas e encorajamento</li>
            <li><strong>Privacidade:</strong> Não compartilhe fotos ou informações de outras famílias sem permissão</li>
            <li><strong>Foco:</strong> Mantenha conversas relacionadas à educação e valores familiares</li>
          </ul>
        </div>
      </div>
    `;
  }

  renderMonthlyMeet() {
    const profile = AppStorage.getProfile();
    const hasMeetLink = profile?.communityLinks?.meetMonthly;

    return `
      <div class="community-section highlight">
        <h2>📅 Encontro Mensal</h2>
        <p>Toda primeira segunda-feira do mês, às 20h (horário de Brasília)</p>
        
        <div class="meet-details">
          <h3>Como funciona?</h3>
          <ul>
            <li><strong>20h - 20h20:</strong> Partilha de experiências da semana</li>
            <li><strong>20h20 - 20h40:</strong> Prática guiada (ritual, música ou atividade)</li>
            <li><strong>20h40 - 21h:</strong> Perguntas e respostas</li>
          </ul>
        </div>
        
        ${hasMeetLink ? `
          <a href="${profile.communityLinks.meetMonthly}" target="_blank" class="btn btn-primary btn-large">
            🎥 Entrar no Encontro (Google Meet)
          </a>
        ` : `
          <div class="meet-placeholder">
            <p>🚧 Link do próximo encontro será divulgado em breve!</p>
            <p>Enquanto isso, você pode criar seu próprio link de Google Meet e adicionar nas configurações.</p>
            <button class="btn btn-secondary" id="addMeetLinkBtn">Adicionar Link do Meet</button>
          </div>
        `}
      </div>
    `;
  }

  renderResources() {
    return `
      <div class="community-section">
        <h2>📚 Recursos Comunitários</h2>
        
        <div class="resources-grid">
          <div class="resource-item">
            <h3>🎬 Conteúdo no Instagram</h3>
            <p>Siga @semear.educacao para dicas diárias, atividades rápidas e inspiração</p>
            <a href="#" class="btn btn-secondary btn-small" target="_blank">Seguir</a>
          </div>
          
          <div class="resource-item">
            <h3>📖 Biblioteca Comunitária</h3>
            <p>Lista colaborativa de livros brasileiros recomendados por famílias</p>
            <button class="btn btn-secondary btn-small" id="viewLibraryBtn">Ver Lista</button>
          </div>
          
          <div class="resource-item">
            <h3>🎵 Playlist Spotify</h3>
            <p>Cantigas brasileiras, músicas infantis e trilhas para atividades</p>
            <a href="https://open.spotify.com/playlist/exemplo" class="btn btn-secondary btn-small" target="_blank">Ouvir</a>
          </div>
          
          <div class="resource-item">
            <h3>🤝 Parcerias Locais</h3>
            <p>Encontre bibliotecas, espaços culturais e grupos na sua região</p>
            <button class="btn btn-secondary btn-small" id="viewPartnersBtn">Ver Mapa</button>
          </div>
        </div>
      </div>
      
      <div class="community-section">
        <h2>💡 Como Contribuir</h2>
        <p>A comunidade Semear cresce com a participação de cada família!</p>
        
        <div class="contribution-ideas">
          <div class="idea-card">
            <h3>📝 Compartilhe Recursos</h3>
            <p>Encontrou uma atividade, história ou ritual que funcionou bem? Compartilhe no grupo!</p>
          </div>
          
          <div class="idea-card">
            <h3>🎨 Organize Encontros Locais</h3>
            <p>Reúna famílias da sua região para atividades presenciais em parques ou bibliotecas</p>
          </div>
          
          <div class="idea-card">
            <h3>🌟 Indique para Amigos</h3>
            <p>Convide outras famílias que se identificam com educação baseada em valores</p>
          </div>
        </div>
      </div>
    `;
  }

  attachEventListeners() {
    // Adicionar links
    const addLinksBtn = document.getElementById('addLinksBtn');
    if (addLinksBtn) {
      addLinksBtn.addEventListener('click', () => {
        this.showAddLinksModal();
      });
    }

    const addMeetLinkBtn = document.getElementById('addMeetLinkBtn');
    if (addMeetLinkBtn) {
      addMeetLinkBtn.addEventListener('click', () => {
        this.showAddLinksModal();
      });
    }

    // Biblioteca
    const viewLibraryBtn = document.getElementById('viewLibraryBtn');
    if (viewLibraryBtn) {
      viewLibraryBtn.addEventListener('click', () => {
        alert('🚧 Funcionalidade em desenvolvimento!\n\nEm breve você poderá acessar uma biblioteca colaborativa de livros brasileiros recomendados.');
      });
    }

    // Parcerias
    const viewPartnersBtn = document.getElementById('viewPartnersBtn');
    if (viewPartnersBtn) {
      viewPartnersBtn.addEventListener('click', () => {
        alert('🚧 Funcionalidade em desenvolvimento!\n\nEm breve você poderá encontrar espaços culturais e grupos educacionais na sua região.');
      });
    }

    AppStorage.logMetric('community.viewed', {});
  }

  showAddLinksModal() {
    const profile = AppStorage.getProfile();
    
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h2>Adicionar Links da Comunidade</h2>
          <button class="modal-close">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label>Link do Grupo WhatsApp</label>
            <input type="url" id="whatsappLink" class="form-input" 
                   placeholder="https://chat.whatsapp.com/..."
                   value="${profile?.communityLinks?.whatsapp || ''}">
          </div>
          
          <div class="form-group">
            <label>Link do Grupo Telegram</label>
            <input type="url" id="telegramLink" class="form-input" 
                   placeholder="https://t.me/..."
                   value="${profile?.communityLinks?.telegram || ''}">
          </div>
          
          <div class="form-group">
            <label>Link do Google Meet Mensal</label>
            <input type="url" id="meetLink" class="form-input" 
                   placeholder="https://meet.google.com/..."
                   value="${profile?.communityLinks?.meetMonthly || ''}">
          </div>
          
          <button class="btn btn-primary" id="saveLinksBtn">Salvar</button>
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

    // Salvar links
    const saveBtn = document.getElementById('saveLinksBtn');
    saveBtn.addEventListener('click', () => {
      const whatsapp = document.getElementById('whatsappLink').value;
      const telegram = document.getElementById('telegramLink').value;
      const meet = document.getElementById('meetLink').value;

      if (profile) {
        profile.communityLinks = {
          whatsapp,
          telegram,
          meetMonthly: meet
        };
        AppStorage.setProfile(profile);
        AppStorage.logMetric('community.linksAdded', {});
        document.body.removeChild(modal);
        this.render();
      }
    });
  }
}

export default Community;
