# 🖥️ Como Rodar o Semear Localmente

**Guia rápido para testar o app na sua máquina antes de publicar**

---

## ⚠️ Por Que Preciso de um Servidor?

O Semear usa **módulos JavaScript (ES6)**, que por segurança do navegador, só funcionam através de um servidor web (HTTP/HTTPS), não abrindo o arquivo HTML diretamente.

**Erro comum**: Se abrir `index.html` diretamente, verá erro no console:
```
Access to script at 'file://...' from origin 'null' has been blocked by CORS policy
```

---

## ✅ Opção 1: VS Code + Live Server (RECOMENDADO)

**Mais fácil e você vai precisar para editar código depois!**

### Passo 1: Baixar VS Code
1. Acesse: https://code.visualstudio.com/
2. Baixe para Mac
3. Instale (arraste para Applications)

### Passo 2: Abrir Projeto
1. Abra VS Code
2. **File → Open Folder**
3. Selecione: `/Users/priscilawollmann/CascadeProjects/semear`

### Passo 3: Instalar Live Server
1. Clique no ícone de **Extensions** (quadrado no lado esquerdo)
2. Busque: **"Live Server"**
3. Clique em **Install** na extensão do Ritwick Dey

### Passo 4: Iniciar Servidor
1. No explorador de arquivos (lado esquerdo), clique direito em **index.html**
2. Selecione **"Open with Live Server"**
3. Navegador abre automaticamente em `http://127.0.0.1:5500`

### Passo 5: Testar! 🎉
- O app deve carregar normalmente
- Faça o onboarding completo
- Teste todas as páginas
- Mudanças no código atualizam automaticamente!

**Tempo**: 5-10 minutos

---

## ✅ Opção 2: Python (Se Já Tiver Instalado)

### Verificar se tem Python
Abra o **Terminal** e execute:
```bash
python3 --version
```

Se mostrar uma versão (ex: `Python 3.x.x`), você tem Python!

### Iniciar Servidor
```bash
cd /Users/priscilawollmann/CascadeProjects/semear
python3 -m http.server 8000
```

Você verá:
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

### Acessar
Abra o navegador em: **http://localhost:8000**

### Parar Servidor
No Terminal, pressione **Ctrl + C**

---

## ✅ Opção 3: Node.js (Se Já Tiver Instalado)

### Verificar se tem Node
Abra o **Terminal** e execute:
```bash
node --version
```

Se mostrar uma versão (ex: `v18.x.x`), você tem Node!

### Iniciar Servidor
```bash
cd /Users/priscilawollmann/CascadeProjects/semear
npx serve
```

Você verá:
```
   ┌────────────────────────────────────────┐
   │                                        │
   │   Serving!                             │
   │                                        │
   │   Local:  http://localhost:3000        │
   │                                        │
   └────────────────────────────────────────┘
```

### Acessar
Abra o navegador em: **http://localhost:3000**

### Parar Servidor
No Terminal, pressione **Ctrl + C**

---

## 🧪 Checklist de Testes Locais

Depois que o servidor estiver rodando, teste:

### Funcionalidades Básicas
- [ ] Site carrega sem erros
- [ ] Navegação funciona (clique nos links do menu)
- [ ] Sem erros no console (F12 → Console)

### Onboarding
- [ ] Passo 1: Preencher dados da família
- [ ] Passo 2: Selecionar 1-3 valores
- [ ] Passo 3: Escolher estilos e tempo
- [ ] Passo 4: Confirmar e criar perfil

### Plano Semanal
- [ ] Plano é gerado automaticamente
- [ ] 5 recursos aparecem (atividade, história, ritual, música, livro)
- [ ] Consegue marcar checklist
- [ ] Consegue trocar um recurso
- [ ] Consegue adicionar notas

### Explorador
- [ ] Lista de recursos carrega
- [ ] Filtros funcionam (tipo, idade, valores, estilos)
- [ ] Consegue ver detalhes de um recurso
- [ ] Modal abre e fecha

