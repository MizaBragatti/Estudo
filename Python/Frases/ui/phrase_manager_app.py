# ui/phrase_manager_app.py
"""
Aplicação principal do gerenciador de frases - usando APIs.
"""

import asyncio
import flet as ft
from api.internal_client import get_api_client
from utils.constants import (
    ACCENT_COLOR, SECONDARY_ACCENT_COLOR, BACKGROUND_COLOR, TEXT_COLOR, 
    SORT_OPTIONS, DEFAULT_INTERVAL_SECONDS
)
from utils.window_manager import WindowManager
from components.dialogs import DialogManager
from components.phrase_list import PhraseListManager
from ui.ui_handlers import UIHandlers

try:
    from coordinate_tracker import CoordinateTracker
except ImportError:
    CoordinateTracker = None


class PhraseManagerApp:
    """Classe principal da aplicação de gerenciamento de frases."""
    
    def __init__(self, page: ft.Page, window_width=700, window_height=620, enable_size_monitoring=False, on_logout=None):
        self.page = page
        self.page.title = "Gerenciador e Lembretes de Frases"
        self.page.vertical_alignment = ft.CrossAxisAlignment.START
        self.page.bgcolor = BACKGROUND_COLOR
        self.on_logout = on_logout  # Callback para logout

        # Inicialização de variáveis
        self.intervalo_lembrete_ms = DEFAULT_INTERVAL_SECONDS * 1000
        self.lembrete_ativo = False
        self.current_reminder_task = None
        self.timeout_task = None
        self.frase_selecionada_para_edicao = None
        self.ctrl_pressed = False  # Flag para detectar CTRL pressionado
        self.multi_select_mode = False  # Flag para modo de seleção múltipla
        self.enable_size_monitoring = enable_size_monitoring  # Controla se monitora tamanho da janela
        
        # Gerenciadores
        self.window_manager = WindowManager()
        self.dialog_manager = DialogManager(page)
        self.ui_handlers = UIHandlers(self)
        
        # Inicializa o rastreador de coordenadas se disponível
        self.coordinate_tracker = CoordinateTracker(page) if CoordinateTracker else None

        # Configura o evento de fechamento da janela para salvar posição/tamanho
        self.page.on_window_event = self._on_window_event
        
        # Configura eventos de teclado para detectar CTRL
        self.page.on_keyboard_event = self._on_keyboard_event

        # Opções de ordenação
        self.opcoes_ordenacao = SORT_OPTIONS
        self.modo_ordenacao = ft.Ref[ft.Dropdown]()

        # Constrói a interface
        self._build_ui()
        self._load_and_display_phrases_initial()
        
        # Aplica o tamanho da janela com delay para garantir que seja respeitado
        self.page.run_task(self._apply_window_size_delayed, window_width, window_height)
        
        # Inicia o rastreamento de coordenadas se disponível
        if self.coordinate_tracker:
            self.page.run_task(self._start_coordinate_tracking)
    
    def _on_window_event(self, e):
        """Trata eventos da janela, especialmente o fechamento."""
        try:
            if e.data == "close":
                # Não salva automaticamente - usuário deve usar o botão "💾 Salvar Posição"
                pass
        except Exception as e:
            pass
    
    def _on_keyboard_event(self, e):
        """Trata eventos de teclado para detectar CTRL pressionado."""
        try:
            # Detecta diferentes variações do CTRL
            ctrl_keys = ["Control Left", "Control Right", "ControlLeft", "ControlRight", "Control"]
            
            if e.key in ctrl_keys or "control" in e.key.lower():
                if e.event_type == "keydown":
                    self.ctrl_pressed = True
                elif e.event_type == "keyup":
                    self.ctrl_pressed = False
        except Exception:
            pass
    
    def _on_multi_select_mode_change(self, e):
        """Trata a mudança do modo de seleção múltipla."""
        self.multi_select_mode = e.control.value
        if not self.multi_select_mode:
            # Se desativou o modo, limpa a seleção múltipla
            self.phrase_list_manager.clear_selection()
            self._reload_list_view_with_sorted_phrases()
            self.ui_handlers._update_button_states()
    
    def _on_logout(self, e):
        """Trata o logout e retorna à tela de login."""
        try:
            # Para qualquer lembrete ativo
            if self.lembrete_ativo:
                self.page.run_task(self.ui_handlers.stop_reminders_gui)
            
            # Para o rastreamento de coordenadas se ativo
            if self.coordinate_tracker:
                self.coordinate_tracker.stop_tracking()
            
            # Limpa a página
            self.page.clean()
            
            # Se há callback de logout, chama ele para retornar ao login
            if self.on_logout:
                self.on_logout()
            else:
                # Fallback: recarrega a aplicação com tela de login
                from ui.login_screen import LoginScreen
                def dummy_callback():
                    pass
                LoginScreen(self.page, dummy_callback)
                
        except Exception as ex:
            print(f"Erro durante logout: {ex}")
    
    def _build_ui(self):
        """Constrói a interface do usuário."""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(""), action="OK")

        # Label de lembretes
        self.label_lembrete = ft.Text(
            value="Clique em 'Iniciar Lembretes' para começar.",
            font_family="Arial", size=16, italic=True,
            color=TEXT_COLOR
        )

        # Campos de entrada
        self.interval_entry = ft.TextField(
            value="5", label="Intervalo (segundos)", width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.CENTER
        )
        self.timeout_entry = ft.TextField(
            value="0", label="Tempo Limite (minutos)", width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.CENTER
        )

        # Botões de controle de lembretes
        self.start_button = ft.ElevatedButton(
            "Iniciar Lembretes",
            on_click=self._on_start_reminders_click,
            bgcolor=ACCENT_COLOR,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.stop_button = ft.ElevatedButton(
            "Parar Lembretes",
            on_click=self.ui_handlers.stop_reminders_gui,
            disabled=True,
            bgcolor=ft.Colors.RED_200,
            color=ft.Colors.GREY_700,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )

        # Linha de configuração de lembretes
        reminder_config_row = ft.Row(
            controls=[
                self.interval_entry,
                ft.Container(width=10),
                self.timeout_entry,
                ft.Container(width=20),
                self.start_button,
                self.stop_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        # Campo de entrada de frases
        self.phrase_input = ft.TextField(
            label="Frase", expand=True, multiline=True, min_lines=1, max_lines=3,
            on_change=lambda e: self.ui_handlers._update_button_states(),
        )

        # Campo de busca de frases
        self.search_input = ft.TextField(
            label="🔍 Buscar frases...", 
            expand=True, 
            on_change=self._on_search_change,
            prefix_icon=ft.Icons.SEARCH,
            hint_text="Digite para buscar frases",
            border_radius=8
        )

        # Botões de gerenciamento de frases
        self._create_phrase_management_buttons()
        
        # Dropdown de ordenação
        options = [ft.dropdown.Option(text=key, key=key) for key in self.opcoes_ordenacao.keys()]
        self.sort_dropdown = ft.Dropdown(
            ref=self.modo_ordenacao,
            options=options,
            value=list(self.opcoes_ordenacao.keys())[0],
            on_change=self._apply_sort,
            label="Ordenar por",
            width=280
        )

        # Lista de frases
        self.list_view = ft.ListView(
            expand=1, padding=10, auto_scroll=False,
            spacing=5
        )
        self.phrase_list_manager = PhraseListManager(self.page, self.list_view)
        
        self.total_phrases_text = ft.Text("Total de Frases: 0", weight=ft.FontWeight.BOLD, color=TEXT_COLOR)
        
        # Texto de instrução para seleção múltipla
        self.multi_select_info = ft.Text(
            "💡 Use o checkbox abaixo para ativar seleção múltipla",
            size=12, italic=True, color=ft.Colors.GREY_600
        )
        
        # Checkbox para modo de seleção múltipla
        self.multi_select_checkbox = ft.Checkbox(
            label="Modo Seleção Múltipla",
            value=False,
            on_change=self._on_multi_select_mode_change
        )

        # Cria o display de coordenadas se o rastreador estiver disponível
        coordinate_display = None
        if self.coordinate_tracker:
            coordinate_display = self.coordinate_tracker.create_coordinate_display()

        # Adiciona todos os elementos à página
        self._add_elements_to_page(coordinate_display, reminder_config_row)
    
    def _create_phrase_management_buttons(self):
        """Cria os botões de gerenciamento de frases."""
        self.add_button = ft.ElevatedButton(
            "Adicionar Frase",
            on_click=self.ui_handlers.add_phrase_from_input,
            bgcolor=ACCENT_COLOR,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.update_button = ft.ElevatedButton(
            "Atualizar Frase",
            on_click=self.ui_handlers.on_update_selected,
            disabled=True,
            bgcolor=ft.Colors.GREY_400,
            color=ft.Colors.GREY_600,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.delete_button = ft.ElevatedButton(
            "Excluir Frase",
            on_click=self.ui_handlers.on_delete_selected,
            disabled=True,
            bgcolor=ft.Colors.GREY_400,
            color=ft.Colors.GREY_600,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.import_button = ft.ElevatedButton(
            "Importar Frases",
            on_click=self.import_phrases_gui,
            bgcolor=SECONDARY_ACCENT_COLOR,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.export_button = ft.ElevatedButton(
            "Exportar Frases",
            on_click=self.export_phrases_gui,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.save_position_button = ft.ElevatedButton(
            "💾 Salvar Posição",
            on_click=self.save_current_position_gui,
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.select_all_button = ft.ElevatedButton(
            "Selecionar Tudo",
            on_click=self.ui_handlers.select_all_phrases,
            bgcolor=ft.Colors.INDIGO_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.logout_button = ft.ElevatedButton(
            "Sair/Logout",
            on_click=self._on_logout,
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
    
    def _add_elements_to_page(self, coordinate_display, reminder_config_row):
        """Adiciona todos os elementos à página."""
        self.page.add(
            # Adiciona o display de coordenadas no topo se disponível
            coordinate_display if coordinate_display else ft.Container(height=0),
            ft.Container(height=10),
            self.label_lembrete,
            ft.Container(height=15),
            reminder_config_row,
            ft.Divider(height=30, thickness=2, color=ft.Colors.GREY_300),
            ft.Text("Gerenciamento de Frases", size=18, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
            ft.Container(height=15),
            ft.Row(
                controls=[
                    ft.Text("Ordenar por:", color=TEXT_COLOR),
                    self.sort_dropdown
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Container(height=15),
            ft.Row(
                controls=[
                    self.search_input
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Container(height=10),
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self.list_view,
                            self.total_phrases_text,
                            self.multi_select_info,
                            self.multi_select_checkbox
                        ],
                        expand=True
                    ),
                    ft.Column(
                        controls=[
                            self.phrase_input,
                            self.add_button,
                            self.update_button,
                            self.delete_button,
                            self.select_all_button,
                            ft.Container(height=10),
                            self.import_button,
                            self.export_button,
                            self.save_position_button,
                            ft.Container(height=20),
                            self.logout_button
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        spacing=10,
                        width=250
                    )
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=20
            )
        )
        self.page.update()
    
    def _load_and_display_phrases_initial(self):
        """Carrega e exibe as frases inicialmente."""
        self.frase_selecionada_para_edicao = None
        self.phrase_input.value = ""
        self.phrase_input.update()
        self.phrase_list_manager.clear_selection()  # Limpa seleção múltipla
        self._apply_sort()
        self.ui_handlers._update_button_states()

    def _apply_sort(self, e=None):
        """Aplica a ordenação selecionada."""
        modo_db = self.opcoes_ordenacao[self.modo_ordenacao.current.value]
        
        # Aplica busca se houver termo
        termo_busca = self.search_input.value if hasattr(self, 'search_input') else ""
        if termo_busca and termo_busca.strip():
            self.phrases_data = get_api_client().search_phrases(termo_busca, sort_order=modo_db)
        else:
            self.phrases_data = get_api_client().get_phrases(sort_order=modo_db)
        
        self._reload_list_view_with_sorted_phrases()

    def _on_search_change(self, e):
        """Evento chamado quando o texto de busca muda."""
        termo_busca = e.control.value
        
        # Aplica a ordenação atual
        modo_db = self.opcoes_ordenacao[self.modo_ordenacao.current.value]
        
        # Busca frases com o termo especificado
        if termo_busca and termo_busca.strip():
            self.phrases_data = get_api_client().search_phrases(termo_busca, sort_order=modo_db)
        else:
            # Se não há termo de busca, mostra todas as frases
            self.phrases_data = get_api_client().get_phrases(sort_order=modo_db)
        
        self._reload_list_view_with_sorted_phrases()

    def _reload_list_view_with_sorted_phrases(self):
        """Recarrega a lista com as frases ordenadas."""
        self.phrase_list_manager.reload_list_view_with_sorted_phrases(
            self.phrases_data, 
            self.ui_handlers.on_list_item_select
        )
        self.total_phrases_text.value = f"Total de Frases: {len(self.phrases_data)}"
        self.page.update()
    
    def _show_duplicate_phrase_alert(self, duplicate_phrase):
        """Exibe um alerta quando uma frase duplicada é detectada."""
        # Primeiro, destaca a frase duplicada na lista
        self._highlight_duplicate_phrase_in_list(duplicate_phrase)
        
        # Mostra uma snack bar como backup
        self.page.snack_bar.content = ft.Text(
            f"ATENÇÃO: A frase '{duplicate_phrase}' já existe na lista!", 
            color=ft.Colors.WHITE
        )
        self.page.snack_bar.bgcolor = ft.Colors.ORANGE_700
        self.page.snack_bar.open = True
        self.page.update()
        
        # Mostra o modal de duplicata
        self.dialog_manager.show_duplicate_phrase_modal(
            duplicate_phrase, 
            self._remove_highlight_from_list
        )
        
        # Também atualiza o label_lembrete para dar feedback visual adicional
        self.label_lembrete.value = f"❌ Frase '{duplicate_phrase}' já existe! Veja destaque na lista."
        self.label_lembrete.color = ft.Colors.RED_600

    def _highlight_duplicate_phrase_in_list(self, duplicate_phrase):
        """Destaca a frase duplicada na lista com cor laranja."""
        self.phrase_list_manager.highlight_duplicate_phrase_in_list(duplicate_phrase)

    def _remove_highlight_from_list(self):
        """Remove o destaque da lista, voltando ao estado normal."""
        self.phrase_list_manager.remove_highlight_from_list(self.ui_handlers.on_list_item_select)
    
    def toggle_timer_controls(self, enabled):
        """Controla se os botões de timer estão habilitados."""
        self.start_button.disabled = not enabled
        self.stop_button.disabled = enabled
        
    def toggle_timer_input_fields(self, enabled):
        """Controla se os campos de entrada de intervalo e tempo limite estão habilitados."""
        self.interval_entry.disabled = not enabled
        self.timeout_entry.disabled = not enabled
        self.page.update()
    
    def _on_start_reminders_click(self, e):
        """Manipula o clique no botão de iniciar lembretes."""
        task = self.page.run_task(self.ui_handlers.start_reminders_gui, e)
        
    def save_current_position_gui(self, e=None):
        """Salva a posição atual quando chamado pela UI."""
        try:
            if self.window_manager.save_window_position():
                x, y, width, height = self.window_manager.get_window_position()
                monitor = self.window_manager.detect_monitor(x)
                
                # Atualiza o snack bar
                self.page.snack_bar.content = ft.Text(f"✅ Posição salva: x={x}, y={y}, {width}x{height} ({monitor})", color=ft.Colors.WHITE)
                self.page.snack_bar.bgcolor = ft.Colors.GREEN_700
                
                # Atualiza o label
                self.label_lembrete.value = f"✅ Posição salva: x={x}, y={y}, {width}x{height} ({monitor})"
                self.label_lembrete.color = ft.Colors.GREEN_600
            else:
                # Atualiza o snack bar
                self.page.snack_bar.content = ft.Text("❌ Erro ao salvar posição", color=ft.Colors.WHITE)
                self.page.snack_bar.bgcolor = ft.Colors.RED_700
                
                # Atualiza o label
                self.label_lembrete.value = "❌ Erro ao salvar posição"
                self.label_lembrete.color = ft.Colors.RED_600
            
            # Mostra o snack bar e atualiza a página
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            print(f"Erro ao salvar posição: {e}")
            self.page.snack_bar.content = ft.Text(f"❌ Erro: {e}", color=ft.Colors.WHITE)
            self.page.snack_bar.bgcolor = ft.Colors.RED_700
            self.page.snack_bar.open = True
            self.page.update()
    
    async def stop_reminders_gui_async(self):
        """Para os lembretes de forma assíncrona."""
        if not self.lembrete_ativo:
            self.label_lembrete.value = "Os lembretes não estão ativos."
            self.page.update()
            return

        self.lembrete_ativo = False
        if self.current_reminder_task and not self.current_reminder_task.done():
            self.current_reminder_task.cancel()
            self.current_reminder_task = None

        if self.timeout_task and not self.timeout_task.done():
            self.timeout_task.cancel()
            self.timeout_task = None

        self.start_button.disabled = False
        self.start_button.bgcolor = ACCENT_COLOR
        self.start_button.color = ft.Colors.WHITE
        self.stop_button.disabled = True
        self.stop_button.bgcolor = ft.Colors.RED_200
        self.stop_button.color = ft.Colors.GREY_700
        
        # Reabilita os campos de entrada quando os lembretes param
        self.toggle_timer_input_fields(True)
        
        self.label_lembrete.value = "Lembretes parados."
        self.page.update()
    
    def import_phrases_gui(self, e):
        """Interface para importar frases de um arquivo."""
        # Cria um FilePicker para seleção de arquivo
        def on_file_picked(e: ft.FilePickerResultEvent):
            if e.files:
                file_path = e.files[0].path
                self._import_phrases_from_file(file_path)
            else:
                self.page.snack_bar.content = ft.Text("Nenhum arquivo selecionado.", color=ft.Colors.WHITE)
                self.page.snack_bar.open = True
                self.page.update()

        file_picker = ft.FilePicker(on_result=on_file_picked)
        self.page.overlay.append(file_picker)
        self.page.update()
        
        # Abre o diálogo de seleção de arquivo
        file_picker.pick_files(
            dialog_title="Selecione um arquivo de texto com frases",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"]
        )

    def _import_phrases_from_file(self, file_path):
        """Importa frases de um arquivo de texto."""
        try:
            total_lidas, total_adicionadas, total_duplicadas = get_api_client().import_phrases_from_file(file_path)
            
            if total_lidas == 0:
                self.label_lembrete.value = "Nenhuma linha encontrada no arquivo."
            else:
                self.label_lembrete.value = f"Importação concluída! {total_adicionadas} frases adicionadas, {total_duplicadas} duplicadas ignoradas."
                
            self.page.snack_bar.content = ft.Text(
                f"Total de linhas lidas: {total_lidas}\n"
                f"Frases adicionadas: {total_adicionadas}\n"
                f"Frases duplicadas ignoradas: {total_duplicadas}", 
                color=ft.Colors.WHITE
            )
            self.page.snack_bar.open = True
            self.page.update()
            
            # Recarrega a lista de frases
            self._load_and_display_phrases_initial()
            
        except Exception as ex:
            self.label_lembrete.value = f"Erro durante a importação: {str(ex)}"
            self.page.snack_bar.content = ft.Text(f"Erro: {str(ex)}", color=ft.Colors.WHITE)
            self.page.snack_bar.open = True
            self.page.update()

    def export_phrases_gui(self, e):
        """Interface para exportar frases para um arquivo."""
        # Cria um FilePicker para seleção do local de salvamento
        def on_save_location_picked(e: ft.FilePickerResultEvent):
            if e.path:
                save_path = e.path
                if not save_path.endswith('.txt'):
                    save_path += '.txt'
                self._export_phrases_to_file(save_path)
            else:
                self.page.snack_bar.content = ft.Text("Exportação cancelada.", color=ft.Colors.WHITE)
                self.page.snack_bar.open = True
                self.page.update()

        file_picker = ft.FilePicker(on_result=on_save_location_picked)
        self.page.overlay.append(file_picker)
        self.page.update()
        
        # Abre o diálogo de salvamento de arquivo
        file_picker.save_file(
            dialog_title="Salvar frases como arquivo de texto",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"],
            file_name="frases_exportadas.txt"
        )

    def _export_phrases_to_file(self, file_path):
        """Exporta todas as frases para um arquivo de texto."""
        try:
            total_exportadas = get_api_client().export_phrases_to_file(file_path)
            
            if total_exportadas > 0:
                self.label_lembrete.value = f"Exportação concluída! {total_exportadas} frases exportadas para {file_path}."
                self.page.snack_bar.content = ft.Text(
                    f"✅ {total_exportadas} frases exportadas com sucesso!", 
                    color=ft.Colors.WHITE
                )
            else:
                self.label_lembrete.value = "Nenhuma frase encontrada para exportar."
                self.page.snack_bar.content = ft.Text(
                    "⚠️ Nenhuma frase encontrada para exportar.", 
                    color=ft.Colors.WHITE
                )
            
            self.page.snack_bar.open = True
            self.page.update()
            
        except Exception as ex:
            self.label_lembrete.value = f"Erro durante a exportação: {str(ex)}"
            self.page.snack_bar.content = ft.Text(f"❌ Erro: {str(ex)}", color=ft.Colors.WHITE)
            self.page.snack_bar.open = True
            self.page.update()

    async def _start_coordinate_tracking(self):
        """Inicia o rastreamento de coordenadas após um pequeno delay."""
        await asyncio.sleep(1.0)  # Aguarda a UI carregar completamente
        if self.coordinate_tracker:
            await self.coordinate_tracker.start_tracking()

    async def _apply_window_size_delayed(self, width, height):
        """Aplica o tamanho da janela com delay para garantir que seja respeitado."""
        try:
            await asyncio.sleep(0.5)  # Aguarda a UI estar completamente carregada
            
            # Reaaplica o tamanho via Flet
            self.page.window_width = width
            self.page.window_height = height
            self.page.update()
            
            # Remove mensagem de debug para console mais limpo
            # print(f"🔧 Tamanho da janela reaplicado: {width}x{height}")
            
            # Inicia verificador contínuo para manter o tamanho (apenas se habilitado)
            if self.enable_size_monitoring:
                self.page.run_task(self._monitor_window_size, width, height)
            
        except Exception as e:
            # Só loga erros críticos
            if "access" not in str(e).lower():
                print(f"❌ Erro ao configurar janela: {e}")

    async def _monitor_window_size(self, target_width, target_height):
        """Monitora e mantém o tamanho da janela."""
        try:
            # Apenas loga o início, sem mensagem no console
            last_logged_size = (target_width, target_height)
            significant_changes = 0
            
            while True:
                await asyncio.sleep(5)  # Verifica a cada 5 segundos (menos frequente)
                
                # Verifica o tamanho atual via Windows API
                try:
                    import ctypes
                    from ctypes import wintypes
                    
                    hwnd = ctypes.windll.user32.GetForegroundWindow()
                    if hwnd:
                        rect = wintypes.RECT()
                        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                        current_width = rect.right - rect.left
                        current_height = rect.bottom - rect.top
                        
                        # Threshold maior para mudanças significativas (50px em vez de 15px)
                        width_diff = abs(current_width - target_width)
                        height_diff = abs(current_height - target_height)
                        
                        if width_diff > 50 or height_diff > 50:
                            # Só loga se a mudança for realmente significativa
                            if (abs(current_width - last_logged_size[0]) > 100 or 
                                abs(current_height - last_logged_size[1]) > 100):
                                
                                significant_changes += 1
                                last_logged_size = (current_width, current_height)
                                
                                # Só mostra a cada 3 mudanças significativas para evitar spam
                                if significant_changes % 3 == 0:
                                    print(f"📏 Janela redimensionada: {current_width}x{current_height}")
                            
                            # Atualiza o tamanho alvo para o tamanho atual (usuário redimensionou)
                            target_width = current_width
                            target_height = current_height
                            
                            # Atualiza as configurações do Flet para match
                            self.page.window_width = target_width
                            self.page.window_height = target_height
                
                except Exception as e:
                    # Silencia erros de verificação para evitar spam no console
                    pass
                    
        except asyncio.CancelledError:
            # Remove mensagem de interrupção para console mais limpo
            pass
        except Exception as e:
            # Só loga erros realmente importantes
            if "access" not in str(e).lower():
                print(f"❌ Erro no monitoramento: {e}")
