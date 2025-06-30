# app_gui.py

import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import random
import frase_manager # <--- Continua importando o frase_manager
import os

class AplicacaoLembretesFrases:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciador e Lembretes de Frases")
        master.geometry("700x620")
        # master.resizable(False, False) # Manter comentado ou remover para redimensionamento

        # Cores Modernas
        MODERN_BACKGROUND = "#f0f0f0"  # Cinza claro para o fundo geral
        MODERN_FOREGROUND = "#333333"  # Cinza escuro para o texto padrão
        MODERN_BUTTON_BG = "#4CAF50"   # Verde moderno para botões
        MODERN_BUTTON_FG = "#ffffff"   # Texto branco nos botões
        MODERN_LISTBOX_BG = "#ffffff"  # Branco para o fundo da listbox

        master.config(bg=MODERN_BACKGROUND) # Cor de fundo da janela principal

        self.intervalo_lembrete_ms = 5000
        self.lembrete_ativo = False
        self.after_id = None
        self.frase_selecionada_para_edicao = None
        self._after_update_buttons_id = None 

        self.opcoes_ordenacao = {
            "Ordem de Criação (Antiga para Nova)": "original",
            "Ordem de Criação Inversa (Nova para Antiga)": "original_inversa",
            "Ordem Alfabética (A-Z)": "alfabetica",
            "Ordem Alfabética Inversa (Z-A)": "alfabetica_inversa"
        }
        self.modo_ordenacao = tk.StringVar(master)
        self.modo_ordenacao.set("Ordem de Criação (Antiga para Nova)")

        # Lembrete
        self.label_lembrete = tk.Label(master, text="Clique em 'Iniciar Lembretes' para começar.", wraplength=650, font=("Arial", 12, "italic"), bg=MODERN_BACKGROUND, fg=MODERN_FOREGROUND)
        self.label_lembrete.pack(pady=(15, 10)) # Mais espaço em cima

        self.frame_lembrete_config = tk.Frame(master, bg=MODERN_BACKGROUND)
        self.frame_lembrete_config.pack(pady=(5, 15)) # Mais espaço abaixo do frame

        tk.Label(self.frame_lembrete_config, text="Intervalo (segundos):", bg=MODERN_BACKGROUND, fg=MODERN_FOREGROUND).pack(side=tk.LEFT, padx=5)
        self.entrada_intervalo = tk.Entry(self.frame_lembrete_config, width=10)
        self.entrada_intervalo.insert(0, "5")
        self.entrada_intervalo.pack(side=tk.LEFT, padx=(0, 10)) # Espaço à direita da entrada

        self.btn_iniciar_lembretes = tk.Button(self.frame_lembrete_config, text="Iniciar Lembretes", command=self.iniciar_lembretes_gui, bg=MODERN_BUTTON_BG, fg=MODERN_BUTTON_FG)
        self.btn_iniciar_lembretes.pack(side=tk.LEFT, padx=(5, 5)) # Espaço entre botões

        self.btn_parar_lembretes = tk.Button(self.frame_lembrete_config, text="Parar Lembretes", command=self.parar_lembretes_gui, state=tk.DISABLED, bg=MODERN_BUTTON_BG, fg=MODERN_BUTTON_FG)
        self.btn_parar_lembretes.pack(side=tk.LEFT, padx=(5, 5)) # Espaço entre botões

        # Linha separadora
        tk.Frame(master, height=2, bd=1, relief=tk.SUNKEN, bg="lightgray").pack(fill=tk.X, padx=10, pady=(10, 20)) # Mais espaço abaixo da linha e cor suave

        tk.Label(master, text="Gerenciamento de Frases", font=("Arial", 14, "bold"), bg=MODERN_BACKGROUND, fg=MODERN_FOREGROUND).pack(pady=(5, 15)) # Mais espaço abaixo do título

        # Ordenação
        self.frame_ordenacao = tk.Frame(master, bg=MODERN_BACKGROUND)
        self.frame_ordenacao.pack(pady=(0, 15)) # Espaço abaixo do menu de ordenação
        tk.Label(self.frame_ordenacao, text="Ordenar por:", bg=MODERN_BACKGROUND, fg=MODERN_FOREGROUND).pack(side=tk.LEFT, padx=5)
        self.menu_ordenacao = tk.OptionMenu(self.frame_ordenacao, self.modo_ordenacao, *self.opcoes_ordenacao.keys(), command=self._aplicar_ordenacao)
        self.menu_ordenacao.pack(side=tk.LEFT, padx=5)

        # Gerenciamento de frases
        self.frame_gerenciamento = tk.Frame(master, bg=MODERN_BACKGROUND)
        self.frame_gerenciamento.pack(pady=(10, 0), fill=tk.BOTH, expand=True, padx=15) # Adicionando padx aqui para toda a seção

        self.listbox_frases = tk.Listbox(self.frame_gerenciamento, selectmode=tk.EXTENDED, height=10, bg=MODERN_LISTBOX_BG, fg=MODERN_FOREGROUND) 
        self.listbox_frases.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20)) # Mais espaço entre listbox e botões

        scrollbar = tk.Scrollbar(self.frame_gerenciamento, orient="vertical", command=self.listbox_frases.yview, bg=MODERN_BACKGROUND) 
        scrollbar.pack(side=tk.LEFT, fill="y", padx=(0, 0)) # Ajuste leve se necessário para a barra de rolagem
        self.listbox_frases.config(yscrollcommand=scrollbar.set)

        frame_botoes_e_entrada_frases = tk.Frame(self.frame_gerenciamento, bg=MODERN_BACKGROUND)
        frame_botoes_e_entrada_frases.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(frame_botoes_e_entrada_frases, text="Frase:", bg=MODERN_BACKGROUND, fg=MODERN_FOREGROUND).pack(pady=(0, 5), anchor='w') # Mais espaço abaixo da label
        self.entrada_frase_gerenciamento = tk.Entry(frame_botoes_e_entrada_frases, width=30)
        self.entrada_frase_gerenciamento.pack(pady=(0, 15), fill=tk.X) # Mais espaço abaixo da entrada

        self.btn_adicionar_da_entrada = tk.Button(frame_botoes_e_entrada_frases, text="Adicionar Frase", command=self.adicionar_frase_da_entrada, bg=MODERN_BUTTON_BG, fg=MODERN_BUTTON_FG)
        self.btn_adicionar_da_entrada.pack(pady=(5, 10), fill=tk.X) # Mais espaço abaixo

        self.btn_atualizar = tk.Button(frame_botoes_e_entrada_frases, text="Atualizar Frase", command=self.on_atualizar_selecionado, bg=MODERN_BUTTON_BG, fg=MODERN_BUTTON_FG, state=tk.DISABLED)
        self.btn_atualizar.pack(pady=(5, 10), fill=tk.X) # Mais espaço abaixo

        self.btn_excluir = tk.Button(frame_botoes_e_entrada_frases, text="Excluir Frase", command=self.on_excluir_selecionado, bg=MODERN_BUTTON_BG, fg=MODERN_BUTTON_FG, state=tk.DISABLED)
        self.btn_excluir.pack(pady=(5, 20), fill=tk.X) # Mais espaço abaixo e separação do próximo botão

        btn_importar = tk.Button(frame_botoes_e_entrada_frases, text="Importar Frases do Arquivo", command=self.importar_frases_gui, bg=MODERN_BUTTON_BG, fg=MODERN_BUTTON_FG)
        btn_importar.pack(pady=(15, 0), fill=tk.X) # Mais espaço acima para separar dos outros botões

        self.label_total_frases = tk.Label(master, text="Total de Frases: 0", font=("Arial", 10, "bold"), bg=MODERN_BACKGROUND, fg=MODERN_FOREGROUND)
        self.label_total_frases.pack(pady=(20, 15)) # Mais espaço acima e abaixo

        self.listbox_frases.bind('<<ListboxSelect>>', self.on_listbox_selection_change)
        
        self._carregar_e_exibir_frases_inicial() 

    def _carregar_e_exibir_frases_inicial(self):
        # Não precisamos mais carregar self.frases aqui, pois ler_frases() faz isso
        self.frase_selecionada_para_edicao = None 
        self.entrada_frase_gerenciamento.delete(0, tk.END) 
        
        self._aplicar_ordenacao(self.modo_ordenacao.get()) 

    def _aplicar_ordenacao(self, *args):
        modo_db = self.opcoes_ordenacao[self.modo_ordenacao.get()]
        # Chama ler_frases passando o modo de ordenação para o DB
        self.frases = frase_manager.ler_frases(ordenacao=modo_db) 
        self._recarregar_listbox_com_frases_ordenadas() 

    def _recarregar_listbox_com_frases_ordenadas(self):
        self.listbox_frases.delete(0, tk.END)
        if self.frases: # self.frases já foi populado por frase_manager.ler_frases()
            for i, frase in enumerate(self.frases):
                self.listbox_frases.insert(tk.END, f"{i+1}. {frase}")
        else:
            self.listbox_frases.insert(tk.END, "Nenhuma frase cadastrada ainda.")
        
        self.label_total_frases.config(text=f"Total de Frases: {len(self.frases)}")
        self._atualizar_estado_botoes()

    def _atualizar_estado_botoes(self):
        selecoes_de_itens = self.listbox_frases.curselection() 
        num_selecoes = len(selecoes_de_itens)

        if num_selecoes == 0:
            self.btn_adicionar_da_entrada.config(state=tk.NORMAL)
            self.btn_atualizar.config(state=tk.DISABLED)
            self.btn_excluir.config(state=tk.DISABLED) 
            self.frase_selecionada_para_edicao = None 
        elif num_selecoes == 1:
            self.btn_adicionar_da_entrada.config(state=tk.DISABLED)
            self.btn_atualizar.config(state=tk.NORMAL)
            self.btn_excluir.config(state=tk.NORMAL)
            
            indice_selecionado = selecoes_de_itens[0] 
            frase_com_numero = self.listbox_frases.get(indice_selecionado)
            frase_limpa = frase_com_numero.split(". ", 1)[1] if ". " in frase_com_numero else frase_com_numero
            self.entrada_frase_gerenciamento.delete(0, tk.END)
            self.entrada_frase_gerenciamento.insert(0, frase_limpa)
            self.frase_selecionada_para_edicao = frase_limpa
        else: # Múltiplas seleções de itens
            self.btn_adicionar_da_entrada.config(state=tk.DISABLED)
            self.btn_atualizar.config(state=tk.DISABLED)
            self.btn_excluir.config(state=tk.NORMAL)
            self.frase_selecionada_para_edicao = None 
            self.entrada_frase_gerenciamento.delete(0, tk.END)

    def on_listbox_selection_change(self, event=None):
        if self._after_update_buttons_id:
            self.master.after_cancel(self._after_update_buttons_id)
        self._after_update_buttons_id = self.master.after(50, self._atualizar_estado_botoes)

    def adicionar_frase_da_entrada(self):
        nova_frase = self.entrada_frase_gerenciamento.get().strip()
        if nova_frase:
            if frase_manager.adicionar_frase(nova_frase):
                self.label_lembrete.config(text=f"Frase '{nova_frase}' adicionada com sucesso!")
            else:
                messagebox.showwarning("Frase Duplicada", f"A frase '{nova_frase}' já existe na lista e não foi adicionada novamente.")
                self.label_lembrete.config(text=f"Frase '{nova_frase}' já existe.")
        else:
            messagebox.showwarning("Frase Vazia", "Por favor, digite uma frase para adicionar.")
        self._carregar_e_exibir_frases_inicial()

    def on_excluir_selecionado(self):
        selecoes = self.listbox_frases.curselection()
        if not selecoes:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma ou mais frases para excluir.")
            return

        frases_para_excluir = []
        for indice in selecoes:
            frase_com_numero = self.listbox_frases.get(indice)
            frase_limpa = frase_com_numero.split(". ", 1)[1] if ". " in frase_com_numero else frase_com_numero
            frases_para_excluir.append(frase_limpa)
        
        frases_para_excluir_unicas = list(set(frases_para_excluir))

        if not frases_para_excluir_unicas:
            messagebox.showwarning("Nenhuma Seleção", "Nenhuma frase válida encontrada na seleção para excluir.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir {len(frases_para_excluir_unicas)} frase(s)?\n\n"
            + "\n".join([f"- {f}" for f in frases_para_excluir_unicas[:5]])
            + ("..." if len(frases_para_excluir_unicas) > 5 else "")
        )
        if confirmar:
            frases_excluidas_count = 0
            for frase in frases_para_excluir_unicas:
                if frase_manager.remover_frase(frase): 
                    frases_excluidas_count += 1
            
            self._carregar_e_exibir_frases_inicial() 
            self.label_lembrete.config(text=f"{frases_excluidas_count} frase(s) excluída(s) com sucesso!")
            
            # Ajuste aqui: agora lemos do DB para verificar se há frases
            if not frase_manager.ler_frases() and self.lembrete_ativo:
                self.parar_lembretes_gui()
                self.label_lembrete.config(text="Todas as frases foram excluídas. Lembretes parados.")
        
    def on_atualizar_selecionado(self):
        frase_antiga = self.frase_selecionada_para_edicao 
        nova_frase = self.entrada_frase_gerenciamento.get().strip()

        if frase_antiga is None:
            messagebox.showwarning("Erro", "Nenhuma frase selecionada para atualização (estado inválido).")
            return

        if not nova_frase:
            messagebox.showwarning("Frase Vazia", "O campo de frase para atualização não pode estar vazio.")
            return

        if nova_frase == frase_antiga:
            messagebox.showinfo("Nenhuma Mudança", "A nova frase é idêntica à frase original. Nenhuma atualização realizada.")
            return
            
        # Não precisamos mais ler todas as frases para verificar duplicidade aqui
        # A função atualizar_frase do frase_manager já lida com isso.
        
        if messagebox.askyesno("Confirmar Atualização", f"Deseja atualizar '{frase_antiga}' para '{nova_frase}'?"):
            if frase_manager.atualizar_frase(frase_antiga, nova_frase):
                self.label_lembrete.config(text=f"Frase atualizada para:\n'{nova_frase}'")
                self._carregar_e_exibir_frases_inicial()
            else:
                # Se retornar False, pode ser porque a nova_frase já existe
                messagebox.showwarning("Atualização Falhou", f"Não foi possível atualizar a frase para '{nova_frase}'. Talvez a frase já exista.")
                self.label_lembrete.config(text=f"Atualização falhou para '{nova_frase}'.")
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

        # Agora lê as frases do DB
        frases_do_db = frase_manager.ler_frases()
        if not frases_do_db:
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
        # Sempre lê as frases do DB para garantir que esteja atualizado
        frases_atuais = frase_manager.ler_frases() 
        if not frases_atuais:
            self.label_lembrete.config(text="Nenhuma frase para lembrar. Parando lembretes.")
            self.parar_lembretes_gui()
            return

        frase_escolhida = random.choice(frases_atuais) # Escolhe de frases_atuais
        self.label_lembrete.config(text=f"**Lembrete:** \"{frase_escolhida}\"")

        if self.lembrete_ativo:
            self.after_id = self.master.after(self.intervalo_lembrete_ms, self._mostrar_lembrete_aleatorio)

    def importar_frases_gui(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo de frases",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if caminho_arquivo:
            total_lidas, total_adicionadas, total_duplicadas = frase_manager.importar_frases_de_arquivo(caminho_arquivo)
            self._carregar_e_exibir_frases_inicial()

            if total_lidas > 0:
                messagebox.showinfo(
                    "Importação Concluída",
                    f"Importação do arquivo '{os.path.basename(caminho_arquivo)}' concluída:\n"
                    f"- Frases lidas: {total_lidas}\n"
                    f"- Frases adicionadas: {total_adicionadas}\n"
                    f"- Frases duplicadas (não adicionadas): {total_duplicadas}"
                )
                self.label_lembrete.config(text=f"Importação de frases concluída. {total_adicionadas} novas frases adicionadas.")
            else:
                messagebox.showwarning("Importação", "Nenhuma frase válida encontrada ou erro ao ler o arquivo.")
                self.label_lembrete.config(text="Falha na importação de frases.")
        else:
            self.label_lembrete.config(text="Importação de frases cancelada.")