# Função para adicionar uma frase ao arquivo
def adicionar_frase(frase):
    with open("frases.txt", "a", encoding="utf-8") as f:
        f.write(frase + "\n")

# Função para ler todas as frases do arquivo
def ler_frases():
    try:
        with open("frases.txt", "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        return []