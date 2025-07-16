# utils/window_manager.py
"""
Gerenciamento de posição e tamanho da janela.
"""

import os
import json
import time
import ctypes
import datetime
import threading
from ctypes import wintypes
from .constants import CONFIG_FILE, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT


class WindowManager:
    """Classe responsável pelo gerenciamento da posição e tamanho da janela."""
    
    def __init__(self):
        self.config_file = CONFIG_FILE
    
    def get_window_position(self):
        """Obtém a posição real da janela usando Win32 API."""
        try:
            # Obtém o handle da janela ativa (presumivelmente nossa janela Flet)
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            
            if hwnd:
                # Estrutura RECT para armazenar as coordenadas
                rect = wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                return rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top
            else:
                return 0, 0, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
        except Exception as e:
            return 0, 0, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
    
    def detect_monitor(self, x):
        """Detecta em qual monitor a janela está baseado na coordenada X."""
        if x < -100:
            return "🟠 Esquerdo"
        elif x < 1820:
            return "🔵 Central" 
        else:
            return "🟢 Direito"
    
    def load_window_position(self):
        """Carrega a posição salva da janela."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    return data.get('x', 100), data.get('y', 100)
        except Exception as e:
            pass
        return 100, 100  # Posição padrão
    
    def save_window_position(self):
        """Salva a posição atual da janela."""
        try:
            x, y, width, height = self.get_window_position()
            
            # Adiciona timestamp para rastreamento
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            data = {
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'monitor': self.detect_monitor(x),
                'last_saved': timestamp
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            return True
        except Exception as e:
            return False
    
    def load_saved_position(self):
        """Carrega a posição e tamanho salvos se existirem."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    return {
                        'x': data.get('x', None),
                        'y': data.get('y', None),
                        'width': data.get('width', DEFAULT_WINDOW_WIDTH),
                        'height': data.get('height', DEFAULT_WINDOW_HEIGHT)
                    }
        except Exception as e:
            pass
        return None
    
    def apply_window_position_and_size(self, saved_position):
        """Aplica a posição e tamanho salvos usando Windows API."""
        def move_window_smoothly():
            time.sleep(0.3)  # Delay maior para garantir que a janela carregou completamente
            try:
                # Usa a API do Windows para mover e redimensionar a janela
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                if hwnd:
                    x = saved_position['x']
                    y = saved_position['y']
                    width = saved_position['width']
                    height = saved_position['height']
                    
                    # Primeiro tenta redimensionar a janela usando SetWindowPos
                    SWP_NOZORDER = 0x0004
                    SWP_SHOWWINDOW = 0x0040
                    
                    # Aplica o tamanho e posição em uma única operação
                    result = ctypes.windll.user32.SetWindowPos(
                        hwnd, 0, x, y, width, height, SWP_NOZORDER | SWP_SHOWWINDOW
                    )
                    
                    # Verifica se o tamanho foi aplicado corretamente
                    time.sleep(0.2)
                    rect = wintypes.RECT()
                    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                    actual_width = rect.right - rect.left
                    actual_height = rect.bottom - rect.top
                    
                    # Se o tamanho não foi aplicado corretamente, tenta novamente
                    if abs(actual_width - width) > 10 or abs(actual_height - height) > 10:
                        time.sleep(0.1)
                        
                        # Força novamente o tamanho via Windows API
                        ctypes.windll.user32.SetWindowPos(
                            hwnd, 0, x, y, width, height, SWP_NOZORDER | SWP_SHOWWINDOW
                        )
                        
                        # Verifica novamente
                        time.sleep(0.1)
                        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                        final_width = rect.right - rect.left
                        final_height = rect.bottom - rect.top
                    
            except Exception as e:
                pass
        
        # Move a janela em uma thread separada
        threading.Thread(target=move_window_smoothly, daemon=True).start()
