#!/usr/bin/env python3
"""
Teste da funcionalidade de busca de frases.
"""

import sys
import os

# Adiciona o diretório atual ao path para importar frase_manager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import frase_manager

def testar_busca():
    """Testa a funcionalidade de busca de frases."""
    print("=== TESTE DE BUSCA DE FRASES ===")
    print()
    
    try:
        # Lista todas as frases primeiro
        todas_frases = frase_manager.ler_frases()
        print(f"📊 Total de frases no banco: {len(todas_frases)}")
        print()
        
        # Teste 1: Busca por palavra comum
        print("🔍 Teste 1: Busca por 'sucesso'")
        frases_sucesso = frase_manager.buscar_frases("sucesso")
        print(f"   Encontradas: {len(frases_sucesso)} frases")
        for i, frase in enumerate(frases_sucesso[:3], 1):
            print(f"   {i}. {frase}")
        print()
        
        # Teste 2: Busca case-insensitive
        print("🔍 Teste 2: Busca por 'SUCESSO' (maiúsculo)")
        frases_sucesso_upper = frase_manager.buscar_frases("SUCESSO")
        print(f"   Encontradas: {len(frases_sucesso_upper)} frases")
        print(f"   Resultado igual ao teste 1: {len(frases_sucesso) == len(frases_sucesso_upper)}")
        print()
        
        # Teste 3: Busca por palavra que não existe
        print("🔍 Teste 3: Busca por 'xyzabc123' (palavra inexistente)")
        frases_inexistente = frase_manager.buscar_frases("xyzabc123")
        print(f"   Encontradas: {len(frases_inexistente)} frases")
        print()
        
        # Teste 4: Busca vazia
        print("🔍 Teste 4: Busca vazia")
        frases_vazia = frase_manager.buscar_frases("")
        print(f"   Encontradas: {len(frases_vazia)} frases")
        print(f"   Igual ao total: {len(frases_vazia) == len(todas_frases)}")
        print()
        
        # Teste 5: Busca por parte de palavra
        print("🔍 Teste 5: Busca por 'bom'")
        frases_bom = frase_manager.buscar_frases("bom")
        print(f"   Encontradas: {len(frases_bom)} frases")
        for i, frase in enumerate(frases_bom[:3], 1):
            print(f"   {i}. {frase}")
        print()
        
        # Teste 6: Busca com ordenação
        print("🔍 Teste 6: Busca por 'o' com ordenação alfabética")
        frases_o_alpha = frase_manager.buscar_frases("o", ordenacao="alfabetica")
        print(f"   Encontradas: {len(frases_o_alpha)} frases")
        print("   Primeiras 3 (ordem alfabética):")
        for i, frase in enumerate(frases_o_alpha[:3], 1):
            print(f"   {i}. {frase}")
        
        print()
        print("🎉 Todos os testes de busca concluídos!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    testar_busca()
    input("\nPressione Enter para continuar...")
