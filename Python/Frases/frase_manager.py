# frase_manager.py

import sqlite3
import os
import sys
import hashlib # Para hash de senhas
import secrets  # Para geração de sal/tokens seguros
import base64   # Para codificação de dados
try:
    import bcrypt   # Hash mais seguro para senhas
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    print("Aviso: bcrypt não está disponível. Usando SHA256 (menos seguro).")

# --- Configuração do Banco de Dados ---
# Determina o caminho base para o arquivo do banco de dados
if getattr(sys, 'frozen', False):
    # Se estiver em um executável PyInstaller, o DB estará ao lado do .exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Se estiver rodando como um script Python normal, o DB estará na pasta do script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = "frases.db" # Nome do arquivo do banco de dados
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

# Chave de criptografia (em produção, deve ser gerada e armazenada com segurança)
ENCRYPTION_KEY_FILE = os.path.join(BASE_DIR, ".encryption_key")

def get_or_create_encryption_key():
    """
    Obtém ou cria uma chave de criptografia para proteger os dados.
    """
    if os.path.exists(ENCRYPTION_KEY_FILE):
        with open(ENCRYPTION_KEY_FILE, 'rb') as f:
            return f.read()
    else:
        # Gera uma nova chave
        key = secrets.token_bytes(32)  # 256 bits
        with open(ENCRYPTION_KEY_FILE, 'wb') as f:
            f.write(key)
        # Torna o arquivo somente leitura
        os.chmod(ENCRYPTION_KEY_FILE, 0o600)
        return key

ENCRYPTION_KEY = get_or_create_encryption_key()

def encrypt_text(text):
    """
    Criptografa um texto usando XOR simples (para demonstração).
    Em produção, use AES ou outra criptografia mais robusta.
    """
    if not text:
        return text
    
    # XOR simples com a chave
    encrypted = bytearray()
    key_len = len(ENCRYPTION_KEY)
    
    for i, char in enumerate(text.encode('utf-8')):
        key_char = ENCRYPTION_KEY[i % key_len]
        encrypted.append(char ^ key_char)
    
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_text(encrypted_text):
    """
    Descriptografa um texto.
    Se o texto não estiver criptografado (compatibilidade), retorna como está.
    """
    if not encrypted_text:
        return encrypted_text
    
    # Verifica se o texto parece estar criptografado (base64)
    if not is_text_encrypted(encrypted_text):
        # Se não parece criptografado, retorna como está (compatibilidade)
        return encrypted_text
    
    try:
        encrypted_bytes = base64.b64decode(encrypted_text.encode('utf-8'))
        decrypted = bytearray()
        key_len = len(ENCRYPTION_KEY)
        
        for i, byte in enumerate(encrypted_bytes):
            key_char = ENCRYPTION_KEY[i % key_len]
            decrypted.append(byte ^ key_char)
        
        return decrypted.decode('utf-8')
    except:
        # Se houver erro na descriptografia, retorna o texto original (compatibilidade)
        return encrypted_text

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
    return conn

# --- Funções de Gerenciamento de Frases (Mantenha as existentes) ---

def create_table():
    """Cria a tabela 'frases' se ela ainda não existir."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS frases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL UNIQUE,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Garante que a tabela seja criada na primeira vez que o módulo é importado/executado
create_table()

def adicionar_frase(frase):
    """Adiciona uma nova frase ao banco de dados (criptografada)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Criptografa a frase antes de armazenar
        frase_criptografada = encrypt_text(frase)
        cursor.execute("INSERT INTO frases (texto) VALUES (?)", (frase_criptografada,))
        conn.commit()
        return True
    except sqlite3.IntegrityError: # Captura erro de UNIQUE (frase duplicada)
        return False
    finally:
        conn.close()

