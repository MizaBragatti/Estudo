# api/internal_client.py
"""
Cliente API interno para uso pela aplicação principal
Otimizado para comunicação local entre a UI e as APIs
"""

import requests
import json
import threading
import time
from datetime import datetime

class InternalAPIClient:
    """Cliente API otimizado para uso interno da aplicação."""
    
    def __init__(self, base_url="http://localhost:5000/api/v1"):
        self.base_url = base_url
        self.user_id = None
        self.session = requests.Session()
        self.session.timeout = 5  # Timeout curto para uso local
        
    def _make_request(self, method, endpoint, data=None, params=None):
        """Faz uma requisição HTTP à API com tratamento de erro otimizado."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, json=data)
            else:
                return {"success": False, "message": f"Método HTTP não suportado: {method}"}
            
            return response.json()
            
        except requests.exceptions.ConnectionError:
            return {"success": False, "message": "API não está disponível. Verifique se o servidor está rodando."}
        except requests.exceptions.Timeout:
            return {"success": False, "message": "Timeout na comunicação com a API"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Erro de rede: {str(e)}"}
        except json.JSONDecodeError:
            return {"success": False, "message": "Resposta inválida da API"}
    
    # ================ MÉTODOS DE AUTENTICAÇÃO ================
    
    def login(self, username, password):
        """Realiza login e armazena user_id."""
        data = {"username": username, "password": password}
        response = self._make_request('POST', '/auth/login', data)
        
        if response.get('success') and response.get('data'):
            self.user_id = response['data'].get('user_id')
            return True, response.get('message', 'Login realizado com sucesso')
        
        return False, response.get('message', 'Erro no login')
    
    def register_user(self, username, password):
        """Registra um novo usuário."""
        data = {"username": username, "password": password}
        response = self._make_request('POST', '/users', data)
        
        if response.get('success'):
            return True, response.get('message', 'Usuário registrado com sucesso')
        else:
            return False, response.get('message', 'Erro no registro')
    
    # ================ MÉTODOS DE FRASES ================
    
    def get_phrases(self, sort_order='original', search_term=''):
        """Busca frases do usuário atual."""
        if not self.user_id:
            return []
        
        params = {'sort': sort_order, 'user_id': self.user_id}
        if search_term:
            params['search'] = search_term
        
        response = self._make_request('GET', '/phrases', params=params)
        
        if response.get('success') and response.get('data'):
            phrases_data = response['data'].get('phrases', [])
            # Converte para lista de strings para compatibilidade com código existente
            return [phrase['text'] for phrase in phrases_data]
        
        return []
    
    def get_phrases_complete(self, sort_order='original', search_term=''):
        """Busca frases completas com todos os dados."""
        if not self.user_id:
            return []
        
        params = {'sort': sort_order, 'user_id': self.user_id}
        if search_term:
            params['search'] = search_term
        
        response = self._make_request('GET', '/phrases', params=params)
        
        if response.get('success') and response.get('data'):
            return response['data'].get('phrases', [])
        
        return []
    
    def add_phrase(self, text):
        """Adiciona uma nova frase."""
        if not self.user_id:
            return "NOT_LOGGED_IN"
        
        data = {"text": text, "user_id": self.user_id}
        response = self._make_request('POST', '/phrases', data)
        
        if response.get('success'):
            return "PHRASE_ADDED_SUCCESS"
        else:
            message = response.get('message', 'Erro ao adicionar frase')
            # Garante que message seja uma string antes de chamar .lower()
            if isinstance(message, str) and 'já existe' in message.lower():
                return "PHRASE_ALREADY_EXISTS"
            return str(message) if message is not None else "ADD_PHRASE_ERROR"
    
    def import_phrases_bulk(self, phrases_list):
        """Importa múltiplas frases de uma vez via API."""
        if not self.user_id:
            return 0, 0, 0
        
        data = {"phrases": phrases_list, "user_id": self.user_id}
        response = self._make_request('POST', '/phrases/import', data)
        
        if response.get('success'):
            data = response.get('data', {})
            return (
                data.get('total_processed', 0),
                data.get('total_added', 0), 
                data.get('total_duplicates', 0)
            )
        else:
            return 0, 0, 0
    
    def update_phrase(self, old_text, new_text):
        """Atualiza uma frase existente."""
        if not self.user_id:
            return "Usuário não logado"
        
        # Para compatibilidade, usamos ID 1 (o ID não é usado na lógica atual da API)
        data = {"old_text": old_text, "new_text": new_text, "user_id": self.user_id}
        response = self._make_request('PUT', '/phrases/1', data)
        
        if response.get('success'):
            return "Frase atualizada com sucesso!"
        else:
            return response.get('message', 'Erro ao atualizar frase')
    
    def delete_phrases(self, phrases_list):
        """Remove uma ou múltiplas frases."""
        if not self.user_id:
            return False
        
        if isinstance(phrases_list, str):
            phrases_list = [phrases_list]
        
        data = {"phrases": phrases_list, "user_id": self.user_id}
        response = self._make_request('DELETE', '/phrases', data)
        
        return response.get('success', False)
    
    def search_phrases(self, search_term, sort_order='original'):
        """Busca frases que contenham o termo especificado."""
        return self.get_phrases(sort_order, search_term)
    
    # ================ MÉTODOS DE ESTATÍSTICAS ================
    
    def get_stats(self):
        """Obtém estatísticas do banco."""
        if not self.user_id:
            return {}
        
        params = {'user_id': self.user_id}
        response = self._make_request('GET', '/stats', params=params)
        
        if response.get('success') and response.get('data'):
            return response['data']
        
        return {}
    
    def get_phrase_count(self):
        """Retorna o número total de frases (compatibilidade)."""
        stats = self.get_stats()
        return stats.get('total_phrases', 0)
    
    def get_statistics(self):
        """Método adicional para compatibilidade com testes."""
        stats = self.get_stats()
        return {
            'total_frases': stats.get('total_phrases', 0),
            'usuarios_cadastrados': stats.get('total_users', 0)
        }
    
    # ================ MÉTODOS DE COMPATIBILIDADE ================
    
    def import_phrases_from_file(self, file_path):
        """Importa frases de um arquivo usando importação em lote via API."""
        if not self.user_id:
            return 0, 0, 0
        
        try:
            # Lê todas as frases do arquivo de uma vez
            phrases_to_import = []
            total_read = 0
            
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    total_read += 1
                    phrase = line.strip()
                    if phrase:  # Só adiciona linhas não vazias
                        phrases_to_import.append(phrase)
            
            if not phrases_to_import:
                return total_read, 0, 0
            
            # Usa a importação em lote via API
            total_processed, total_added, total_duplicates = self.import_phrases_bulk(phrases_to_import)
            
            return total_read, total_added, total_duplicates
            
        except FileNotFoundError:
            return 0, 0, 0
        except Exception:
            return 0, 0, 0
    
    def export_phrases_to_file(self, file_path, sort_order='original'):
        """Exporta frases para um arquivo."""
        phrases = self.get_phrases(sort_order)
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for phrase in phrases:
                    f.write(phrase + "\n")
            
            return len(phrases)
        except Exception:
            return 0
    
    # ================ MÉTODOS DE CONTROLE ================
    
    def is_connected(self):
        """Verifica se a API está acessível."""
        response = self._make_request('GET', '/health')
        return response.get('success', False)
    
    def get_current_user_id(self):
        """Retorna o ID do usuário atual (compatibilidade)."""
        return self.user_id
    
    def set_current_user(self, user_id):
        """Define o usuário atual (compatibilidade)."""
        self.user_id = user_id


# ================ SINGLETON PARA USO GLOBAL ================

# Instância global para uso na aplicação
_api_client_instance = None

def get_api_client():
    """Retorna a instância global do cliente API."""
    global _api_client_instance
    if _api_client_instance is None:
        _api_client_instance = InternalAPIClient()
    return _api_client_instance

def initialize_api_client(base_url="http://localhost:5000/api/v1"):
    """Inicializa o cliente API com URL personalizada."""
    global _api_client_instance
    _api_client_instance = InternalAPIClient(base_url)
    return _api_client_instance


# ================ FUNÇÕES DE COMPATIBILIDADE ================
# Essas funções mantêm a mesma interface do frase_manager.py original

def set_current_user(user_id):
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    client.set_current_user(user_id)

def get_current_user():
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    return client.get_current_user_id()

def adicionar_frase(frase):
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    result = client.add_phrase(frase)
    return result == "PHRASE_ADDED_SUCCESS"

def ler_frases(ordenacao="original"):
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    return client.get_phrases(sort_order=ordenacao)

def buscar_frases(termo_busca, ordenacao="original"):
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    return client.search_phrases(termo_busca, sort_order=ordenacao)

def remover_frase(frase_para_remover):
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    return client.delete_phrases([frase_para_remover])

def remover_multiplas_frases(frases_para_remover):
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    success = client.delete_phrases(frases_para_remover)
    return len(frases_para_remover) if success else 0

def atualizar_frase(old_texto, new_texto):
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    result = client.update_phrase(old_texto, new_texto)
    # Retorna a mensagem em vez de booleano para melhor compatibilidade
    return result

def importar_frases_de_arquivo(caminho_arquivo):
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    return client.import_phrases_from_file(caminho_arquivo)

def exportar_frases_para_arquivo(caminho_arquivo, ordenacao="original"):
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    return client.export_phrases_to_file(caminho_arquivo, sort_order=ordenacao)

def authenticate_user(username, password):
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    success, message = client.login(username, password)
    return client.get_current_user_id() if success else None

def register_user(username, password):
    """Compatibilidade com frase_manager.py"""
    client = get_api_client()
    success, message = client.register_user(username, password)
    return message

# Funções que ainda precisam do banco direto (para criação de tabelas)
def create_table():
    """Mantém acesso direto para criação inicial"""
    import frase_manager as fm
    return fm.create_table()

def create_users_table():
    """Mantém acesso direto para criação inicial"""
    import frase_manager as fm
    return fm.create_users_table()
