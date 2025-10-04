# 🌱 Semear - Educação com Valores e Cultura Brasileira

Programa educacional para famílias brasileiras que querem ser protagonistas na formação de seus filhos, integrando valores universais com a rica cultura brasileira.

## 🎯 Sobre o Projeto

O Semear é um MVP (Produto Mínimo Viável) 100% gratuito e local que ajuda pais e mães ocupados a:

- Criar planos semanais personalizados de atividades educacionais
- Explorar recursos brasileiros (histórias, músicas, rituais, atividades)
- Integrar diferentes estilos pedagógicos (Montessori, Waldorf, Clássico, Religioso)
- Registrar momentos especiais e acompanhar progresso
- Conectar-se com outras famílias

## ✨ Funcionalidades

### MVP Inicial
- ✅ **Onboarding personalizado** - Configure perfil da família, valores e estilos
- ✅ **Plano da Semana** - Sugestões automáticas de atividades, histórias, rituais, músicas e livros
- ✅ **Explorar recursos** - Filtros por idade, valores, estilos e formato
- ✅ **Guia pedagógico** - Entenda cada estilo e sua versão brasileira
- ✅ **Comunidade** - Links para grupos e encontros mensais
- ✅ **Diário de memórias** - Registre momentos especiais e progresso
- ✅ **Export/Import** - Backup em JSON e métricas em CSV
- ✅ **PWA** - Instalável e funciona offline

## 🚀 Como Usar

### Opção 1: GitHub Pages (Recomendado)

1. Faça fork deste repositório
2. Vá em Settings → Pages
3. Selecione branch `main` e pasta `/root`
4. Acesse em `https://seu-usuario.github.io/semear`

### Opção 2: Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/semear.git
cd semear

# Inicie um servidor local (escolha um):
# Python 3
python -m http.server 8000

# Node.js (npx)
npx serve

# Acesse http://localhost:8000
```

## 📁 Estrutura do Projeto

```
/semear/
  index.html              # Página principal
  404.html                # Fallback para SPA
  manifest.json           # PWA manifest
  service-worker.js       # Service Worker para offline
  
  /assets/
    /css/
      styles.css          # Estilos responsivos
    /js/
      app.js              # Aplicação principal
      router.js           # SPA Router
      storage.js          # Abstração localStorage
      data-loader.js      # Carregamento de dados
      export.js           # Export/Import JSON/CSV
      /components/
        onboarding.js     # Componente de onboarding
        weekly-plan.js    # Gerador de plano semanal
        explorer.js       # Explorador de recursos
        guide.js          # Guia pedagógico
        community.js      # Página de comunidade
        diary.js          # Diário de memórias
        settings.js       # Configurações
  
  /data/
    values.json           # Valores (respeito, paciência, etc)
    resources.json        # Recursos brasileiros (20+ itens)
    /seeds/
      family-profile.json
      weekly-plan.json
      diary.json
```

## 🛠️ Tecnologias

- **Frontend**: HTML5, CSS3, JavaScript Vanilla (ES6 modules)
- **Armazenamento**: localStorage (sem banco de dados)
- **PWA**: Service Worker + Manifest
- **Deploy**: GitHub Pages (gratuito)
- **Zero dependências externas** - Tudo funciona offline!

## 📊 Dados e Privacidade

- ✅ **100% local** - Todos os dados ficam no seu navegador
- ✅ **Sem servidor** - Não enviamos nada para nenhum lugar
- ✅ **Exportável** - Faça backup quando quiser
- ✅ **Portável** - Importe em outro navegador/dispositivo

## 🎨 Conteúdo Brasileiro

O Semear inclui recursos autênticos da cultura brasileira:

- 📖 **Histórias**: Saci-Pererê, Iara, Curupira, Bumba Meu Boi
- 🎵 **Músicas**: Ciranda Cirandinha, Peixe Vivo, Borboletinha
- 📚 **Livros**: Menina Bonita do Laço de Fita, Flicts, Chapeuzinho Amarelo
- 🎨 **Atividades**: Plantio de feijão, massinha caseira, brinquedo de sucata
- 🕯️ **Rituais**: Roda de gratidão, banho de ervas, ritual da mesa

## 🗺️ Roadmap

### ✅ MVP (Concluído)
- Onboarding, Plano Semanal, Explorar, Guia, Comunidade, Diário
- Export/Import, PWA básico

### 🔄 Fase 1 (Próximos passos)
- IndexedDB para dados volumosos
- Melhorias de filtros
- Gráficos de progresso

### 📅 Fase 2
- Templates por faixa etária
- Favoritos
- Multi-perfil (várias crianças)

### 🎯 Fase 3
- Editor de recursos
- Pacotes de conteúdo
- Busca local (Lunr.js)

## 🤝 Como Contribuir

1. **Compartilhe recursos** - Adicione atividades, histórias ou rituais brasileiros
2. **Reporte bugs** - Abra uma issue no GitHub
3. **Traduza** - Ajude a adaptar para outras regiões do Brasil
4. **Divulgue** - Compartilhe com outras famílias

## 📝 Licença

MIT License - Use livremente, modifique e compartilhe!

## 💬 Comunidade

- **WhatsApp/Telegram**: Configure nos links da comunidade
- **Encontro Mensal**: Primeira segunda-feira do mês, 20h
- **Email**: contato@semear.com.br (em breve)

## 🙏 Agradecimentos

Inspirado por famílias brasileiras que acreditam na educação com valores e cultura local.

---

**Feito com 💚 para famílias brasileiras**

🌱 Semear - Cultivando valores, colhendo memórias
