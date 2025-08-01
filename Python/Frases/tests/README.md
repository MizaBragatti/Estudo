# SISTEMA DE TESTES REGRESSIVOS

## 📖 Visão Geral

Este sistema de testes regressivos garante que todas as funcionalidades do Gerenciador de Frases permaneçam funcionando após alterações no código.

## 🚀 Como Executar

### Teste Rápido (Recomendado)
```bash
python run_regression_tests.py
```
Executa verificações básicas de funcionalidade.

### Testes Completos
```bash
python tests/test_regression.py
```
Executa toda a suíte de testes regressivos.

### Testes Específicos
```bash
python tests/run_specific_tests.py [tipo]
```

Tipos disponíveis:
- `quick`: Teste rápido (padrão)
- `database`: Testes do banco de dados
- `api`: Testes da API
- `ui`: Testes da interface
- `integration`: Testes de integração
- `all`: Todos os testes

## 📋 Funcionalidades Testadas

### 🗄️ Banco de Dados
- ✅ Criação de tabelas (frases, users)
- ✅ Registro de usuários
- ✅ Autenticação e login
- ✅ CRUD de frases (Criar, Ler, Atualizar, Deletar)
- ✅ Sistema de criptografia/descriptografia
- ✅ Ordenação de frases (original, alfabética, inversa)
- ✅ Busca de frases por termo
- ✅ Constraints de unicidade (frases duplicadas)

### 🌐 API
- ✅ Health check da API
- ✅ Endpoints de frases (GET, POST, PUT, DELETE)
- ✅ Detecção de frases duplicadas
- ✅ Busca via API
- ✅ Autenticação via API
- ✅ Responses padronizados (success/error)

### 🖥️ Interface (UI)
- ✅ Criação de componentes principais
- ✅ Estados dos botões (Adicionar, Atualizar, Excluir)
- ✅ Validação de entrada de dados
- ✅ Gerenciamento de seleções
- ✅ Tela de login funcional
- ✅ Diálogos de confirmação

### 🔗 Integração
- ✅ Funções de compatibilidade (frase_manager ↔ API)
- ✅ Migração para arquitetura de APIs
- ✅ Preservação de funcionalidades existentes
- ✅ Comunicação entre componentes

## 📊 Relatórios

Os testes geram relatórios detalhados incluindo:
- Total de testes executados
- Sucessos vs Falhas
- Tempo de execução
- Detalhes de erros (se houver)

## 🔧 Configuração

### Dependências
```bash
pip install flet requests flask
```

### Variáveis de Ambiente
Os testes usam um banco de dados temporário e não afetam os dados de produção.

## 📅 Quando Executar

### Obrigatório
- ✅ Antes de cada commit importante
- ✅ Antes de releases/deployments
- ✅ Após alterações na API
- ✅ Após mudanças na interface

### Recomendado
- ✅ Após correções de bugs
- ✅ Após adição de novas funcionalidades
- ✅ Semanalmente (automático)

## 🐛 Resolução de Problemas

### Erro: "API não está disponível"
```bash
# Verifique se a porta 5000 está livre
netstat -an | findstr :5000

# Execute manualmente
python api/phrase_api.py
```

### Erro: "Módulo não encontrado"
```bash
# Instale dependências
pip install -r requirements.txt

# Verifique PYTHONPATH
echo $PYTHONPATH
```

### Erro: "Banco de dados bloqueado"
```bash
# Feche outras instâncias da aplicação
# Reinicie o teste
```

## 📂 Estrutura dos Testes

```
tests/
├── test_regression.py      # Testes principais
├── test_ui_regression.py   # Testes de interface
├── test_config.py          # Configurações
├── run_specific_tests.py   # Executor específico
└── README.md              # Esta documentação
```

## 🎯 Exemplos de Uso

### Teste antes de commit
```bash
# Teste rápido
python tests/run_specific_tests.py quick

# Se passou, pode commitar
git add .
git commit -m "feat: nova funcionalidade"
```

### Teste após alteração na API
```bash
# Teste específico da API
python tests/run_specific_tests.py api

# Teste de integração
python tests/run_specific_tests.py integration
```

### Teste completo antes de release
```bash
# Todos os testes
python tests/run_specific_tests.py all

# Gera relatório
python run_regression_tests.py
# Escolha opção 3 para relatório
```

## 📈 Métricas de Sucesso

- ✅ **100% dos testes passando**: Aplicação estável
- ✅ **90-99% passando**: Verificar falhas menores
- ✅ **< 90% passando**: ⚠️ Não fazer deploy!

## 🚀 Integração Contínua

Para automação, adicione ao seu pipeline:

```yaml
# GitHub Actions exemplo
- name: Run Regression Tests
  run: |
    python tests/run_specific_tests.py all
```

## 📞 Suporte

Em caso de dúvidas sobre os testes:
1. Verifique esta documentação
2. Execute teste rápido: `python tests/run_specific_tests.py quick`
3. Analise logs de erro detalhados
4. Verifique se todas as dependências estão instaladas

---

**Lembre-se**: Testes regressivos são sua rede de segurança! 🛡️
