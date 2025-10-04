# ⚡ Início Rápido - Semear

Comece a usar o Semear em 5 minutos!

---

## 🚀 Para Usuários

### 1. Acesse o Site

Abra no navegador (Chrome ou Safari recomendados):
```
https://SEU_USUARIO.github.io/semear/
```

### 2. Complete o Onboarding (5 min)

**Passo 1**: Informações da família
- Nome dos pais/responsáveis
- Nome e data de nascimento da criança

**Passo 2**: Escolha até 3 valores
- Respeito, Paciência, Coragem, Gratidão, etc.

**Passo 3**: Estilos pedagógicos
- Montessori, Waldorf, Clássico, Religioso
- Tempo disponível por semana

**Passo 4**: Revisão e confirmação

### 3. Explore seu Plano Semanal

Você verá automaticamente:
- 🎨 1 Atividade prática
- 📖 1 História brasileira
- 🕯️ 1 Ritual familiar
- 🎵 1 Música (com link Spotify)
- 📚 1 Livro recomendado

### 4. Use Durante a Semana

- ✅ Marque o checklist conforme realiza
- 📝 Adicione notas sobre a experiência
- 🔄 Troque recursos se quiser

### 5. Registre Momentos Especiais

No **Diário**:
- ✨ Adicione momentos marcantes
- ⭐ Dê nota (1-5 estrelas)
- 💭 Reflita sobre a semana

---

## 💻 Para Desenvolvedores

### Setup Local

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/semear.git
cd semear

# Inicie servidor local (escolha um):

# Opção 1: Python 3
python3 -m http.server 8000

# Opção 2: Node.js
npx serve

# Opção 3: PHP
php -S localhost:8000

# Acesse http://localhost:8000
```

### Estrutura Básica

```
/semear/
  index.html          # Página principal
  /assets/
    /js/
      app.js          # App principal
      /components/    # Componentes SPA
    /css/
      styles.css      # Estilos
  /data/
    values.json       # Valores
    resources.json    # Recursos brasileiros
```

### Adicionar Novos Recursos

Edite `/data/resources.json`:

```json
{
  "id": "seu-recurso",
  "type": "activity",
  "title": "Nome da Atividade",
  "ageRange": "3-6",
  "values": ["respeito", "criatividade"],
  "styles": ["Montessori"],
  "format": "prática",
  "durationMin": 30,
  "locale": "pt-BR",
  "culturalNotes": "Contexto brasileiro",
  "instructions": [
    "Passo 1",
    "Passo 2"
  ],
  "materials": ["Material 1", "Material 2"]
}
```

### Deploy

```bash
# Commit mudanças
git add .
git commit -m "Adiciona novos recursos"
git push

# GitHub Pages atualiza automaticamente!
```

---

## 📱 Instalar como App (PWA)

### Android (Chrome)
1. Abra o site no Chrome
2. Menu (⋮) → "Adicionar à tela inicial"
3. Confirme

### iOS (Safari)
1. Abra o site no Safari
2. Botão compartilhar (□↑)
3. "Adicionar à Tela de Início"
4. Confirme

### Desktop (Chrome/Edge)
1. Ícone de instalação na barra de endereço
2. Ou Menu → "Instalar Semear"

---

## 🎯 Primeiros Passos Recomendados

### Semana 1: Exploração
- [ ] Complete o onboarding
- [ ] Veja o plano gerado
- [ ] Explore 5 recursos diferentes
- [ ] Leia o Guia Pedagógico

### Semana 2: Experimentação
- [ ] Realize 1 atividade do plano
- [ ] Marque checklist
- [ ] Registre 1 momento no diário
- [ ] Troque 1 recurso

### Semana 3: Personalização
- [ ] Explore filtros avançados
- [ ] Favorite recursos
- [ ] Adicione reflexão semanal
- [ ] Exporte seus dados (backup)

### Semana 4: Comunidade
- [ ] Entre no grupo WhatsApp/Telegram
- [ ] Compartilhe uma experiência
- [ ] Participe do encontro mensal
- [ ] Indique para 1 amigo

---

## 💡 Dicas de Uso

### Para Pais Ocupados
- ⏰ Reserve 10-15 min no domingo para ver o plano
- 📅 Escolha 2-3 itens prioritários da semana
- 🎯 Foco na qualidade, não quantidade
- 📸 Tire fotos dos momentos (opcional)

### Para Maximizar Valor
- 🔄 Troque recursos até encontrar os ideais
- 📝 Use as notas para lembrar o que funcionou
- ⭐ Dê notas honestas no diário
- 🤝 Compartilhe descobertas na comunidade

### Para Engajamento das Crianças
- 🎨 Deixe a criança escolher entre 2 opções
- 📖 Leia histórias com vozes diferentes
- 🎵 Cante junto e crie coreografias
- 🕯️ Rituais viram tradições familiares

---

## ❓ FAQ Rápido

**P: É realmente gratuito?**
R: Sim! 100% gratuito, sem anúncios, sem custos ocultos.

**P: Meus dados são seguros?**
R: Sim! Tudo fica no seu navegador, não enviamos nada para servidores.

**P: Funciona offline?**
R: Sim! Após a primeira visita, funciona sem internet.

**P: Posso usar para várias crianças?**
R: No MVP, 1 criança por perfil. Multi-perfil vem na Fase 2.

**P: Como faço backup?**
R: Configurações → Exportar Dados (JSON). Salve o arquivo!

**P: Posso adicionar meus próprios recursos?**
R: Na Fase 3 terá editor. Por ora, sugira na comunidade!

**P: Funciona em qual navegador?**
R: Chrome, Safari, Firefox, Edge (versões recentes).

**P: E se eu perder meus dados?**
R: Por isso recomendamos export regular! Dados ficam no navegador.

---

## 🆘 Precisa de Ajuda?

### Documentação
- 📖 [README.md](README.md) - Visão geral
- 🗺️ [ROADMAP.md](ROADMAP.md) - Plano de 6 meses
- 🚀 [DEPLOY.md](DEPLOY.md) - Guia de deploy
- 🧪 [PILOT_TEST.md](tests/PILOT_TEST.md) - Testes piloto

### Comunidade
- 💬 Grupo WhatsApp/Telegram (configure no app)
- 📅 Encontro Mensal (primeira segunda, 20h)
- 🐛 Issues no GitHub

### Contato
- 📧 contato@semear.com.br (em breve)
- 💻 GitHub: [github.com/semear-educacao](https://github.com)

---

## 🎉 Pronto para Começar!

1. ✅ Acesse o site
2. ✅ Complete onboarding (5 min)
3. ✅ Veja seu plano personalizado
4. ✅ Comece a cultivar momentos especiais!

**🌱 Semear - Cultivando valores, colhendo memórias**

---

*Última atualização: Outubro 2025*
