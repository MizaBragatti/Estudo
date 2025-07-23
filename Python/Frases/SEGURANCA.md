# 🔒 Documentação de Segurança - Gerenciador de Frases

## Implementações de Segurança

### 1. **Autenticação de Usuário**
- ✅ Sistema de login obrigatório
- ✅ Senhas com hash seguro (PBKDF2 + SHA256 ou bcrypt)
- ✅ Validação de força da senha (mínimo 6 caracteres)
- ✅ Proteção contra ataques de força bruta (hashing custoso)

### 2. **Criptografia de Dados**
- ✅ Frases armazenadas criptografadas no banco
- ✅ Chave de criptografia única por instalação
- ✅ Descriptografia automática na leitura
- ✅ Arquivo de chave protegido (permissões 600)

### 3. **Proteção do Banco de Dados**
- ✅ Dados sensíveis criptografados
- ✅ Senhas nunca armazenadas em texto claro
- ✅ Transações seguras com rollback em erro
- ✅ Prevenção de SQL injection (prepared statements)

### 4. **Proteção de Arquivos**
- ✅ Chave de criptografia em `.gitignore`
- ✅ Arquivo de chave com permissões restritas
- ✅ Banco de dados local (não exposição web)

## Como Funciona a Segurança

### Fluxo de Autenticação:
1. Usuário insere credenciais
2. Senha é hashada com PBKDF2 (100.000 iterações) + sal único
3. Hash é comparado com valor armazenado
4. Acesso liberado apenas se hash coincidir

### Fluxo de Criptografia:
1. Frase inserida pelo usuário
2. Texto é criptografado com chave única
3. Dados criptografados salvos no banco
4. Na leitura, dados são descriptografados automaticamente

## Melhorias Recomendadas

### Para Segurança Máxima:
1. **Instalar bcrypt**: `pip install bcrypt`
   - Hash de senha mais robusto
   
2. **Criptografia AES** (futuro):
   ```python
   pip install cryptography
   ```
   - Substituir XOR por AES-256

3. **Timeout de Sessão**:
   - Logout automático após inatividade
   
4. **Log de Auditoria**:
   - Registrar tentativas de login
   - Rastrear alterações nos dados

5. **Backup Seguro**:
   - Backup automático criptografado
   - Verificação de integridade

## Avisos Importantes

⚠️ **NUNCA commitar:**
- Arquivo `.encryption_key`
- Arquivos `*.key`
- Banco de dados com dados reais

⚠️ **Backup da chave:**
- Faça backup seguro do arquivo `.encryption_key`
- Sem a chave, os dados são irrecuperáveis

⚠️ **Primeira execução:**
- Primeira vez que rodar, será criada chave única
- Usuário admin deve ser criado imediatamente

## Status de Implementação

✅ **Implementado:**
- Autenticação com hash seguro
- Criptografia básica de dados
- Proteção de arquivos sensíveis
- Validação de senhas

🔄 **Em desenvolvimento:**
- Criptografia AES mais robusta
- Sistema de auditoria
- Timeout de sessão

📋 **Planejado:**
- Backup automático
- Recuperação de senha
- Autenticação em dois fatores

---
**Última atualização:** $(Get-Date -Format "yyyy-MM-dd HH:mm")
