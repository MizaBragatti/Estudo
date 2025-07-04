import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog # Necessário para a caixa de diálogo de atualização
import random
import os

# --- Funções de Armazenamento de Arquivo ---
NOME_ARQUIVO = "frases.txt"

def adicionar_frase(frase):
    with open(NOME_ARQUIVO, "a", encoding="utf-8") as f:
        f.write(frase + "\n")

def ler_frases():
    if not os.path.exists(NOME_ARQUIVO):
        return []
    try:
        with open(NOME_ARQUIVO, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f if linha.strip()]
    except Exception as e:
        print(f"Erro ao ler frases: {e}")
        return []

def remover_frase_do_arquivo(frase_para_remover):
    frases_atuais = ler_frases()
    frases_restantes = []
    removido = False
    for f in frases_atuais:
        if f == frase_para_remover and not removido: # Remove apenas a primeira ocorrência
            removido = True
        else:
            frases_restantes.append(f)

    with open(NOME_ARQUIVO, "w", encoding="utf-8") as f: # Abre em modo escrita para reescrever
        for frase in frases_restantes:
            f.write(frase + "\n")

def atualizar_frase_no_arquivo(frase_antiga, nova_frase):
    """
    Atualiza uma frase existente no arquivo de frases.
    Substitui a frase antiga pela nova.
    """
    frases_atuais = ler_frases()
    try:
        index = frases_atuais.index(frase_antiga) # Encontra a posição da frase antiga
        frases_atuais[index] = nova_frase # Substitui pela nova frase
    except ValueError:
        print(f"Frase '{frase_antiga}' não encontrada no arquivo.")
        return False # Indica que a frase não foi encontrada

    with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
        for frase in frases_atuais:
            f.write(frase + "\n")
    return True # Indica que a atualização foi bem-sucedida

# ---

# ### **Interface Gráfica com Todas as Funcionalidades (Completa)**

