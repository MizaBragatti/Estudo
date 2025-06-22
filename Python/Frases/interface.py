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