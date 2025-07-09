# main.py

import flet as ft
import frase_manager
import random
import os
import asyncio

# Cores e Constantes para o Flet
ACCENT_COLOR = ft.Colors.GREEN_500
SECONDARY_ACCENT_COLOR = ft.Colors.BLUE_400
BACKGROUND_COLOR = ft.Colors.GREY_100
TEXT_COLOR = ft.Colors.GREY_900
SURFACE_COLOR = ft.Colors.WHITE

class PhraseManagerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Gerenciador e Lembretes de Frases"
        self.page.vertical_alignment = ft.CrossAxisAlignment.START
        self.page.window_width = 700
        self.page.window_height = 620
        self.page.bgcolor = BACKGROUND_COLOR

        self.intervalo_lembrete_ms = 5000
        self.lembrete_ativo = False
        self.current_reminder_task = None
        self.timeout_task = None

        self.frase_selecionada_para_edicao = None

        self.opcoes_ordenacao = {
            "Ordem de Criação (Antiga para Nova)": "original",
            "Ordem de Criação Inversa (Nova para Antiga)": "original_inversa",
            "Ordem Alfabética (A-Z)": "alfabetica",
            "Ordem Alfabética Inversa (Z-A)": "alfabetica_inversa"
        }
        self.modo_ordenacao = ft.Ref[ft.Dropdown]()

        self._build_ui()
        self._load_and_display_phrases_initial()

    def _build_ui(self):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(""), action="OK")

        self.label_lembrete = ft.Text(
            value="Clique em 'Iniciar Lembretes' para começar.",
            font_family="Arial", size=16, italic=True,
            color=TEXT_COLOR
        )

        self.interval_entry = ft.TextField(
            value="5", label="Intervalo (segundos)", width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.CENTER
        )
        self.timeout_entry = ft.TextField(
            value="0", label="Tempo Limite (minutos)", width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.CENTER
        )

        self.start_button = ft.ElevatedButton(
            "Iniciar Lembretes",
            on_click=self.start_reminders_gui,
            bgcolor=ACCENT_COLOR,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5),
            )
        )
        self.stop_button = ft.ElevatedButton(
            "Parar Lembretes",
            on_click=self.stop_reminders_gui,
            disabled=True,
            bgcolor=ft.Colors.RED_200,
            color=ft.Colors.GREY_700,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5),
            )
        )

        reminder_config_row = ft.Row(
            controls=[
                self.interval_entry,
                ft.Container(width=10),
                self.timeout_entry,
                ft.Container(width=20),
                self.start_button,
                self.stop_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        self.phrase_input = ft.TextField(
            label="Frase", expand=True, multiline=True, min_lines=1, max_lines=3,
            on_change=lambda e: self._update_button_states(),
        )

        self.add_button = ft.ElevatedButton(
            "Adicionar Frase",
            on_click=self.add_phrase_from_input,
            bgcolor=ACCENT_COLOR,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.update_button = ft.ElevatedButton(
            "Atualizar Frase",
            on_click=self.on_update_selected,
            disabled=True,
            bgcolor=ACCENT_COLOR,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.delete_button = ft.ElevatedButton(
            "Excluir Frase",
            on_click=self.on_delete_selected,
            disabled=True,
            bgcolor=ft.Colors.RED_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.import_button = ft.ElevatedButton(
            "Importar Frases",
            on_click=self.import_phrases_gui,
            bgcolor=SECONDARY_ACCENT_COLOR,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )

        options = [ft.dropdown.Option(text=key, key=key) for key in self.opcoes_ordenacao.keys()]
        self.sort_dropdown = ft.Dropdown(
            ref=self.modo_ordenacao,
            options=options,
            value=list(self.opcoes_ordenacao.keys())[0],
            on_change=self._apply_sort,
            label="Ordenar por",
            width=280
        )

        self.list_view = ft.ListView(
            expand=1, padding=10, auto_scroll=True,
            spacing=5
        )
        self.total_phrases_text = ft.Text("Total de Frases: 0", weight=ft.FontWeight.BOLD, color=TEXT_COLOR)

        self.page.add(
            ft.Container(height=10),
            self.label_lembrete,
            ft.Container(height=15),
            reminder_config_row,
            ft.Divider(height=30, thickness=2, color=ft.Colors.GREY_300),
            ft.Text("Gerenciamento de Frases", size=18, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
            ft.Container(height=15),
            ft.Row(
                controls=[
                    ft.Text("Ordenar por:", color=TEXT_COLOR),
                    self.sort_dropdown
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Container(height=15),
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self.list_view,
                            self.total_phrases_text
                        ],
                        expand=True
                    ),
                    ft.Column(
                        controls=[
                            self.phrase_input,
                            self.add_button,
                            self.update_button,
                            self.delete_button,
                            ft.Container(height=20),
                            self.import_button
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        spacing=10,
                        width=250
                    )
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=20
            )
        )
        self.page.update()

    def _load_and_display_phrases_initial(self):
        self.frase_selecionada_para_edicao = None
        self.phrase_input.value = ""
        self.phrase_input.update()
        self._apply_sort()
        self._update_button_states()

    def _apply_sort(self, e=None):
        modo_db = self.opcoes_ordenacao[self.modo_ordenacao.current.value]
        self.phrases_data = frase_manager.ler_frases(ordenacao=modo_db)
        self._reload_list_view_with_sorted_phrases()

    def _reload_list_view_with_sorted_phrases(self):
        self.list_view.controls.clear()
        if self.phrases_data:
            for i, phrase in enumerate(self.phrases_data):
                item_text = ft.Text(f"{i+1}. {phrase}", color=TEXT_COLOR)
                list_tile = ft.ListTile(
                    title=item_text,
                    on_click=lambda e, p=phrase: self._on_list_item_select(e, p),
                    hover_color=ft.Colors.BLUE_50
                )
                self.list_view.controls.append(list_tile)
        else:
            self.list_view.controls.append(ft.Text("Nenhuma frase cadastrada ainda.", color=TEXT_COLOR))

        self.total_phrases_text.value = f"Total de Frases: {len(self.phrases_data)}"
        self.page.update()

    def _on_list_item_select(self, e, phrase_text):
        self.phrase_input.value = phrase_text
        self.frase_selecionada_para_edicao = phrase_text
        self.phrase_input.update()
        self._update_button_states()

    def _update_button_states(self):
        has_selection = bool(self.frase_selecionada_para_edicao)
        input_has_text = bool(self.phrase_input.value.strip())
        self.add_button.disabled = has_selection or not input_has_text
        self.update_button.disabled = not has_selection or not input_has_text
        self.delete_button.disabled = not has_selection
        self.page.update()

    def add_phrase_from_input(self, e):
        new_phrase = self.phrase_input.value.strip()
        if new_phrase:
            if frase_manager.adicionar_frase(new_phrase):
                self.label_lembrete.value = f"Frase '{new_phrase}' adicionada com sucesso!"
                self.phrase_input.value = ""
            else:
                self.page.snack_bar.content = ft.Text(f"A frase '{new_phrase}' já existe na lista.", color=ft.Colors.WHITE)
                self.page.snack_bar.open = True
                self.label_lembrete.value = f"Frase '{new_phrase}' já existe."
        else:
            self.page.snack_bar.content = ft.Text("Por favor, digite uma frase para adicionar.", color=ft.Colors.WHITE)
            self.page.snack_bar.open = True
        self.page.update()
        self._load_and_display_phrases_initial()

    def on_delete_selected(self, e):
        phrase_to_delete = self.frase_selecionada_para_edicao
        if not phrase_to_delete:
            self.page.snack_bar.content = ft.Text("Por favor, selecione uma frase para excluir.", color=ft.Colors.WHITE)
            self.page.snack_bar.open = True
            self.page.update()
            return

        def close_dlg(e):
            self.page.dialog.open = False
            self.page.update()

        def confirm_delete(e):
            self.page.dialog.open = False
            self.page.update()
            if frase_manager.remover_frase(phrase_to_delete):
                self.label_lembrete.value = f"Frase '{phrase_to_delete}' excluída com sucesso!"
                self.frase_selecionada_para_edicao = None
                self.phrase_input.value = ""
                self.phrase_input.update()
            else:
                self.label_lembrete.value = f"Erro ao excluir a frase '{phrase_to_delete}'."
            self.page.update()
            self._load_and_display_phrases_initial()
            if not frase_manager.ler_frases() and self.lembrete_ativo:
                asyncio.create_task(self.stop_reminders_gui_async())
                self.label_lembrete.value = "Todas as frases foram excluídas. Lembretes parados."
                self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Tem certeza que deseja excluir a frase:\n'{phrase_to_delete}'?"),
            actions=[
                ft.TextButton("Sim", on_click=confirm_delete),
                ft.TextButton("Não", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dialog
        if dialog not in self.page.controls:
            self.page.controls.append(dialog)
        dialog.open = True
        self.page.update()

    async def on_update_selected(self, e):
        old_phrase = self.frase_selecionada_para_edicao
        new_phrase = self.phrase_input.value.strip()
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
            self.page.snack_bar.content = ft.Text("A nova frase é idêntica à frase original. Nenhuma atualização realizada.", color=ft.Colors.WHITE)
            self.page.snack_bar.open = True
            self.page.update()
            return

        def close_dlg(e):
            self.page.dialog.open = False
            self.page.update()

        def confirm_update(e):
            self.page.dialog.open = False
            self.page.update()
            if frase_manager.atualizar_frase(old_phrase, new_phrase):
                self.label_lembrete.value = f"Frase atualizada para:\n'{new_phrase}'"
                self.frase_selecionada_para_edicao = None
                self.phrase_input.value = ""
                self.phrase_input.update()
            else:
                self.page.snack_bar.content = ft.Text(f"Não foi possível atualizar a frase para '{new_phrase}'. Talvez a frase já exista.", color=ft.Colors.WHITE)
                self.page.snack_bar.open = True
                self.label_lembrete.value = f"Atualização falhou para '{new_phrase}'."
            self.page.update()
            self._load_and_display_phrases_initial()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Atualização"),
            content=ft.Text(f"Deseja atualizar '{old_phrase}' para '{new_phrase}'?"),
            actions=[
                ft.TextButton("Sim", on_click=confirm_update),
                ft.TextButton("Não", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dialog
        if dialog not in self.page.controls:
            self.page.controls.append(dialog)
        dialog.open = True
        self.page.update()

    async def start_reminders_gui(self, e):
        if self.lembrete_ativo:
            self.label_lembrete.value = "Lembretes já estão ativos."
            self.page.update()
            return

        try:
            interval_seconds = float(self.interval_entry.value)
            if interval_seconds <= 0:
                self.label_lembrete.value = "O intervalo deve ser um número positivo."
                self.page.update()
                return
            self.intervalo_lembrete_ms = int(interval_seconds * 1000)
        except ValueError:
            self.label_lembrete.value = "Por favor, digite um número válido para o intervalo."
            self.page.update()
            return

        try:
            timeout_minutes = float(self.timeout_entry.value)
            if timeout_minutes < 0:
                self.label_lembrete.value = "O tempo limite deve ser um número positivo ou zero para sem limite."
                self.page.update()
                return
        except ValueError:
            self.label_lembrete.value = "Por favor, digite um número válido para o tempo limite."
            self.page.update()
            return

        phrases_from_db = frase_manager.ler_frases()
        if not phrases_from_db:
            self.label_lembrete.value = "Nenhuma frase cadastrada para iniciar os lembretes."
            self.page.update()
            return

        self.lembrete_ativo = True
        self.start_button.disabled = True
        self.start_button.bgcolor = ft.Colors.GREEN_200
        self.start_button.color = ft.Colors.GREY_700
        self.stop_button.disabled = False
        self.stop_button.bgcolor = ft.Colors.RED_500
        self.stop_button.color = ft.Colors.WHITE

        if timeout_minutes > 0:
            timeout_ms = int(timeout_minutes * 60 * 1000)
            async def stop_after_timeout_task():
                await asyncio.sleep(timeout_ms / 1000)
                if self.lembrete_ativo:
                    self.page.snack_bar.content = ft.Text("Tempo limite dos lembretes atingido. Parando...", color=ft.Colors.WHITE)
                    self.page.snack_bar.open = True
                    await self.stop_reminders_gui_async()
            self.timeout_task = asyncio.create_task(stop_after_timeout_task())
            self.label_lembrete.value = f"Lembretes iniciados! A cada {interval_seconds} segundos, por {timeout_minutes} minuto(s)."
        else:
            self.label_lembrete.value = f"Lembretes iniciados! A cada {interval_seconds} segundos (sem tempo limite)."

        self.page.update()
        self.current_reminder_task = asyncio.create_task(self._show_random_reminder_loop())

    async def stop_reminders_gui(self, e):
        await self.stop_reminders_gui_async()

    async def stop_reminders_gui_async(self):
        if not self.lembrete_ativo:
            self.label_lembrete.value = "Os lembretes não estão ativos."
            self.page.update()
            return

        self.lembrete_ativo = False
        if self.current_reminder_task and not self.current_reminder_task.done():
            self.current_reminder_task.cancel()
            try:
                await self.current_reminder_task
            except asyncio.CancelledError:
                pass
            self.current_reminder_task = None

        if self.timeout_task and not self.timeout_task.done():
            self.timeout_task.cancel()
            try:
                await self.timeout_task
            except asyncio.CancelledError:
                pass
            self.timeout_task = None

        self.start_button.disabled = False
        self.start_button.bgcolor = ACCENT_COLOR
        self.start_button.color = ft.Colors.WHITE
        self.stop_button.disabled = True
        self.stop_button.bgcolor = ft.Colors.RED_200
        self.stop_button.color = ft.Colors.GREY_700
        self.label_lembrete.value = "Lembretes parados."
        self.page.update()

    async def _show_random_reminder_loop(self):
        while self.lembrete_ativo:
            phrases_current = frase_manager.ler_frases()
            if not phrases_current:
                self.label_lembrete.value = "Nenhuma frase para lembrar. Parando lembretes."
                await self.stop_reminders_gui_async()
                return
            chosen_phrase = random.choice(phrases_current)
            self.label_lembrete.value = f"**Lembrete:** \"{chosen_phrase}\""
            self.page.update()
            await asyncio.sleep(self.intervalo_lembrete_ms / 1000)

    def import_phrases_gui(self, e):
        self.page.snack_bar.content = ft.Text("Importação de arquivo requer funcionalidades mais avançadas do Flet (FilePicker).", color=ft.Colors.WHITE)
        self.page.snack_bar.open = True
        self.page.update()
        return

# --- Classe da Tela de Login para Flet ---
class LoginScreen:
    def __init__(self, page: ft.Page, on_login_success):
        self.page = page
        self.on_login_success = on_login_success
        self.page.title = "Login de Usuário"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.window_width = 400
        self.page.window_height = 300
        self.page.bgcolor = BACKGROUND_COLOR

        self.username_entry = ft.TextField(
            label="Usuário", width=250,
            text_align=ft.TextAlign.CENTER,
            on_submit=lambda e: self.password_entry.focus()
        )
        self.password_entry = ft.TextField(
            label="Senha", password=True, can_reveal_password=True, width=250,
            text_align=ft.TextAlign.CENTER,
            on_submit=self.attempt_login
        )

        self.login_button = ft.ElevatedButton(
            "Entrar", on_click=self.attempt_login,
            bgcolor=ACCENT_COLOR, color=ft.Colors.WHITE,
            width=250,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.register_button = ft.ElevatedButton(
            "Registrar Novo Usuário", on_click=self.attempt_register,
            bgcolor=SECONDARY_ACCENT_COLOR, color=ft.Colors.WHITE,
            width=250,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )

        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Bem-vindo!", size=24, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                    ft.Container(height=20),
                    self.username_entry,
                    self.password_entry,
                    ft.Container(height=20),
                    self.login_button,
                    self.register_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        )
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(""),
            action="OK"
        )
        self.page.update()

    def show_message(self, message, is_error=False):
        self.page.snack_bar.content = ft.Text(message, color=ft.Colors.WHITE)
        self.page.snack_bar.bgcolor = ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700
        self.page.snack_bar.open = True
        self.page.update()

    def attempt_login(self, e):
        username = self.username_entry.value.strip()
        password = self.password_entry.value.strip()
        if not username or not password:
            self.show_message("Por favor, insira usuário e senha.", is_error=True)
            return
        if frase_manager.authenticate_user(username, password):
            self.show_message("Login bem-sucedido!")
            self.on_login_success()
        else:
            self.show_message("Usuário ou senha inválidos.", is_error=True)
            self.password_entry.value = ""
            self.password_entry.update()

    def attempt_register(self, e):
        username = self.username_entry.value.strip()
        password = self.password_entry.value.strip()
        if not username or not password:
            self.show_message("Por favor, insira usuário e senha para registrar.", is_error=True)
            return
        if len(password) < 6:
            self.show_message("A senha deve ter pelo menos 6 caracteres.", is_error=True)
            return
        if frase_manager.register_user(username, password):
            self.show_message(f"Usuário '{username}' registrado com sucesso! Agora você pode fazer login.")
            self.username_entry.value = ""
            self.password_entry.value = ""
            self.username_entry.update()
            self.password_entry.update()
        else:
            self.show_message(f"O usuário '{username}' já existe. Por favor, escolha outro nome.", is_error=True)
            self.username_entry.value = ""
            self.password_entry.value = ""
            self.username_entry.update()
            self.password_entry.update()

def main(page: ft.Page):
    frase_manager.create_table()
    frase_manager.create_users_table()
    page.clean()
    PhraseManagerApp(page)

if __name__ == "__main__":
    ft.app(target=main)