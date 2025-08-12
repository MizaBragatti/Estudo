# components/dialogs.py
"""
Componentes de diálogos e modais da aplicação.
"""

import flet as ft
from utils.constants import TEXT_COLOR


class DialogManager:
    """Classe responsável pelos diálogos da aplicação."""
    
    def __init__(self, page: ft.Page, language_manager=None):
        self.page = page
        self.language_manager = language_manager
    
    def show_confirmation_dialog(self, title: str, content: str, on_confirm, on_cancel=None):
        """Mostra um diálogo de confirmação."""
        def close_dlg(e):
            self.page.dialog.open = False
            self.page.update()
            if on_cancel:
                on_cancel()
        
        def confirm_action(e):
            self.page.dialog.open = False
            self.page.update()
            on_confirm()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("Sim", on_click=confirm_action),
                ft.TextButton("Não", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        if dialog not in self.page.controls:
            self.page.controls.append(dialog)
        dialog.open = True
        self.page.update()
    
    def show_duplicate_phrase_modal(self, duplicate_phrase: str, on_close=None):
        """Mostra um modal para frase duplicada."""
        def close_overlay(e):
            # Remove o overlay da página
            if hasattr(self, 'duplicate_overlay') and self.duplicate_overlay in self.page.overlay:
                self.page.overlay.remove(self.duplicate_overlay)
                self.page.update()
            if on_close:
                on_close()

        # Container principal do modal - responsivo
        modal_width = min(450, self.page.window_width * 0.8)
        modal_height = min(300, self.page.window_height * 0.5)
        
        modal_content = ft.Container(
            content=ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                # Cabeçalho com ícone e título
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.WARNING_ROUNDED, 
                                                   color=ft.Colors.ORANGE_600, 
                                                   size=32),
                                            ft.Text(self.language_manager.t("duplicate_phrase_title") if self.language_manager else "Frase Duplicada", 
                                                   size=18, 
                                                   weight=ft.FontWeight.BOLD, 
                                                   color=ft.Colors.ORANGE_700)
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=12
                                    ),
                                    margin=ft.margin.only(bottom=20)
                                ),
                                
                                # Conteúdo principal
                                ft.Container(
                                    content=ft.Text(
                                        self.language_manager.t("duplicate_phrase_message").format(duplicate_phrase) if self.language_manager else f"A frase abaixo já existe na sua lista:\n\n'{duplicate_phrase}'\n\n🔍 Veja a frase destacada em laranja na lista ao lado.\nDigite uma frase diferente ou edite a existente.",
                                        text_align=ft.TextAlign.CENTER,
                                        color=ft.Colors.GREY_700,
                                        size=14,
                                        weight=ft.FontWeight.W_400
                                    ),
                                    margin=ft.margin.only(bottom=25)
                                ),
                                
                                # Botão de ação
                                ft.Container(
                                    content=ft.ElevatedButton(
                                        self.language_manager.t("ok_understood") if self.language_manager else "OK, ENTENDI",
                                        on_click=close_overlay,
                                        bgcolor=ft.Colors.ORANGE_600,
                                        color=ft.Colors.WHITE,
                                        width=160,
                                        height=40,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            elevation=2
                                        )
                                    ),
                                    alignment=ft.alignment.center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                            tight=True
                        ),
                        padding=ft.padding.all(25),
                        width=modal_width,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=12
                    ),
                    elevation=8,
                    color=ft.Colors.WHITE
                ),
                alignment=ft.alignment.center,
                width=self.page.window_width,
                height=self.page.window_height
            ),
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),  # Fundo semi-transparente
            alignment=ft.alignment.center,
            expand=True
        )
        
        self.duplicate_overlay = modal_content
        self.page.overlay.append(self.duplicate_overlay)
        self.page.update()
        
        return self.duplicate_overlay
