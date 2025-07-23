#!/usr/bin/env python3
"""
Teste simples para verificar se as frases podem ser lidas após a migração.
"""

import sys
import os

# Adiciona o diretório atual ao path para importar frase_manager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import frase_manager

def testar_leitura_frases():
    """Testa a leitura das frases após migração."""
    print("=== TESTE DE LEITURA DAS FRASES ===")
    print()
    
    try:
        # Testa a função ler_frases
        print("📖 Testando ler_frases()...")
        frases = frase_manager.ler_frases()
        
        print(f"✅ {len(frases)} frases carregadas com sucesso!")
        print()
        
        # Mostra algumas frases
        print("🔍 Primeiras 5 frases:")
        for i, frase in enumerate(frases[:5], 1):
            print(f"  {i}. {frase}")
        
        print()
        
        # Testa ordenação alfabética
        print("📝 Testando ordenação alfabética...")
        frases_alfabeticas = frase_manager.ler_frases(ordenacao="alfabetica")
        print(f"✅ {len(frases_alfabeticas)} frases ordenadas alfabeticamente")
        
        print("🔍 Primeiras 3 frases (ordem alfabética):")
        for i, frase in enumerate(frases_alfabeticas[:3], 1):
            print(f"  {i}. {frase}")
        
        print()
        print("🎉 Todos os testes de leitura passaram!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    testar_leitura_frases()
    input("\nPressione Enter para continuar...")
