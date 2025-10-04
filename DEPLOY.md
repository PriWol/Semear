# 🚀 Guia de Deploy - Semear

Este guia explica como fazer deploy do Semear usando opções 100% gratuitas.

---

## Opção 1: GitHub Pages (Recomendado) ⭐

### Vantagens
- ✅ 100% gratuito
- ✅ HTTPS automático
- ✅ Domínio customizado (opcional)
- ✅ Deploy automático via Git
- ✅ Estável e confiável

### Passo a Passo

#### 1. Criar Repositório no GitHub

```bash
# No terminal, dentro da pasta semear
git init
git add .
git commit -m "Initial commit - MVP Semear"

# Criar repositório no GitHub (via interface web)
# Depois conectar:
git remote add origin https://github.com/SEU_USUARIO/semear.git
git branch -M main
git push -u origin main
```

#### 2. Ativar GitHub Pages

1. Acesse seu repositório no GitHub
2. Vá em **Settings** → **Pages**
3. Em **Source**, selecione:
   - Branch: `main`
   - Folder: `/ (root)`
4. Clique em **Save**
5. Aguarde 2-3 minutos

#### 3. Acessar o Site

Seu site estará disponível em:
```
https://SEU_USUARIO.github.io/semear/
```

#### 4. Configurar Domínio Customizado (Opcional)

Se você tem um domínio próprio:

1. No GitHub Pages, adicione seu domínio customizado
2. No seu provedor de DNS, adicione um registro CNAME:
   ```
   CNAME: www.seudominio.com.br → SEU_USUARIO.github.io
   ```
3. Aguarde propagação do DNS (até 24h)

### Atualizações

Para atualizar o site:

