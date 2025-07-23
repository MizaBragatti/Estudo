#!/usr/bin/env python3
"""
Script para verificar a estrutura completa do banco de dados.
"""

import sqlite3
import sys
import os

def verificar_banco():
    """Verifica a estrutura completa do banco de dados."""
    print("=== VERIFICAÇÃO COMPLETA DO BANCO DE DADOS ===")
    print()
    
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect('frases.db')
        cursor = conn.cursor()
        
        # Lista todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = cursor.fetchall()
        
        print(f"📊 Tabelas encontradas: {len(tabelas)}")
        print()
        
        for tabela in tabelas:
            nome_tabela = tabela[0]
            print(f"--- TABELA: {nome_tabela} ---")
            
            # Mostra a estrutura da tabela
            cursor.execute(f"PRAGMA table_info({nome_tabela})")
            colunas = cursor.fetchall()
            
            print("Colunas:")
            for coluna in colunas:
                print(f"  - {coluna[1]} ({coluna[2]}) {'NOT NULL' if coluna[3] else 'NULL'}")
            
            # Conta registros
            cursor.execute(f"SELECT COUNT(*) FROM {nome_tabela}")
            count = cursor.fetchone()[0]
            print(f"Registros: {count}")
            
            # Mostra alguns registros se houver
            if count > 0:
                cursor.execute(f"SELECT * FROM {nome_tabela} LIMIT 3")
                registros = cursor.fetchall()
                print("Primeiros registros:")
                for i, registro in enumerate(registros, 1):
                    print(f"  {i}. {registro}")
            
            print()
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    verificar_banco()
    input("\nPressione Enter para continuar...")
