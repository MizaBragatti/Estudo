#!/usr/bin/env python3
"""
Script de debug para verificar o estado das frases no banco de dados.
Verifica se as frases estão criptografadas corretamente e se podem ser descriptografadas.
"""

import sqlite3
import base64
import traceback
import sys
import os

# Adiciona o diretório atual ao path para importar frase_manager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import frase_manager

def debug_frases():
    """Debug das frases no banco de dados."""
    print("=== DEBUG DE FRASES ===")
    print()
    
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect('frases.db')
        cursor = conn.cursor()
        
        # Verifica se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='phrases'")
        if not cursor.fetchone():
            print("❌ Tabela 'phrases' não encontrada!")
            return
        
        print("✅ Tabela 'phrases' encontrada")
        
        # Lista todas as frases
        cursor.execute("SELECT id, phrase, is_encrypted FROM phrases")
        frases = cursor.fetchall()
        
        print(f"📊 Total de frases encontradas: {len(frases)}")
        print()
        
        if not frases:
            print("ℹ️  Nenhuma frase encontrada no banco de dados")
            return
        
        # Verifica cada frase
        for i, (id_frase, frase_texto, is_encrypted) in enumerate(frases, 1):
            print(f"--- Frase {i} (ID: {id_frase}) ---")
            print(f"Criptografada: {bool(is_encrypted)}")
            print(f"Texto original (primeiro 50 chars): {frase_texto[:50]}...")
            
            if is_encrypted:
                try:
                    # Tenta descriptografar
                    texto_descriptografado = frase_manager.decrypt_text(frase_texto)
                    print(f"✅ Descriptografia bem-sucedida")
                    print(f"Texto descriptografado (primeiro 50 chars): {texto_descriptografado[:50]}...")
                except Exception as e:
                    print(f"❌ Erro na descriptografia: {e}")
                    print(f"Tipo do erro: {type(e).__name__}")
            else:
                print("ℹ️  Frase não criptografada (texto simples)")
            
            print()
        
        conn.close()
        
        # Testa as funções de listagem do frase_manager
        print("=== TESTE DAS FUNÇÕES DE LISTAGEM ===")
        print()
        
        try:
            todas_frases = frase_manager.list_phrases()
            print(f"✅ list_phrases() retornou {len(todas_frases)} frases")
            
            for i, frase in enumerate(todas_frases[:3], 1):  # Mostra apenas as 3 primeiras
                print(f"Frase {i}: {frase[:50]}...")
        except Exception as e:
            print(f"❌ Erro em list_phrases(): {e}")
            print(f"Traceback: {traceback.format_exc()}")
        
        print()
        
        # Verifica se a chave de criptografia está funcionando
        print("=== TESTE DA CHAVE DE CRIPTOGRAFIA ===")
        print()
        
        try:
            # Testa criptografia/descriptografia
            texto_teste = "Esta é uma frase de teste para verificar a criptografia"
            texto_criptografado = frase_manager.encrypt_text(texto_teste)
            texto_descriptografado = frase_manager.decrypt_text(texto_criptografado)
            
            if texto_teste == texto_descriptografado:
                print("✅ Criptografia/descriptografia funcionando corretamente")
            else:
                print("❌ Erro: texto descriptografado não confere com o original")
                print(f"Original: {texto_teste}")
                print(f"Descriptografado: {texto_descriptografado}")
        except Exception as e:
            print(f"❌ Erro no teste de criptografia: {e}")
            print(f"Traceback: {traceback.format_exc()}")
    
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    debug_frases()
    input("\nPressione Enter para continuar...")
