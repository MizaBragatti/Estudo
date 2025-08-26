# ui/phrase_manager_app.py
"""
Aplicação principal do gerenciador de frases - usando APIs.
"""

import asyncio
import flet as ft
from api.internal_client import get_api_client
from utils.constants import (
    ACCENT_COLOR, SECONDARY_ACCENT_COLOR, BACKGROUND_COLOR, TEXT_COLOR, 
    SORT_OPTIONS_KEYS, DEFAULT_INTERVAL_SECONDS
)
from utils.theme_manager import ThemeManager
from utils.language_manager import LanguageManager
from utils.window_manager import WindowManager
from components.dialogs import DialogManager
from components.phrase_list import PhraseListManager
from ui.ui_handlers import UIHandlers

try:
    from coordinate_tracker import CoordinateTracker
except ImportError:
    CoordinateTracker = None  # Mantém compatibilidade se não estiver disponível


class PhraseManagerApp:
    """Classe principal da aplicação de gerenciamento de frases."""
    
    def __init__(self, page: ft.Page, window_width=700, window_height=620, enable_size_monitoring=False, on_logout=None):
        self.page = page
        self.theme_manager = ThemeManager()
        self.language_manager = LanguageManager()
        
        # Aplica o tema atual
        self._apply_current_theme()
        
        self.page.title = self.language_manager.t("app_title")
        self.page.vertical_alignment = ft.CrossAxisAlignment.START
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
        self.dialog_manager = DialogManager(page, self.language_manager)
        self.ui_handlers = UIHandlers(self)

        # Configura o evento de fechamento da janela para salvar posição/tamanho
        self.page.on_window_event = self._on_window_event
        
        # Configura eventos de teclado para detectar CTRL
        self.page.on_keyboard_event = self._on_keyboard_event

        # Inicialização das opções de ordenação com traduções
        self._init_sort_options()
        self.modo_ordenacao = ft.Ref[ft.Dropdown]()

        # Constrói a interface
        self._build_ui()
        self._load_and_display_phrases_initial()
        
        # Aplica o tamanho da janela com delay para garantir que seja respeitado
        self.page.run_task(self._apply_window_size_delayed, window_width, window_height)
    
    def _apply_current_theme(self):
        """Aplica o tema atual à página."""
        colors = self.theme_manager.get_theme_colors()
        self.page.bgcolor = colors['BACKGROUND_COLOR']
        
        # Atualiza cores dos campos de entrada se já existirem
        if hasattr(self, 'interval_entry'):
            self._update_input_field_colors()
    
    def _init_sort_options(self):
        """Inicializa as opções de ordenação com traduções."""
        self.opcoes_ordenacao = {}
        for sort_key, sort_value in SORT_OPTIONS_KEYS.items():
            translated_text = self.language_manager.t(sort_key)
            self.opcoes_ordenacao[translated_text] = sort_value
    
    def _update_input_field_colors(self):
        """Atualiza as cores dos campos de entrada com o tema atual."""
        colors = self.theme_manager.get_theme_colors()
        
        # Atualiza campos de lembretes
        if hasattr(self, 'interval_entry'):
            self.interval_entry.color = colors['TEXT_COLOR']
            self.interval_entry.label_style = ft.TextStyle(color=colors['TEXT_COLOR'])
            self.interval_entry.border_color = colors['BORDER_COLOR']
            self.interval_entry.update()
        
        if hasattr(self, 'timeout_entry'):
            self.timeout_entry.color = colors['TEXT_COLOR']
            self.timeout_entry.label_style = ft.TextStyle(color=colors['TEXT_COLOR'])
            self.timeout_entry.border_color = colors['BORDER_COLOR']
            self.timeout_entry.update()
        
        # Atualiza campo de entrada de frases
        if hasattr(self, 'phrase_input'):
            self.phrase_input.color = colors['TEXT_COLOR']
            self.phrase_input.label_style = ft.TextStyle(color=colors['TEXT_COLOR'])
            self.phrase_input.border_color = colors['BORDER_COLOR']
            self.phrase_input.fill_color = colors['SURFACE_COLOR']
            self.phrase_input.update()
        
        # Atualiza campo de busca
        if hasattr(self, 'search_input'):
            self.search_input.color = colors['TEXT_COLOR']
            self.search_input.label_style = ft.TextStyle(color=colors['TEXT_COLOR'])
            self.search_input.border_color = colors['BORDER_COLOR']
            self.search_input.fill_color = colors['SURFACE_COLOR']
            self.search_input.update()
        
        # Atualiza dropdown de ordenação
        if hasattr(self, 'sort_dropdown'):
            self.sort_dropdown.color = colors['TEXT_COLOR']
            self.sort_dropdown.label_style = ft.TextStyle(color=colors['TEXT_COLOR'])
            self.sort_dropdown.border_color = colors['BORDER_COLOR']
            self.sort_dropdown.fill_color = colors['SURFACE_COLOR']
            self.sort_dropdown.update()
    
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
            self.select_all_button.text = self.language_manager.t("select_all")
            self.select_all_button.update()
            self._reload_list_view_with_sorted_phrases()
            self.ui_handlers._update_button_states()
    
    def _on_logout(self, e):
        """Trata o logout e retorna à tela de login."""
        try:
            # Para qualquer lembrete ativo
            if self.lembrete_ativo:
                self.page.run_task(self.ui_handlers.stop_reminders_gui)
            
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
    
    def update_language(self):
        """Atualiza o idioma da interface."""
        self.page.title = self.language_manager.t("app_title")
        # Atualiza outros elementos da UI que precisam de tradução
        self._update_ui_labels()
        self.page.update()
    
    def _update_ui_labels(self):
        """Atualiza os labels da interface com as traduções atuais."""
        if hasattr(self, 'label_lembrete'):
            # Atualiza apenas se o lembrete não estiver ativo
            if not self.lembrete_ativo:
                self.label_lembrete.value = self.language_manager.t("click_start_reminders")
        
        # Atualiza botões de lembrete
        if hasattr(self, 'start_button'):
            self.start_button.text = self.language_manager.t("start_reminders")
        if hasattr(self, 'stop_button'):
            self.stop_button.text = self.language_manager.t("stop_reminders")
        
        # Atualiza campo de busca
        if hasattr(self, 'search_input'):
            self.search_input.label = self.language_manager.t("search_phrases")
            self.search_input.hint_text = self.language_manager.t("search_placeholder")
        
        # Atualiza campo de entrada de frases
        if hasattr(self, 'phrase_input'):
            self.phrase_input.label = self.language_manager.t("phrase")
        
        # Atualiza botões de gerenciamento
        if hasattr(self, 'add_button'):
            self.add_button.text = self.language_manager.t("add_phrase")
        if hasattr(self, 'update_button'):
            self.update_button.text = self.language_manager.t("update_phrase")
        if hasattr(self, 'delete_button'):
            self.delete_button.text = self.language_manager.t("delete_phrase")
        if hasattr(self, 'import_button'):
            self.import_button.text = self.language_manager.t("import_phrases")
        if hasattr(self, 'export_button'):
            self.export_button.text = self.language_manager.t("export_phrases")
        if hasattr(self, 'select_all_button'):
            # Verifica o estado atual para definir o texto correto
            if hasattr(self, 'phrase_list_manager') and hasattr(self, 'phrases_data'):
                all_selected = len(self.phrase_list_manager.selected_phrases) == len(self.phrases_data)
                self.select_all_button.text = self.language_manager.t("deselect_all") if all_selected else self.language_manager.t("select_all")
            else:
                self.select_all_button.text = self.language_manager.t("select_all")
        if hasattr(self, 'logout_button'):
            self.logout_button.text = self.language_manager.t("logout")
        
        # Atualiza contador de frases
        if hasattr(self, 'total_phrases_text') and hasattr(self, 'phrases_data'):
            self.total_phrases_text.value = self.language_manager.t("total_phrases").format(len(self.phrases_data))
    
    def _build_ui(self):
        """Constrói a interface do usuário."""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(""), action=self.language_manager.t("ok"))

        # Cores do tema
        colors = self.theme_manager.get_theme_colors()

        # Label de lembretes
        self.label_lembrete = ft.Text(
            value=self.language_manager.t("click_start_reminders"),
            font_family="Arial", size=16, italic=True,
            color=colors['TEXT_COLOR']
        )
        
        self.interval_entry = ft.TextField(
            value="5", label=self.language_manager.t("interval_seconds"), width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.CENTER,
            color=colors['TEXT_COLOR'],
            label_style=ft.TextStyle(color=colors['TEXT_COLOR']),
            border_color=colors['BORDER_COLOR']
        )
        self.timeout_entry = ft.TextField(
            value="0", label=self.language_manager.t("timeout_minutes"), width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.CENTER,
            color=colors['TEXT_COLOR'],
            label_style=ft.TextStyle(color=colors['TEXT_COLOR']),
            border_color=colors['BORDER_COLOR']
        )

        # Botões de controle de lembretes
        self.start_button = ft.ElevatedButton(
            self.language_manager.t("start_reminders"),
            on_click=self._on_start_reminders_click,
            bgcolor=ACCENT_COLOR,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.stop_button = ft.ElevatedButton(
            self.language_manager.t("stop_reminders"),
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

        # Campo de entrada de frases com cores do tema
        self.phrase_input = ft.TextField(
            label=self.language_manager.t("phrase"), expand=True, multiline=True, min_lines=1, max_lines=3,
            on_change=lambda e: self.ui_handlers._update_button_states(),
            color=colors['TEXT_COLOR'],
            label_style=ft.TextStyle(color=colors['TEXT_COLOR']),
            border_color=colors['BORDER_COLOR'],
            fill_color=colors['SURFACE_COLOR']
        )

        # Campo de busca de frases com cores do tema
        self.search_input = ft.TextField(
            label=self.language_manager.t("search_phrases"),
            expand=True,
            on_change=self._on_search_change,
            prefix=ft.Icon(ft.Icons.SEARCH, color=colors['TEXT_COLOR']),
            hint_text=self.language_manager.t("search_placeholder"),
            hint_style=ft.TextStyle(color=colors['TEXT_COLOR']),
            border_radius=8,
            color=colors['TEXT_COLOR'],
            label_style=ft.TextStyle(color=colors['TEXT_COLOR']),
            border_color=colors['BORDER_COLOR'],
            fill_color=colors['SURFACE_COLOR']
        )

        # Botões de gerenciamento de frases
        self._create_phrase_management_buttons()
        
        # Dropdown de ordenação com cores do tema
        options = [ft.dropdown.Option(text=key, key=key) for key in self.opcoes_ordenacao.keys()]
        self.sort_dropdown = ft.Dropdown(
            ref=self.modo_ordenacao,
            options=options,
            value=list(self.opcoes_ordenacao.keys())[0],
            on_change=self._apply_sort,
            label=self.language_manager.t("sort_by"),
            width=280,
            color=colors['TEXT_COLOR'],
            label_style=ft.TextStyle(color=colors['TEXT_COLOR']),
            border_color=colors['BORDER_COLOR'],
            fill_color=colors['SURFACE_COLOR']
        )

        # Lista de frases

        self.list_view = ft.ListView(
            padding=10, auto_scroll=False,
            spacing=5
        )
        self.list_view_container = ft.Container(
            content=self.list_view,
            bgcolor=colors['SURFACE_COLOR'],
            border=ft.border.all(2, colors['BORDER_COLOR']),
            border_radius=8,
            expand=True
        )
        self.phrase_list_manager = PhraseListManager(self.page, self.list_view)

        self.total_phrases_text = ft.Text(
            self.language_manager.t("total_phrases").format(0),
            weight=ft.FontWeight.BOLD,
            color=colors['TEXT_COLOR']
        )

        # Texto de instrução para seleção múltipla
        self.multi_select_info = ft.Text(
            self.language_manager.t("multiple_selection_info"),
            size=12, italic=True, color=colors['TEXT_COLOR']
        )

        # Checkbox para modo de seleção múltipla
        self.multi_select_checkbox = ft.Checkbox(
            label=self.language_manager.t("multiple_selection_mode"),
            value=False,
            on_change=self._on_multi_select_mode_change,
            label_style=ft.TextStyle(color=colors['TEXT_COLOR'])
        )

        # Adiciona todos os elementos à página
        self._add_elements_to_page(reminder_config_row)
    
    def _create_phrase_management_buttons(self):
        """Cria os botões de gerenciamento de frases."""
        colors = self.theme_manager.get_theme_colors()
        
        self.add_button = ft.ElevatedButton(
            self.language_manager.t("add_phrase"),
            on_click=self.ui_handlers.add_phrase_from_input,
            bgcolor=colors['ACCENT_COLOR'],
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.update_button = ft.ElevatedButton(
            self.language_manager.t("update_phrase"),
            on_click=self.ui_handlers.on_update_selected,
            disabled=True,
            bgcolor=colors['DISABLED_COLOR'],
            color=ft.Colors.GREY_600,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.delete_button = ft.ElevatedButton(
            self.language_manager.t("delete_phrase"),
            on_click=self.ui_handlers.on_delete_selected,
            disabled=True,
            bgcolor=colors['DISABLED_COLOR'],
            color=ft.Colors.GREY_600,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.import_button = ft.ElevatedButton(
            self.language_manager.t("import_phrases"),
            on_click=self.import_phrases_gui,
            bgcolor=colors['SECONDARY_ACCENT_COLOR'],
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.export_button = ft.ElevatedButton(
            self.language_manager.t("export_phrases"),
            on_click=self.export_phrases_gui,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.select_all_button = ft.ElevatedButton(
            self.language_manager.t("select_all"),
            on_click=self.ui_handlers.select_all_phrases,
            bgcolor=ft.Colors.INDIGO_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        self.logout_button = ft.ElevatedButton(
            self.language_manager.t("logout"),
            on_click=self._on_logout,
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
    
    def _add_elements_to_page(self, reminder_config_row):
        """Adiciona todos os elementos à página."""
        colors = self.theme_manager.get_theme_colors()
        
        self.page.add(
            ft.Container(height=10),
            self.label_lembrete,
            ft.Container(height=15),
            reminder_config_row,
            ft.Divider(height=30, thickness=2, color=colors['BORDER_COLOR']),
            ft.Text(self.language_manager.t("phrase_management"), size=18, weight=ft.FontWeight.BOLD, color=colors['TEXT_COLOR']),
            ft.Container(height=15),
            ft.Row(
                controls=[
                    ft.Text(self.language_manager.t("sort_by"), color=colors['TEXT_COLOR']),
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
                            self.list_view_container,
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
        self.select_all_button.text = self.language_manager.t("select_all")
        self.select_all_button.update()
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
        self.total_phrases_text.value = self.language_manager.t("total_phrases").format(len(self.phrases_data))
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
