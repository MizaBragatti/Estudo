# ui/ui_handlers.py
"""
Manipuladores de eventos da interface do usuário.
"""

import random
import asyncio
import flet as ft
from api.internal_client import get_api_client
from utils.constants import ACCENT_COLOR, SECONDARY_ACCENT_COLOR


class UIHandlers:
    """Classe que contém os manipuladores de eventos da UI."""
    
    def __init__(self, app):
        self.app = app
        self.page = app.page
    
    def on_list_item_select(self, e, phrase_text):
        """Manipula a seleção de um item da lista."""
        # Usa apenas o modo checkbox por enquanto (mais confiável que detecção de CTRL)
        multi_select_active = self.app.multi_select_mode
        
        if multi_select_active:
            # Seleção múltipla
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
        add_enabled = input_has_text and not has_multiple_selection
        self.app.add_button.disabled = not add_enabled
        self._update_button_visual_state(self.app.add_button, add_enabled, "green")
        
        # Botão Atualizar: habilitado quando há seleção simples E há texto no input
        update_enabled = has_single_selection and input_has_text and not has_multiple_selection
        self.app.update_button.disabled = not update_enabled
        self._update_button_visual_state(self.app.update_button, update_enabled, "blue")
        
        # Botão Excluir: habilitado quando há seleção simples OU múltipla
        delete_enabled = has_single_selection or has_multiple_selection
        self.app.delete_button.disabled = not delete_enabled
        self._update_button_visual_state(self.app.delete_button, delete_enabled, "red")
        
        # Atualiza o texto do botão de exclusão baseado no tipo de seleção
        if has_multiple_selection:
            selected_count = len(self.app.phrase_list_manager.get_selected_phrases())
            self.app.delete_button.text = self.app.language_manager.t("delete_multiple_phrases").format(selected_count)
        else:
            self.app.delete_button.text = self.app.language_manager.t("delete_single_phrase")
        
        self.page.update()
    
    def _update_button_visual_state(self, button, enabled, color_theme):
        """Atualiza o estado visual do botão baseado se está habilitado ou não."""
        if enabled:
            # Botão habilitado - cores normais
            if color_theme == "green":
                button.bgcolor = ACCENT_COLOR  # Verde
                button.color = ft.Colors.WHITE
            elif color_theme == "blue":
                button.bgcolor = SECONDARY_ACCENT_COLOR  # Azul
                button.color = ft.Colors.WHITE
            elif color_theme == "red":
                button.bgcolor = ft.Colors.RED_500
                button.color = ft.Colors.WHITE
            button.opacity = 1.0
        else:
            # Botão desabilitado - aparência esmaecida
            button.bgcolor = ft.Colors.GREY_400
            button.color = ft.Colors.GREY_600
            button.opacity = 0.6
    
    def add_phrase_from_input(self, e):
        """Adiciona uma nova frase a partir do input."""
        new_phrase = self.app.phrase_input.value.strip()
        if new_phrase:
            # Tenta adicionar a frase diretamente
            result = get_api_client().add_phrase(new_phrase)
            
            if result == self.app.language_manager.t("phrase_added_success"):
                self.app.label_lembrete.value = self.app.language_manager.t("phrase_added_success_detail").format(new_phrase)
                self.app.label_lembrete.color = ACCENT_COLOR  # Cor verde para sucesso
                self.app.phrase_input.value = ""
                self.app.frase_selecionada_para_edicao = None  # Limpa a seleção
                self.page.update()
                self.app._load_and_display_phrases_initial()
            elif result == self.app.language_manager.t("phrase_already_exists"):
                # Se falhou (frase duplicada), mostra o alerta
                self.app._show_duplicate_phrase_alert(new_phrase)
            else:
                # Outros erros (usuário não logado, etc.)
                self.app.label_lembrete.value = self.app.language_manager.t("error").format(result)
                self.app.label_lembrete.color = ft.Colors.RED_600
                self.page.update()
        else:
            self.page.snack_bar.content = ft.Text(self.app.language_manager.t("please_enter_phrase"), color=ft.Colors.WHITE)
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
            self.page.snack_bar.content = ft.Text(self.app.language_manager.t("please_select_phrases"), color=ft.Colors.WHITE)
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Monta a mensagem de confirmação
        if len(phrases_to_delete) == 1:
            title = self.app.language_manager.t("confirm_deletion")
            message = self.app.language_manager.t("confirm_delete_single").format(phrases_to_delete[0])
        else:
            title = self.app.language_manager.t("confirm_multiple_deletion")
            phrase_list = '\n'.join([f"• {phrase}" for phrase in phrases_to_delete[:5]])  # Mostra até 5 frases
            if len(phrases_to_delete) > 5:
                phrase_list += f"\n{self.app.language_manager.t('and_more_phrases').format(len(phrases_to_delete) - 5)}"
            message = self.app.language_manager.t("confirm_delete_multiple").format(len(phrases_to_delete), phrase_list)

        def confirm_delete():
            if len(phrases_to_delete) == 1:
                # Exclusão simples
                success = get_api_client().delete_phrases([phrases_to_delete[0]])
                if success:
                    self.app.label_lembrete.value = self.app.language_manager.t("phrase_deleted_success").format(phrases_to_delete[0])
                else:
                    self.app.label_lembrete.value = self.app.language_manager.t("phrase_delete_error").format(phrases_to_delete[0])
            else:
                # Exclusão múltipla
                removed_count = get_api_client().delete_phrases(phrases_to_delete)
                if removed_count > 0:
                    self.app.label_lembrete.value = self.app.language_manager.t("phrases_deleted_success").format(removed_count)
                else:
                    self.app.label_lembrete.value = self.app.language_manager.t("phrases_delete_error")
            
            # Limpa as seleções
            self.app.phrase_list_manager.clear_selection()
            self.app.frase_selecionada_para_edicao = None
            self.app.phrase_input.value = ""
            # Removido phrase_input.update() duplicado - será feito em _load_and_display_phrases_initial()
            self.page.update()
            self.app._load_and_display_phrases_initial()
            
            # Verifica se ainda há frases e para lembretes se necessário
            if not get_api_client().get_phrases() and self.app.lembrete_ativo:
                async def stop_task():
                    await self.app.stop_reminders_gui_async()
                self.page.run_task(stop_task)
                self.app.label_lembrete.value = self.app.language_manager.t("all_phrases_deleted")
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
        existing_phrases = get_api_client().get_phrases()
        if new_phrase in existing_phrases:
            # Se falhou (frase duplicada), mostra o alerta imediatamente
            self.app._show_duplicate_phrase_alert(new_phrase)
            return

        def confirm_update():
            result = get_api_client().update_phrase(old_phrase, new_phrase)
            if result == "Frase atualizada com sucesso!":
                self.app.label_lembrete.value = f"Frase atualizada para:\n'{new_phrase}'"
                self.app.frase_selecionada_para_edicao = None
                self.app.phrase_input.value = ""
                # Removido phrase_input.update() duplicado - será feito em _load_and_display_phrases_initial()
                self.page.update()
                self.app._load_and_display_phrases_initial()
            else:
                # Mostra o erro específico retornado pela API
                self.app.label_lembrete.value = f"❌ Erro ao atualizar: {result}"
                self.app.label_lembrete.color = ft.Colors.RED_600
                self.page.snack_bar.content = ft.Text(f"Erro ao atualizar a frase: {result}", color=ft.Colors.WHITE)
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

        phrases_from_db = get_api_client().get_phrases()
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
        
        # Desabilita os campos de entrada enquanto os lembretes estão ativos
        self.app.toggle_timer_input_fields(False)

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
        # Chama diretamente o método async através de uma task simples
        async def stop_task():
            await self.app.stop_reminders_gui_async()
        
        # Executa a task
        self.page.run_task(stop_task)
    
    async def _show_random_reminder_loop(self):
        """Loop para mostrar lembretes aleatórios."""
        while self.app.lembrete_ativo:
            phrases_current = get_api_client().get_phrases()
            if not phrases_current:
                self.app.label_lembrete.value = "Nenhuma frase para lembrar. Parando lembretes."
                await self.app.stop_reminders_gui_async()
                return
            chosen_phrase = random.choice(phrases_current)
            self.app.label_lembrete.value = f"**Lembrete:** \"{chosen_phrase}\""
            self.page.update()
            await asyncio.sleep(self.app.intervalo_lembrete_ms / 1000)
