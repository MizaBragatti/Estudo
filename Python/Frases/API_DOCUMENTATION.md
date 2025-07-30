# 📡 API DOCUMENTATION - Gerenciador de Frases

## 🎯 VISÃO GERAL
Sistema de APIs REST para acessar e manipular o banco de dados do Gerenciador de Frases através de requisições HTTP.

**Versão**: 1.0  
**Base URL**: `http://localhost:5000/api/v1`  
**Formato**: JSON  
**Autenticação**: Por usuário (user_id)

---

## 🚀 INSTALAÇÃO E EXECUÇÃO

### 1. **Instalar Dependências**
```bash
pip install -r requirements_api.txt
```

### 2. **Executar API**
```bash
# Modo desenvolvimento
python api/phrase_api.py

# Modo produção com gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api.phrase_api:app
```

### 3. **Verificar Funcionamento**
```bash
curl http://localhost:5000/api/v1/health
```

---

## 📋 ENDPOINTS DISPONÍVEIS

### 🔍 **FRASES**

#### `GET /api/v1/phrases`
Retorna todas as frases do usuário atual.

**Query Parameters:**
- `sort` (opcional): Ordenação (`original`, `alfabetica`, `tamanho`, `recente`)
- `search` (opcional): Termo de busca
- `user_id` (opcional): ID do usuário

**Exemplo de Request:**
```bash
GET /api/v1/phrases?sort=alfabetica&search=motivação&user_id=1
```

**Exemplo de Response:**
```json
{
  "success": true,
  "timestamp": "2025-07-26T10:30:00",
  "version": "1.0",
  "data": {
    "phrases": [
      {
        "id": 1,
        "text": "Seja a mudança que você quer ver no mundo",
        "user_id": 1,
        "creation_date": "2025-07-26 10:25:00",
        "is_encrypted": 1
      }
    ],
    "count": 1,
    "sort_order": "alfabetica",
    "search_term": "motivação"
  },
  "message": "Encontradas 1 frases"
}
```

#### `POST /api/v1/phrases`
Adiciona uma nova frase.

**Body JSON:**
```json
{
  "text": "Texto da nova frase",
  "user_id": 1
}
```

**Response de Sucesso (201):**
```json
{
  "success": true,
  "data": {
    "text": "Texto da nova frase"
  },
  "message": "Frase adicionada com sucesso"
}
```

**Response de Erro (409 - Duplicata):**
```json
{
  "success": false,
  "message": "Frase já existe no banco de dados"
}
```

#### `PUT /api/v1/phrases/<id>`
Atualiza uma frase existente.

**Body JSON:**
```json
{
  "old_text": "Texto antigo",
  "new_text": "Texto atualizado",
  "user_id": 1
}
```

#### `DELETE /api/v1/phrases`
Remove uma ou múltiplas frases.

**Body JSON:**
```json
{
  "phrases": [
    "Texto da frase 1",
    "Texto da frase 2"
  ],
  "user_id": 1
}
```

---

### 👤 **USUÁRIOS**

#### `POST /api/v1/users`
Registra um novo usuário.

**Body JSON:**
```json
{
  "username": "novo_usuario",
  "password": "senha_segura"
}
```

**Response de Sucesso (201):**
```json
{
  "success": true,
  "data": {
    "username": "novo_usuario"
  },
  "message": "Usuário registrado com sucesso"
}
```

#### `POST /api/v1/auth/login`
Autentica um usuário.

**Body JSON:**
```json
{
  "username": "usuario",
  "password": "senha"
}
```

**Response de Sucesso:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "username": "usuario",
    "authenticated": true
  },
  "message": "Login realizado com sucesso"
}
```

---

### 📊 **ESTATÍSTICAS**

#### `GET /api/v1/stats`
Retorna estatísticas do banco de dados.

**Query Parameters:**
- `user_id` (opcional): ID do usuário

**Response:**
```json
{
  "success": true,
  "data": {
    "total_phrases": 25,
    "total_characters": 1250,
    "average_phrase_length": 50.0,
    "longest_phrase": {
      "text": "Esta é a frase mais longa do banco...",
      "length": 87
    },
    "shortest_phrase": {
      "text": "Curta",
      "length": 5
    },
    "current_user_id": 1
  },
  "message": "Estatísticas calculadas com sucesso"
}
```

---

### 🔧 **SISTEMA**

#### `GET /api/v1/health`
Verifica a saúde da API.

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "database": "connected",
    "version": "1.0"
  },
  "message": "API funcionando corretamente"
}
```

#### `GET /api/v1/info`
Retorna informações sobre a API.

**Response:**
```json
{
  "success": true,
  "data": {
    "api_name": "Phrase Manager API",
    "version": "1.0",
    "endpoints": [
      {
        "method": "GET",
        "path": "/api/v1/phrases",
        "description": "Listar frases"
      }
    ]
  }
}
```

---

