#!/usr/bin/env python3
# monitor_coordinates.py

import tracemalloc
import warnings

# Suprimir warnings específicos
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*tracemalloc.*")

# Inicializar tracemalloc para evitar warnings
tracemalloc.start()

import flet as ft
import asyncio
import ctypes
from ctypes import wintypes

class WindowCoordinatesApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Monitor de Coordenadas da Janela"
        self.page.window_width = 400
        self.page.window_height = 300
        self.page.bgcolor = ft.Colors.BLUE_GREY_50
        
        # Controla se o monitoramento está ativo
        self.monitoring = False
        self.monitor_task = None
        
        self._build_ui()
    
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
                return 0, 0, 400, 300
        except Exception as e:
            print(f"Erro ao obter posição da janela: {e}")
            return 0, 0, 400, 300
        
    def _build_ui(self):
        # Labels para mostrar as coordenadas
        self.coord_text = ft.Text(
            "Posição: x=?, y=?",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900
        )
        
        self.size_text = ft.Text(
            "Tamanho: 400x300",
            size=16,
            color=ft.Colors.GREY_700
        )
        
        self.monitor_info = ft.Text(
            "Monitor: Detectando...",
            size=14,
            color=ft.Colors.GREEN_700
        )
        
        # Botões de controle
        self.start_button = ft.ElevatedButton(
            "Iniciar Monitoramento",
            on_click=self.start_monitoring,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.PLAY_ARROW
        )
        
        self.stop_button = ft.ElevatedButton(
            "Parar Monitoramento",
            on_click=self.stop_monitoring,
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.STOP,
            disabled=True
        )
        
        # Informações de monitores estimadas
        self.monitor_guide = ft.Column([
            ft.Text("Guia Aproximado de Monitores:", 
                   size=14, weight=ft.FontWeight.BOLD),
            ft.Text("• Monitor Esquerdo: x < 0", size=12),
            ft.Text("• Monitor Central: 0 ≤ x < 1920", size=12),
            ft.Text("• Monitor Direito: x ≥ 1920", size=12),
            ft.Text("(Valores dependem da resolução)", size=10, italic=True)
        ])
        
        # Layout principal
        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Monitor de Coordenadas",
                           size=20,
                           weight=ft.FontWeight.BOLD,
                           color=ft.Colors.BLUE_900),
                    ft.Divider(),
                    
                    self.coord_text,
                    self.size_text,
                    self.monitor_info,
                    
                    ft.Container(height=20),
                    
                    ft.Row([
                        self.start_button,
                        self.stop_button
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    
                    ft.Container(height=20),
                    ft.Divider(),
                    
                    self.monitor_guide
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10),
                padding=20
            )
        )
        
    def start_monitoring(self, e):
        if not self.monitoring:
            self.monitoring = True
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.page.update()
            
            # Inicia o monitoramento assíncrono usando page.run_task
            self.page.run_task(self._monitor_coordinates)
    
    def stop_monitoring(self, e):
        if self.monitoring:
            self.monitoring = False
            if self.monitor_task:
                self.monitor_task.cancel()
            
            self.start_button.disabled = False
            self.stop_button.disabled = True
            self.page.update()
    
    async def _monitor_coordinates(self):
        """Monitora as coordenadas da janela em tempo real."""
        while self.monitoring:
            try:
                # Obtém as coordenadas reais da janela
                x, y, width, height = self.get_window_position()
                
                # Atualiza os textos
                self.coord_text.value = f"Posição: x={x}, y={y}"
                self.size_text.value = f"Tamanho: {width}x{height}"
                
                # Detecta em qual monitor provavelmente está
                monitor_name = self._detect_monitor(x)
                self.monitor_info.value = f"Monitor: {monitor_name}"
                
                # Atualiza a UI
                self.page.update()
                
                # Aguarda antes da próxima verificação
                await asyncio.sleep(0.1)  # Atualiza 10 vezes por segundo
                
            except asyncio.CancelledError:
                break
            except Exception as ex:
                print(f"Erro no monitoramento: {ex}")
                break
    
    def _detect_monitor(self, x):
        """Detecta aproximadamente em qual monitor a janela está."""
        if x < 0:
            return "🖥️ Esquerdo (x < 0)"
        elif x < 1920:  # Assumindo monitor central Full HD
            return "🖥️ Central (0 ≤ x < 1920)"
        else:
            return "🖥️ Direito (x ≥ 1920)"

def main(page: ft.Page):
    WindowCoordinatesApp(page)

if __name__ == "__main__":
    ft.app(target=main)
