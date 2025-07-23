#!/usr/bin/env python3
"""
Script de migração para adicionar suporte à criptografia nas frases existentes.
"""

import sqlite3
import sys
import os

# Adiciona o diretório atual ao path para importar frase_manager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import frase_manager

def migrar_frases():
    """Migra as frases existentes para o novo formato com criptografia."""
    print("=== MIGRAÇÃO DE FRASES PARA CRIPTOGRAFIA ===")
    print()
    
    try:
        conn = sqlite3.connect('frases.db')
        cursor = conn.cursor()
        
        # Verifica se a coluna is_encrypted já existe
        cursor.execute("PRAGMA table_info(frases)")
        colunas = cursor.fetchall()
        
        tem_is_encrypted = any(coluna[1] == 'is_encrypted' for coluna in colunas)
        
        if not tem_is_encrypted:
            print("📝 Adicionando coluna 'is_encrypted' à tabela frases...")
            cursor.execute("ALTER TABLE frases ADD COLUMN is_encrypted INTEGER DEFAULT 0")
            conn.commit()
            print("✅ Coluna 'is_encrypted' adicionada com sucesso")
        else:
            print("ℹ️  Coluna 'is_encrypted' já existe")
        
        # Lista todas as frases não criptografadas
        cursor.execute("SELECT id, texto FROM frases WHERE is_encrypted = 0 OR is_encrypted IS NULL")
        frases_nao_criptografadas = cursor.fetchall()
        
        print(f"📊 Frases não criptografadas encontradas: {len(frases_nao_criptografadas)}")
        
        if frases_nao_criptografadas:
            print("\n🔐 Iniciando criptografia das frases...")
            
            for id_frase, texto in frases_nao_criptografadas:
                try:
                    # Criptografa o texto
                    texto_criptografado = frase_manager.encrypt_text(texto)
                    
                    # Atualiza no banco
                    cursor.execute(
                        "UPDATE frases SET texto = ?, is_encrypted = 1 WHERE id = ?",
                        (texto_criptografado, id_frase)
                    )
                    
                    print(f"✅ Frase ID {id_frase} criptografada")
                    
                except Exception as e:
                    print(f"❌ Erro ao criptografar frase ID {id_frase}: {e}")
            
            conn.commit()
            print(f"\n🎉 Migração concluída! {len(frases_nao_criptografadas)} frases criptografadas")
        else:
            print("ℹ️  Todas as frases já estão criptografadas")
        
        conn.close()
        
        # Testa se as frases podem ser lidas após a migração
        print("\n=== TESTE DE LEITURA APÓS MIGRAÇÃO ===")
        
        try:
            frases = frase_manager.ler_frases()
            print(f"✅ ler_frases() retornou {len(frases)} frases")
            
            for i, frase in enumerate(frases[:3], 1):  # Mostra apenas as 3 primeiras
                print(f"Frase {i}: {frase[:50]}...")
        except Exception as e:
            print(f"❌ Erro ao ler frases: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
    
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    migrar_frases()
    input("\nPressione Enter para continuar...")
