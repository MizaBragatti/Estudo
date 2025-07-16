# ui/login_screen.py
"""
Tela de login da aplicação.
"""

import flet as ft
import frase_manager
from utils.constants import ACCENT_COLOR, SECONDARY_ACCENT_COLOR, BACKGROUND_COLOR, TEXT_COLOR


class LoginScreen:
    """Classe da Tela de Login para Flet."""
    
    def __init__(self, page: ft.Page, on_login_success):
        self.page = page
        self.on_login_success = on_login_success
        self.page.title = "Login de Usuário"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.window_width = 400
        self.page.window_height = 300
        self.page.bgcolor = BACKGROUND_COLOR

        self._build_ui()
        self.page.update()

    def _build_ui(self):
        """Constrói a interface da tela de login."""
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

    def show_message(self, message, is_error=False):
        """Mostra uma mensagem na tela."""
        self.page.snack_bar.content = ft.Text(message, color=ft.Colors.WHITE)
        self.page.snack_bar.bgcolor = ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700
        self.page.snack_bar.open = True
        self.page.update()

    def attempt_login(self, e):
        """Tenta realizar o login."""
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
        """Tenta registrar um novo usuário."""
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
