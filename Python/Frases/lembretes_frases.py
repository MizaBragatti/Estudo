import random
import time

# --- Funções de Armazenamento (re-copiadas para clareza) ---
def adicionar_frase(frase):
    with open("frases.txt", "a", encoding="utf-8") as f:
        f.write(frase + "\n")

def ler_frases():
    try:
        with open("frases.txt", "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        return []

# --- Função de Menu de Cadastro (re-copiada para clareza) ---
def menu_cadastro():
    while True:
        print("\n--- Cadastro de Frases ---")
        print("1. Adicionar nova frase")
        print("2. Ver frases cadastradas")
        print("3. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            frase = input("Digite a frase que deseja cadastrar: ")
            adicionar_frase(frase)
            print("Frase adicionada com sucesso!")
        elif opcao == "2":
            frases = ler_frases()
            if frases:
                print("\n--- Frases Cadastradas ---")
                for i, frase in enumerate(frases):
                    print(f"{i+1}. {frase}")
            else:
                print("Nenhuma frase cadastrada ainda.")
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")

# --- Função de Lembrete (re-copiada para clareza) ---
def mostrar_lembrete(intervalo_segundos):
    frases = ler_frases()
    if not frases:
        print("Nenhuma frase cadastrada para exibir lembretes.")
        return

    print(f"\nIniciando lembretes a cada {intervalo_segundos} segundos. Pressione Ctrl+C para parar.")
    try:
        while True:
            frase_aleatoria = random.choice(frases)
            print(f"\n--- Lembrete: ---\n'{frase_aleatoria}'")
            time.sleep(intervalo_segundos)
    except KeyboardInterrupt:
        print("\nLembretes parados.")


# --- Programa Principal ---
def main():
    while True:
        print("\n### Ferramenta de Lembretes de Frases ###")
        print("1. Cadastrar/Ver frases")
        print("2. Iniciar Lembretes")
        print("3. Sair")
        opcao_principal = input("Escolha uma opção: ")

        if opcao_principal == "1":
            menu_cadastro()
        elif opcao_principal == "2":
            try:
                intervalo = float(input("Digite o intervalo entre os lembretes em segundos (ex: 60 para 1 minuto): "))
                if intervalo <= 0:
                    print("O intervalo deve ser um número positivo.")
                else:
                    mostrar_lembrete(intervalo)
            except ValueError:
                print("Entrada inválida. Digite um número para o intervalo.")
        elif opcao_principal == "3":
            print("Saindo da ferramenta. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()