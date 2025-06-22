import tkinter as tk

class AplicacaoFrases:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciador de Frases")
        master.geometry("500x300")

        self.label = tk.Label(master, text="Bem-vindo ao Gerenciador de Frases!")
        self.label.pack(pady=10)

        self.frase_entrada = tk.Entry(master, width=50)
        self.frase_entrada.pack(pady=5)

        self.btn_adicionar = tk.Button(master, text="Adicionar Frase", command=self.adicionar_frase)
        self.btn_adicionar.pack(pady=5)

        self.btn_mostrar = tk.Button(master, text="Mostrar Próxima Frase", command=self.mostrar_frase)
        self.btn_mostrar.pack(pady=5)

        self.frases = [] # Lista para armazenar as frases
        self.indice_frase = 0

    def adicionar_frase(self):
        nova_frase = self.frase_entrada.get()
        if nova_frase:
            self.frases.append(nova_frase)
            self.frase_entrada.delete(0, tk.END) # Limpa a caixa de entrada
            self.label.config(text=f"Frase '{nova_frase}' adicionada!")
        else:
            self.label.config(text="Por favor, digite uma frase.")

    def mostrar_frase(self):
        if not self.frases:
            self.label.config(text="Nenhuma frase cadastrada ainda.")
            return

        frase_atual = self.frases[self.indice_frase]
        self.label.config(text=f"Sua frase: \"{frase_atual}\"")

        # Avança para a próxima frase ou volta ao início da lista
        self.indice_frase = (self.indice_frase + 1) % len(self.frases)


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoFrases(root)
    root.mainloop()