# main.py
"""
Arquivo principal da aplicação - versão modularizada com APIs.
"""


import os
import tracemalloc
import warnings
import flet as ft
from api.api_manager import ensure_api_running, stop_api
from api.internal_client import create_table, create_users_table
from utils.constants import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
from utils.window_manager import WindowManager
from ui.phrase_manager_app import PhraseManagerApp
from ui.login_screen import LoginScreen
from config import DEVELOPER_MODE, DEVELOPER_USER

# Habilita o tracemalloc para rastreamento de memória
tracemalloc.start()

# Configura warnings para serem menos verbosos em produção
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*tracemalloc.*")


def main(page: ft.Page, window_width=DEFAULT_WINDOW_WIDTH, window_height=DEFAULT_WINDOW_HEIGHT):
    """Função principal da aplicação."""
    # Aplica o tamanho da janela diretamente no page
    page.window_width = window_width
    page.window_height = window_height
    
    # Inicializa a API e o banco de dados
    print("🚀 Inicializando aplicação com APIs...")
    
    # Garante que a API esteja rodando
    if not ensure_api_running():
        page.add(ft.Text(
            "❌ Erro: Não foi possível iniciar o servidor da API.\n"
            "Verifique se as dependências estão instaladas:\n"
            "pip install flask flask-cors requests",
            color=ft.Colors.RED
        ))
        return
    
    # Inicializa o banco de dados (ainda usa acesso direto para criação inicial)
    create_table()
    create_users_table()
    
    def on_login_success():
        """Callback chamado quando o login é bem-sucedido."""
        def on_logout():
            page.clean()
            if DEVELOPER_MODE:
                # No modo dev, volta direto para app
                PhraseManagerApp(page, window_width, window_height, on_logout=on_logout)
            else:
                LoginScreen(page, on_login_success)
        page.clean()
        PhraseManagerApp(page, window_width, window_height, on_logout=on_logout)

    # Modo desenvolvedor: pula login e entra direto
    if DEVELOPER_MODE:
        print("[DEV MODE] Login automático como:", DEVELOPER_USER)
        # Opcional: criar usuário dev se não existir
        api_client = None
        try:
            from api.internal_client import get_api_client
            api_client = get_api_client()
            if not api_client.login(DEVELOPER_USER, DEVELOPER_USER)[0]:
                api_client.register_user(DEVELOPER_USER, DEVELOPER_USER)
        except Exception as e:
            print("[DEV MODE] Erro ao garantir usuário dev:", e)
        page.clean()
        PhraseManagerApp(page, window_width, window_height, on_logout=on_login_success)
    else:
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
    
    # Aplica a posição usando o WindowManager
    window_manager = WindowManager()
    window_manager.apply_window_position_and_size(saved_position)
    
    # Inicializa a API e o banco de dados
    print("🚀 Inicializando aplicação com APIs...")
    
    # Garante que a API esteja rodando
    if not ensure_api_running():
        page.add(ft.Text(
            "❌ Erro: Não foi possível iniciar o servidor da API.\n"
            "Verifique se as dependências estão instaladas:\n"
            "pip install flask flask-cors requests",
            color=ft.Colors.RED
        ))
        return
    
    # Inicializa o banco de dados
    create_table()
    create_users_table()
    
    def on_login_success():
        """Callback chamado quando o login é bem-sucedido."""
        def on_logout():
            page.clean()
            if DEVELOPER_MODE:
                PhraseManagerApp(page, saved_width, saved_height, on_logout=on_logout)
            else:
                LoginScreen(page, on_login_success)
        page.clean()
        window_manager = WindowManager()
        window_manager.apply_window_position_and_size(saved_position)
        PhraseManagerApp(page, saved_width, saved_height, on_logout=on_logout)

    # Modo desenvolvedor: pula login e entra direto
    if DEVELOPER_MODE:
        print("[DEV MODE] Login automático como:", DEVELOPER_USER)
        api_client = None
        try:
            from api.internal_client import get_api_client
            api_client = get_api_client()
            if not api_client.login(DEVELOPER_USER, DEVELOPER_USER)[0]:
                api_client.register_user(DEVELOPER_USER, DEVELOPER_USER)
        except Exception as e:
            print("[DEV MODE] Erro ao garantir usuário dev:", e)
        page.clean()
        window_manager = WindowManager()
        window_manager.apply_window_position_and_size(saved_position)
        PhraseManagerApp(page, saved_width, saved_height, on_logout=on_login_success)
    else:
        # Limpa a página e inicia com a tela de login
        page.clean()
        LoginScreen(page, on_login_success)


if __name__ == "__main__":
    import atexit
    
    # Registra função de limpeza para quando a aplicação fechar
    atexit.register(stop_api)
    
    try:
        # Carrega a posição salva se existir
        window_manager = WindowManager()
        saved_position = window_manager.load_saved_position()
        
        if saved_position and saved_position['x'] is not None and saved_position['y'] is not None:
            ft.app(target=lambda page: main_with_position(page, saved_position))
        else:
            ft.app(target=main)
    except KeyboardInterrupt:
        print("\n🛑 Aplicação interrompida pelo usuário")
        stop_api()
    except Exception as e:
        print(f"❌ Erro na aplicação: {e}")
        stop_api()
    finally:
        # Garante que a API seja parada
        stop_api()