```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

O GitHub Pages atualiza automaticamente em 1-2 minutos.

---

## Opção 2: Vercel (Alternativa)

### Vantagens
- ✅ 100% gratuito (free tier)
- ✅ Deploy automático
- ✅ Preview de branches
- ✅ Analytics básico
- ✅ Domínio .vercel.app

### Passo a Passo

#### 1. Criar Conta no Vercel

1. Acesse [vercel.com](https://vercel.com)
2. Faça login com GitHub

#### 2. Importar Projeto

1. Clique em **New Project**
2. Selecione o repositório `semear`
3. Configure:
   - Framework Preset: **Other**
   - Build Command: (deixe vazio)
   - Output Directory: `./`
4. Clique em **Deploy**

#### 3. Acessar o Site

Seu site estará em:
```
https://semear-SEU_USUARIO.vercel.app
```

### Atualizações

Deploy automático a cada push no GitHub!

---

## Opção 3: Netlify (Alternativa)

### Vantagens
- ✅ 100% gratuito
- ✅ Deploy automático
- ✅ Formulários gratuitos
- ✅ Redirects e headers customizados

### Passo a Passo

#### 1. Criar Conta no Netlify

1. Acesse [netlify.com](https://netlify.com)
2. Faça login com GitHub

#### 2. Importar Projeto

1. Clique em **Add new site** → **Import an existing project**
2. Conecte com GitHub
3. Selecione o repositório `semear`
4. Configure:
   - Build command: (deixe vazio)
   - Publish directory: `./`
5. Clique em **Deploy**

#### 3. Acessar o Site

Seu site estará em:
```
https://semear-SEU_USUARIO.netlify.app
```

---

## Opção 4: Servidor Local (Desenvolvimento)

### Para Testes Locais

#### Python 3
```bash
cd semear
python -m http.server 8000
# Acesse http://localhost:8000
```

#### Node.js (npx)
```bash
cd semear
npx serve
# Acesse http://localhost:3000
```

#### PHP
```bash
cd semear
php -S localhost:8000
# Acesse http://localhost:8000
```

#### VS Code Live Server
1. Instale a extensão "Live Server"
2. Clique com botão direito em `index.html`
3. Selecione "Open with Live Server"

---

## ⚙️ Configurações Importantes

### 1. Ajustar Caminhos (se necessário)

Se o site não estiver na raiz do domínio, ajuste os caminhos:

**Em `index.html`**:
```html
<!-- Se estiver em /semear/ -->
<base href="/semear/">
```

**Em `manifest.json`**:
```json
{
  "start_url": "/semear/",
  "scope": "/semear/"
}
```

### 2. HTTPS

Todos os serviços mencionados fornecem HTTPS automático. Isso é importante para:
- Service Workers (PWA)
- Segurança dos dados
- SEO

### 3. Cache e Atualizações

O Service Worker cacheia recursos. Para forçar atualização:

1. Incremente a versão em `service-worker.js`:
   ```javascript
   const CACHE_NAME = 'semear-v1.0.1'; // Incrementar aqui
   ```

2. Usuários verão a atualização na próxima visita

---

## 🔍 Verificação Pós-Deploy

### Checklist

- [ ] Site carrega corretamente
- [ ] Todas as páginas funcionam
- [ ] Navegação entre páginas funciona
- [ ] Dados salvam no localStorage
- [ ] PWA é instalável
- [ ] Funciona offline (após primeira visita)
- [ ] Responsivo em mobile
- [ ] Sem erros no console

### Ferramentas de Teste

#### Lighthouse (Chrome DevTools)
```
1. Abra o site no Chrome
2. F12 → Lighthouse
3. Gere relatório
4. Alvos: Performance >80, Accessibility >90, PWA >80
```

#### Teste de Responsividade
```
1. Chrome DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Teste em: iPhone, iPad, Desktop
```

#### Teste Offline
```
1. Chrome DevTools → Network
2. Marque "Offline"
3. Recarregue a página
4. Deve funcionar (após primeira visita)
```

---

## 🐛 Troubleshooting

### Problema: Site não carrega

**Solução**:
1. Verifique se todos os arquivos foram commitados
2. Confira caminhos relativos (use `/` no início)
3. Veja o console do navegador para erros

### Problema: PWA não instala

**Solução**:
1. Verifique se está em HTTPS
2. Confirme que `manifest.json` está acessível
3. Valide o manifest em [Web App Manifest Validator](https://manifest-validator.appspot.com/)

### Problema: Service Worker não funciona

**Solução**:
1. Só funciona em HTTPS (ou localhost)
2. Limpe cache: DevTools → Application → Clear storage
3. Verifique erros em: DevTools → Application → Service Workers

### Problema: Dados não salvam

**Solução**:
1. Verifique se localStorage está habilitado
2. Teste em modo anônimo (pode ter restrições)
3. Veja console para erros de storage

---

## 📊 Monitoramento (Gratuito)

### Google Analytics (Opcional)

Se quiser métricas centralizadas:

1. Crie conta no [Google Analytics](https://analytics.google.com)
2. Adicione o código de tracking em `index.html`:

```html
<!-- Antes de </head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**Nota**: Isso envia dados para o Google. Use apenas se estiver confortável com isso.

### Alternativa: Métricas Locais

O Semear já tem sistema de métricas local:
- Export CSV de eventos
- Análise manual
- 100% privado

---

## 🔐 Segurança

### Boas Práticas

- ✅ Use HTTPS sempre
- ✅ Não commite dados sensíveis
- ✅ Valide inputs do usuário
- ✅ Mantenha dependências atualizadas (se usar)
- ✅ Faça backups regulares

### Dados dos Usuários

- Todos os dados ficam no navegador do usuário
- Você (desenvolvedor) não tem acesso aos dados
- Usuários podem exportar/deletar quando quiserem

---

## 📱 Teste em Dispositivos Reais

### Android

1. Acesse o site no Chrome mobile
2. Menu → "Adicionar à tela inicial"
3. Teste todas as funcionalidades

### iOS

1. Acesse o site no Safari
2. Botão compartilhar → "Adicionar à Tela de Início"
3. Teste todas as funcionalidades

**Nota**: iOS tem limitações com PWAs (sem notificações push, etc)

---

## 🎉 Pronto!

Seu MVP está no ar! Agora:

1. ✅ Compartilhe com as 5 famílias piloto
2. ✅ Colete feedback
3. ✅ Itere e melhore
4. ✅ Expanda gradualmente

**Lembre-se**: Comece pequeno, aprenda rápido, cresça organicamente!

---

**Dúvidas?** Abra uma issue no GitHub ou entre em contato pela comunidade.
