// components/guide.js
import { AppStorage } from '../storage.js';

class Guide {
  constructor(router) {
    this.router = router;
  }

  async render() {
    const app = document.getElementById('app');
    
    app.innerHTML = `
      <div class="guide-container">
        <div class="guide-header">
          <h1>📚 Guia Pedagógico</h1>
          <p>Entenda os estilos e como adaptá-los à realidade brasileira</p>
        </div>

        <div class="guide-content">
          ${this.renderStyleGuides()}
        </div>
      </div>
    `;

    this.attachEventListeners();
  }

  renderStyleGuides() {
    const styles = [
      {
        name: 'Montessori',
        icon: '🌱',
        description: 'Educação pela autonomia e ambiente preparado',
        principles: [
          'Autonomia: a criança aprende fazendo',
          'Ambiente preparado: materiais acessíveis e organizados',
          'Respeito ao ritmo individual',
          'Educação cósmica: conexão com o universo'
        ],
        brazilianAdaptation: [
          'Use materiais naturais brasileiros (sementes, madeiras, pedras)',
          'Inclua elementos da cultura local (instrumentos, artesanato)',
          'Atividades práticas com ingredientes regionais (tapioca, milho)',
          'Observação da natureza brasileira (plantas, animais, clima)'
        ],
        examples: [
          'Plantio de feijão no algodão',
          'Preparar suco de frutas regionais',
          'Organizar brinquedos por categoria',
          'Cuidar de uma horta caseira'
        ]
      },
      {
        name: 'Waldorf',
        icon: '🎨',
        description: 'Educação pela arte, ritmo e imaginação',
        principles: [
          'Arte como caminho de aprendizado',
          'Ritmos diários e sazonais',
          'Imaginação e fantasia',
          'Conexão com a natureza e festivais'
        ],
        brazilianAdaptation: [
          'Festivais brasileiros (Festa Junina, Carnaval, Folclore)',
          'Cantigas de roda e brincadeiras tradicionais',
          'Histórias do folclore brasileiro (Saci, Curupira, Iara)',
          'Artesanato com materiais locais (barro, palha, tecidos)'
        ],
        examples: [
          'Roda de ciranda ao ar livre',
          'Teatro de sombras com lendas brasileiras',
          'Pintura com tintas naturais',
          'Celebrar mudanças de estação'
        ]
      },
      {
        name: 'Clássico',
        icon: '📖',
        description: 'Educação pelas virtudes e grandes obras',
        principles: [
          'Virtudes cardeais (prudência, justiça, fortaleza, temperança)',
          'Grandes livros e histórias',
          'Tradição e memória',
          'Busca pela verdade, beleza e bondade'
        ],
        brazilianAdaptation: [
          'Clássicos da literatura brasileira (Monteiro Lobato, Ana Maria Machado)',
          'Histórias de heróis e heroínas brasileiras',
          'Valores familiares e comunitários',
          'Memória oral: histórias dos avós e antepassados'
        ],
        examples: [
          'Ler "O Menino Maluquinho" e discutir coragem',
          'Contar histórias de família',
          'Memorizar poesias brasileiras',
          'Estudar biografias de brasileiros inspiradores'
        ]
      },
      {
        name: 'Religioso',
        icon: '🕯️',
        description: 'Educação pela fé e valores espirituais',
        principles: [
          'Fé e vida espiritual',
          'Amor ao próximo e serviço',
          'Gratidão e oração',
          'Comunidade e tradições religiosas'
        ],
        brazilianAdaptation: [
          'Festividades religiosas brasileiras (Natal, Páscoa, Santos Juninos)',
          'Solidariedade e mutirão comunitário',
          'Gratidão pelas bênçãos da terra brasileira',
          'Respeito à diversidade religiosa (católica, evangélica, afro-brasileira, indígena)'
        ],
        examples: [
          'Roda de gratidão antes das refeições',
          'Ajudar vizinhos e comunidade',
          'Celebrar festas religiosas com rituais familiares',
          'Banho de ervas e conexão espiritual'
        ]
      }
    ];

    return styles.map(style => `
      <div class="style-guide-card">
        <div class="style-guide-header">
          <span class="style-icon">${style.icon}</span>
          <h2>${style.name}</h2>
        </div>
        
        <p class="style-description">${style.description}</p>
        
        <div class="style-section">
          <h3>Princípios Fundamentais</h3>
          <ul>
            ${style.principles.map(p => `<li>${p}</li>`).join('')}
          </ul>
        </div>
        
        <div class="style-section highlight">
          <h3>🇧🇷 Adaptação Brasileira</h3>
          <ul>
            ${style.brazilianAdaptation.map(a => `<li>${a}</li>`).join('')}
          </ul>
        </div>
        
        <div class="style-section">
          <h3>Exemplos Práticos</h3>
          <ul>
            ${style.examples.map(e => `<li>${e}</li>`).join('')}
          </ul>
        </div>
      </div>
    `).join('');
  }

  attachEventListeners() {
    AppStorage.logMetric('guide.viewed', {});
  }
}

export default Guide;
