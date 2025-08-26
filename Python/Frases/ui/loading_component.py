# ui/loading_component.py
"""
Componente de loading reutilizável para a aplicação.
"""

import flet as ft

class LoadingComponent:
    """Componente de loading com animação e texto personalizável."""
    
    def __init__(self, language_manager, theme_manager=None):
        self.language_manager = language_manager
        self.theme_manager = theme_manager
        self.loading_container = None
        self.loading_text = None
        self.progress_ring = None
        
    def create_loading_overlay(self, message_key="loading", custom_message=None):
        """Cria um overlay de loading que cobre toda a tela."""
        
        # Define cores baseadas no tema
        if self.theme_manager:
            colors = self.theme_manager.get_theme_colors()
            bg_color = colors.get('BACKGROUND_COLOR', ft.Colors.WHITE)
            text_color = colors.get('TEXT_COLOR', ft.Colors.BLACK)
            accent_color = colors.get('ACCENT_COLOR', ft.Colors.BLUE_600)
        else:
            bg_color = ft.Colors.WHITE
            text_color = ft.Colors.BLACK
            accent_color = ft.Colors.BLUE_600
        
        # Texto do loading
        message = custom_message if custom_message else self.language_manager.t(message_key)
        
        self.loading_text = ft.Text(
            value=message,
            size=16,
            color=text_color,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_500
        )
        
        # Ring de progresso animado
        self.progress_ring = ft.ProgressRing(
            width=50,
            height=50,
            stroke_width=4,
            color=accent_color
        )
        
        # Container principal do loading
        self.loading_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.progress_ring,
                    ft.Container(height=20),
                    self.loading_text,
                    ft.Container(height=10),
                    ft.Text(
                        value=self.language_manager.t("please_wait"),
                        size=12,
                        color=ft.Colors.GREY_600,
                        italic=True,
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
            ),
            alignment=ft.alignment.center,
            bgcolor=f"{bg_color}E6",  # Adiciona transparência
            expand=True,
            padding=40,
            border_radius=10
        )
        
        return self.loading_container
    
    def create_loading_row(self, message_key="loading", custom_message=None, compact=False):
        """Cria uma linha de loading mais compacta para usar dentro de outras interfaces."""
        
        # Define cores baseadas no tema
        if self.theme_manager:
            colors = self.theme_manager.get_theme_colors()
            text_color = colors.get('TEXT_COLOR', ft.Colors.BLACK)
            accent_color = colors.get('ACCENT_COLOR', ft.Colors.BLUE_600)
        else:
            text_color = ft.Colors.BLACK
            accent_color = ft.Colors.BLUE_600
        
        # Texto do loading
        message = custom_message if custom_message else self.language_manager.t(message_key)
        
        # Tamanhos baseados no modo compacto
        ring_size = 20 if compact else 30
        text_size = 12 if compact else 14
        
        self.loading_text = ft.Text(
            value=message,
            size=text_size,
            color=text_color,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_500
        )
        
        # Ring de progresso menor
        self.progress_ring = ft.ProgressRing(
            width=ring_size,
            height=ring_size,
            stroke_width=3,
            color=accent_color
        )
        
        # Row com o loading
        loading_row = ft.Row(
            controls=[
                self.progress_ring,
                ft.Container(width=10),
                self.loading_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        return loading_row
    
    def update_message(self, message_key=None, custom_message=None):
        """Atualiza a mensagem do loading."""
        if self.loading_text:
            message = custom_message if custom_message else self.language_manager.t(message_key)
            self.loading_text.value = message
            self.loading_text.update()
    
    def create_inline_loading(self, message_key="loading", custom_message=None):
        """Cria um loading inline muito simples para usar em botões ou campos."""
        
        # Define cores baseadas no tema
        if self.theme_manager:
            colors = self.theme_manager.get_theme_colors()
            accent_color = colors.get('ACCENT_COLOR', ft.Colors.BLUE_600)
        else:
            accent_color = ft.Colors.BLUE_600
        
        # Texto do loading
        message = custom_message if custom_message else self.language_manager.t(message_key)
        
        # Container inline muito compacto
        inline_loading = ft.Row(
            controls=[
                ft.ProgressRing(
                    width=16,
                    height=16,
                    stroke_width=2,
                    color=accent_color
                ),
                ft.Container(width=5),
                ft.Text(
                    value=message,
                    size=12,
                    color=ft.Colors.GREY_700
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            tight=True
        )
        
        return inline_loading

class LoadingManager:
    """Gerenciador de loading para facilitar o uso em toda a aplicação."""
    
    def __init__(self, page: ft.Page, language_manager, theme_manager=None):
        self.page = page
        self.language_manager = language_manager
        self.theme_manager = theme_manager
        self.current_loading = None
        self.original_content = None
        
    def show_full_screen_loading(self, message_key="loading", custom_message=None):
        """Mostra um loading de tela cheia."""
        # Salva o conteúdo atual
        self.original_content = self.page.controls.copy()
        
        # Cria o componente de loading
        loading_component = LoadingComponent(self.language_manager, self.theme_manager)
        self.current_loading = loading_component.create_loading_overlay(message_key, custom_message)
        
        # Limpa a página e adiciona o loading
        self.page.clean()
        self.page.add(self.current_loading)
        self.page.update()
        
        return loading_component
    
    def hide_loading(self):
        """Esconde o loading e restaura o conteúdo original."""
        if self.original_content is not None:
            self.page.clean()
            for control in self.original_content:
                self.page.add(control)
            self.page.update()
            
            # Limpa as referências
            self.current_loading = None
            self.original_content = None
    
    def show_loading_in_container(self, container: ft.Container, message_key="loading", custom_message=None):
        """Mostra loading dentro de um container específico."""
        loading_component = LoadingComponent(self.language_manager, self.theme_manager)
        loading_overlay = loading_component.create_loading_overlay(message_key, custom_message)
        
        # Substitui o conteúdo do container
        container.content = loading_overlay
        container.update()
        
        return loading_component
