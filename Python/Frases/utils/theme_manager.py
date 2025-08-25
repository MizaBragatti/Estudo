# utils/theme_manager.py
"""
Gerenciador de temas da aplicação.
"""

import json
import os
import flet as ft

class ThemeManager:
    """Gerenciador de temas da aplicação."""
    
    THEME_FILE = "theme_config.json"
    
    # Tema claro
    LIGHT_THEME = {
        "name": "light",
        "accent_color": ft.Colors.GREEN_500,
        "secondary_accent_color": ft.Colors.BLUE_400,
        "background_color": ft.Colors.GREY_100,
        "text_color": ft.Colors.GREY_900,
        "surface_color": ft.Colors.WHITE,
        "border_color": ft.Colors.GREY_300,
        "disabled_color": ft.Colors.GREY_400,
        "error_color": ft.Colors.RED_500
    }
    
    # Tema escuro
    DARK_THEME = {
        "name": "dark",
        "accent_color": ft.Colors.GREEN_400,
        "secondary_accent_color": ft.Colors.BLUE_300,
        "background_color": ft.Colors.GREY_900,
        "text_color": ft.Colors.WHITE,  # Texto branco para tema escuro
        "surface_color": ft.Colors.GREY_800,
        "border_color": ft.Colors.GREY_600,
        "disabled_color": ft.Colors.GREY_600,
        "error_color": ft.Colors.RED_400
    }
    
    def __init__(self):
        self.current_theme = self.load_theme()
    
    def load_theme(self):
        """Carrega o tema salvo ou retorna o tema padrão."""
        try:
            if os.path.exists(self.THEME_FILE):
                with open(self.THEME_FILE, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    theme_name = saved_config.get('theme', 'light')
                    if theme_name == 'dark':
                        return self.DARK_THEME.copy()
                    else:
                        return self.LIGHT_THEME.copy()
            else:
                return self.LIGHT_THEME.copy()
        except Exception as e:
            print(f"Erro ao carregar tema: {e}")
            return self.LIGHT_THEME.copy()
    
    def save_theme(self, theme_name):
        """Salva o tema escolhido."""
        try:
            config = {"theme": theme_name}
            with open(self.THEME_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # Atualiza o tema atual
            if theme_name == 'dark':
                self.current_theme = self.DARK_THEME.copy()
            else:
                self.current_theme = self.LIGHT_THEME.copy()
            
            return True
        except Exception as e:
            print(f"Erro ao salvar tema: {e}")
            return False
    
    def get_current_theme(self):
        """Retorna o tema atual."""
        return self.current_theme
    
    def is_dark_theme(self):
        """Verifica se o tema atual é escuro."""
        return self.current_theme["name"] == "dark"
    
    def toggle_theme(self):
        """Alterna entre tema claro e escuro."""
        current_name = self.current_theme["name"]
        new_theme = "dark" if current_name == "light" else "light"
        return self.save_theme(new_theme)
    
    def get_theme_colors(self):
        """Retorna as cores do tema atual para uso na aplicação."""
        return {
            'ACCENT_COLOR': self.current_theme["accent_color"],
            'SECONDARY_ACCENT_COLOR': self.current_theme["secondary_accent_color"],
            'BACKGROUND_COLOR': self.current_theme["background_color"],
            'TEXT_COLOR': self.current_theme["text_color"],
            'SURFACE_COLOR': self.current_theme["surface_color"],
            'BORDER_COLOR': self.current_theme["border_color"],
            'DISABLED_COLOR': self.current_theme["disabled_color"],
            'ERROR_COLOR': self.current_theme["error_color"],
            'name': self.current_theme["name"]
        }
