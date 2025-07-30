# api/api_manager.py
"""
Gerenciador de API que inicia automaticamente o servidor quando necessário
"""

import threading
import time
import os
import sys
import subprocess
from typing import Optional

class APIManager:
    """Gerencia o servidor da API automaticamente."""
    
    def __init__(self, api_port=5000):
        self.api_port = api_port
        self.api_thread: Optional[threading.Thread] = None
        self.api_process: Optional[subprocess.Popen] = None
        self.is_running = False
        
    def start_api_server(self, background=True):
        """Inicia o servidor da API."""
        if self.is_running:
            return True
        
        try:
            if background:
                # Inicia em thread separada
                self._start_api_thread()
            else:
                # Inicia em processo separado
                self._start_api_process()
                
            # Aguarda um pouco para o servidor inicializar
            time.sleep(2)
            
            # Verifica se está funcionando
            if self._check_api_health():
                self.is_running = True
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Erro ao iniciar API: {e}")
            return False
    
    def _start_api_thread(self):
        """Inicia API em thread separada."""
        def run_api():
            try:
                # Importa e executa a API
                sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from api.phrase_api import app
                app.run(host='localhost', port=self.api_port, debug=False, use_reloader=False)
            except Exception as e:
                print(f"Erro na thread da API: {e}")
        
        self.api_thread = threading.Thread(target=run_api, daemon=True)
        self.api_thread.start()
    
    def _start_api_process(self):
        """Inicia API em processo separado."""
        try:
            api_script = os.path.join(os.path.dirname(__file__), 'phrase_api.py')
            self.api_process = subprocess.Popen([
                sys.executable, api_script
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Erro ao iniciar processo da API: {e}")
    
    def _check_api_health(self):
        """Verifica se a API está funcionando."""
        try:
            import requests
            response = requests.get(f'http://localhost:{self.api_port}/api/v1/health', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def stop_api_server(self):
        """Para o servidor da API."""
        self.is_running = False
        
        if self.api_process:
            try:
                self.api_process.terminate()
                self.api_process.wait(timeout=5)
            except:
                try:
                    self.api_process.kill()
                except:
                    pass
            self.api_process = None
    
    def ensure_api_running(self):
        """Garante que a API esteja rodando."""
        if not self.is_running or not self._check_api_health():
            print("🚀 Iniciando servidor da API...")
            return self.start_api_server()
        return True
    
    def __del__(self):
        """Limpa recursos ao destruir o objeto."""
        self.stop_api_server()


# Instância global do gerenciador
_api_manager = None

def get_api_manager():
    """Retorna a instância global do gerenciador de API."""
    global _api_manager
    if _api_manager is None:
        _api_manager = APIManager()
    return _api_manager

def ensure_api_running():
    """Função utilitária para garantir que a API esteja rodando."""
    manager = get_api_manager()
    return manager.ensure_api_running()

def stop_api():
    """Função utilitária para parar a API."""
    manager = get_api_manager()
    manager.stop_api_server()
