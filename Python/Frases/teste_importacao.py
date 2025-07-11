#!/usr/bin/env python3
# teste_importacao.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import frase_manager

def test_import():
    # Testa a função de importação
    file_path = "frases_teste.txt"
    
    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado!")
        return
    
    print(f"Testando importação do arquivo: {file_path}")
    total_lidas, total_adicionadas, total_duplicadas = frase_manager.importar_frases_de_arquivo(file_path)
    
    print(f"Total de linhas lidas: {total_lidas}")
    print(f"Frases adicionadas: {total_adicionadas}")
    print(f"Frases duplicadas ignoradas: {total_duplicadas}")
    
    # Lista todas as frases
    frases = frase_manager.ler_frases()
    print(f"\nTotal de frases no banco: {len(frases)}")
    for i, frase in enumerate(frases, 1):
        print(f"{i}. {frase}")

if __name__ == "__main__":
    test_import()
