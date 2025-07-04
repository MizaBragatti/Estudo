# frase_manager.py

import sqlite3
import os
import sys

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

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
    return conn

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
    """Adiciona uma nova frase ao banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO frases (texto) VALUES (?)", (frase,))
        conn.commit()
        return True
    except sqlite3.IntegrityError: # Captura erro de UNIQUE (frase duplicada)
        return False
    finally:
        conn.close()

def ler_frases(ordenacao="original"):
    """Lê todas as frases do banco de dados com opção de ordenação."""
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
    frases = [row['texto'] for row in cursor.fetchall()]
    conn.close()
    return frases

def remover_frase(frase_para_remover):
    """Remove uma frase do banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM frases WHERE texto = ?", (frase_para_remover,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def atualizar_frase(frase_antiga, nova_frase):
    """Atualiza uma frase existente no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE frases SET texto = ? WHERE texto = ?", (nova_frase, frase_antiga))
        rows_affected = cursor.rowcount
        conn.commit()
        return rows_affected > 0
    except sqlite3.IntegrityError: # Captura erro se a nova_frase já existir
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