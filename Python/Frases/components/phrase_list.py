# components/phrase_list.py
"""
Componentes relacionados à lista de frases.
"""

import asyncio
import flet as ft
from utils.constants import TEXT_COLOR, ESTIMATED_ITEM_HEIGHT, VISIBLE_LIST_HEIGHT


class PhraseListManager:
    """Classe responsável pelo gerenciamento da lista de frases."""
    
    def __init__(self, page: ft.Page, list_view: ft.ListView):
        self.page = page
        self.list_view = list_view
        self.phrases_data = []
        self.selected_phrases = set()  # Conjunto para armazenar frases selecionadas
    
    def reload_list_view_with_sorted_phrases(self, phrases_data: list, on_item_select=None):
        """Recarrega a lista com as frases ordenadas."""
        self.phrases_data = phrases_data
        self.list_view.controls.clear()
        
        if self.phrases_data:
            for i, phrase in enumerate(self.phrases_data):
                is_selected = phrase in self.selected_phrases
                from utils.theme_manager import ThemeManager
                theme_colors = ThemeManager().get_theme_colors()
                # Ajusta cor do texto para hover: se hover ou selecionado, texto branco; senão, cor do tema
                def get_item_text(is_hovered=False):
                    return ft.Text(
                        f"{i+1}. {phrase}",
                        color=ft.Colors.WHITE if is_selected or is_hovered else theme_colors['TEXT_COLOR'],
                        weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL
                    )
                # ListTile não tem callback direto de hover, mas podemos garantir contraste para selecionado e padrão
                list_tile = ft.ListTile(
                    title=get_item_text(),
                    on_click=lambda e, p=phrase: on_item_select(e, p) if on_item_select else None,
                    hover_color=ft.Colors.BLUE_600 if theme_colors['name']=='dark' else ft.Colors.BLUE_50,
                    bgcolor=ft.Colors.BLUE_600 if is_selected else None,
                    shape=ft.RoundedRectangleBorder(radius=8) if is_selected else None
                )
                self.list_view.controls.append(list_tile)
        else:
            from utils.theme_manager import ThemeManager
            theme_colors = ThemeManager().get_theme_colors()
            self.list_view.controls.append(ft.Text("Nenhuma frase cadastrada ainda.", color=theme_colors['TEXT_COLOR']))
        
        self.page.update()
    
    def highlight_duplicate_phrase_in_list(self, duplicate_phrase: str):
        """Destaca a frase duplicada na lista com cor laranja."""
        duplicate_index = -1
        
        # Recarrega a lista com destaque
        self.list_view.controls.clear()
        if self.phrases_data:
            for i, phrase in enumerate(self.phrases_data):
                # Verifica se é a frase duplicada
                is_duplicate = phrase == duplicate_phrase
                if is_duplicate:
                    duplicate_index = i
                
                from utils.theme_manager import ThemeManager
                theme_colors = ThemeManager().get_theme_colors()
                item_text = ft.Text(
                    f"{i+1}. {phrase}",
                    color=ft.Colors.WHITE if is_duplicate else theme_colors['TEXT_COLOR'],
                    weight=ft.FontWeight.BOLD if is_duplicate else ft.FontWeight.NORMAL
                )
                
                list_tile = ft.ListTile(
                    title=item_text,
                    on_click=lambda e, p=phrase: None,  # Temporarily disabled during highlight
                    hover_color=ft.Colors.BLUE_50,
                    bgcolor=ft.Colors.ORANGE_600 if is_duplicate else None,
                    shape=ft.RoundedRectangleBorder(radius=8) if is_duplicate else None
                )
                self.list_view.controls.append(list_tile)
        else:
            from utils.theme_manager import ThemeManager
            theme_colors = ThemeManager().get_theme_colors()
            self.list_view.controls.append(ft.Text("Nenhuma frase cadastrada ainda.", color=theme_colors['TEXT_COLOR']))
        
        self.page.update()
        
        # Rola até a frase duplicada após um pequeno delay
        if duplicate_index >= 0:
            async def scroll_task():
                await self._scroll_to_duplicate_after_delay(duplicate_index)
            self.page.run_task(scroll_task)
        
        return duplicate_index
    
    async def _scroll_to_duplicate_after_delay(self, duplicate_index: int):
        """Rola para a frase duplicada após um pequeno delay."""
        await asyncio.sleep(0.1)  # Pequeno delay para garantir que a UI foi renderizada
        try:
            # Calcula a posição aproximada do item (altura estimada por item)
            scroll_position = duplicate_index * ESTIMATED_ITEM_HEIGHT
            
            # Ajusta para centralizar o item na view
            centered_position = max(0, scroll_position - (VISIBLE_LIST_HEIGHT / 2))
            
            self.list_view.scroll_to(offset=centered_position, duration=500)
        except Exception as e:
            pass  # Se houver erro no scroll, apenas ignora
    
    def remove_highlight_from_list(self, on_item_select=None):
        """Remove o destaque da lista, voltando ao estado normal."""
        self.reload_list_view_with_sorted_phrases(self.phrases_data, on_item_select)
    
    def toggle_phrase_selection(self, phrase: str):
        """Adiciona ou remove uma frase da seleção múltipla."""
        if phrase in self.selected_phrases:
            self.selected_phrases.remove(phrase)
        else:
            self.selected_phrases.add(phrase)
    
    def clear_selection(self):
        """Limpa toda a seleção atual."""
        self.selected_phrases.clear()
    
    def get_selected_phrases(self):
        """Retorna a lista de frases selecionadas."""
        return list(self.selected_phrases)
    
    def select_all_phrases(self):
        """Seleciona todas as frases."""
        self.selected_phrases = set(self.phrases_data)
    
    def has_selection(self):
        """Verifica se há frases selecionadas."""
        return len(self.selected_phrases) > 0
