# api/phrase_api.py
"""
Sistema de APIs REST para o Gerenciador de Frases
Fornece endpoints HTTP para acessar e manipular frases no banco de dados
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sys
import os
from datetime import datetime
import threading

# Adiciona o diretório pai ao path para importar frase_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import frase_manager

app = Flask(__name__)
CORS(app)  # Permite requisições cross-origin

# Configuração global
API_VERSION = "1.0"
API_PREFIX = "/api/v1"

# ================ UTILITÁRIOS ================

def format_response(success=True, data=None, message="", status_code=200):
    """Formata resposta padrão da API."""
    response = {
        "success": success,
        "timestamp": datetime.now().isoformat(),
        "version": API_VERSION,
        "data": data,
        "message": message
    }
    return jsonify(response), status_code

def handle_error(error, status_code=500):
    """Trata erros e retorna resposta formatada."""
    return format_response(
        success=False,
        message=f"Erro: {str(error)}",
        status_code=status_code
    )

# ================ ENDPOINTS DE FRASES ================

@app.route(f"{API_PREFIX}/phrases", methods=['GET'])
def get_phrases():
    """
    GET /api/v1/phrases
    Retorna todas as frases do usuário atual
    
    Query Parameters:
    - sort: ordenação (original, alfabetica, tamanho, recente)
    - search: termo de busca
    - user_id: ID do usuário (opcional)
    """
    try:
        # Parâmetros da query
        sort_order = request.args.get('sort', 'original')
        search_term = request.args.get('search', '')
        user_id = request.args.get('user_id')
        
        # Define usuário se fornecido
        if user_id:
            frase_manager.set_current_user(int(user_id))
        
        # Busca frases
        if search_term:
            phrases = frase_manager.buscar_frases_completas(search_term, sort_order)
        else:
            phrases = frase_manager.ler_frases_completas(sort_order)
        
        # Formata dados para JSON
        phrases_data = []
        for phrase in phrases:
            phrases_data.append({
                "id": phrase['id'],
                "text": phrase['texto'],  # Já vem descriptografado
                "user_id": phrase['user_id'],
                "creation_date": phrase['data_criacao'],
                "is_encrypted": phrase['is_encrypted']
            })
        
        return format_response(
            data={
                "phrases": phrases_data,
                "count": len(phrases_data),
                "sort_order": sort_order,
                "search_term": search_term
            },
            message=f"Encontradas {len(phrases_data)} frases"
        )
        
    except Exception as e:
        return handle_error(e)

@app.route(f"{API_PREFIX}/phrases", methods=['POST'])
def add_phrase():
    """
    POST /api/v1/phrases
    Adiciona uma nova frase
    
    Body JSON:
    {
        "text": "Texto da frase",
        "user_id": 1 (opcional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return format_response(
                success=False,
                message="Campo 'text' é obrigatório",
                status_code=400
            )
        
        phrase_text = data['text'].strip()
        user_id = data.get('user_id')
        
        if not phrase_text:
            return format_response(
                success=False,
                message="Texto da frase não pode estar vazio",
                status_code=400
            )
        
        # Define usuário se fornecido
        if user_id:
            frase_manager.set_current_user(int(user_id))
        
        # Adiciona a frase
        result = frase_manager.adicionar_frase(phrase_text)
        
        if result is True:
            return format_response(
                data={"text": phrase_text},
                message="Frase adicionada com sucesso",
                status_code=201
            )
        elif result is False:
            return format_response(
                success=False,
                message="Frase já existe no banco de dados",
                status_code=409
            )
        elif result == "Frase já existe!":
            return format_response(
                success=False,
                message="Frase já existe no banco de dados",
                status_code=409
            )
        elif result == "Frase adicionada com sucesso!":
            return format_response(
                data={"text": phrase_text},
                message="Frase adicionada com sucesso",
                status_code=201
            )
        else:
            return format_response(
                success=False,
                message=str(result) if result is not None else "Erro ao adicionar frase",
                status_code=400
            )
        
    except Exception as e:
        return handle_error(e)

@app.route(f"{API_PREFIX}/phrases/import", methods=['POST'])
def import_phrases():
    """
    Importa múltiplas frases de uma vez.
    
    Body JSON:
    {
        "phrases": ["frase1", "frase2", "frase3"],
        "user_id": 1 (opcional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'phrases' not in data:
            return format_response(
                success=False,
                message="Campo 'phrases' é obrigatório",
                status_code=400
            )
        
        phrases_list = data['phrases']
        user_id = data.get('user_id')
        
        if not isinstance(phrases_list, list):
            return format_response(
                success=False,
                message="Campo 'phrases' deve ser uma lista",
                status_code=400
            )
        
        if not phrases_list:
            return format_response(
                success=False,
                message="Lista de frases não pode estar vazia",
                status_code=400
            )
        
        # Define usuário se fornecido
        if user_id:
            frase_manager.set_current_user(int(user_id))
        
        total_processed = 0
        total_added = 0
        total_duplicates = 0
        errors = []
        
        # Processa cada frase
        for i, phrase in enumerate(phrases_list):
            phrase_text = str(phrase).strip()
            if phrase_text:
                total_processed += 1
                try:
                    result = frase_manager.adicionar_frase(phrase_text)
                    
                    if result is True:
                        total_added += 1
                    elif result is False:
                        total_duplicates += 1
                    else:
                        errors.append(f"Erro ao adicionar '{phrase_text}': {result}")
                        
                except ValueError as ve:
                    errors.append(f"Erro de usuário '{phrase_text}': {str(ve)}")
                except Exception as e:
                    errors.append(f"Erro ao processar '{phrase_text}': {str(e)}")
        
        return format_response(
            data={
                "total_processed": total_processed,
                "total_added": total_added,
                "total_duplicates": total_duplicates,
                "errors": errors,
                "success_rate": f"{(total_added / total_processed * 100):.1f}%" if total_processed > 0 else "0%"
            },
            message=f"Importação concluída: {total_added} adicionadas, {total_duplicates} duplicadas"
        )
        
    except Exception as e:
        return handle_error(e)

@app.route(f"{API_PREFIX}/phrases/<int:phrase_id>", methods=['PUT'])
def update_phrase(phrase_id):
    """
    PUT /api/v1/phrases/<id>
    Atualiza uma frase existente
    
    Body JSON:
    {
        "old_text": "Texto antigo",
        "new_text": "Texto novo",
        "user_id": 1 (opcional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'old_text' not in data or 'new_text' not in data:
            return format_response(
                success=False,
                message="Campos 'old_text' e 'new_text' são obrigatórios",
                status_code=400
            )
        
        old_text = data['old_text']
        new_text = data['new_text'].strip()
        user_id = data.get('user_id')
        
        if not new_text:
            return format_response(
                success=False,
                message="Novo texto não pode estar vazio",
                status_code=400
            )
        
        # Define usuário se fornecido
        if user_id:
            frase_manager.set_current_user(int(user_id))
        
        # Atualiza a frase
        result = frase_manager.atualizar_frase(old_text, new_text)
        
        if result is True:
            return format_response(
                data={
                    "id": phrase_id,
                    "old_text": old_text,
                    "new_text": new_text
                },
                message="Frase atualizada com sucesso"
            )
        elif result is False:
            return format_response(
                success=False,
                message="Erro ao atualizar frase. Possível duplicata ou frase não encontrada.",
                status_code=400
            )
        elif result == "Frase atualizada com sucesso!":
            return format_response(
                data={
                    "id": phrase_id,
                    "old_text": old_text,
                    "new_text": new_text
                },
                message="Frase atualizada com sucesso"
            )
        else:
            return format_response(
                success=False,
                message=str(result) if result is not None else "Erro desconhecido ao atualizar frase",
                status_code=400
            )
        
    except Exception as e:
        return handle_error(e)

@app.route(f"{API_PREFIX}/phrases", methods=['DELETE'])
def delete_phrases():
    """
    DELETE /api/v1/phrases
    Remove uma ou múltiplas frases
    
    Body JSON:
    {
        "phrases": ["Texto da frase 1", "Texto da frase 2"],
        "user_id": 1 (opcional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'phrases' not in data:
            return format_response(
                success=False,
                message="Campo 'phrases' é obrigatório",
                status_code=400
            )
        
        phrases_to_delete = data['phrases']
        user_id = data.get('user_id')
        
        if not isinstance(phrases_to_delete, list) or len(phrases_to_delete) == 0:
            return format_response(
                success=False,
                message="Campo 'phrases' deve ser uma lista não vazia",
                status_code=400
            )
        
        # Define usuário se fornecido
        if user_id:
            frase_manager.set_current_user(int(user_id))
        
        # Remove frases
        if len(phrases_to_delete) == 1:
            result = frase_manager.remover_frase(phrases_to_delete[0])
        else:
            result = frase_manager.remover_multiplas_frases(phrases_to_delete)
        
        return format_response(
            data={
                "deleted_phrases": phrases_to_delete,
                "count": len(phrases_to_delete)
            },
            message=f"Removidas {len(phrases_to_delete)} frases"
        )
        
    except Exception as e:
        return handle_error(e)

# ================ ENDPOINTS DE USUÁRIOS ================

@app.route(f"{API_PREFIX}/users", methods=['POST'])
def register_user():
    """
    POST /api/v1/users
    Registra um novo usuário
    
    Body JSON:
    {
        "username": "nome_usuario",
        "password": "senha"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return format_response(
                success=False,
                message="Campos 'username' e 'password' são obrigatórios",
                status_code=400
            )
        
        username = data['username'].strip()
        password = data['password']
        
        if not username or not password:
            return format_response(
                success=False,
                message="Username e password não podem estar vazios",
                status_code=400
            )
        
        # Registra usuário
        result = frase_manager.register_user(username, password)
        
        if result == "Usuário criado com sucesso!":
            return format_response(
                data={"username": username},
                message="Usuário registrado com sucesso",
                status_code=201
            )
        else:
            return format_response(
                success=False,
                message=result,
                status_code=409
            )
        
    except Exception as e:
        return handle_error(e)

@app.route(f"{API_PREFIX}/auth/login", methods=['POST'])
def login_user():
    """
    POST /api/v1/auth/login
    Autentica um usuário
    
    Body JSON:
    {
        "username": "nome_usuario",
        "password": "senha"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return format_response(
                success=False,
                message="Campos 'username' e 'password' são obrigatórios",
                status_code=400
            )
        
        username = data['username']
        password = data['password']
        
        # Autentica usuário
        user_id = frase_manager.authenticate_user(username, password)
        
        if user_id:
            frase_manager.set_current_user(user_id)
            return format_response(
                data={
                    "user_id": user_id,
                    "username": username,
                    "authenticated": True
                },
                message="Login realizado com sucesso"
            )
        else:
            return format_response(
                success=False,
                message="Credenciais inválidas",
                status_code=401
            )
        
    except Exception as e:
        return handle_error(e)

# ================ ENDPOINTS DE ESTATÍSTICAS ================

@app.route(f"{API_PREFIX}/stats", methods=['GET'])
def get_stats():
    """
    GET /api/v1/stats
    Retorna estatísticas do banco de dados
    
    Query Parameters:
    - user_id: ID do usuário (opcional)
    """
    try:
        user_id = request.args.get('user_id')
        
        # Define usuário se fornecido
        if user_id:
            frase_manager.set_current_user(int(user_id))
        
        # Busca todas as frases para calcular estatísticas
        phrases = frase_manager.ler_frases_completas()
        
        total_phrases = len(phrases)
        total_characters = sum(len(phrase['texto']) for phrase in phrases)
        avg_phrase_length = total_characters / total_phrases if total_phrases > 0 else 0
        
        # Calcula outros dados
        longest_phrase = max(phrases, key=lambda x: len(x['texto'])) if phrases else None
        shortest_phrase = min(phrases, key=lambda x: len(x['texto'])) if phrases else None
        
        stats_data = {
            "total_phrases": total_phrases,
            "total_characters": total_characters,
            "average_phrase_length": round(avg_phrase_length, 2),
            "longest_phrase": {
                "text": longest_phrase['texto'] if longest_phrase else "",
                "length": len(longest_phrase['texto']) if longest_phrase else 0
            },
            "shortest_phrase": {
                "text": shortest_phrase['texto'] if shortest_phrase else "",
                "length": len(shortest_phrase['texto']) if shortest_phrase else 0
            },
            "current_user_id": frase_manager.get_current_user()
        }
        
        return format_response(
            data=stats_data,
            message="Estatísticas calculadas com sucesso"
        )
        
    except Exception as e:
        return handle_error(e)

# ================ ENDPOINTS DE SISTEMA ================

@app.route(f"{API_PREFIX}/health", methods=['GET'])
def health_check():
    """
    GET /api/v1/health
    Verifica a saúde da API
    """
    try:
        # Testa conexão com banco
        conn = frase_manager.get_db_connection()
        conn.close()
        
        return format_response(
            data={
                "status": "healthy",
                "database": "connected",
                "version": API_VERSION
            },
            message="API funcionando corretamente"
        )
        
    except Exception as e:
        return handle_error(e)

@app.route(f"{API_PREFIX}/info", methods=['GET'])
def api_info():
    """
    GET /api/v1/info
    Retorna informações sobre a API
    """
    endpoints = [
        {"method": "GET", "path": "/api/v1/phrases", "description": "Listar frases"},
        {"method": "POST", "path": "/api/v1/phrases", "description": "Adicionar frase"},
        {"method": "PUT", "path": "/api/v1/phrases/<id>", "description": "Atualizar frase"},
        {"method": "DELETE", "path": "/api/v1/phrases", "description": "Remover frases"},
        {"method": "POST", "path": "/api/v1/users", "description": "Registrar usuário"},
        {"method": "POST", "path": "/api/v1/auth/login", "description": "Login"},
        {"method": "GET", "path": "/api/v1/stats", "description": "Estatísticas"},
        {"method": "GET", "path": "/api/v1/health", "description": "Verificar saúde"},
        {"method": "GET", "path": "/api/v1/info", "description": "Informações da API"}
    ]
    
    return format_response(
        data={
            "api_name": "Phrase Manager API",
            "version": API_VERSION,
            "endpoints": endpoints,
            "documentation": "Consulte a documentação completa no arquivo API_DOCUMENTATION.md"
        },
        message="Informações da API"
    )

# ================ INICIALIZAÇÃO ================

def run_api(host='localhost', port=5000, debug=False):
    """Executa a API."""
    print(f"🚀 Iniciando Phrase Manager API v{API_VERSION}")
    print(f"📡 Servidor rodando em http://{host}:{port}")
    print(f"📚 Documentação disponível em http://{host}:{port}/api/v1/info")
    
    app.run(host=host, port=port, debug=debug)

def run_api_background(host='localhost', port=5000):
    """Executa a API em background."""
    def run():
        app.run(host=host, port=port, debug=False, use_reloader=False)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread

if __name__ == "__main__":
    # Inicializa banco de dados
    frase_manager.create_table()
    frase_manager.create_users_table()
    
    # Executa API
    run_api(debug=True)
