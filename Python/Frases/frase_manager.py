# frase_manager.py

import os
import sys

if getattr(sys, 'frozen', False):
    # Se o script estiver sendo executado como um executável empacotado
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Se o script estiver sendo executado como um script Python normal
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOME_ARQUIVO = os.path.join(BASE_DIR, "frases.txt")

def adicionar_frase(frase):
    frases_atuais = ler_frases()
    if frase in frases_atuais:
        return False
    with open(NOME_ARQUIVO, "a", encoding="utf-8") as f:
        f.write(frase + "\n")
    return True

def ler_frases():
    if not os.path.exists(NOME_ARQUIVO):
        return []
    try:
        with open(NOME_ARQUIVO, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f if linha.strip()]
    except Exception as e:
        print(f"Erro ao ler frases: {e}")
        return []

def remover_frase(frase_para_remover):
    """
    Remove a primeira ocorrência de uma frase específica do arquivo.
    Reescreve o arquivo com as frases restantes.
    Retorna True se a frase foi removida, False caso não seja encontrada.
    """
    frases_atuais = ler_frases()
    frases_restantes = []
    removido = False
    for f in frases_atuais:
        if f == frase_para_remover and not removido:
            removido = True # Marca que a frase foi encontrada e "removida"
        else:
            frases_restantes.append(f)

    # Se algo foi removido ou a lista está vazia, reescreve
    if removido or not frases_atuais: # Adicionei 'or not frases_atuais' para caso o arquivo precise ser reescrito vazio
        with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
            for frase in frases_restantes:
                f.write(frase + "\n")
    return removido # Retorna se a frase foi de fato removida

def atualizar_frase(frase_antiga, nova_frase):
    frases_atuais = ler_frases()
    try:
        index = frases_atuais.index(frase_antiga)
        frases_atuais[index] = nova_frase
    except ValueError:
        print(f"Frase '{frase_antiga}' não encontrada no arquivo.")
        return False

    with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
        for frase in frases_atuais:
            f.write(frase + "\n")
    return True

def importar_frases_de_arquivo(caminho_arquivo):
    total_lidas = 0
    total_adicionadas = 0
    total_duplicadas = 0

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                total_lidas += 1
                frase = linha.strip()
                if frase:
                    if adicionar_frase(frase):
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