# ```python
class AplicacaoLembretesFrases:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciador e Lembretes de Frases")
        master.geometry("500x350")

        self.frases = ler_frases() # Carrega as frases na inicialização
        self.intervalo_lembrete_ms = 5000
        self.lembrete_ativo = False
        self.after_id = None

        # --- Widgets da Interface Principal ---
        self.label_status = tk.Label(master, text="Bem-vindo! Cadastre suas frases.", wraplength=400)
        self.label_status.pack(pady=10)

        self.frame_cadastro = tk.Frame(master)
        self.frame_cadastro.pack(pady=10)

        self.label_nova_frase = tk.Label(self.frame_cadastro, text="Nova Frase:")
        self.label_nova_frase.pack(side=tk.LEFT, padx=5)

        self.entrada_frase = tk.Entry(self.frame_cadastro, width=40)
        self.entrada_frase.pack(side=tk.LEFT, padx=5)

        self.btn_adicionar = tk.Button(self.frame_cadastro, text="Adicionar", command=self.adicionar_frase_gui)
        self.btn_adicionar.pack(side=tk.LEFT, padx=5)

        self.btn_ver_frases = tk.Button(master, text="Ver, Excluir e Atualizar Frases", command=self.mostrar_todas_frases)
        self.btn_ver_frases.pack(pady=5)

        self.frame_lembrete_config = tk.Frame(master)
        self.frame_lembrete_config.pack(pady=10)

        self.label_intervalo = tk.Label(self.frame_lembrete_config, text="Intervalo (segundos):")
        self.label_intervalo.pack(side=tk.LEFT, padx=5)

        self.entrada_intervalo = tk.Entry(self.frame_lembrete_config, width=10)
        self.entrada_intervalo.insert(0, "5") # Valor padrão
        self.entrada_intervalo.pack(side=tk.LEFT, padx=5)

        self.btn_iniciar_lembretes = tk.Button(master, text="Iniciar Lembretes", command=self.iniciar_lembretes_gui)
        self.btn_iniciar_lembretes.pack(pady=5)

        self.btn_parar_lembretes = tk.Button(master, text="Parar Lembretes", command=self.parar_lembretes_gui, state=tk.DISABLED)
        self.btn_parar_lembretes.pack(pady=5)

    def adicionar_frase_gui(self):
        nova_frase = self.entrada_frase.get().strip()
        if nova_frase:
            adicionar_frase(nova_frase)
            self.frases.append(nova_frase) # Atualiza a lista em memória
            self.entrada_frase.delete(0, tk.END) # Limpa a caixa de entrada
            self.label_status.config(text=f"Frase '{nova_frase}' adicionada com sucesso!")
        else:
            self.label_status.config(text="Por favor, digite uma frase para adicionar.")

    def mostrar_todas_frases(self):
        self.frases = ler_frases() # Recarrega para garantir que está atualizado
        if not self.frases:
            self.label_status.config(text="Nenhuma frase cadastrada ainda.")
            return

        janela_frases = tk.Toplevel(self.master)
        janela_frases.title("Frases Cadastradas, Excluir e Atualizar")
        janela_frases.geometry("600x400") # Aumenta a altura da janela para os botões

        frame_listbox = tk.Frame(janela_frases)
        frame_listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        listbox = tk.Listbox(frame_listbox, selectmode=tk.SINGLE) # Permite selecionar apenas um item
        listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(frame_listbox, orient="vertical", command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        self.carregar_frases_no_listbox(listbox)

        def on_excluir_selecionado():
            selecao = listbox.curselection() # Obtém o índice do item selecionado
            if selecao:
                indice_selecionado = selecao[0]
                frase_com_numero = listbox.get(indice_selecionado)
                # Remove o prefixo "N. " antes de passar para a função de remoção
                frase_para_excluir = frase_com_numero.split(". ", 1)[1] if ". " in frase_com_numero else frase_com_numero

                confirmar = messagebox.askyesno(
                    "Confirmar Exclusão",
                    f"Tem certeza que deseja excluir a frase:\n'{frase_para_excluir}'?"
                )
                if confirmar:
                    remover_frase_do_arquivo(frase_para_excluir)
                    self.frases = ler_frases() # Recarrega a lista principal
                    self.label_status.config(text=f"Frase '{frase_para_excluir}' excluída com sucesso!")
                    
                    # Atualiza a listbox sem fechar e reabrir a janela, para melhor UX
                    self.carregar_frases_no_listbox(listbox) 
                    if not self.frases: # Se não houver mais frases, fecha a janela de frases
                        janela_frases.destroy()
                        self.label_status.config(text="Todas as frases foram excluídas.")
            else:
                messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma frase para excluir.")

        def on_atualizar_selecionado():
            selecao = listbox.curselection()
            if selecao:
                indice_selecionado = selecao[0]
                frase_com_numero = listbox.get(indice_selecionado)
                frase_antiga = frase_com_numero.split(". ", 1)[1] if ". " in frase_com_numero else frase_com_numero

                # Abre uma caixa de diálogo para inserir a nova frase
                nova_frase = simpledialog.askstring("Atualizar Frase", f"Digite a nova frase para:\n'{frase_antiga}'")
                
                if nova_frase is not None: # Verifica se o usuário não cancelou a caixa de diálogo
                    nova_frase = nova_frase.strip() # Remove espaços em branco extras
                    if nova_frase: # Verifica se a nova frase não está vazia
                        if atualizar_frase_no_arquivo(frase_antiga, nova_frase):
                            self.frases = ler_frases() # Recarrega a lista principal
                            self.label_status.config(text=f"Frase atualizada para:\n'{nova_frase}'")
                            self.carregar_frases_no_listbox(listbox) # Atualiza a listbox
                        else:
                            messagebox.showerror("Erro", f"Não foi possível atualizar a frase '{frase_antiga}'.")
                    else:
                        messagebox.showwarning("Frase Vazia", "A nova frase não pode ser vazia.")
                else:
                    messagebox.showinfo("Atualização Cancelada", "Nenhuma nova frase foi fornecida.")
            else:
                messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma frase para atualizar.")

        # --- Botões na Janela de Frases (exclusão e atualização) ---
        frame_botoes = tk.Frame(janela_frases)
        frame_botoes.pack(pady=10)

        btn_excluir = tk.Button(frame_botoes, text="Excluir Frase", command=on_excluir_selecionado)
        btn_excluir.pack(side=tk.LEFT, padx=5)

        btn_atualizar = tk.Button(frame_botoes, text="Atualizar Frase", command=on_atualizar_selecionado)
        btn_atualizar.pack(side=tk.LEFT, padx=5)

    def carregar_frases_no_listbox(self, listbox_widget):
        listbox_widget.delete(0, tk.END) # Limpa o listbox
        for i, frase in enumerate(self.frases):
            listbox_widget.insert(tk.END, f"{i+1}. {frase}")

    def iniciar_lembretes_gui(self):
        if self.lembrete_ativo:
            self.label_status.config(text="Lembretes já estão ativos.")
            return

        try:
            intervalo_segundos = float(self.entrada_intervalo.get())
            if intervalo_segundos <= 0:
                self.label_status.config(text="Intervalo deve ser um número positivo.")
                return
            self.intervalo_lembrete_ms = int(intervalo_segundos * 1000)
        except ValueError:
            self.label_status.config(text="Por favor, digite um número válido para o intervalo.")
            return

        self.frases = ler_frases() # Carrega as frases mais recentes
        if not self.frases:
            self.label_status.config(text="Nenhuma frase cadastrada para iniciar os lembretes.")
            return

        self.lembrete_ativo = True
        self.btn_iniciar_lembretes.config(state=tk.DISABLED)
        self.btn_parar_lembretes.config(state=tk.NORMAL)
        self.label_status.config(text=f"Lembretes iniciados! A cada {intervalo_segundos} segundos.")
        self._agendar_proximo_lembrete()

    def parar_lembretes_gui(self):
        if not self.lembrete_ativo:
            self.label_status.config(text="Os lembretes não estão ativos.")
            return

        if self.after_id:
            self.master.after_cancel(self.after_id) # Cancela o próximo agendamento
            self.after_id = None

        self.lembrete_ativo = False
        self.btn_iniciar_lembretes.config(state=tk.NORMAL)
        self.btn_parar_lembretes.config(state=tk.DISABLED)
        self.label_status.config(text="Lembretes parados.")

    def _mostrar_lembrete_aleatorio(self):
        self.frases = ler_frases() # Recarrega as frases para garantir que excluídas não apareçam
        if not self.frases:
            self.label_status.config(text="Nenhuma frase para lembrar. Parando lembretes.")
            self.parar_lembretes_gui()
            return

        frase_escolhida = random.choice(self.frases)
        self.label_status.config(text=f"**Lembrete:** \"{frase_escolhida}\"")

        if self.lembrete_ativo: # Continua agendando se ainda estiver ativo
            self._agendar_proximo_lembrete()

    def _agendar_proximo_lembrete(self):
        # Agenda a próxima chamada da função _mostrar_lembrete_aleatorio
        # depois de 'self.intervalo_lembrete_ms' milissegundos.
        # Retorna um ID que pode ser usado para cancelar o agendamento.
        self.after_id = self.master.after(self.intervalo_lembrete_ms, self._mostrar_lembrete_aleatorio)


# --- Execução Principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoLembretesFrases(root)
    root.mainloop()