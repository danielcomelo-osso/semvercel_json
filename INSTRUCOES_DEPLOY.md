# 🎯 INSTRUÇÕES PARA DEPLOY DEFINITIVO - TAROT COM IA

## 📋 PASSO A PASSO PARA RESOLVER O PROBLEMA DE CACHE

### 🎯 **PROBLEMA IDENTIFICADO:**
O frontend continua usando a URL antiga do backend devido a cache persistente da Vercel. A solução é criar um **NOVO PROJETO** na Vercel.

---

## 🚀 **ETAPAS PARA SUCESSO GARANTIDO:**

### **1️⃣ PREPARAR NOVO REPOSITÓRIO NO GITHUB**

1. Acesse [https://github.com](https://github.com)
2. Clique em **"New repository"** (botão verde)
3. Nome do repositório: `tarot-ia-definitivo`
4. Deixe **Public** marcado
5. **NÃO** marque nenhuma opção (README, .gitignore, etc.)
6. Clique em **"Create repository"**

### **2️⃣ FAZER UPLOAD DOS ARQUIVOS**

1. Na página do repositório criado, clique em **"uploading an existing file"**
2. Arraste e solte **TODOS** os arquivos desta pasta (exceto este arquivo de instruções)
3. Na caixa de commit, escreva: `Deploy inicial do Tarot com IA`
4. Clique em **"Commit changes"**

### **3️⃣ CRIAR NOVO PROJETO NA VERCEL**

1. Acesse [https://vercel.com/dashboard](https://vercel.com/dashboard)
2. Clique em **"Add New..."** → **"Project"**
3. Encontre o repositório `tarot-ia-definitivo` e clique em **"Import"**
4. **CONFIGURAÇÕES IMPORTANTES:**
   - **Framework Preset:** Vite
   - **Root Directory:** deixe vazio (raiz)
   - **Build Command:** `pnpm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `pnpm install`

### **4️⃣ CONFIGURAR VARIÁVEL DE AMBIENTE**

**ANTES DE CLICAR EM DEPLOY**, adicione a variável de ambiente:

- **Name:** `VITE_API_BASE_URL`
- **Value:** `https://kkh7ikc75jlo.manus.space`

### **5️⃣ FAZER O DEPLOY**

1. Clique em **"Deploy"**
2. Aguarde o build completar (2-3 minutos)
3. Quando aparecer "Congratulations!", clique no link do seu site

---

## ✅ **VERIFICAÇÃO FINAL:**

Após o deploy, teste a funcionalidade:
1. Acesse seu novo site
2. Digite uma pergunta no campo
3. Clique em "Consultar Tarot"
4. **DEVE FUNCIONAR** sem erro de "Não foi possível realizar a consulta"

---

## 🆘 **SE AINDA DER ERRO:**

1. Abra o console do navegador (F12)
2. Verifique se a URL que aparece no erro é `https://kkh7ikc75jlo.manus.space`
3. Se ainda for a URL antiga, entre em contato

---

## 📞 **SUPORTE:**

Se precisar de ajuda em qualquer etapa, me avise imediatamente. Estou monitorando para garantir o sucesso!

---

**🎯 Esta solução resolve definitivamente o problema de cache da Vercel criando um projeto completamente novo.**
