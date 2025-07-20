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
        
        # Apenas define configurações básicas, SEM forçar tamanho/posição
        self.page.window_maximized = False
        self.page.window_resizable = True
        self.page.bgcolor = ft.Colors.BLUE_GREY_50
        
        # Controla se o monitoramento está ativo
        self.monitoring = False
        self.monitor_task = None
        
        self._build_ui()
        
        # REMOVIDO: Não força mais o tamanho automaticamente
    
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
            "Posição: x=?, y=?, largura=?, altura=?",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900
        )
        
        self.size_text = ft.Text(
            "Tamanho: -",
            size=16,
            color=ft.Colors.GREY_700
        )
        
        self.monitor_info = ft.Text(
            "Monitor: Detectando...",
            size=14,
            color=ft.Colors.GREEN_700
        )
        
        # Campos para o usuário definir posição e tamanho
        self.x_input = ft.TextField(
            label="Posição X",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
            value="100"
        )
        
        self.y_input = ft.TextField(
            label="Posição Y", 
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
            value="100"
        )
        
        self.width_input = ft.TextField(
            label="Largura",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
            value="400"
        )
        
        self.height_input = ft.TextField(
            label="Altura",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
            value="300"
        )
        
        # Botão para aplicar posição/tamanho
        self.apply_button = ft.ElevatedButton(
            "Aplicar Posição/Tamanho",
            on_click=self.apply_window_settings,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.SETTINGS
        )
        
        # Botões de controle do monitoramento
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
                    
                    ft.Container(height=15),
                    
                    # Seção de controle de posição/tamanho
                    ft.Text("Definir Posição e Tamanho:", 
                           size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        self.x_input,
                        self.y_input,
                        self.width_input,
                        self.height_input
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    
                    ft.Row([
                        self.apply_button,
                        ft.ElevatedButton(
                            "Capturar Posição Atual",
                            on_click=self.capture_current_position,
                            bgcolor=ft.Colors.ORANGE_600,
                            color=ft.Colors.WHITE,
                            icon=ft.Icons.CAMERA_ALT
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    
                    ft.Container(height=15),
                    ft.Divider(),
                    
                    # Seção de monitoramento
                    ft.Text("Monitoramento:", 
                           size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        self.start_button,
                        self.stop_button
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    
                    ft.Container(height=15),
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
                self.coord_text.value = f"Posição: x={x}, y={y}, largura={width}, altura={height}"
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

    def apply_window_settings(self, e):
        """Aplica as configurações de posição e tamanho definidas pelo usuário."""
        try:
            x = int(self.x_input.value)
            y = int(self.y_input.value)
            width = int(self.width_input.value)
            height = int(self.height_input.value)
            
            # Aplica via Flet primeiro
            self.page.window_width = width
            self.page.window_height = height
            self.page.update()
            
            # Usa API do Windows para posição e tamanho exatos
            self.page.run_task(self._apply_settings_delayed, x, y, width, height)
            
        except ValueError:
            # Mostra erro se valores inválidos
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, insira valores numéricos válidos.", 
                               color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    async def _apply_settings_delayed(self, x, y, width, height):
        """Aplica as configurações usando API do Windows após um delay."""
        await asyncio.sleep(0.3)  # Aguarda Flet processar
        
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if hwnd:
                # Aplica posição e tamanho
                result = ctypes.windll.user32.SetWindowPos(
                    hwnd, 0, x, y, width, height,
                    0x0004 | 0x0040  # SWP_NOZORDER | SWP_SHOWWINDOW
                )
                
                if result:
                    print(f"✅ Janela configurada: x={x}, y={y}, {width}x{height}")
                    
                    # Mostra confirmação
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"Aplicado: x={x}, y={y}, {width}x{height}", 
                                       color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_700
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                else:
                    print("❌ Falha ao configurar janela")
                    
        except Exception as e:
            print(f"⚠️ Erro ao aplicar configurações: {e}")

    def capture_current_position(self, e):
        """Captura a posição e tamanho atual da janela e preenche os campos."""
        try:
            x, y, width, height = self.get_window_position()
            
            # Preenche os campos com os valores atuais
            self.x_input.value = str(x)
            self.y_input.value = str(y)
            self.width_input.value = str(width)
            self.height_input.value = str(height)
            
            self.page.update()
            
            # Mostra confirmação
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Capturado: x={x}, y={y}, {width}x{height}", 
                               color=ft.Colors.WHITE),
                bgcolor=ft.Colors.ORANGE_700
            )
            self.page.snack_bar.open = True
            self.page.update()
            
        except Exception as ex:
            print(f"Erro ao capturar posição: {ex}")

def main(page: ft.Page):
    WindowCoordinatesApp(page)

if __name__ == "__main__":
    ft.app(target=main)