### Diário
- [ ] Consegue adicionar momento
- [ ] Avaliação por estrelas funciona
- [ ] Consegue adicionar reflexão
- [ ] Progresso aparece

### Configurações
- [ ] Consegue exportar JSON
- [ ] Consegue exportar CSV
- [ ] Consegue limpar dados

### Responsividade
- [ ] Redimensione a janela (simule mobile)
- [ ] Menu funciona em telas pequenas
- [ ] Cards se reorganizam

### Console (F12)
- [ ] Sem erros vermelhos
- [ ] Avisos amarelos são ok (service worker, etc)

---

## 🐛 Problemas Comuns

### "Cannot use import statement outside a module"
**Causa**: Abriu o HTML diretamente (file://)
**Solução**: Use um servidor (opções acima)

### "Failed to load module script"
**Causa**: Caminho errado ou servidor não está rodando
**Solução**: 
- Verifique se está na pasta correta
- Reinicie o servidor

### "Service Worker registration failed"
**Causa**: Service Worker só funciona em HTTPS ou localhost
**Solução**: Normal em desenvolvimento local, ignore

### Página em branco
**Causa**: Erro de JavaScript
**Solução**: 
- Abra console (F12)
- Veja o erro
- Verifique se todos os arquivos existem

### "Address already in use"
**Causa**: Porta já está sendo usada
**Solução**: 
- Feche outros servidores
- Ou use outra porta: `python3 -m http.server 8001`

---

## 📱 Testar em Mobile (Mesma Rede)

Se quiser testar no celular:

### Passo 1: Descobrir IP do Mac
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Procure algo como: `inet 192.168.1.X`

### Passo 2: Acessar do Celular
No celular (conectado na mesma WiFi):
```
http://192.168.1.X:8000
```
(substitua X pelo número do seu IP)

### Passo 3: Testar PWA
- No Chrome Android: Menu → "Adicionar à tela inicial"
- No Safari iOS: Compartilhar → "Adicionar à Tela de Início"

---

## 🎯 Próximos Passos

Depois de testar localmente:

1. ✅ **Tudo funciona?** → Prossiga para deploy!
2. ❌ **Encontrou bugs?** → Anote e corrija antes
3. 💡 **Quer mudar algo?** → Edite e teste novamente

---

## 📝 Dicas

### Desenvolvimento
- Use VS Code + Live Server (atualização automática)
- Mantenha console aberto (F12) para ver erros
- Teste em diferentes navegadores (Chrome, Safari, Firefox)

### Performance
- Abra Network tab (F12) para ver tempo de carregamento
- Deve ser <2s em localhost

### Dados
- localStorage persiste entre recarregamentos
- Para resetar: Settings → Limpar Dados
- Ou: Console → `localStorage.clear()`

---

## 🆘 Ainda Não Conseguiu?

### Opção Mais Simples
1. Baixe VS Code: https://code.visualstudio.com/
2. Abra a pasta do projeto
3. Instale extensão "Live Server"
4. Clique direito em index.html → "Open with Live Server"

**Isso sempre funciona!** ✅

---

## ✨ Resumo Rápido

```bash
# Opção 1: VS Code + Live Server (RECOMENDADO)
# - Baixe VS Code
# - Instale extensão "Live Server"
# - Clique direito em index.html → "Open with Live Server"

# Opção 2: Python (se tiver)
cd /Users/priscilawollmann/CascadeProjects/semear
python3 -m http.server 8000
# Acesse: http://localhost:8000

# Opção 3: Node.js (se tiver)
cd /Users/priscilawollmann/CascadeProjects/semear
npx serve
# Acesse: http://localhost:3000
```

---

**🌱 Pronto para testar seu MVP localmente!**

*Qualquer dúvida, abra o arquivo ABRIR_NO_NAVEGADOR.html para mais instruções*