def ler_frases(ordenacao="original"):
    """Lê todas as frases do banco de dados com opção de ordenação (descriptografadas)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT texto FROM frases"
    
    if ordenacao == "alfabetica":
        query += " ORDER BY texto ASC"
    elif ordenacao == "alfabetica_inversa":
        query += " ORDER BY texto DESC"
    elif ordenacao == "original_inversa":
        query += " ORDER BY data_criacao DESC"
    else: # "original" ou qualquer outra coisa
        query += " ORDER BY data_criacao ASC"

    cursor.execute(query)
    frases_criptografadas = [row['texto'] for row in cursor.fetchall()]
    conn.close()
    
    # Descriptografa as frases antes de retornar
    frases_descriptografadas = [decrypt_text(frase) for frase in frases_criptografadas]
    
    # Se a ordenação for alfabética, precisa reordenar após descriptografar
    if ordenacao == "alfabetica":
        frases_descriptografadas.sort()
    elif ordenacao == "alfabetica_inversa":
        frases_descriptografadas.sort(reverse=True)
    
    return frases_descriptografadas

def remover_frase(frase_para_remover):
    """Remove uma frase do banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Criptografa a frase para encontrar no banco
    frase_criptografada = encrypt_text(frase_para_remover)
    cursor.execute("DELETE FROM frases WHERE texto = ?", (frase_criptografada,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def remover_multiplas_frases(frases_para_remover):
    """Remove múltiplas frases do banco de dados."""
    if not frases_para_remover:
        return 0
    
    conn = get_db_connection()
    cursor = conn.cursor()
    total_removed = 0
    
    try:
        for frase in frases_para_remover:
            # Criptografa cada frase para encontrar no banco
            frase_criptografada = encrypt_text(frase)
            cursor.execute("DELETE FROM frases WHERE texto = ?", (frase_criptografada,))
            total_removed += cursor.rowcount
        conn.commit()
    except Exception as e:
        conn.rollback()
        total_removed = 0
    finally:
        conn.close()
    
    return total_removed


def buscar_frases(termo_busca, ordenacao="original"):
    """
    Busca frases que contenham o termo especificado.
    
    Args:
        termo_busca (str): Termo a ser buscado nas frases
        ordenacao (str): Tipo de ordenação ("original", "alfabetica", etc.)
    
    Returns:
        list: Lista de frases que contêm o termo de busca
    """
    if not termo_busca or termo_busca.strip() == "":
        # Se não há termo de busca, retorna todas as frases
        return ler_frases(ordenacao)
    
    # Obtém todas as frases
    todas_frases = ler_frases(ordenacao)
    
    # Filtra frases que contêm o termo de busca (case-insensitive)
    termo_lower = termo_busca.lower().strip()
    frases_encontradas = [
        frase for frase in todas_frases 
        if termo_lower in frase.lower()
    ]
    
    return frases_encontradas

def atualizar_frase(old_texto, new_texto):
    """Atualiza uma frase no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Primeiro, verifica se a nova frase já existe para evitar duplicatas
        new_texto_criptografado = encrypt_text(new_texto)
        cursor.execute("SELECT COUNT(*) FROM frases WHERE texto = ?", (new_texto_criptografado,))
        if cursor.fetchone()[0] > 0 and new_texto != old_texto:
            # Se a nova frase já existe e é diferente da antiga, não permite a atualização
            return False 

        # Atualiza a frase no banco de dados
        old_texto_criptografado = encrypt_text(old_texto)
        cursor.execute("UPDATE frases SET texto = ? WHERE texto = ?", (new_texto_criptografado, old_texto_criptografado))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao atualizar frase: {e}")
        return False
    finally:
        conn.close()

def importar_frases_de_arquivo(caminho_arquivo):
    """Importa frases de um arquivo de texto para o banco de dados."""
    total_lidas = 0
    total_adicionadas = 0
    total_duplicadas = 0

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                total_lidas += 1
                frase = linha.strip()
                if frase:
                    if adicionar_frase(frase): # Usa a função de adicionar_frase que já lida com duplicatas
                        total_adicionadas += 1
                    else:
                        total_duplicadas += 1
        return total_lidas, total_adicionadas, total_duplicadas
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return 0, 0, 0
    except Exception as e:
        print(f"Erro ao importar frases do arquivo: {e}")
        return 0, 0, 0

def exportar_frases_para_arquivo(caminho_arquivo, ordenacao="original"):
    """Exporta todas as frases do banco de dados para um arquivo de texto."""
    try:
        frases = ler_frases(ordenacao)
        
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            for frase in frases:
                f.write(frase + "\n")
        
        return len(frases)
    except Exception as e:
        print(f"Erro ao exportar frases para arquivo: {e}")
        return 0


# --- Funções de Gerenciamento de Usuários (NOVAS) ---

def hash_password(password, salt=None):
    """
    Gera o hash de uma senha com sal para maior segurança.
    Se bcrypt estiver disponível, usa bcrypt. Caso contrário, usa PBKDF2 com SHA256.
    """
    if not password:
        return ""
    
    try:
        if BCRYPT_AVAILABLE:
            # Usar bcrypt (recomendado)
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            # Fallback para PBKDF2 com SHA256 (mais seguro que SHA256 simples)
            if salt is None:
                salt = secrets.token_hex(16)  # Gera sal aleatório
            
            # PBKDF2 com 100.000 iterações
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
            return f"{salt}:{base64.b64encode(key).decode('utf-8')}"
    except Exception as e:
        print(f"Erro ao gerar hash da senha: {e}")
        # Fallback para SHA256 simples em caso de erro
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password, hashed_password):
    """
    Verifica se a senha corresponde ao hash armazenado.
    Suporta múltiplos formatos para compatibilidade.
    """
    if not password or not hashed_password:
        return False
    
    try:
        if BCRYPT_AVAILABLE and not ':' in hashed_password and len(hashed_password) == 60:
            # Hash do bcrypt (tem 60 caracteres)
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        elif ':' in hashed_password:
            # Formato PBKDF2: "salt:hash"
            try:
                salt, stored_hash = hashed_password.split(':', 1)
                # Verifica se o sal é válido (não vazio)
                if not salt or not stored_hash:
                    return False
                key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
                return base64.b64encode(key).decode('utf-8') == stored_hash
            except Exception as e:
                print(f"Erro ao verificar PBKDF2: {e}")
                return False
        else:
            # Formato SHA256 legado (compatibilidade)
            return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed_password
    except Exception as e:
        print(f"Erro geral na verificação de senha: {e}")
        return False

def create_users_table():
    """Cria a tabela 'users' se ela ainda não existir."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Garante que a tabela de usuários também seja criada
create_users_table()

def register_user(username, password):
    """
    Tenta registrar um novo usuário.
    Retorna True em caso de sucesso, False se o usuário já existir.
    """
    if len(password) < 6:
        return False, "Senha deve ter pelo menos 6 caracteres"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True, "Usuário registrado com sucesso"
    except sqlite3.IntegrityError: # Usuário já existe
        return False, "Usuário já existe"
    finally:
        conn.close()

def authenticate_user(username, password):
    """
    Autentica um usuário.
    Retorna True se as credenciais estiverem corretas, False caso contrário.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    conn.close()

    if record:
        stored_password_hash = record['password_hash']
        return verify_password(password, stored_password_hash)
    return False

def migrate_existing_phrases():
    """
    Migra frases existentes (não criptografadas) para o formato criptografado.
    Esta função deve ser executada apenas uma vez após implementar a criptografia.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Busca todas as frases
        cursor.execute("SELECT id, texto FROM frases")
        frases = cursor.fetchall()
        
        migrated_count = 0
        for frase_row in frases:
            frase_id = frase_row['id']
            texto_atual = frase_row['texto']
            
            # Verifica se a frase já está criptografada
            # (frases criptografadas geralmente são base64 e não têm caracteres legíveis)
            try:
                # Tenta descriptografar - se funcionar, já está criptografada
                decrypt_text(texto_atual)
                # Se chegou aqui, a descriptografia funcionou, então já está criptografada
                continue
            except:
                # Se deu erro na descriptografia, provavelmente é texto puro
                # Vamos criptografar
                texto_criptografado = encrypt_text(texto_atual)
                cursor.execute("UPDATE frases SET texto = ? WHERE id = ?", (texto_criptografado, frase_id))
                migrated_count += 1
        
        conn.commit()
        print(f"Migração concluída: {migrated_count} frases migradas para formato criptografado.")
        return migrated_count
        
    except Exception as e:
        conn.rollback()
        print(f"Erro durante a migração: {e}")
        return 0
    finally:
        conn.close()

def debug_user_passwords():
    """
    Função de debug para verificar os hashes de senha armazenados.
    Útil para identificar problemas com formato de senhas.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT username, password_hash FROM users")
        users = cursor.fetchall()
        
        print("\n=== DEBUG: Hashes de senha armazenados ===")
        for user in users:
            username = user['username']
            password_hash = user['password_hash']
            hash_length = len(password_hash)
            has_colon = ':' in password_hash
            
            if has_colon:
                hash_type = "PBKDF2 (novo formato)"
            elif hash_length == 60:
                hash_type = "bcrypt"
            elif hash_length == 64:
                hash_type = "SHA256 (formato antigo)"
            else:
                hash_type = f"Desconhecido (tamanho: {hash_length})"
            
            print(f"Usuário: {username}")
            print(f"  Tipo: {hash_type}")
            print(f"  Tamanho: {hash_length}")
            print(f"  Tem ':': {has_colon}")
            print(f"  Hash: {password_hash[:20]}...")
            print()
            
    except Exception as e:
        print(f"Erro no debug: {e}")
    finally:
        conn.close()

def migrate_user_passwords():
    """
    Migra senhas de usuários existentes para o novo formato com sal.
    Esta função deve ser executada apenas uma vez.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Busca todos os usuários
        cursor.execute("SELECT id, username, password_hash FROM users")
        users = cursor.fetchall()
        
        migrated_count = 0
        for user_row in users:
            user_id = user_row['id']
            username = user_row['username']
            current_hash = user_row['password_hash']
            
            # Verifica se a senha já está no novo formato (contém ':' ou é bcrypt)
            if ':' in current_hash or (BCRYPT_AVAILABLE and len(current_hash) == 60):
                continue  # Já está no novo formato
            
            # Senha está no formato SHA256 antigo - não podemos migrar automaticamente
            # pois não temos a senha original
            print(f"Aviso: Usuário '{username}' tem senha no formato antigo.")
            print(f"O usuário precisará fazer login novamente ou ser re-registrado.")
            
        print(f"Verificação de migração de senhas concluída.")
        return migrated_count
        
    except Exception as e:
        print(f"Erro durante a verificação de migração de senhas: {e}")
        return 0
    finally:
        conn.close()

def is_text_encrypted(text):
    """
    Verifica se um texto está criptografado verificando se é base64 válido.
    """
    if not text or len(text) < 4:
        return False
    
    try:
        # Verifica se é base64 válido
        decoded = base64.b64decode(text.encode('utf-8'))
        # Se conseguiu decodificar e tem tamanho razoável, provavelmente é criptografado
        return len(decoded) > 0
    except:
        return False

# --- Inicialização no módulo ---
create_table() # Garante que a tabela de frases exista
create_users_table() # Garante que a tabela de usuários exista

# Executa migração automática de frases existentes (apenas uma vez)
try:
    # Verifica se existe um arquivo de flag indicando que a migração já foi feita
    migration_flag_file = os.path.join(BASE_DIR, ".migration_done")
    if not os.path.exists(migration_flag_file):
        print("Primeira execução com criptografia - migrando dados existentes...")
        
        # Migra frases
        migrated_phrases = migrate_existing_phrases()
        
        # Verifica senhas de usuários
        migrate_user_passwords()
        
        if migrated_phrases >= 0:  # Migração bem-sucedida (mesmo que 0 frases)
            # Cria arquivo de flag para não repetir a migração
            with open(migration_flag_file, 'w') as f:
                f.write("Migration completed")
            print("Migração concluída com sucesso!")
except Exception as e:
    print(f"Aviso: Erro durante migração automática: {e}")
    print("Você pode tentar executar a migração manualmente ou recriar usuários.")