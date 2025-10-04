# 🚀 Instruções de Deploy - Semear

**Guia passo a passo para publicar seu MVP no GitHub Pages**

---

## ⚠️ Pré-requisito: Instalar Git

Você precisa instalar as ferramentas de desenvolvedor do Xcode primeiro.

### Opção 1: Via Terminal (Recomendado)
```bash
xcode-select --install
```
- Uma janela vai aparecer
- Clique em "Instalar"
- Aguarde 5-10 minutos
- Depois continue com os passos abaixo

### Opção 2: GitHub Desktop (Mais Fácil)
Se preferir interface visual:
1. Baixe [GitHub Desktop](https://desktop.github.com/)
2. Instale e faça login com sua conta GitHub
3. Pule para "Opção B: Deploy via GitHub Desktop"

---

## 📋 Opção A: Deploy via Terminal

### Passo 1: Instalar Xcode Command Line Tools
```bash
xcode-select --install
```
Aguarde a instalação completar.

### Passo 2: Verificar Git
```bash
git --version
```
Deve mostrar algo como: `git version 2.x.x`

### Passo 3: Configurar Git (Primeira Vez)
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### Passo 4: Inicializar Repositório
```bash
cd /Users/priscilawollmann/CascadeProjects/semear
git init
git add .
git commit -m "Initial commit - Semear MVP v1.0.0"
```

### Passo 5: Criar Repositório no GitHub
1. Acesse [github.com](https://github.com)
2. Clique no **+** (canto superior direito) → **New repository**
3. Preencha:
   - **Repository name**: `semear`
   - **Description**: "Programa educacional para famílias brasileiras"
   - **Public** (marque esta opção)
   - **NÃO** marque "Add a README" (já existe)
4. Clique em **Create repository**

### Passo 6: Conectar e Enviar
Na página que abrir, copie os comandos da seção **"…or push an existing repository from the command line"**

Ou use estes (substitua SEU_USUARIO):
```bash
git remote add origin https://github.com/SEU_USUARIO/semear.git
git branch -M main
git push -u origin main
```

Se pedir usuário/senha:
- **Username**: seu username do GitHub
- **Password**: use um [Personal Access Token](https://github.com/settings/tokens) (não a senha)

### Passo 7: Ativar GitHub Pages
1. No GitHub, vá em **Settings** do repositório
2. Menu lateral → **Pages**
3. Em **Source**:
   - Branch: `main`
   - Folder: `/ (root)`
4. Clique em **Save**
5. Aguarde 2-3 minutos

### Passo 8: Acessar Seu Site! 🎉
```
https://SEU_USUARIO.github.io/semear/
```

---

## 📋 Opção B: Deploy via GitHub Desktop

### Passo 1: Baixar GitHub Desktop
1. Acesse [desktop.github.com](https://desktop.github.com/)
2. Baixe e instale
3. Faça login com sua conta GitHub

### Passo 2: Adicionar Repositório Local
1. Abra GitHub Desktop
2. **File** → **Add Local Repository**
3. Escolha a pasta: `/Users/priscilawollmann/CascadeProjects/semear`
4. Se disser que não é um repositório, clique em **Create a repository**

### Passo 3: Fazer Commit
1. Na aba **Changes**, você verá todos os arquivos
2. No campo **Summary**, escreva: `Initial commit - Semear MVP v1.0.0`
3. Clique em **Commit to main**

### Passo 4: Publicar no GitHub
1. Clique em **Publish repository** (topo)
2. Preencha:
   - **Name**: `semear`
   - **Description**: "Programa educacional para famílias brasileiras"
   - **Desmarque** "Keep this code private"
3. Clique em **Publish repository**

### Passo 5: Ativar GitHub Pages
1. No GitHub Desktop, clique em **Repository** → **View on GitHub**
2. No site, vá em **Settings**
3. Menu lateral → **Pages**
4. Em **Source**:
   - Branch: `main`
   - Folder: `/ (root)`
5. Clique em **Save**

### Passo 6: Acessar Seu Site! 🎉
Aguarde 2-3 minutos e acesse:
```
https://SEU_USUARIO.github.io/semear/
```

---

## 📋 Opção C: Deploy via Vercel (Alternativa)

Se preferir Vercel ao invés de GitHub Pages:

### Passo 1: Criar Conta
1. Acesse [vercel.com](https://vercel.com)
2. Clique em **Sign Up**
3. Escolha **Continue with GitHub**

### Passo 2: Importar Projeto
1. Clique em **Add New** → **Project**
2. Clique em **Import Git Repository**
3. Se não aparecer seu repositório:
   - Primeiro faça upload no GitHub (use Opção A ou B acima)
   - Depois volte aqui e importe

### Passo 3: Configurar Deploy
1. Selecione o repositório `semear`
2. Configure:
   - **Framework Preset**: Other
   - **Build Command**: (deixe vazio)
   - **Output Directory**: `./`
3. Clique em **Deploy**

### Passo 4: Acessar Seu Site! 🎉
Após 1-2 minutos:
```
https://semear-SEU_USUARIO.vercel.app
```

---

## ✅ Verificação Pós-Deploy

Depois que o site estiver no ar, teste:

### Checklist Básico
- [ ] Site carrega (sem erro 404)
- [ ] Navegação funciona
- [ ] Onboarding completo funciona
- [ ] Dados salvam no localStorage
- [ ] Plano semanal é gerado
- [ ] PWA é instalável (ícone na barra de endereço)

### Teste em Dispositivos
- [ ] Desktop (Chrome/Safari/Firefox)
- [ ] Mobile (Chrome Android ou Safari iOS)
- [ ] Tablet (se tiver)

### Teste PWA
1. No Chrome mobile, abra o site
2. Menu (⋮) → "Adicionar à tela inicial"
3. Confirme
4. Abra o app da tela inicial
5. Deve funcionar como app nativo

---

## 🐛 Problemas Comuns

### "git: command not found"
**Solução**: Instale Xcode Command Line Tools
```bash
xcode-select --install
```

### "Permission denied (publickey)"
**Solução**: Use HTTPS ao invés de SSH, ou configure SSH keys
```bash
# Use esta URL (HTTPS):
git remote set-url origin https://github.com/SEU_USUARIO/semear.git
```

### "Authentication failed"
**Solução**: Use Personal Access Token ao invés de senha
1. Acesse [github.com/settings/tokens](https://github.com/settings/tokens)
2. **Generate new token** → **Classic**
3. Dê um nome: "Semear Deploy"
4. Marque: `repo` (todos os sub-items)
5. **Generate token**
6. Copie o token (só aparece uma vez!)
7. Use este token como senha no git push

### "GitHub Pages não ativa"
**Solução**: 
- Certifique-se que o repositório é público
- Aguarde 5 minutos (pode demorar)
- Verifique se escolheu branch `main` e folder `/ (root)`

### "Site carrega mas não funciona"
**Solução**: Verifique console do navegador (F12)
- Pode ser problema de caminhos
- Verifique se todos os arquivos foram commitados

---

## 🔄 Atualizações Futuras

Quando fizer mudanças no código:

### Via Terminal
```bash
cd /Users/priscilawollmann/CascadeProjects/semear
git add .
git commit -m "Descrição das mudanças"
git push
```

### Via GitHub Desktop
1. Abra GitHub Desktop
2. Veja mudanças na aba **Changes**
3. Escreva descrição no **Summary**
4. Clique em **Commit to main**
5. Clique em **Push origin** (topo)

GitHub Pages atualiza automaticamente em 1-2 minutos!

---

## 📊 Monitoramento (Opcional)

### Google Analytics (Se Quiser)
1. Crie conta em [analytics.google.com](https://analytics.google.com)
2. Adicione código de tracking em `index.html` (antes de `</head>`):

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**Nota**: Isso envia dados para o Google. Use apenas se confortável.

---

## 🎯 Próximos Passos Após Deploy

1. ✅ **Testar tudo** - Use o checklist acima
2. ✅ **Compartilhar com pilotos** - Envie o link para 5 famílias
3. ✅ **Coletar feedback** - Use formulário do Google Forms
4. ✅ **Iterar** - Faça melhorias baseadas no feedback

---

## 📞 Precisa de Ajuda?

### Recursos
- 📖 [Documentação GitHub Pages](https://docs.github.com/pages)
- 📖 [Guia Git Básico](https://git-scm.com/book/pt-br/v2)
- 💬 [GitHub Community](https://github.community/)

### Erros Comuns
- Veja seção "Problemas Comuns" acima
- Verifique console do navegador (F12)
- Teste em modo anônimo (sem extensões)

---

## ✨ Resumo Rápido

**Caminho mais fácil**: GitHub Desktop
1. Instale GitHub Desktop
2. Adicione pasta do projeto
3. Commit → Publish
4. Ative Pages no GitHub
5. Pronto! 🎉

**Tempo total**: 15-20 minutos

---

**🌱 Semear - Cultivando valores, colhendo memórias**

*Seu MVP está pronto para o mundo! 🚀*
