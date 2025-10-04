# 🐙 GitHub Desktop - Passo a Passo Completo

**Guia para criar repositório e fazer deploy do Semear**

---

## ✅ Situação Atual

A pasta `/Users/priscilawollmann/CascadeProjects/semear` **ainda não é um repositório Git**.

Isso é normal! Vamos criar o repositório agora usando o GitHub Desktop.

---

## 📋 Passo a Passo Completo

### Passo 1: Abrir GitHub Desktop

1. Abra o **GitHub Desktop** (que você está baixando)
2. Se for a primeira vez:
   - Faça login com sua conta GitHub
   - Configure seu nome e email (se pedir)

---

### Passo 2: Criar Repositório Local

1. No GitHub Desktop, clique em **File** (menu superior)
2. Selecione **Add Local Repository**
3. Clique em **Choose...**
4. Navegue até: `/Users/priscilawollmann/CascadeProjects/semear`
5. Clique em **Add Repository**

**Você verá uma mensagem**: *"This directory does not appear to be a Git repository"*

6. ✅ Clique em **create a repository** (link azul na mensagem)

---

### Passo 3: Configurar o Repositório

Uma janela vai abrir com opções:

**Preencha assim:**

- **Name**: `semear` (já deve estar preenchido)
- **Description**: `Programa educacional para famílias brasileiras`
- **Local Path**: `/Users/priscilawollmann/CascadeProjects/semear` (já preenchido)
- **Initialize this repository with a README**: ❌ **DESMARQUE** (já temos README)
- **Git Ignore**: None
- **License**: None (ou MIT se quiser)

7. Clique em **Create Repository**

---

### Passo 4: Fazer o Primeiro Commit

Agora você verá todos os arquivos na aba **Changes**:

1. Na aba **Changes** (lado esquerdo), você verá ~40 arquivos
2. Todos devem estar marcados (✓)
3. No campo **Summary** (embaixo), escreva:
   ```
   Initial commit - Semear MVP v1.0.0
   ```
4. No campo **Description** (opcional), escreva:
   ```
   - MVP completo com todas funcionalidades
   - 24 recursos brasileiros
   - Documentação completa
   - PWA funcional
   ```
5. Clique no botão azul **Commit to main**

**Pronto!** Seu repositório local está criado! 🎉

---

### Passo 5: Publicar no GitHub

Agora vamos enviar para o GitHub:

1. No topo do GitHub Desktop, clique em **Publish repository**
2. Uma janela vai abrir:

**Configure assim:**

- **Name**: `semear`
- **Description**: `Programa educacional para famílias brasileiras`
- **Keep this code private**: ❌ **DESMARQUE** (precisa ser público para GitHub Pages)
- **Organization**: None (deixe em branco)

3. Clique em **Publish Repository**

**Aguarde 10-30 segundos** enquanto faz upload...

✅ **Pronto!** Seu código está no GitHub!

---

### Passo 6: Ativar GitHub Pages

Agora vamos ativar o site:

1. No GitHub Desktop, clique em **Repository** (menu superior)
2. Selecione **View on GitHub**
3. Isso abre o navegador no seu repositório

**No navegador:**

4. Clique em **Settings** (aba no topo)
5. No menu lateral esquerdo, clique em **Pages**
6. Em **Source**, configure:
   - **Branch**: `main` (selecione no dropdown)
   - **Folder**: `/ (root)` (deixe assim)
7. Clique em **Save**

**Aguarde 2-3 minutos...**

8. Recarregue a página (F5)
9. Você verá uma mensagem verde:
   ```
   Your site is live at https://SEU_USUARIO.github.io/semear/
   ```

---

### Passo 7: Acessar Seu Site! 🎉

Clique no link ou acesse:
```
https://SEU_USUARIO.github.io/semear/
```

**Seu MVP está no ar!** 🚀

---

## 🧪 Testar o Site Publicado

Quando o site carregar:

### Teste Básico
- [ ] Site carrega (não dá erro 404)
- [ ] Navegação funciona
- [ ] Onboarding completo
- [ ] Plano semanal é gerado
- [ ] Dados salvam no localStorage

### Teste Mobile
- [ ] Abra no celular (Chrome ou Safari)
- [ ] Teste navegação
- [ ] Menu funciona em tela pequena
- [ ] Tente instalar como PWA:
  - **Android**: Menu → "Adicionar à tela inicial"
  - **iOS**: Compartilhar → "Adicionar à Tela de Início"

### Teste Console
- [ ] Pressione F12
- [ ] Vá na aba Console
- [ ] Não deve ter erros vermelhos críticos

---

## 🔄 Fazer Atualizações Futuras

Quando você editar algum arquivo:

### No GitHub Desktop:

1. Você verá as mudanças na aba **Changes**
2. Escreva um resumo do que mudou (ex: "Adiciona novos recursos")
3. Clique em **Commit to main**
4. Clique em **Push origin** (botão no topo)

