#!/usr/bin/env python3
# coordinate_tracker.py
"""
Módulo para rastrear coordenadas da janela em tempo real
Pode ser integrado à aplicação principal de frases
"""

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

class CoordinateTracker:
    """Classe para rastrear coordenadas da janela em tempo real."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.monitoring = False
        self.monitor_task = None
        self.coord_display = None
    
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
                return 0, 0, 700, 620
        except Exception as e:
            print(f"Erro ao obter posição da janela: {e}")
            return 0, 0, 700, 620
        
    def create_coordinate_display(self):
        """Cria um display compacto de coordenadas para integrar em outras UIs."""
        self.coord_display = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.DESKTOP_WINDOWS, size=16, color=ft.Colors.BLUE_600),
                ft.Text("x=?, y=?", size=12, color=ft.Colors.BLUE_800),
                ft.VerticalDivider(width=1),
                ft.Text("Monitor: ?", size=12, color=ft.Colors.GREEN_700)
            ], spacing=5),
            bgcolor=ft.Colors.BLUE_50,
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=8,
            border=ft.border.all(1, ft.Colors.BLUE_200)
        )
        return self.coord_display
    
    async def start_tracking(self):
        """Inicia o rastreamento de coordenadas."""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_task = asyncio.create_task(self._track_coordinates())
    
    def stop_tracking(self):
        """Para o rastreamento de coordenadas."""
        if self.monitoring:
            self.monitoring = False
            if self.monitor_task:
                self.monitor_task.cancel()
    
    async def _track_coordinates(self):
        """Rastreia as coordenadas da janela em tempo real."""
        while self.monitoring:
            try:
                x, y, width, height = self.get_window_position()
                
                if self.coord_display:
                    # Atualiza o display compacto
                    row_controls = self.coord_display.content.controls
                    row_controls[1].value = f"x={x}, y={y}"
                    row_controls[3].value = f"Monitor: {self._detect_monitor(x)}"
                    self.page.update()
                
                await asyncio.sleep(0.2)  # Atualiza 5 vezes por segundo
                
            except asyncio.CancelledError:
                break
            except Exception as ex:
                print(f"Erro no rastreamento: {ex}")
                break
    
    def _detect_monitor(self, x):
        """Detecta aproximadamente em qual monitor a janela está."""
        if x < -100:
            return "Esquerdo"
        elif x < 1820:  # Margem para bordas
            return "Central"
        else:
            return "Direito"

# Aplicação standalone para testar coordenadas
class FullCoordinateApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Rastreador de Coordenadas - 3 Monitores"
        self.page.window_width = 500
        self.page.window_height = 400
        self.page.bgcolor = ft.Colors.GREY_50
        
        self.tracker = CoordinateTracker(page)
        self._build_ui()
        
    def _build_ui(self):
        # Display principal de coordenadas
        self.main_coord_text = ft.Text(
            "Posição: Aguardando...",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900
        )
        
        self.detail_text = ft.Text(
            "Tamanho: 500x400",
            size=16,
            color=ft.Colors.GREY_700
        )
        
        self.monitor_text = ft.Text(
            "Monitor Atual: Detectando...",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_700
        )
        
        # Botões de controle
        self.toggle_button = ft.ElevatedButton(
            "Iniciar Rastreamento",
            on_click=self._toggle_tracking,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.PLAY_ARROW,
            width=200
        )
        
        # Guia de monitores
        monitor_guide = ft.Container(
            content=ft.Column([
                ft.Text("📍 Guia de Posicionamento:", 
                       size=16, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10),
                
                ft.Row([
                    ft.Icon(ft.Icons.DESKTOP_WINDOWS, color=ft.Colors.ORANGE_600),
                    ft.Text("Monitor Esquerdo: x < -100", size=14)
                ]),
                
                ft.Row([
                    ft.Icon(ft.Icons.DESKTOP_WINDOWS, color=ft.Colors.BLUE_600),
                    ft.Text("Monitor Central: -100 ≤ x < 1820", size=14)
                ]),
                
                ft.Row([
                    ft.Icon(ft.Icons.DESKTOP_WINDOWS, color=ft.Colors.GREEN_600),
                    ft.Text("Monitor Direito: x ≥ 1820", size=14)
                ]),
                
                ft.Container(height=10),
                ft.Text("💡 Mova a janela para ver as coordenadas mudarem!",
                       size=12, italic=True, color=ft.Colors.GREY_600)
            ]),
            bgcolor=ft.Colors.BLUE_50,
            padding=15,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_200)
        )
        
        # Layout principal
        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("🖥️ Rastreador de Coordenadas",
                           size=24,
                           weight=ft.FontWeight.BOLD,
                           color=ft.Colors.BLUE_900),
                    
                    ft.Container(height=20),
                    
                    self.main_coord_text,
                    self.detail_text,
                    self.monitor_text,
                    
                    ft.Container(height=20),
                    self.toggle_button,
                    
                    ft.Container(height=30),
                    monitor_guide
                    
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10),
                padding=20
            )
        )
        
        # Inicia o rastreamento automaticamente
        asyncio.create_task(self._auto_start())
    
    async def _auto_start(self):
        """Inicia o rastreamento automaticamente após um pequeno delay."""
        await asyncio.sleep(0.5)
        await self._toggle_tracking(None)
    
    async def _toggle_tracking(self, e):
        """Alterna entre iniciar e parar o rastreamento."""
        if not self.tracker.monitoring:
            # Inicia
            await self.tracker.start_tracking()
            self.toggle_button.text = "Parar Rastreamento"
            self.toggle_button.icon = ft.Icons.STOP
            self.toggle_button.bgcolor = ft.Colors.RED_600
            
            # Inicia monitoramento customizado
            asyncio.create_task(self._update_display())
        else:
            # Para
            self.tracker.stop_tracking()
            self.toggle_button.text = "Iniciar Rastreamento"
            self.toggle_button.icon = ft.Icons.PLAY_ARROW
            self.toggle_button.bgcolor = ft.Colors.GREEN_600
        
        self.page.update()
    
    async def _update_display(self):
        """Atualiza o display principal com informações detalhadas."""
        while self.tracker.monitoring:
            try:
                x, y, width, height = self.tracker.get_window_position()
                
                self.main_coord_text.value = f"Posição: x={x}, y={y}"
                self.detail_text.value = f"Tamanho: {width}x{height}"
                
                monitor_name = self.tracker._detect_monitor(x)
                monitor_emoji = {"Esquerdo": "🟠", "Central": "🔵", "Direito": "🟢"}
                self.monitor_text.value = f"Monitor Atual: {monitor_emoji.get(monitor_name, '⚪')} {monitor_name}"
                
                self.page.update()
                await asyncio.sleep(0.1)
                
            except asyncio.CancelledError:
                break
            except Exception as ex:
                print(f"Erro na atualização: {ex}")
                break

def main(page: ft.Page):
    FullCoordinateApp(page)

if __name__ == "__main__":
    ft.app(target=main)
