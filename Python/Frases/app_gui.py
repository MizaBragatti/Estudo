# app_gui.py

import tkinter as tk
import tkinter.messagebox as messagebox
import random
import frase_manager

class AplicacaoLembretesFrases:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciador e Lembretes de Frases")
        master.geometry("700x550")
        master.resizable(False, False)

        self.frases = frase_manager.ler_frases()
        self.intervalo_lembrete_ms = 5000
        self.lembrete_ativo = False
        self.after_id = None
        self.frase_selecionada_para_edicao = None

        # --- Seção de Status e Lembretes ---
        self.label_lembrete = tk.Label(master, text="Clique em 'Iniciar Lembretes' para começar.", wraplength=650, font=("Arial", 12, "italic"))
        self.label_lembrete.pack(pady=10)
        
        self.frame_lembrete_config = tk.Frame(master)
        self.frame_lembrete_config.pack(pady=5)

        tk.Label(self.frame_lembrete_config, text="Intervalo (segundos):").pack(side=tk.LEFT, padx=5)
        self.entrada_intervalo = tk.Entry(self.frame_lembrete_config, width=10)
        self.entrada_intervalo.insert(0, "5")
        self.entrada_intervalo.pack(side=tk.LEFT, padx=5)

        self.btn_iniciar_lembretes = tk.Button(self.frame_lembrete_config, text="Iniciar Lembretes", command=self.iniciar_lembretes_gui)
        self.btn_iniciar_lembretes.pack(side=tk.LEFT, padx=5)

        self.btn_parar_lembretes = tk.Button(self.frame_lembrete_config, text="Parar Lembretes", command=self.parar_lembretes_gui, state=tk.DISABLED)
        self.btn_parar_lembretes.pack(side=tk.LEFT, padx=5)

        tk.Frame(master, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=10, pady=10)

        # --- Seção de Gerenciamento de Frases ---
        tk.Label(master, text="Gerenciamento de Frases", font=("Arial", 14, "bold")).pack(pady=5)

        self.frame_gerenciamento = tk.Frame(master)
        self.frame_gerenciamento.pack(pady=10, fill=tk.BOTH, expand=True)

        # Listbox para exibir as frases
        self.listbox_frases = tk.Listbox(self.frame_gerenciamento, selectmode=tk.SINGLE, height=10)
        self.listbox_frases.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        scrollbar = tk.Scrollbar(self.frame_gerenciamento, orient="vertical", command=self.listbox_frases.yview)
        scrollbar.pack(side=tk.LEFT, fill="y")
        self.listbox_frases.config(yscrollcommand=scrollbar.set)

        self._carregar_frases_no_listbox()

        # --- Botões de Ação para Frases e Campo de Entrada para Nova Frase/Edição ---
        frame_botoes_e_entrada_frases = tk.Frame(self.frame_gerenciamento)
        frame_botoes_e_entrada_frases.pack(side=tk.RIGHT, fill=tk.Y)

        # Campo de entrada para adicionar/editar frases
        tk.Label(frame_botoes_e_entrada_frases, text="Frase:").pack(pady=(0, 2), anchor='w')
        self.entrada_frase_gerenciamento = tk.Entry(frame_botoes_e_entrada_frases, width=30)
        self.entrada_frase_gerenciamento.pack(pady=(0, 10), fill=tk.X)

        # Botão para adicionar a frase do campo de entrada
        btn_adicionar_da_entrada = tk.Button(frame_botoes_e_entrada_frases, text="Adicionar Frase", command=self.adicionar_frase_da_entrada)
        btn_adicionar_da_entrada.pack(pady=5, fill=tk.X)

        # Botão para atualizar (agora usará o campo de entrada para a nova frase)
        btn_atualizar = tk.Button(frame_botoes_e_entrada_frases, text="Atualizar Frase", command=self.on_atualizar_selecionado)
        btn_atualizar.pack(pady=5, fill=tk.X)

        # Botão para excluir
        btn_excluir = tk.Button(frame_botoes_e_entrada_frases, text="Excluir Frase", command=self.on_excluir_selecionado)
        btn_excluir.pack(pady=5, fill=tk.X)

        # Adicionar um evento para quando uma frase for selecionada na Listbox
        self.listbox_frases.bind('<<ListboxSelect>>', self.preencher_e_armazenar_frase)

    def _carregar_frases_no_listbox(self):
        self.frases = frase_manager.ler_frases()
        self.listbox_frases.delete(0, tk.END)
        if self.frases:
            for i, frase in enumerate(self.frases):
                self.listbox_frases.insert(tk.END, f"{i+1}. {frase}")
        else:
            self.listbox_frases.insert(tk.END, "Nenhuma frase cadastrada ainda.")
        self.frase_selecionada_para_edicao = None

    def preencher_e_armazenar_frase(self, event):
        """Preenche o campo de entrada e armazena a frase selecionada."""
        selecao = self.listbox_frases.curselection()
        if selecao:
            indice_selecionado = selecao[0]
            frase_com_numero = self.listbox_frases.get(indice_selecionado)
            frase_limpa = frase_com_numero.split(". ", 1)[1] if ". " in frase_com_numero else frase_com_numero
            
            self.entrada_frase_gerenciamento.delete(0, tk.END)
            self.entrada_frase_gerenciamento.insert(0, frase_limpa)
            self.frase_selecionada_para_edicao = frase_limpa

    def adicionar_frase_da_entrada(self):
        nova_frase = self.entrada_frase_gerenciamento.get().strip()
        if nova_frase:
            # Verifica se a frase foi adicionada com sucesso (não é duplicada)
            if frase_manager.adicionar_frase(nova_frase):
                self._carregar_frases_no_listbox()
                self.entrada_frase_gerenciamento.delete(0, tk.END)
                self.label_lembrete.config(text=f"Frase '{nova_frase}' adicionada com sucesso!")
            else:
                messagebox.showwarning("Frase Duplicada", f"A frase '{nova_frase}' já existe na lista e não foi adicionada novamente.")
                self.label_lembrete.config(text=f"Frase '{nova_frase}' já existe.")
        else:
            messagebox.showwarning("Frase Vazia", "Por favor, digite uma frase para adicionar.")
        self.frase_selecionada_para_edicao = None

    def on_excluir_selecionado(self):
        selecao = self.listbox_frases.curselection()
        if selecao:
            indice_selecionado = selecao[0]
            frase_com_numero = self.listbox_frases.get(indice_selecionado)
            frase_para_excluir = frase_com_numero.split(". ", 1)[1] if ". " in frase_com_numero else frase_com_numero

            confirmar = messagebox.askyesno(
                "Confirmar Exclusão",
                f"Tem certeza que deseja excluir a frase:\n'{frase_para_excluir}'?"
            )
            if confirmar:
                frase_manager.remover_frase(frase_para_excluir)
                self.frases = frase_manager.ler_frases()
                self.label_lembrete.config(text=f"Frase '{frase_para_excluir}' excluída com sucesso!")
                self._carregar_frases_no_listbox()
                self.entrada_frase_gerenciamento.delete(0, tk.END)
                if not self.frases and self.lembrete_ativo:
                    self.parar_lembretes_gui()
                    self.label_lembrete.config(text="Todas as frases foram excluídas. Lembretes parados.")
        else:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma frase para excluir.")
        self.frase_selecionada_para_edicao = None

    def on_atualizar_selecionado(self):
        frase_antiga = self.frase_selecionada_para_edicao 
        nova_frase = self.entrada_frase_gerenciamento.get().strip()

        if frase_antiga is None:
            messagebox.showwarning("Nenhuma Frase Selecionada", "Por favor, selecione uma frase na lista para atualizar.")
            return

        if not nova_frase:
            messagebox.showwarning("Frase Vazia", "O campo de frase para atualização não pode estar vazio.")
            return

        if nova_frase == frase_antiga:
            messagebox.showinfo("Nenhuma Mudança", "A nova frase é idêntica à frase original. Nenhuma atualização realizada.")
            return
            
        # Adicionar verificação se a nova frase já existe (apenas se for diferente da antiga)
        if nova_frase in frase_manager.ler_frases():
            messagebox.showwarning("Frase Duplicada", f"A frase '{nova_frase}' já existe na lista. Não é possível atualizar para uma frase duplicada.")
            return

        if messagebox.askyesno("Confirmar Atualização", f"Deseja atualizar '{frase_antiga}' para '{nova_frase}'?"):
            if frase_manager.atualizar_frase(frase_antiga, nova_frase):
                self.frases = frase_manager.ler_frases()
                self.label_lembrete.config(text=f"Frase atualizada para:\n'{nova_frase}'")
                self._carregar_frases_no_listbox()
                self.entrada_frase_gerenciamento.delete(0, tk.END)
                self.frase_selecionada_para_edicao = None
            else:
                messagebox.showerror("Erro", f"Não foi possível atualizar a frase '{frase_antiga}'.")
        else:
            self.label_lembrete.config(text="Atualização de frase cancelada.")
        

    def iniciar_lembretes_gui(self):
        if self.lembrete_ativo:
            self.label_lembrete.config(text="Lembretes já estão ativos.")
            return

        try:
            intervalo_segundos = float(self.entrada_intervalo.get())
            if intervalo_segundos <= 0:
                self.label_lembrete.config(text="O intervalo deve ser um número positivo.")
                return
            self.intervalo_lembrete_ms = int(intervalo_segundos * 1000)
        except ValueError:
            self.label_lembrete.config(text="Por favor, digite um número válido para o intervalo.")
            return

        self.frases = frase_manager.ler_frases()
        if not self.frases:
            self.label_lembrete.config(text="Nenhuma frase cadastrada para iniciar os lembretes.")
            return

        self.lembrete_ativo = True
        self.btn_iniciar_lembretes.config(state=tk.DISABLED)
        self.btn_parar_lembretes.config(state=tk.NORMAL)
        self.label_lembrete.config(text=f"Lembretes iniciados! A cada {intervalo_segundos} segundos. Selecione uma frase para gerenciar.")
        self._mostrar_lembrete_aleatorio()

    def parar_lembretes_gui(self):
        if not self.lembrete_ativo:
            self.label_lembrete.config(text="Os lembretes não estão ativos.")
            return

        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        self.lembrete_ativo = False
        self.btn_iniciar_lembretes.config(state=tk.NORMAL)
        self.btn_parar_lembretes.config(state=tk.DISABLED)
        self.label_lembrete.config(text="Lembretes parados.")

    def _mostrar_lembrete_aleatorio(self):
        self.frases = frase_manager.ler_frases()
        if not self.frases:
            self.label_lembrete.config(text="Nenhuma frase para lembrar. Parando lembretes.")
            self.parar_lembretes_gui()
            return

        frase_escolhida = random.choice(self.frases)
        self.label_lembrete.config(text=f"**Lembrete:** \"{frase_escolhida}\"")

        if self.lembrete_ativo:
            self.after_id = self.master.after(self.intervalo_lembrete_ms, self._mostrar_lembrete_aleatorio)