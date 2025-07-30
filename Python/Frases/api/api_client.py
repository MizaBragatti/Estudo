# api/api_client.py
"""
Cliente de exemplo para testar as APIs do Gerenciador de Frases
"""

import requests
import json
from datetime import datetime

class PhraseAPIClient:
    """Cliente para interagir com a API de Frases."""
    
    def __init__(self, base_url="http://localhost:5000/api/v1"):
        self.base_url = base_url
        self.user_id = None
        self.session = requests.Session()
    
    def _make_request(self, method, endpoint, data=None, params=None):
        """Faz uma requisição HTTP à API."""
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
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Erro de conexão: {str(e)}"}
        except json.JSONDecodeError:
            return {"success": False, "message": "Resposta inválida da API"}
    
    # ================ MÉTODOS DE AUTENTICAÇÃO ================
    
    def register_user(self, username, password):
        """Registra um novo usuário."""
        data = {"username": username, "password": password}
        return self._make_request('POST', '/users', data)
    
    def login(self, username, password):
        """Realiza login do usuário."""
        data = {"username": username, "password": password}
        response = self._make_request('POST', '/auth/login', data)
        
        if response.get('success') and response.get('data'):
            self.user_id = response['data'].get('user_id')
        
        return response
    
    # ================ MÉTODOS DE FRASES ================
    
    def get_phrases(self, sort_order='original', search_term=''):
        """Busca frases."""
        params = {'sort': sort_order}
        if search_term:
            params['search'] = search_term
        if self.user_id:
            params['user_id'] = self.user_id
        
        return self._make_request('GET', '/phrases', params=params)
    
    def add_phrase(self, text):
        """Adiciona uma nova frase."""
        data = {"text": text}
        if self.user_id:
            data['user_id'] = self.user_id
        
        return self._make_request('POST', '/phrases', data)
    
    def update_phrase(self, phrase_id, old_text, new_text):
        """Atualiza uma frase existente."""
        data = {"old_text": old_text, "new_text": new_text}
        if self.user_id:
            data['user_id'] = self.user_id
        
        return self._make_request('PUT', f'/phrases/{phrase_id}', data)
    
    def delete_phrases(self, phrases_list):
        """Remove uma ou múltiplas frases."""
        data = {"phrases": phrases_list}
        if self.user_id:
            data['user_id'] = self.user_id
        
        return self._make_request('DELETE', '/phrases', data)
    
    # ================ MÉTODOS DE ESTATÍSTICAS ================
    
    def get_stats(self):
        """Obtém estatísticas do banco."""
        params = {}
        if self.user_id:
            params['user_id'] = self.user_id
        
        return self._make_request('GET', '/stats', params=params)
    
    def health_check(self):
        """Verifica saúde da API."""
        return self._make_request('GET', '/health')
    
    def get_api_info(self):
        """Obtém informações da API."""
        return self._make_request('GET', '/info')
    
    # ================ MÉTODOS UTILITÁRIOS ================
    
    def print_response(self, response):
        """Imprime resposta formatada."""
        if response.get('success'):
            print(f"✅ {response.get('message', 'Sucesso')}")
            if response.get('data'):
                print(f"📊 Dados: {json.dumps(response['data'], indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ {response.get('message', 'Erro')}")
    
    def test_all_endpoints(self):
        """Testa todos os endpoints da API."""
        print("🧪 TESTANDO TODOS OS ENDPOINTS DA API")
        print("=" * 50)
        
        # Teste de saúde
        print("\n1. Verificando saúde da API...")
        health = self.health_check()
        self.print_response(health)
        
        # Informações da API
        print("\n2. Obtendo informações da API...")
        info = self.get_api_info()
        self.print_response(info)
        
        # Registro de usuário
        print("\n3. Registrando usuário de teste...")
        register = self.register_user("teste_api", "senha123")
        self.print_response(register)
        
        # Login
        print("\n4. Fazendo login...")
        login = self.login("teste_api", "senha123")
        self.print_response(login)
        
        if not login.get('success'):
            print("⚠️ Tentando com usuário existente...")
            login = self.login("admin", "admin")
            self.print_response(login)
        
        # Adicionar frases
        print("\n5. Adicionando frases de teste...")
        test_phrases = [
            "Esta é uma frase de teste da API",
            "Segundo exemplo para testar as APIs",
            "Terceira frase para demonstração"
        ]
        
        for phrase in test_phrases:
            result = self.add_phrase(phrase)
            print(f"   • {phrase[:30]}{'...' if len(phrase) > 30 else ''}")
            if not result.get('success'):
                print(f"     ❌ {result.get('message')}")
        
        # Listar frases
        print("\n6. Listando frases...")
        phrases = self.get_phrases()
        self.print_response(phrases)
        
        # Buscar frases
        print("\n7. Buscando frases com termo 'teste'...")
        search = self.get_phrases(search_term='teste')
        self.print_response(search)
        
        # Estatísticas
        print("\n8. Obtendo estatísticas...")
        stats = self.get_stats()
        self.print_response(stats)
        
        # Atualizar frase
        if phrases.get('success') and phrases.get('data', {}).get('phrases'):
            first_phrase = phrases['data']['phrases'][0]
            print(f"\n9. Atualizando frase: {first_phrase['text'][:30]}...")
            update = self.update_phrase(
                first_phrase['id'],
                first_phrase['text'],
                first_phrase['text'] + " (ATUALIZADA VIA API)"
            )
            self.print_response(update)
        
        print("\n" + "=" * 50)
        print("🎉 TESTE COMPLETO DOS ENDPOINTS!")

def main():
    """Função principal para demonstrar o uso do cliente."""
    client = PhraseAPIClient()
    
    print("🔗 CLIENTE DE TESTE DA API DE FRASES")
    print("=" * 50)
    
    # Teste completo
    client.test_all_endpoints()
    
    print("\n" + "=" * 50)
    print("📚 EXEMPLOS DE USO:")
    print("=" * 50)
    
    # Exemplos específicos
    print("\n# Exemplo 1: Verificar saúde")
    print("client = PhraseAPIClient()")
    print("health = client.health_check()")
    print("client.print_response(health)")
    
    print("\n# Exemplo 2: Login e buscar frases")
    print("client.login('usuario', 'senha')")
    print("phrases = client.get_phrases(sort_order='alfabetica')")
    print("client.print_response(phrases)")
    
    print("\n# Exemplo 3: Adicionar e buscar")
    print("client.add_phrase('Nova frase via API')")
    print("search = client.get_phrases(search_term='API')")
    print("client.print_response(search)")

if __name__ == "__main__":
    main()
