# tests/test_config.py
"""
Configurações para testes regressivos.
"""

import os
import tempfile

# Configurações de teste
TEST_CONFIG = {
    # Banco de dados de teste
    'TEST_DB_PATH': os.path.join(tempfile.gettempdir(), 'test_frases.db'),
    
    # API de teste
    'TEST_API_PORT': 5001,
    'TEST_API_URL': 'http://localhost:5001/api/v1',
    
    # Timeout para testes
    'API_TIMEOUT': 30,  # segundos
    'DB_TIMEOUT': 10,   # segundos
    
    # Dados de teste
    'TEST_USERS': [
        {'username': 'test_user_1', 'password': 'senha123456'},
        {'username': 'test_user_2', 'password': 'senha123456'},
        {'username': 'admin_test', 'password': 'admin123456'},
    ],
    
    'TEST_PHRASES': [
        "Esta é uma frase de teste",
        "Segunda frase para testes",
        "Terceira frase de exemplo",
        "Frase com palavra especial: gato",
        "Outra frase com: cachorro",
        "Frase final de teste"
    ],
    
    # Configurações de interface
    'UI_TEST_CONFIG': {
        'window_width': 700,
        'window_height': 620,
        'timeout_ui': 5,  # segundos
    },
    
    # Logs de teste
    'LOG_LEVEL': 'INFO',
    'LOG_FILE': os.path.join(tempfile.gettempdir(), 'test_regression.log'),
    
    # Relatórios
    'REPORT_DIR': 'test_reports',
    'COVERAGE_REPORT': True,
}

# Funções utilitárias
def get_test_db_path():
    """Retorna caminho para banco de teste."""
    return TEST_CONFIG['TEST_DB_PATH']

def get_test_api_config():
    """Retorna configuração da API de teste."""
    return {
        'port': TEST_CONFIG['TEST_API_PORT'],
        'url': TEST_CONFIG['TEST_API_URL']
    }

def cleanup_test_files():
    """Limpa arquivos de teste."""
    test_files = [
        TEST_CONFIG['TEST_DB_PATH'],
        TEST_CONFIG['LOG_FILE'],
    ]
    
    for file_path in test_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError:
            pass

def setup_test_environment():
    """Configura ambiente de teste."""
    # Cria diretório de relatórios
    report_dir = TEST_CONFIG['REPORT_DIR']
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    # Limpa arquivos de teste antigos
    cleanup_test_files()
    
    return True
