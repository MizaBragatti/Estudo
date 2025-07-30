# 🔓 GUIA PARA TESTAR FRASES DESCRIPTOGRAFADAS NO INSOMNIA

## 🎯 PROBLEMA RESOLVIDO
As frases estavam sendo retornadas criptografadas pela API. Implementei correções para retornar automaticamente as frases descriptografadas.

## ✅ CORREÇÕES IMPLEMENTADAS

### 🔧 **Novas Funções no frase_manager.py**
1. **`ler_frases_completas()`** - Retorna frases com todos os dados descriptografados
2. **`buscar_frases_completas()`** - Busca frases descriptografadas

### 🔄 **API Atualizada**
- Endpoint `/api/v1/phrases` agora usa as novas funções
- Endpoint `/api/v1/stats` também atualizado
- Frases são descriptografadas automaticamente antes da resposta

---

## 🧪 COMO TESTAR NO INSOMNIA

### **1. Iniciar a API**
```bash
python api/phrase_api.py
```
A API estará disponível em: `http://localhost:5000`

### **2. Fazer Login (Obter user_id)**

**Request:**
```
POST http://localhost:5000/api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

**Response Esperada:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "username": "admin",
    "authenticated": true
  },
  "message": "Login realizado com sucesso"
}
```

**⚠️ IMPORTANTE**: Anote o `user_id` da resposta!

### **3. Listar Frases (Descriptografadas)**

**Request:**
```
GET http://localhost:5000/api/v1/phrases?user_id=1
```

**Response Esperada (ANTES - criptografadas):**
```json
{
  "data": {
    "phrases": [
      {
        "id": 1,
        "text": "gAAAAABm2K7X8sZ9vQJ4K5...", // ❌ Criptografada
        "user_id": 1
      }
    ]
  }
}
```

**Response Esperada (AGORA - descriptografadas):**
```json
{
  "data": {
    "phrases": [
      {
        "id": 1,
        "text": "Seja a mudança que você quer ver no mundo", // ✅ Descriptografada
        "user_id": 1,
        "creation_date": "2025-07-28 10:30:00",
        "is_encrypted": 1
      }
    ]
  }
}
```

### **4. Buscar Frases (Descriptografadas)**

**Request:**
```
GET http://localhost:5000/api/v1/phrases?user_id=1&search=motivação
```

**Response:** Frases filtradas e descriptografadas

### **5. Estatísticas (Descriptografadas)**

**Request:**
```
GET http://localhost:5000/api/v1/stats?user_id=1
```

**Response:** Estatísticas baseadas em texto descriptografado

---

## 🔄 ENDPOINTS PARA TESTAR

### **📋 Coleção Completa para Insomnia:**

```json
{
  "name": "Phrase API - Descriptografadas",
  "requests": [
    {
      "name": "1. Health Check",
      "method": "GET",
      "url": "http://localhost:5000/api/v1/health"
    },
    {
      "name": "2. Login",
      "method": "POST",
      "url": "http://localhost:5000/api/v1/auth/login",
      "body": {
        "username": "admin",
        "password": "admin"
      }
    },
    {
      "name": "3. Listar Frases (Descriptografadas)",
      "method": "GET",
      "url": "http://localhost:5000/api/v1/phrases?user_id=1"
    },
    {
      "name": "4. Buscar Frases",
      "method": "GET",
      "url": "http://localhost:5000/api/v1/phrases?user_id=1&search=motivação"
    },
    {
      "name": "5. Adicionar Frase",
      "method": "POST",
      "url": "http://localhost:5000/api/v1/phrases",
      "body": {
        "text": "Nova frase de teste via API",
        "user_id": 1
      }
    },
    {
      "name": "6. Estatísticas",
      "method": "GET", 
      "url": "http://localhost:5000/api/v1/stats?user_id=1"
    }
  ]
}
```

---

## ✅ VERIFICAÇÃO VISUAL

### **🔍 Como Saber se Está Funcionando:**

**❌ ANTES (Criptografada):**
```
"text": "gAAAAABm2K7X8sZ9vQJ4K5mL3nJ8..."
```

**✅ AGORA (Descriptografada):**
```
"text": "Seja a mudança que você quer ver no mundo"
```

### **🎯 Pontos de Verificação:**
1. ✅ Campo `text` deve conter texto legível
2. ✅ Sem caracteres como `=`, `+`, base64
3. ✅ Texto deve fazer sentido
4. ✅ Busca deve funcionar corretamente
5. ✅ Estatísticas devem mostrar textos reais

---

## 🛠️ TROUBLESHOOTING

### **Problema: API não inicia**
```bash
# Verificar dependências
pip install flask flask-cors requests

# Testar importação
python -c "from api.phrase_api import app; print('OK')"
```

### **Problema: Ainda retorna criptografadas**
```bash
# Verificar se as funções existem
python -c "import frase_manager; print(hasattr(frase_manager, 'ler_frases_completas'))"

# Deve retornar: True
```

### **Problema: Usuário não encontrado**
```bash
# Registrar usuário admin
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'
```

---

## 📋 COMANDOS RÁPIDOS PARA TESTE

### **Terminal 1 - Iniciar API:**
```bash
cd "c:\Users\Miza\Documents\Estudo\Python\Frases"
python api/phrase_api.py
```

### **Terminal 2 - Teste com curl:**
```bash
# Health check
curl http://localhost:5000/api/v1/health

# Login e obter user_id
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Listar frases descriptografadas
curl "http://localhost:5000/api/v1/phrases?user_id=1"
```

---

## 🎉 RESULTADO ESPERADO

Após essas correções, todas as frases retornadas pela API devem estar **completamente descriptografadas** e **legíveis**, mantendo a criptografia apenas no banco de dados para segurança.

**Status**: ✅ **PROBLEMA RESOLVIDO**  
**Data**: 28 de julho de 2025  
**Versão da API**: 1.0.1 (com descriptografia automática)
