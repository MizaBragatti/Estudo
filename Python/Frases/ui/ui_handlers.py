# ui/ui_handlers.py
"""
Manipuladores de eventos da interface do usuário.
"""

import random
import asyncio
import flet as ft
import frase_manager
from utils.constants import ACCENT_COLOR


class UIHandlers:
    """Classe que contém os manipuladores de eventos da UI."""
    
    def __init__(self, app):
        self.app = app
        self.page = app.page
    
    def on_list_item_select(self, e, phrase_text):
        """Manipula a seleção de um item da lista."""
        # Usa a flag de CTRL da aplicação principal
        ctrl_pressed = self.app.ctrl_pressed
        
        if ctrl_pressed:
            # Seleção múltipla com CTRL
            self.app.phrase_list_manager.toggle_phrase_selection(phrase_text)
            self.app.phrase_list_manager.reload_list_view_with_sorted_phrases(
                self.app.phrases_data, self.on_list_item_select
            )
            
            # Se há seleção múltipla, limpa o campo de entrada e seleção individual
            if self.app.phrase_list_manager.has_selection():
                self.app.phrase_input.value = ""
                self.app.frase_selecionada_para_edicao = None
            else:
                # Se não há mais seleções múltiplas, volta ao comportamento normal
                self.app.phrase_input.value = phrase_text
                self.app.frase_selecionada_para_edicao = phrase_text
        else:
            # Seleção simples (comportamento original)
            self.app.phrase_list_manager.clear_selection()
            self.app.phrase_input.value = phrase_text
            self.app.frase_selecionada_para_edicao = phrase_text
            self.app.phrase_list_manager.reload_list_view_with_sorted_phrases(
                self.app.phrases_data, self.on_list_item_select
            )
        
        self.app.phrase_input.update()
        self._update_button_states()
    
    def _update_button_states(self):
        """Atualiza o estado dos botões baseado na seleção e input."""
        has_single_selection = bool(self.app.frase_selecionada_para_edicao)
        has_multiple_selection = self.app.phrase_list_manager.has_selection()
        input_has_text = bool(self.app.phrase_input.value.strip())
        
        # Botão Adicionar: habilitado apenas quando há texto no input e não há seleção múltipla
        self.app.add_button.disabled = not input_has_text or has_multiple_selection
        
        # Botão Atualizar: habilitado quando há seleção simples E há texto no input
        self.app.update_button.disabled = not has_single_selection or not input_has_text or has_multiple_selection
        
        # Botão Excluir: habilitado quando há seleção simples OU múltipla
        self.app.delete_button.disabled = not (has_single_selection or has_multiple_selection)
        
        # Atualiza o texto do botão de exclusão baseado no tipo de seleção
        if has_multiple_selection:
            selected_count = len(self.app.phrase_list_manager.get_selected_phrases())
            self.app.delete_button.text = f"Excluir {selected_count} Frases"
        else:
            self.app.delete_button.text = "Excluir Frase"
        
        self.page.update()
    
    def add_phrase_from_input(self, e):
        """Adiciona uma nova frase a partir do input."""
        new_phrase = self.app.phrase_input.value.strip()
        if new_phrase:
            # Tenta adicionar a frase diretamente
            if frase_manager.adicionar_frase(new_phrase):
                self.app.label_lembrete.value = f"✅ Frase '{new_phrase}' adicionada com sucesso!"
                self.app.label_lembrete.color = ACCENT_COLOR  # Cor verde para sucesso
                self.app.phrase_input.value = ""
                self.app.frase_selecionada_para_edicao = None  # Limpa a seleção
                self.page.update()
                self.app._load_and_display_phrases_initial()
            else:
                # Se falhou (provavelmente frase duplicada), mostra o alerta
                self.app._show_duplicate_phrase_alert(new_phrase)
        else:
            self.page.snack_bar.content = ft.Text("Por favor, digite uma frase para adicionar.", color=ft.Colors.WHITE)
            self.page.snack_bar.open = True
            self.page.update()
    
    def on_delete_selected(self, e):
        """Manipula a exclusão de uma ou múltiplas frases selecionadas."""
        selected_phrases = self.app.phrase_list_manager.get_selected_phrases()
        single_selected_phrase = self.app.frase_selecionada_para_edicao
        
        # Determina quais frases excluir
        phrases_to_delete = []
        if selected_phrases:
            # Seleção múltipla tem prioridade
            phrases_to_delete = selected_phrases
        elif single_selected_phrase:
            # Seleção simples
            phrases_to_delete = [single_selected_phrase]
        
        if not phrases_to_delete:
            self.page.snack_bar.content = ft.Text("Por favor, selecione uma ou mais frases para excluir.", color=ft.Colors.WHITE)
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Monta a mensagem de confirmação
        if len(phrases_to_delete) == 1:
            title = "Confirmar Exclusão"
            message = f"Tem certeza que deseja excluir a frase:\n'{phrases_to_delete[0]}'?"
        else:
            title = "Confirmar Exclusão Múltipla"
            phrase_list = '\n'.join([f"• {phrase}" for phrase in phrases_to_delete[:5]])  # Mostra até 5 frases
            if len(phrases_to_delete) > 5:
                phrase_list += f"\n... e mais {len(phrases_to_delete) - 5} frases"
            message = f"Tem certeza que deseja excluir {len(phrases_to_delete)} frases?\n\n{phrase_list}"

        def confirm_delete():
            if len(phrases_to_delete) == 1:
                # Exclusão simples
                success = frase_manager.remover_frase(phrases_to_delete[0])
                if success:
                    self.app.label_lembrete.value = f"Frase '{phrases_to_delete[0]}' excluída com sucesso!"
                else:
                    self.app.label_lembrete.value = f"Erro ao excluir a frase '{phrases_to_delete[0]}'."
            else:
                # Exclusão múltipla
                removed_count = frase_manager.remover_multiplas_frases(phrases_to_delete)
                if removed_count > 0:
                    self.app.label_lembrete.value = f"{removed_count} frases excluídas com sucesso!"
                else:
                    self.app.label_lembrete.value = "Erro ao excluir as frases selecionadas."
            
            # Limpa as seleções
            self.app.phrase_list_manager.clear_selection()
            self.app.frase_selecionada_para_edicao = None
            self.app.phrase_input.value = ""
            self.app.phrase_input.update()
            self.page.update()
            self.app._load_and_display_phrases_initial()
            
            # Verifica se ainda há frases e para lembretes se necessário
            if not frase_manager.ler_frases() and self.app.lembrete_ativo:
                self.page.run_task(self.app.stop_reminders_gui_async)
                self.app.label_lembrete.value = "Todas as frases foram excluídas. Lembretes parados."
                self.page.update()

        self.app.dialog_manager.show_confirmation_dialog(title, message, confirm_delete)
    
    def select_all_phrases(self, e):
        """Seleciona todas as frases da lista."""
        if not self.app.phrases_data:
            self.page.snack_bar.content = ft.Text("Não há frases para selecionar.", color=ft.Colors.WHITE)
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        # Seleciona todas as frases
        self.app.phrase_list_manager.select_all_phrases()
        
        # Limpa a seleção individual e o campo de entrada
        self.app.frase_selecionada_para_edicao = None
        self.app.phrase_input.value = ""
        self.app.phrase_input.update()
        
        # Recarrega a lista para mostrar as seleções
        self.app.phrase_list_manager.reload_list_view_with_sorted_phrases(
            self.app.phrases_data, self.on_list_item_select
        )
        
        # Atualiza os botões
        self._update_button_states()
        
        # Mostra mensagem de confirmação
        count = len(self.app.phrases_data)
        self.app.label_lembrete.value = f"✅ {count} frases selecionadas"
        self.app.label_lembrete.color = ACCENT_COLOR
        self.page.update()
    
    def on_update_selected(self, e):
        """Manipula a atualização de uma frase selecionada."""
        old_phrase = self.app.frase_selecionada_para_edicao
        new_phrase = self.app.phrase_input.value.strip()
        
        if old_phrase is None:
            self.page.snack_bar.content = ft.Text("Nenhuma frase selecionada para atualização.", color=ft.Colors.WHITE)
            self.page.snack_bar.open = True
            self.page.update()
            return
        if not new_phrase:
            self.page.snack_bar.content = ft.Text("O campo de frase para atualização não pode estar vazio.", color=ft.Colors.WHITE)
            self.page.snack_bar.open = True
            self.page.update()
            return
        if new_phrase == old_phrase:
            # Mesmo comportamento do botão "Adicionar" - limpa o campo e a seleção
            self.app.label_lembrete.value = f"✅ Nenhuma alteração realizada - frase mantida!"
            self.app.label_lembrete.color = ACCENT_COLOR
            self.app.phrase_input.value = ""
            self.app.frase_selecionada_para_edicao = None
            self.page.update()
            self.app._load_and_display_phrases_initial()
            return

        # Verifica se a nova frase já existe (mesmo comportamento do "Adicionar")
        existing_phrases = frase_manager.ler_frases()
        if new_phrase in existing_phrases:
            # Se falhou (frase duplicada), mostra o alerta imediatamente
            self.app._show_duplicate_phrase_alert(new_phrase)
            return

        def confirm_update():
            if frase_manager.atualizar_frase(old_phrase, new_phrase):
                self.app.label_lembrete.value = f"Frase atualizada para:\n'{new_phrase}'"
                self.app.frase_selecionada_para_edicao = None
                self.app.phrase_input.value = ""
                self.app.phrase_input.update()
                self.page.update()
                self.app._load_and_display_phrases_initial()
            else:
                # Caso inesperado - não deveria chegar aqui se a verificação acima funcionou
                self.page.snack_bar.content = ft.Text(f"Erro inesperado ao atualizar a frase.", color=ft.Colors.WHITE)
                self.page.snack_bar.open = True
                self.page.update()

        self.app.dialog_manager.show_confirmation_dialog(
            "Confirmar Atualização",
            f"Deseja atualizar '{old_phrase}' para '{new_phrase}'?",
            confirm_update
        )
    
    async def start_reminders_gui(self, e):
        """Inicia os lembretes."""
        if self.app.lembrete_ativo:
            self.app.label_lembrete.value = "Lembretes já estão ativos."
            self.page.update()
            return

        try:
            interval_seconds = float(self.app.interval_entry.value)
            if interval_seconds <= 0:
                self.app.label_lembrete.value = "O intervalo deve ser um número positivo."
                self.page.update()
                return
            self.app.intervalo_lembrete_ms = int(interval_seconds * 1000)
        except ValueError:
            self.app.label_lembrete.value = "Por favor, digite um número válido para o intervalo."
            self.page.update()
            return

        try:
            timeout_minutes = float(self.app.timeout_entry.value)
            if timeout_minutes < 0:
                self.app.label_lembrete.value = "O tempo limite deve ser um número positivo ou zero para sem limite."
                self.page.update()
                return
        except ValueError:
            self.app.label_lembrete.value = "Por favor, digite um número válido para o tempo limite."
            self.page.update()
            return

        phrases_from_db = frase_manager.ler_frases()
        if not phrases_from_db:
            self.app.label_lembrete.value = "Nenhuma frase cadastrada para iniciar os lembretes."
            self.page.update()
            return

        self.app.lembrete_ativo = True
        self.app.start_button.disabled = True
        self.app.start_button.bgcolor = ft.Colors.GREEN_200
        self.app.start_button.color = ft.Colors.GREY_700
        self.app.stop_button.disabled = False
        self.app.stop_button.bgcolor = ft.Colors.RED_500
        self.app.stop_button.color = ft.Colors.WHITE

        if timeout_minutes > 0:
            timeout_ms = int(timeout_minutes * 60 * 1000)
            async def stop_after_timeout_task():
                await asyncio.sleep(timeout_ms / 1000)
                if self.app.lembrete_ativo:
                    self.page.snack_bar.content = ft.Text("Tempo limite dos lembretes atingido. Parando...", color=ft.Colors.WHITE)
                    self.page.snack_bar.open = True
                    await self.app.stop_reminders_gui_async()
            self.app.timeout_task = self.page.run_task(stop_after_timeout_task)
            self.app.label_lembrete.value = f"Lembretes iniciados! A cada {interval_seconds} segundos, por {timeout_minutes} minuto(s)."
        else:
            self.app.label_lembrete.value = f"Lembretes iniciados! A cada {interval_seconds} segundos (sem tempo limite)."

        self.page.update()
        self.app.current_reminder_task = self.page.run_task(self._show_random_reminder_loop)
    
    def stop_reminders_gui(self, e):
        """Para os lembretes."""
        # Executa a função async em uma task
        self.page.run_task(self.app.stop_reminders_gui_async)
    
    async def _show_random_reminder_loop(self):
        """Loop para mostrar lembretes aleatórios."""
        while self.app.lembrete_ativo:
            phrases_current = frase_manager.ler_frases()
            if not phrases_current:
                self.app.label_lembrete.value = "Nenhuma frase para lembrar. Parando lembretes."
                await self.app.stop_reminders_gui_async()
                return
            chosen_phrase = random.choice(phrases_current)
            self.app.label_lembrete.value = f"**Lembrete:** \"{chosen_phrase}\""
            self.page.update()
            await asyncio.sleep(self.app.intervalo_lembrete_ms / 1000)