**Pronto!** O site atualiza automaticamente em 1-2 minutos.

---

## 🐛 Problemas Comuns

### "This directory does not appear to be a Git repository"

✅ **Isso é esperado!** Siga o Passo 2 e clique em "create a repository"

---

### "Repository not found" ao publicar

**Solução**: 
1. Verifique se está logado no GitHub Desktop
2. Vá em **GitHub Desktop → Preferences → Accounts**
3. Faça login novamente se necessário

---

### "Keep this code private" está marcado

**Importante**: Desmarque! GitHub Pages free só funciona com repositórios públicos.

---

### GitHub Pages não ativa

**Soluções**:
1. Certifique-se que o repositório é **público**
2. Aguarde 5 minutos (pode demorar)
3. Recarregue a página de Settings → Pages
4. Verifique se escolheu branch `main` e folder `/ (root)`

---

### Site carrega mas não funciona

**Soluções**:
1. Abra o Console (F12) e veja os erros
2. Aguarde 5 minutos (cache do GitHub)
3. Limpe cache do navegador (Ctrl+Shift+R ou Cmd+Shift+R)
4. Tente em modo anônimo

---

### "Push rejected" ou erro ao fazer push

**Solução**:
1. Clique em **Repository → Pull** primeiro
2. Depois tente **Push** novamente

---

## 📊 Verificar Status

### No GitHub Desktop

- **Current Branch**: deve mostrar `main`
- **Fetch origin**: deve estar atualizado
- **No local changes**: depois do commit

### No GitHub.com

- Vá em seu repositório
- Deve mostrar todos os arquivos
- Último commit deve ser "Initial commit - Semear MVP v1.0.0"

---

## ✅ Checklist Final

Antes de compartilhar com outras pessoas:

- [ ] Repositório criado no GitHub Desktop
- [ ] Primeiro commit feito
- [ ] Publicado no GitHub (público)
- [ ] GitHub Pages ativado
- [ ] Site acessível via URL
- [ ] Testado em desktop
- [ ] Testado em mobile
- [ ] Sem erros críticos no console
- [ ] PWA instalável

---

## 🎯 Próximos Passos

Agora que está no ar:

### 1. Compartilhar com Pilotos
```
🌱 Convite: Teste o Semear

Olá! Criei um app gratuito para famílias que querem 
educar com valores e cultura brasileira.

Preciso de feedback! Pode testar?

Link: https://SEU_USUARIO.github.io/semear/

Leva 5 minutos para criar seu plano personalizado.

Obrigada! 💚
```

### 2. Coletar Feedback
- Use Google Forms (gratuito)
- Pergunte: O que gostou? O que faltou? Usaria semanalmente?
- Veja arquivo `tests/PILOT_TEST.md` para roteiro completo

### 3. Iterar
- Faça melhorias baseadas no feedback
- Commit → Push no GitHub Desktop
- Site atualiza automaticamente!

---

## 💡 Dicas

### Commits Frequentes
- Faça commits pequenos e frequentes
- Escreva mensagens claras (ex: "Adiciona recurso X", "Corrige bug Y")

### Branches (Futuro)
- Por enquanto, trabalhe na branch `main`
- Quando dominar, pode criar branches para features

### Backup
- Seu código está seguro no GitHub
- Mas faça export dos dados do app regularmente (Settings → Export JSON)

---

## 🎉 Parabéns!

Você acabou de:
- ✅ Criar seu primeiro repositório Git
- ✅ Publicar código no GitHub
- ✅ Fazer deploy de um app web
- ✅ Ativar GitHub Pages
- ✅ Ter um MVP no ar!

**Isso é uma conquista enorme!** 🚀

---

## 📞 Precisa de Ajuda?

### Recursos
- [Documentação GitHub Desktop](https://docs.github.com/pt/desktop)
- [Guia GitHub Pages](https://docs.github.com/pt/pages)
- [Comunidade GitHub](https://github.community/)

### Arquivos do Projeto
- `START_HERE.md` - Visão geral
- `DEPLOY.md` - Guia completo de deploy
- `COMO_RODAR_LOCAL.md` - Testar localmente

---

## 📝 Resumo Visual

```
1. GitHub Desktop → Add Local Repository
   ↓
2. Pasta não é Git? → Create a repository
   ↓
3. Configurar (nome: semear, público)
   ↓
4. Commit (mensagem: "Initial commit - Semear MVP v1.0.0")
   ↓
5. Publish repository (desmarque "private")
   ↓
6. View on GitHub → Settings → Pages
   ↓
7. Source: main, / (root) → Save
   ↓
8. Aguarde 2-3 minutos
   ↓
9. 🎉 Site no ar!
```

---

**🌱 Semear - Cultivando valores, colhendo memórias**

*Seu MVP está pronto para o mundo! 🚀*

---

**Última atualização**: 04/10/2025
