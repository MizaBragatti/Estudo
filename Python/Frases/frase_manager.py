# frase_manager.py

import os

NOME_ARQUIVO = "Python/Frases/frases.txt"

def adicionar_frase(frase):
    """
    Adiciona uma nova frase ao arquivo, verificando antes se ela já existe.
    Retorna True se a frase foi adicionada, False se já existia.
    """
    frases_atuais = ler_frases()
    if frase in frases_atuais:
        return False # Frase já existe, não adiciona

    with open(NOME_ARQUIVO, "a", encoding="utf-8") as f:
        f.write(frase + "\n")
    return True # Frase adicionada com sucesso

def ler_frases():
    """Lê todas as frases do arquivo e as retorna como uma lista."""
    if not os.path.exists(NOME_ARQUIVO):
        return []
    try:
        with open(NOME_ARQUIVO, "r", encoding="utf-8") as f:
            # Garante que as frases são lidas na ordem em que aparecem no arquivo
            return [linha.strip() for linha in f if linha.strip()]
    except Exception as e:
        print(f"Erro ao ler frases: {e}")
        return []

def remover_frase(frase_para_remover):
    """
    Remove a primeira ocorrência de uma frase específica do arquivo.
    Reescreve o arquivo com as frases restantes.
    """
    frases_atuais = ler_frases()
    frases_restantes = []
    removido = False
    for f in frases_atuais:
        if f == frase_para_remover and not removido:
            removido = True
        else:
            frases_restantes.append(f)

    with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
        for frase in frases_restantes:
            f.write(frase + "\n")

def atualizar_frase(frase_antiga, nova_frase):
    """
    Atualiza uma frase existente no arquivo de frases.
    Substitui a frase antiga pela nova.
    """
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
    """
    Lê frases de um arquivo TXT externo e as adiciona ao arquivo principal.
    Retorna uma tupla (total_lidas, total_adicionadas, total_duplicadas).
    """
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