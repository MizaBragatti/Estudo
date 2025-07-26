# main.py
"""
Arquivo principal da aplicação - versão modularizada.
"""

import os
import tracemalloc
import warnings
import flet as ft
import frase_manager
from utils.constants import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
from utils.window_manager import WindowManager
from ui.phrase_manager_app import PhraseManagerApp
from ui.login_screen import LoginScreen

# Habilita o tracemalloc para rastreamento de memória
tracemalloc.start()

# Configura warnings para serem menos verbosos em produção
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*tracemalloc.*")


def main(page: ft.Page, window_width=DEFAULT_WINDOW_WIDTH, window_height=DEFAULT_WINDOW_HEIGHT):
    """Função principal da aplicação."""
    # Aplica o tamanho da janela diretamente no page
    page.window_width = window_width
    page.window_height = window_height
    
    # Inicializa o banco de dados
    frase_manager.create_table()
    frase_manager.create_users_table()
    
    def on_login_success():
        """Callback chamado quando o login é bem-sucedido."""
        def on_logout():
            """Callback chamado quando o usuário faz logout."""
            page.clean()
            LoginScreen(page, on_login_success)
        
        page.clean()
        PhraseManagerApp(page, window_width, window_height, on_logout=on_logout)
    
    # Limpa a página e inicia com a tela de login
    page.clean()
    LoginScreen(page, on_login_success)


def main_with_position(page: ft.Page, saved_position: dict):
    """Função principal com posição personalizada."""
    # Obtém as dimensões salvas
    saved_width = saved_position.get('width', DEFAULT_WINDOW_WIDTH)
    saved_height = saved_position.get('height', DEFAULT_WINDOW_HEIGHT)
    
    # Aplica o tamanho da janela diretamente no page antes de qualquer outra coisa
    page.window_width = saved_width
    page.window_height = saved_height
    page.update()  # Force a atualização do tamanho
    
    def on_login_success():
        """Callback chamado quando o login é bem-sucedido."""
        def on_logout():
            """Callback chamado quando o usuário faz logout."""
            page.clean()
            LoginScreen(page, on_login_success)
        
        page.clean()
        # Aplica a posição usando o WindowManager
        window_manager = WindowManager()
        window_manager.apply_saved_position(saved_position)
        PhraseManagerApp(page, saved_width, saved_height, on_logout=on_logout)
    
    # Limpa a página e inicia com a tela de login
    page.clean()
    LoginScreen(page, on_login_success)
    window_manager.apply_window_position_and_size(saved_position)
    
    # Chama a função main com as dimensões salvas
    main(page, saved_width, saved_height)


if __name__ == "__main__":
    # Carrega a posição salva se existir
    window_manager = WindowManager()
    saved_position = window_manager.load_saved_position()
    
    if saved_position and saved_position['x'] is not None and saved_position['y'] is not None:
        ft.app(target=lambda page: main_with_position(page, saved_position))
    else:
        ft.app(target=main)
