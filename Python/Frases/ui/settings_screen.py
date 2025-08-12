# ui/settings_screen.py
"""
Tela de configurações da aplicação.
"""

import flet as ft
from utils.theme_manager import ThemeManager
from utils.language_manager import LanguageManager
from utils.window_manager import WindowManager
import subprocess
import platform


class SettingsScreen:
    """Tela de configurações da aplicação."""
    
    def __init__(self, page: ft.Page, on_back_callback, theme_manager=None, language_manager=None, on_language_change=None):
        self.page = page
        self.on_back_callback = on_back_callback
        self.theme_manager = theme_manager or ThemeManager()
        self.language_manager = language_manager or LanguageManager()
        self.window_manager = WindowManager()
        self.on_language_change = on_language_change  # Callback para mudança de idioma
        
        # Aplica o tema atual
        self._apply_current_theme()
        
        self.page.title = self.language_manager.t("settings_title")
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self._build_ui()
        self.page.update()
    
    def _apply_current_theme(self):
        """Aplica o tema atual à página."""
        colors = self.theme_manager.get_theme_colors()
        self.page.bgcolor = colors['BACKGROUND_COLOR']
    
    def _build_ui(self):
        """Constrói a interface da tela de configurações."""
        colors = self.theme_manager.get_theme_colors()
        
        # Título
        title = ft.Text(
            self.language_manager.t("settings_title"),
            size=24,
            weight=ft.FontWeight.BOLD,
            color=colors['TEXT_COLOR']
        )
        
        # Seção de posição da janela
        self._create_position_section(colors)
        
        # Seção de tema
        self._create_theme_section(colors)
        
        # Seção de idioma
        self._create_language_section(colors)
        
        # Seção de monitor
        self._create_monitor_section(colors)
        
        # Botões de ação
        self._create_action_buttons(colors)
        
        # Container principal
        main_container = ft.Container(
            content=ft.Column(
                controls=[
                    title,
                    ft.Container(height=20),
                    
                    # Seção de Posição
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    self.language_manager.t("window_position"),
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=colors['TEXT_COLOR']
                                ),
                                ft.Container(height=10),
                                self.position_info,
                                ft.Container(height=10),
                                ft.Row(
                                    controls=[
                                        self.save_position_button,
                                        self.reset_position_button
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=10
                                )
                            ]
                        ),
                        bgcolor=colors['SURFACE_COLOR'],
                        border_radius=10,
                        padding=20,
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Seção de Monitor
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    self.language_manager.t("monitor_title"),
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=colors['TEXT_COLOR']
                                ),
                                ft.Container(height=10),
                                self.monitor_info
                            ]
                        ),
                        bgcolor=colors['SURFACE_COLOR'],
                        border_radius=10,
                        padding=20,
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Seção de Tema
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    self.language_manager.t("theme_title"),
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=colors['TEXT_COLOR']
                                ),
                                ft.Container(height=10),
                                ft.Row(
                                    controls=[
                                        self.theme_light_button,
                                        self.theme_dark_button
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=10
                                )
                            ]
                        ),
                        bgcolor=colors['SURFACE_COLOR'],
                        border_radius=10,
                        padding=20,
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Seção de Idioma
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    self.language_manager.t("language_title"),
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=colors['TEXT_COLOR']
                                ),
                                ft.Container(height=10),
                                ft.Row(
                                    controls=[
                                        self.language_pt_button,
                                        self.language_en_button,
                                        self.language_es_button
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=10
                                )
                            ]
                        ),
                        bgcolor=colors['SURFACE_COLOR'],
                        border_radius=10,
                        padding=20,
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Botão Voltar
                    ft.Container(height=20),
                    self.back_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
            ),
            width=500,
            padding=20
        )
        
        self.page.add(main_container)
    
    def _create_position_section(self, colors):
        """Cria a seção de posição da janela."""
        # Obtém informações da posição atual
        try:
            position_info = self.window_manager.get_current_position_info()
            x = position_info.get('x', 'N/A')
            y = position_info.get('y', 'N/A')
            width = position_info.get('width', 'N/A')
            height = position_info.get('height', 'N/A')
        except:
            x = y = width = height = 'N/A'
        
        self.position_info = ft.Text(
            f"X: {x} | Y: {y} | {self.language_manager.t('width')}: {width} | {self.language_manager.t('height')}: {height}",
            size=14,
            color=colors['TEXT_COLOR'],
            text_align=ft.TextAlign.CENTER
        )
        
        self.save_position_button = ft.ElevatedButton(
            self.language_manager.t("save_position"),
            on_click=self._save_position,
            bgcolor=colors['ACCENT_COLOR'],
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        
        self.reset_position_button = ft.ElevatedButton(
            self.language_manager.t("reset_position"),
            on_click=self._reset_position,
            bgcolor=colors['SECONDARY_ACCENT_COLOR'],
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
    
    def _create_monitor_section(self, colors):
        """Cria a seção de informações do monitor."""
        try:
            position_info = self.window_manager.get_current_position_info()
            monitor = position_info.get('monitor', 'N/A')
        except:
            monitor = 'N/A'
        
        self.monitor_info = ft.Text(
            self.language_manager.t("current_monitor").format(monitor),
            size=14,
            color=colors['TEXT_COLOR'],
            text_align=ft.TextAlign.CENTER
        )
    
    def _create_theme_section(self, colors):
        """Cria a seção de seleção de tema."""
        is_dark = self.theme_manager.is_dark_theme()
        
        # Corrige a lógica dos botões - tema ativo deve ter cor de destaque
        self.theme_light_button = ft.ElevatedButton(
            self.language_manager.t("light_theme"),
            on_click=lambda e: self._change_theme('light'),
            bgcolor=colors['ACCENT_COLOR'] if not is_dark else ft.Colors.GREY_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        
        self.theme_dark_button = ft.ElevatedButton(
            self.language_manager.t("dark_theme"),
            on_click=lambda e: self._change_theme('dark'),
            bgcolor=colors['ACCENT_COLOR'] if is_dark else ft.Colors.GREY_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
    
    def _create_language_section(self, colors):
        """Cria a seção de seleção de idioma."""
        current_lang = self.language_manager.get_current_language()
        
        self.language_pt_button = ft.ElevatedButton(
            self.language_manager.t("language_pt"),
            on_click=lambda e: self._change_language('pt'),
            bgcolor=colors['ACCENT_COLOR'] if current_lang == 'pt' else ft.Colors.GREY_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        
        self.language_en_button = ft.ElevatedButton(
            self.language_manager.t("language_en"),
            on_click=lambda e: self._change_language('en'),
            bgcolor=colors['ACCENT_COLOR'] if current_lang == 'en' else ft.Colors.GREY_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        
        self.language_es_button = ft.ElevatedButton(
            self.language_manager.t("language_es"),
            on_click=lambda e: self._change_language('es'),
            bgcolor=colors['ACCENT_COLOR'] if current_lang == 'es' else ft.Colors.GREY_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
    
    def _create_action_buttons(self, colors):
        """Cria os botões de ação."""
        self.back_button = ft.ElevatedButton(
            self.language_manager.t("back"),
            on_click=self._on_back,
            bgcolor=colors['SECONDARY_ACCENT_COLOR'],
            color=ft.Colors.WHITE,
            width=200,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
    
    def _save_position(self, e):
        """Salva a posição atual da janela."""
        try:
            success = self.window_manager.save_current_position()
            if success:
                self._show_message(self.language_manager.t("position_saved"), False)
                self._update_position_info()
            else:
                self._show_message(self.language_manager.t("position_save_error"), True)
        except Exception as ex:
            self._show_message(f"❌ Erro: {ex}", True)
    
    def _reset_position(self, e):
        """Reseta a posição da janela para o padrão."""
        try:
            success = self.window_manager.reset_position()
            if success:
                self._show_message(self.language_manager.t("position_reset"), False)
                self._update_position_info()
            else:
                self._show_message(self.language_manager.t("position_reset_error"), True)
        except Exception as ex:
            self._show_message(f"❌ Erro: {ex}", True)
    
    def _change_theme(self, theme_name):
        """Muda o tema da aplicação."""
        try:
            current_theme = self.theme_manager.get_current_theme()['name']
            if current_theme == theme_name:
                self._show_message(self.language_manager.t("theme_already_active"), False)
                return
                
            success = self.theme_manager.save_theme(theme_name)
            if success:
                self._show_message(self.language_manager.t("theme_changed"), False)
                # Atualiza a interface imediatamente com o novo tema
                self._apply_current_theme()
                self._update_theme_buttons()
                self._rebuild_interface()
            else:
                self._show_message(self.language_manager.t("theme_change_error"), True)
        except Exception as ex:
            self._show_message(f"❌ Erro: {ex}", True)
    
    def _change_language(self, language):
        """Muda o idioma da aplicação."""
        try:
            current_lang = self.language_manager.get_current_language()
            if current_lang == language:
                self._show_message(self.language_manager.t("language_already_active"), False)
                return
                
            success = self.language_manager.save_language(language)
            if success:
                # Reconstrói a interface com o novo idioma primeiro
                self._rebuild_interface()
                # Agora mostra a mensagem no novo idioma
                self._show_message(self.language_manager.t("language_changed"), False)
                # Notifica callback de mudança de idioma se existir
                if self.on_language_change:
                    self.on_language_change()
            else:
                self._show_message(self.language_manager.t("language_change_error"), True)
        except Exception as ex:
            self._show_message(f"❌ Erro: {ex}", True)
    
    def _rebuild_interface(self):
        """Reconstrói toda a interface com as traduções atuais."""
        # Força o recarregamento do idioma atual
        self.language_manager.current_language = self.language_manager.load_language()
        
        # Atualiza o título da página
        self.page.title = self.language_manager.t("settings_title")
        
        # Limpa e reconstrói a interface
        self.page.clean()
        self._build_ui()
        
        # Atualiza os botões de idioma com o novo texto
        self._update_language_buttons()
        
        self.page.update()
    
    def _update_position_info(self):
        """Atualiza as informações de posição na tela."""
        try:
            position_info = self.window_manager.get_current_position_info()
            x = position_info.get('x', 'N/A')
            y = position_info.get('y', 'N/A')
            width = position_info.get('width', 'N/A')
            height = position_info.get('height', 'N/A')
            monitor = position_info.get('monitor', 'N/A')
            
            self.position_info.value = f"X: {x} | Y: {y} | Largura: {width} | Altura: {height}"
            self.monitor_info.value = f"Monitor Atual: {monitor}"
            
            self.position_info.update()
            self.monitor_info.update()
        except Exception as e:
            print(f"Erro ao atualizar informações de posição: {e}")
    
    def _update_theme_buttons(self):
        """Atualiza a aparência dos botões de tema."""
        colors = self.theme_manager.get_theme_colors()
        is_dark = self.theme_manager.is_dark_theme()
        
        # Atualiza os botões com a lógica correta
        self.theme_light_button.bgcolor = colors['ACCENT_COLOR'] if not is_dark else ft.Colors.GREY_500
        self.theme_dark_button.bgcolor = colors['ACCENT_COLOR'] if is_dark else ft.Colors.GREY_500
        
        self.theme_light_button.update()
        self.theme_dark_button.update()
    
    def _update_language_buttons(self):
        """Atualiza o texto e aparência dos botões de idioma."""
        colors = self.theme_manager.get_theme_colors()
        current_lang = self.language_manager.get_current_language()
        
        # Atualiza o texto dos botões
        self.language_pt_button.text = self.language_manager.t("language_pt")
        self.language_en_button.text = self.language_manager.t("language_en")
        self.language_es_button.text = self.language_manager.t("language_es")
        
        # Atualiza as cores dos botões
        self.language_pt_button.bgcolor = colors['ACCENT_COLOR'] if current_lang == 'pt' else ft.Colors.GREY_500
        self.language_en_button.bgcolor = colors['ACCENT_COLOR'] if current_lang == 'en' else ft.Colors.GREY_500
        self.language_es_button.bgcolor = colors['ACCENT_COLOR'] if current_lang == 'es' else ft.Colors.GREY_500
        
        # Atualiza os botões na interface
        self.language_pt_button.update()
        self.language_en_button.update()
        self.language_es_button.update()
    
    def _show_message(self, message, is_error=False):
        """Mostra uma mensagem na tela."""
        colors = self.theme_manager.get_theme_colors()
        
        # Configura a snack bar
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=colors['ERROR_COLOR'] if is_error else colors['ACCENT_COLOR'],
            action="OK",
            action_color=ft.Colors.WHITE,
            duration=4000
        )
        
        self.page.snack_bar.open = True
        self.page.update()
    
    def _on_back(self, e):
        """Callback para voltar à tela anterior."""
        if self.on_back_callback:
            self.on_back_callback()
