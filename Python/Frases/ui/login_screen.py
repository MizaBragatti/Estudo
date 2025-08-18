# ui/login_screen.py
"""
Tela de login da aplicação - usando APIs.
"""

import flet as ft
from api.internal_client import get_api_client
from utils.constants import ACCENT_COLOR, SECONDARY_ACCENT_COLOR, BACKGROUND_COLOR, TEXT_COLOR
from utils.theme_manager import ThemeManager
from utils.language_manager import LanguageManager

# Variável global para controlar se é a primeira inicialização
_first_login_initialization = True


class LoginScreen:
    """Classe da Tela de Login para Flet."""
    
    def __init__(self, page: ft.Page, on_login_success):
        global _first_login_initialization
        
        self.page = page
        self.on_login_success = on_login_success
        self.theme_manager = ThemeManager()
        self.language_manager = LanguageManager()
        
        # Variáveis para preservar valores dos campos
        self.preserved_username = ""
        self.preserved_password = ""
        
        # Estado da API - na primeira inicialização, campos ficam bloqueados até verificação
        self.api_ready = False  # Sempre começa bloqueado para segurança
        
        # Aplica o tema atual
        colors = self.theme_manager.get_theme_colors()
        
        self.page.title = self.language_manager.t("login_title")
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.window_width = 400
        self.page.window_height = 300
        self.page.bgcolor = colors['BACKGROUND_COLOR']

        self._build_ui()
        
        # Só verifica API na primeira inicialização
        if _first_login_initialization:
            self._check_api_status()  # Verifica status da API apenas na primeira vez
            _first_login_initialization = False  # Marca que já foi inicializado
        else:
            # Se não é primeira inicialização, assume que API está pronta
            self.api_ready = True
            self._enable_fields()
        
        self.page.update()

    def _build_ui(self):
        """Constrói a interface da tela de login."""
        colors = self.theme_manager.get_theme_colors()
        
        self.username_entry = ft.TextField(
            label=self.language_manager.t("username"), width=250,
            text_align=ft.TextAlign.CENTER,
            on_submit=lambda e: self.password_entry.focus(),
            on_change=self._on_username_change,  # Preserva valor ao digitar
            color=colors['TEXT_COLOR'],
            label_style=ft.TextStyle(color=colors['TEXT_COLOR']),
            border_color=colors['BORDER_COLOR'],
            fill_color=colors['SURFACE_COLOR'],
            value=self.preserved_username,  # Restaura valor preservado
            disabled=True,  # Sempre inicia desabilitado
            hint_text=self.language_manager.t("waiting_api")
        )
        self.password_entry = ft.TextField(
            label=self.language_manager.t("password"), password=True, can_reveal_password=True, width=250,
            text_align=ft.TextAlign.CENTER,
            on_submit=self.attempt_login,
            on_change=self._on_password_change,  # Preserva valor ao digitar
            color=colors['TEXT_COLOR'],
            label_style=ft.TextStyle(color=colors['TEXT_COLOR']),
            border_color=colors['BORDER_COLOR'],
            fill_color=colors['SURFACE_COLOR'],
            value=self.preserved_password,  # Restaura valor preservado
            disabled=True,  # Sempre inicia desabilitado
            hint_text=self.language_manager.t("waiting_api")
        )

        self.login_button = ft.ElevatedButton(
            self.language_manager.t("login"), on_click=self.attempt_login,
            bgcolor=colors['ACCENT_COLOR'], color=ft.Colors.WHITE,
            width=250,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
            disabled=True  # Sempre inicia desabilitado
        )
        self.register_button = ft.ElevatedButton(
            self.language_manager.t("register"), on_click=self.attempt_register,
            bgcolor=colors['SECONDARY_ACCENT_COLOR'], color=ft.Colors.WHITE,
            width=250,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
            disabled=True  # Sempre inicia desabilitado
        )

        # Botão de configurações (engrenagem)
        self.settings_button = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            icon_color=colors['TEXT_COLOR'],
            tooltip=self.language_manager.t("settings"),
            on_click=self._open_settings
        )

        # Texto para mensagens de status/erro
        self.status_text = ft.Text(
            self.language_manager.t("api_connecting"), 
            size=14, 
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            width=250,
            color=ft.Colors.BLUE_500
        )

        # Cabeçalho centralizado com título e botão de configurações
        header_row = ft.Row(
            controls=[
                ft.Text(
                    self.language_manager.t("welcome"),
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=colors['TEXT_COLOR'],
                    text_align=ft.TextAlign.CENTER,
                    expand=True
                ),
                self.settings_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        self.page.add(
            ft.Column(
                controls=[
                    header_row,
                    ft.Container(height=20),
                    self.username_entry,
                    self.password_entry,
                    ft.Container(height=10),
                    self.status_text,  # Adicionado texto de status
                    ft.Container(height=10),
                    self.login_button,
                    self.register_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
                expand=True
            )
        )
        # Configura a snack bar para mensagens
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(""),
            action="OK",
            action_color=ft.Colors.WHITE,
            duration=4000  # 4 segundos
        )

    def _open_settings(self, e):
        """Abre a tela de configurações."""
        from ui.settings_screen import SettingsScreen
        
        # Preserva os valores dos campos antes de limpar
        self.preserved_username = self.username_entry.value
        self.preserved_password = self.password_entry.value
        
        # Limpa a página atual
        self.page.clean()
        
        # Callback para voltar à tela de login
        def on_back():
            self.page.clean()
            self._rebuild_ui()  # Reconstrói a UI sem reinicializar dados
        
        # Abre a tela de configurações passando os gerenciadores
        SettingsScreen(self.page, on_back, self.theme_manager, self.language_manager)
    
    def _rebuild_ui(self):
        """Reconstrói a interface sem reinicializar os dados preservados."""
        # Atualiza configurações da página com tema atual
        colors = self.theme_manager.get_theme_colors()
        self.page.title = self.language_manager.t("login_title")
        self.page.bgcolor = colors['BACKGROUND_COLOR']
        
        # Reconstrói a interface
        self._build_ui()
        
        # Se não é primeira inicialização, habilita campos imediatamente
        if not _first_login_initialization:
            self.api_ready = True
            self._enable_fields()
        
        self.page.update()
    
    def _update_input_field_colors(self):
        """Atualiza as cores dos campos de entrada com o tema atual."""
        colors = self.theme_manager.get_theme_colors()
        
        if hasattr(self, 'username_entry'):
            self.username_entry.color = colors['TEXT_COLOR']
            self.username_entry.label_style = ft.TextStyle(color=colors['TEXT_COLOR'])
            self.username_entry.border_color = colors['BORDER_COLOR']
            self.username_entry.fill_color = colors['SURFACE_COLOR']
            self.username_entry.update()
        
        if hasattr(self, 'password_entry'):
            self.password_entry.color = colors['TEXT_COLOR']
            self.password_entry.label_style = ft.TextStyle(color=colors['TEXT_COLOR'])
            self.password_entry.border_color = colors['BORDER_COLOR']
            self.password_entry.fill_color = colors['SURFACE_COLOR']
            self.password_entry.update()

    def _clear_status_message(self, e):
        """Limpa a mensagem de status quando o usuário começa a digitar."""
        if hasattr(self, 'status_text') and self.status_text.value:
            self.status_text.value = ""
            self.status_text.update()
    
    def _on_username_change(self, e):
        """Preserva o valor do username e limpa mensagem de status."""
        self.preserved_username = e.control.value
        self._clear_status_message(e)
    
    def _on_password_change(self, e):
        """Preserva o valor da senha e limpa mensagem de status."""
        self.preserved_password = e.control.value
        self._clear_status_message(e)
    
    def _enable_fields(self):
        """Habilita os campos de entrada e botões."""
        try:
            # Habilita os campos
            self.username_entry.disabled = False
            self.username_entry.hint_text = ""
            self.password_entry.disabled = False
            self.password_entry.hint_text = ""
            self.login_button.disabled = False
            self.register_button.disabled = False
            
            # Limpa status ou mostra mensagem de sucesso
            self.status_text.value = ""
            
            # Foca no campo de usuário
            self.username_entry.focus()
            
            # Atualiza a interface
            self.username_entry.update()
            self.password_entry.update()
            self.login_button.update()
            self.register_button.update()
            self.status_text.update()
            
        except Exception as e:
            print(f"Erro ao habilitar campos: {e}")
    
    def _check_api_status(self):
        """Simula verificação da API sem fazer nova requisição HTTP."""
        import threading
        import time
        
        def check_api():
            try:
                # Atualiza status para "conectando"
                self._update_api_status("connecting")
                
                # Pequeno delay para mostrar o status de conectando
                time.sleep(1)
                
                # Como a API já foi verificada no main.py, assumimos que está pronta
                self.api_ready = True
                self._update_api_status("ready")
                    
            except Exception as e:
                print(f"Erro ao verificar API: {e}")
                self._update_api_status("error")
        
        # Executa verificação em thread separada para não bloquear UI
        threading.Thread(target=check_api, daemon=True).start()
    
    def _update_api_status(self, status):
        """Atualiza o status da API na interface."""
        try:
            if status == "connecting":
                self.status_text.value = self.language_manager.t("api_connecting")
                self.status_text.color = ft.Colors.BLUE_500
                self.status_text.update()
                
            elif status == "ready":
                self.status_text.value = self.language_manager.t("api_ready")
                self.status_text.color = ft.Colors.GREEN_500
                self.status_text.update()
                
                # Habilita os campos usando a função dedicada
                self._enable_fields()
                
            elif status == "error":
                self.status_text.value = self.language_manager.t("api_error")
                self.status_text.color = ft.Colors.RED_500
                self.status_text.update()
            
        except Exception as e:
            print(f"Erro ao atualizar status da API: {e}")

    def show_message(self, message, is_error=False):
        """Mostra uma mensagem na tela."""
        # Atualiza o texto de status diretamente na interface
        self.status_text.value = message
        self.status_text.color = ft.Colors.RED_500 if is_error else ft.Colors.GREEN_500
        self.status_text.update()
        
        # Também mostra na snack bar como backup
        # Fecha a snack bar atual se estiver aberta
        if self.page.snack_bar.open:
            self.page.snack_bar.open = False
            self.page.update()
        
        # Configura a nova mensagem na snack bar
        self.page.snack_bar.content = ft.Text(
            message, 
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            size=14
        )
        self.page.snack_bar.bgcolor = ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700
        
        # Abre a snack bar
        self.page.snack_bar.open = True
        self.page.update()

    def attempt_login(self, e):
        """Tenta realizar o login."""
        username = self.username_entry.value.strip()
        password = self.password_entry.value.strip()
        if not username or not password:
            self.show_message(self.language_manager.t("login_required"), is_error=True)
            return
        
        # Desabilita os campos durante a verificação
        self._disable_login_fields()
        
        # Usa o cliente API em vez do frase_manager direto
        api_client = get_api_client()
        success, message = api_client.login(username, password)
        
        if success:
            self.show_message(self.language_manager.t("login_success"))
            self.on_login_success()
        else:
            self.show_message(message or self.language_manager.t("login_error"), is_error=True)
            self.password_entry.value = ""
            self.password_entry.update()
            # Reabilita os campos após erro
            self._enable_login_fields()

    def attempt_register(self, e):
        """Tenta registrar um novo usuário."""
        username = self.username_entry.value.strip()
        password = self.password_entry.value.strip()
        
        if not username or not password:
            self.show_message(self.language_manager.t("register_required"), is_error=True)
            return
        
        # Desabilita os campos durante a verificação
        self._disable_login_fields()
        
        # Usa o cliente API em vez do frase_manager direto
        api_client = get_api_client()
        success, message = api_client.register_user(username, password)
        
        if success:
            self.show_message(self.language_manager.t("register_success").format(username))
            self.username_entry.value = ""
            self.password_entry.value = ""
            self.username_entry.update()
            self.password_entry.update()
        else:
            self.show_message(message, is_error=True)
        
        # Reabilita os campos após operação
        self._enable_login_fields()
    
    def _disable_login_fields(self):
        """Desabilita os campos de login durante verificação."""
        self.username_entry.disabled = True
        self.password_entry.disabled = True
        self.login_button.disabled = True
        self.register_button.disabled = True
        self.settings_button.disabled = True
        
        self.username_entry.update()
        self.password_entry.update()
        self.login_button.update()
        self.register_button.update()
        self.settings_button.update()
    
    def _enable_login_fields(self):
        """Reabilita os campos de login após verificação."""
        self.username_entry.disabled = False
        self.password_entry.disabled = False
        self.login_button.disabled = False
        self.register_button.disabled = False
        self.settings_button.disabled = False
        
        self.username_entry.update()
        self.password_entry.update()
        self.login_button.update()
        self.register_button.update()
        self.settings_button.update()