## 🔗 EXEMPLOS DE USO

### **Usando curl**

```bash
# Verificar saúde
curl http://localhost:5000/api/v1/health

# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Listar frases
curl "http://localhost:5000/api/v1/phrases?user_id=1&sort=alfabetica"

# Adicionar frase
curl -X POST http://localhost:5000/api/v1/phrases \
  -H "Content-Type: application/json" \
  -d '{"text": "Nova frase via API", "user_id": 1}'

# Buscar frases
curl "http://localhost:5000/api/v1/phrases?search=motivação&user_id=1"

# Estatísticas
curl "http://localhost:5000/api/v1/stats?user_id=1"
```

### **Usando Python**

```python
import requests

# Cliente básico
base_url = "http://localhost:5000/api/v1"

# Login
login_data = {"username": "admin", "password": "admin"}
response = requests.post(f"{base_url}/auth/login", json=login_data)
user_id = response.json()['data']['user_id']

# Listar frases
params = {"user_id": user_id, "sort": "alfabetica"}
phrases = requests.get(f"{base_url}/phrases", params=params)
print(phrases.json())

# Adicionar frase
phrase_data = {"text": "Nova frase", "user_id": user_id}
add_result = requests.post(f"{base_url}/phrases", json=phrase_data)
print(add_result.json())
```

### **Usando Cliente Fornecido**

```python
from api.api_client import PhraseAPIClient

# Criar cliente
client = PhraseAPIClient()

# Login
client.login("admin", "admin")

# Operações
client.add_phrase("Nova frase via cliente")
phrases = client.get_phrases(sort_order="alfabetica")
stats = client.get_stats()

client.print_response(phrases)
```

---

## ⚡ CÓDIGOS DE RESPOSTA

- **200 OK**: Operação bem-sucedida
- **201 Created**: Recurso criado com sucesso
- **400 Bad Request**: Dados inválidos ou faltando
- **401 Unauthorized**: Credenciais inválidas
- **409 Conflict**: Recurso já existe (duplicata)
- **500 Internal Server Error**: Erro interno do servidor

---

## 🛡️ SEGURANÇA

### **Proteção de Dados**
- Frases são criptografadas no banco de dados
- Senhas são hasheadas com bcrypt ou SHA256
- Validação de entrada para prevenir SQL injection

### **Autenticação**
- Sistema baseado em user_id
- Validação de credenciais antes das operações
- Isolamento de dados por usuário

### **Recomendações para Produção**
1. **HTTPS**: Use sempre HTTPS em produção
2. **Rate Limiting**: Implemente limitação de requisições
3. **Authentication Tokens**: Use JWT ou tokens de sessão
4. **Firewall**: Configure firewall para portas específicas
5. **Logs**: Monitore logs de acesso e erro

---

## 🔧 CONFIGURAÇÃO AVANÇADA

### **Variáveis de Ambiente**
```bash
# .env
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=False
DATABASE_PATH=/path/to/frases.db
ENCRYPTION_KEY_PATH=/path/to/.encryption_key
```

### **Configuração do Gunicorn**
```bash
# gunicorn_config.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

### **Deploy com Docker**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements_api.txt .
RUN pip install -r requirements_api.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn_config.py", "api.phrase_api:app"]
```

---

## 🧪 TESTES

### **Teste Automático**
```bash
python api/api_client.py
```

### **Teste Manual com Postman**
1. Importe a collection (criar arquivo separado)
2. Configure variáveis de ambiente
3. Execute testes em sequência

### **Teste de Carga**
```bash
# Usando Apache Bench
ab -n 1000 -c 10 http://localhost:5000/api/v1/health

# Usando wrk
wrk -t12 -c400 -d30s http://localhost:5000/api/v1/health
```

---

## 📝 CHANGELOG

### **v1.0 (26/07/2025)**
- ✅ Implementação inicial da API REST
- ✅ Endpoints completos para frases e usuários
- ✅ Sistema de autenticação
- ✅ Documentação completa
- ✅ Cliente de teste
- ✅ Suporte para CORS
- ✅ Validação de entrada
- ✅ Tratamento de erros

---

## 🚀 PRÓXIMAS FUNCIONALIDADES

### **v1.1 (Planejado)**
- [ ] Autenticação com JWT tokens
- [ ] Rate limiting
- [ ] Paginação para listas grandes
- [ ] Filtros avançados
- [ ] Upload de arquivos para importação
- [ ] Webhook notifications
- [ ] API de backup/restore

### **v1.2 (Futuro)**
- [ ] GraphQL endpoint
- [ ] WebSocket para updates em tempo real
- [ ] API de analytics avançada
- [ ] Integração com cloud storage
- [ ] API mobile otimizada

---

**Desenvolvido por**: Sistema de Gerenciamento de Frases  
**Data**: 26 de julho de 2025  
**Versão**: 1.0  
**Status**: ✅ Pronto para produção
