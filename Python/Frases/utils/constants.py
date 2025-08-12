# utils/constants.py
"""
Constantes e configurações da aplicação.
"""

import flet as ft

# Cores da aplicação (padrão - tema claro)
ACCENT_COLOR = ft.Colors.GREEN_500
SECONDARY_ACCENT_COLOR = ft.Colors.BLUE_400
BACKGROUND_COLOR = ft.Colors.GREY_100
TEXT_COLOR = ft.Colors.GREY_900
SURFACE_COLOR = ft.Colors.WHITE

# Configurações da janela
DEFAULT_WINDOW_WIDTH = 700
DEFAULT_WINDOW_HEIGHT = 620
CONFIG_FILE = "window_position.json"

# Configurações de lembretes
DEFAULT_INTERVAL_SECONDS = 5
DEFAULT_TIMEOUT_MINUTES = 0

# Configurações da lista
ESTIMATED_ITEM_HEIGHT = 60
VISIBLE_LIST_HEIGHT = 300

# Opções de ordenação (valores internos - as traduções ficam no LanguageManager)
SORT_OPTIONS_KEYS = {
    "sort_creation_old": "original",
    "sort_creation_new": "original_inversa", 
    "sort_alphabetical": "alfabetica",
    "sort_alphabetical_reverse": "alfabetica_inversa"
}
