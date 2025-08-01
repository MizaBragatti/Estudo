# tests/test_ui_regression.py
"""
Testes regressivos específicos para a interface do usuário.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import tempfile

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock do Flet para testes sem interface gráfica
class MockFletPage:
    def __init__(self):
        self.title = ""
        self.vertical_alignment = None
        self.bgcolor = None
        self.window = Mock()
        self.window.width = 700
        self.window.height = 620
        self.snack_bar = Mock()
        self.snack_bar.content = Mock()
        self.snack_bar.open = False
        
    def add(self, *args):
        pass
    
    def update(self):
        pass

class MockFletControls:
    """Mocks para controles do Flet."""
    
    class TextField:
        def __init__(self, **kwargs):
            self.value = kwargs.get('value', '')
            self.label = kwargs.get('label', '')
            self.multiline = kwargs.get('multiline', False)
            self.min_lines = kwargs.get('min_lines', 1)
            self.max_lines = kwargs.get('max_lines', 1)
            self.expand = kwargs.get('expand', False)
            self.on_change = kwargs.get('on_change')
        
        def update(self):
            pass
    
    class ElevatedButton:
        def __init__(self, text="", **kwargs):
            self.text = text
            self.disabled = kwargs.get('disabled', False)
            self.bgcolor = kwargs.get('bgcolor')
            self.color = kwargs.get('color')
            self.on_click = kwargs.get('on_click')
            self.opacity = 1.0
        
        def update(self):
            pass
    
    class ListView:
        def __init__(self, **kwargs):
            self.controls = []
            self.expand = kwargs.get('expand', False)
        
        def update(self):
            pass
    
    class Text:
        def __init__(self, value="", **kwargs):
            self.value = value
            self.color = kwargs.get('color')
            self.size = kwargs.get('size')
        
        def update(self):
            pass
    
    class Dropdown:
        def __init__(self, **kwargs):
            self.value = kwargs.get('value')
            self.options = kwargs.get('options', [])
            self.on_change = kwargs.get('on_change')
        
        def update(self):
            pass
    
    class Column:
        def __init__(self, controls=None, **kwargs):
            self.controls = controls or []
        
        def update(self):
            pass
    
    class Row:
        def __init__(self, controls=None, **kwargs):
            self.controls = controls or []
        
        def update(self):
            pass


class TesteUIComponentes(unittest.TestCase):
    """Testes dos componentes da interface."""
    
    def setUp(self):
        """Configuração para cada teste."""
        # Mock do Flet
        self.flet_patch = patch.dict('sys.modules', {
            'flet': Mock(),
        })
        self.flet_patch.start()
        
        # Importa módulos após mock
        import flet as ft
        ft.Page = MockFletPage
        ft.TextField = MockFletControls.TextField
        ft.ElevatedButton = MockFletControls.ElevatedButton
        ft.ListView = MockFletControls.ListView
        ft.Text = MockFletControls.Text
        ft.Dropdown = MockFletControls.Dropdown
        ft.Column = MockFletControls.Column
        ft.Row = MockFletControls.Row
        ft.Colors = Mock()
        ft.CrossAxisAlignment = Mock()
        
        # Cria página mock
        self.mock_page = MockFletPage()
    
    def tearDown(self):
        """Limpeza após cada teste."""
        self.flet_patch.stop()
    
    @patch('api.internal_client.get_api_client')
    def test_01_criacao_app_principal(self, mock_client):
        """Testa se o app principal pode ser criado."""
        mock_client.return_value = Mock()
        
        from ui.phrase_manager_app import PhraseManagerApp
        
        # Deve conseguir criar sem erro
        app = PhraseManagerApp(self.mock_page)
        
        # Verifica componentes principais
        self.assertIsNotNone(app.phrase_input)
        self.assertIsNotNone(app.search_input)
        self.assertIsNotNone(app.add_button)
        self.assertIsNotNone(app.update_button)
        self.assertIsNotNone(app.delete_button)
    
    @patch('api.internal_client.get_api_client')
    def test_02_handlers_existem(self, mock_client):
        """Testa se os handlers de UI existem."""
        mock_client.return_value = Mock()
        
        from ui.phrase_manager_app import PhraseManagerApp
        app = PhraseManagerApp(self.mock_page)
        
        # Verifica se handlers existem
        self.assertIsNotNone(app.ui_handlers)
        self.assertTrue(hasattr(app.ui_handlers, 'add_phrase_from_input'))
        self.assertTrue(hasattr(app.ui_handlers, 'on_update_selected'))
        self.assertTrue(hasattr(app.ui_handlers, 'on_delete_selected'))
    
    @patch('api.internal_client.get_api_client')
    def test_03_componentes_frase(self, mock_client):
        """Testa componentes específicos de frases."""
        mock_client.return_value = Mock()
        
        from components.phrase_list import PhraseListManager
        
        # Deve conseguir criar sem erro
        phrase_manager = PhraseListManager(Mock())
        
        # Verifica métodos principais
        self.assertTrue(hasattr(phrase_manager, 'reload_list_view_with_sorted_phrases'))
        self.assertTrue(hasattr(phrase_manager, 'clear_selection'))
        self.assertTrue(hasattr(phrase_manager, 'has_selection'))
    
    @patch('api.internal_client.get_api_client')
    def test_04_dialogs_existem(self, mock_client):
        """Testa se os diálogos existem."""
        mock_client.return_value = Mock()
        
        from components.dialogs import DialogManager
        
        # Deve conseguir criar sem erro
        dialog_manager = DialogManager(self.mock_page)
        
        # Verifica métodos principais
        self.assertTrue(hasattr(dialog_manager, 'show_confirmation_dialog'))
        self.assertTrue(hasattr(dialog_manager, 'show_duplicate_phrase_modal'))
    
    def test_05_login_screen_funciona(self):
        """Testa se a tela de login funciona."""
        from ui.login_screen import LoginScreen
        
        # Deve conseguir criar sem erro
        login_screen = LoginScreen(self.mock_page, Mock())
        
        # Verifica componentes
        self.assertIsNotNone(login_screen.username_field)
        self.assertIsNotNone(login_screen.password_field)
        self.assertIsNotNone(login_screen.login_button)


class TesteUILogica(unittest.TestCase):
    """Testes da lógica da interface."""
    
    def setUp(self):
        """Configuração para cada teste."""
        # Mock do Flet
        self.flet_patch = patch.dict('sys.modules', {
            'flet': Mock(),
        })
        self.flet_patch.start()
        
        # Setup mocks
        import flet as ft
        ft.Page = MockFletPage
        ft.TextField = MockFletControls.TextField
        ft.ElevatedButton = MockFletControls.ElevatedButton
        ft.Colors = Mock()
        
        self.mock_page = MockFletPage()
    
    def tearDown(self):
        """Limpeza após cada teste."""
        self.flet_patch.stop()
    
    @patch('api.internal_client.get_api_client')
    def test_01_estados_botoes(self, mock_client):
        """Testa se os estados dos botões funcionam corretamente."""
        mock_client.return_value = Mock()
        
        from ui.phrase_manager_app import PhraseManagerApp
        app = PhraseManagerApp(self.mock_page)
        
        # Testa estado inicial (sem texto, sem seleção)
        app.ui_handlers._update_button_states()
        
        self.assertTrue(app.add_button.disabled, "Botão adicionar deveria estar desabilitado")
        self.assertTrue(app.update_button.disabled, "Botão atualizar deveria estar desabilitado")
        self.assertTrue(app.delete_button.disabled, "Botão excluir deveria estar desabilitado")
        
        # Testa com texto no input
        app.phrase_input.value = "Texto de teste"
        app.ui_handlers._update_button_states()
        
        self.assertFalse(app.add_button.disabled, "Botão adicionar deveria estar habilitado")
        self.assertTrue(app.update_button.disabled, "Botão atualizar ainda deveria estar desabilitado")
        
        # Testa com seleção para edição
        app.frase_selecionada_para_edicao = "Frase selecionada"
        app.ui_handlers._update_button_states()
        
        self.assertFalse(app.add_button.disabled, "Botão adicionar deveria estar habilitado")
        self.assertFalse(app.update_button.disabled, "Botão atualizar deveria estar habilitado")
        self.assertTrue(app.delete_button.disabled, "Botão excluir deveria estar desabilitado sem seleção múltipla")
    
    @patch('api.internal_client.get_api_client')
    def test_02_validacao_entrada(self, mock_client):
        """Testa validação de entrada de dados."""
        mock_api = Mock()
        mock_client.return_value = mock_api
        
        from ui.phrase_manager_app import PhraseManagerApp
        app = PhraseManagerApp(self.mock_page)
        
        # Testa entrada vazia
        app.phrase_input.value = ""
        mock_event = Mock()
        
        # Simula click no botão adicionar
        app.ui_handlers.add_phrase_from_input(mock_event)
        
        # Deve mostrar erro de campo vazio
        # (verificamos se a API não foi chamada)
        mock_api.add_phrase.assert_not_called()
    
    @patch('api.internal_client.get_api_client')
    def test_03_ordenacao_funciona(self, mock_client):
        """Testa se a ordenação funciona."""
        mock_api = Mock()
        mock_api.get_phrases.return_value = ["Zebra", "Abelha", "Gato"]
        mock_client.return_value = mock_api
        
        from ui.phrase_manager_app import PhraseManagerApp
        app = PhraseManagerApp(self.mock_page)
        
        # Simula mudança de ordenação
        app._apply_sort()
        
        # Verifica se get_phrases foi chamado
        mock_api.get_phrases.assert_called()


def run_ui_regression_tests():
    """Executa testes regressivos da UI."""
    print("🖥️ TESTES REGRESSIVOS DA INTERFACE")
    print("=" * 40)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona testes
    suite.addTests(loader.loadTestsFromTestCase(TesteUIComponentes))
    suite.addTests(loader.loadTestsFromTestCase(TesteUILogica))
    
    # Executa
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_ui_regression_tests()
    sys.exit(0 if success else 1)
