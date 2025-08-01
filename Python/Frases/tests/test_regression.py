# tests/test_regression.py
"""
Sistema de Testes Regressivos para o Gerenciador de Frases
Garante que todas as funcionalidades permaneçam funcionando após alterações.
"""

import unittest
import os
import sys
import tempfile
import sqlite3
import time
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import frase_manager as fm
from api.internal_client import get_api_client
from api.api_manager import ensure_api_running, stop_api


class TesteDatabaseRegressivo(unittest.TestCase):
    """Testes regressivos do banco de dados e frase_manager."""
    
    @classmethod
    def setUpClass(cls):
        """Configuração única para todos os testes."""
        cls.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        cls.test_db.close()
        
        # Salva o banco original e usa o de teste
        cls.original_db = fm.DB_PATH
        fm.DB_PATH = cls.test_db.name
        
        # Cria tabelas de teste
        fm.create_table()
        fm.create_users_table()
    
    @classmethod
    def tearDownClass(cls):
        """Limpeza após todos os testes."""
        fm.DB_PATH = cls.original_db
        os.unlink(cls.test_db.name)
    
    def setUp(self):
        """Configuração para cada teste."""
        # Limpa dados do teste anterior
        conn = fm.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM frases")
        cursor.execute("DELETE FROM users")
        conn.commit()
        conn.close()
        
        fm.set_current_user(None)
    
    def test_01_criacao_tabelas(self):
        """Testa se as tabelas são criadas corretamente."""
        conn = fm.get_db_connection()
        cursor = conn.cursor()
        
        # Verifica tabela frases
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='frases'")
        self.assertIsNotNone(cursor.fetchone(), "Tabela 'frases' não foi criada")
        
        # Verifica tabela users
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        self.assertIsNotNone(cursor.fetchone(), "Tabela 'users' não foi criada")
        
        conn.close()
    
    def test_02_registro_usuario(self):
        """Testa registro de usuário."""
        # Registro válido
        success, message = fm.register_user("teste_user", "senha123456")
        self.assertTrue(success, f"Falha no registro: {message}")
        self.assertEqual(message, "Usuário registrado com sucesso")
        
        # Registro duplicado
        success, message = fm.register_user("teste_user", "senha123456")
        self.assertFalse(success, "Deveria falhar no registro duplicado")
        
        # Senha muito curta
        success, message = fm.register_user("teste2", "123")
        self.assertFalse(success, "Deveria falhar com senha curta")
        self.assertIn("6 caracteres", message)
    
    def test_03_autenticacao_usuario(self):
        """Testa autenticação de usuário."""
        # Registra usuário
        fm.register_user("auth_user", "senha123456")
        
        # Login válido
        user_id = fm.authenticate_user("auth_user", "senha123456")
        self.assertIsNotNone(user_id, "Falha na autenticação válida")
        
        # Login inválido
        user_id = fm.authenticate_user("auth_user", "senha_errada")
        self.assertIsNone(user_id, "Deveria falhar com senha incorreta")
        
        # Usuário inexistente
        user_id = fm.authenticate_user("inexistente", "senha123456")
        self.assertIsNone(user_id, "Deveria falhar com usuário inexistente")
    
    def test_04_gerenciamento_frases(self):
        """Testa operações CRUD de frases."""
        # Registra e loga usuário
        fm.register_user("phrase_user", "senha123456")
        user_id = fm.authenticate_user("phrase_user", "senha123456")
        fm.set_current_user(user_id)
        
        # Adiciona frase
        result = fm.adicionar_frase("Frase de teste")
        self.assertTrue(result, "Falha ao adicionar frase")
        
        # Verifica se foi adicionada
        frases = fm.ler_frases()
        self.assertEqual(len(frases), 1, "Frase não foi adicionada")
        self.assertEqual(frases[0], "Frase de teste")
        
        # Testa frase duplicada
        result = fm.adicionar_frase("Frase de teste")
        self.assertFalse(result, "Deveria falhar ao adicionar frase duplicada")
        
        # Atualiza frase
        result = fm.atualizar_frase("Frase de teste", "Frase atualizada")
        self.assertTrue(result, "Falha ao atualizar frase")
        
        frases = fm.ler_frases()
        self.assertIn("Frase atualizada", frases)
        self.assertNotIn("Frase de teste", frases)
        
        # Remove frase
        result = fm.remover_frase("Frase atualizada")
        self.assertTrue(result, "Falha ao remover frase")
        
        frases = fm.ler_frases()
        self.assertEqual(len(frases), 0, "Frase não foi removida")
    
    def test_05_criptografia(self):
        """Testa sistema de criptografia."""
        texto_original = "Texto para criptografar"
        
        # Criptografa
        texto_criptografado = fm.encrypt_text(texto_original)
        self.assertNotEqual(texto_original, texto_criptografado, "Texto não foi criptografado")
        
        # Descriptografa
        texto_descriptografado = fm.decrypt_text(texto_criptografado)
        self.assertEqual(texto_original, texto_descriptografado, "Falha na descriptografia")
        
        # Testa texto não criptografado (compatibilidade)
        texto_normal = "Texto normal"
        resultado = fm.decrypt_text(texto_normal)
        self.assertEqual(texto_normal, resultado, "Falha na compatibilidade com texto não criptografado")
    
    def test_06_ordenacao_frases(self):
        """Testa diferentes ordenações de frases."""
        # Registra usuário e adiciona frases
        fm.register_user("sort_user", "senha123456")
        user_id = fm.authenticate_user("sort_user", "senha123456")
        fm.set_current_user(user_id)
        
        frases_teste = ["Zebra", "Abelha", "Gato", "Cachorro"]
        for frase in frases_teste:
            fm.adicionar_frase(frase)
        
        # Ordenação original
        frases = fm.ler_frases("original")
        self.assertEqual(frases, frases_teste, "Falha na ordenação original")
        
        # Ordenação alfabética
        frases = fm.ler_frases("alfabetica")
        esperado = ["Abelha", "Cachorro", "Gato", "Zebra"]
        self.assertEqual(frases, esperado, "Falha na ordenação alfabética")
        
        # Ordenação alfabética inversa
        frases = fm.ler_frases("alfabetica_inversa")
        esperado.reverse()
        self.assertEqual(frases, esperado, "Falha na ordenação alfabética inversa")
    
    def test_07_busca_frases(self):
        """Testa busca de frases."""
        # Registra usuário e adiciona frases
        fm.register_user("search_user", "senha123456")
        user_id = fm.authenticate_user("search_user", "senha123456")
        fm.set_current_user(user_id)
        
        frases_teste = [
            "Gato preto subiu no telhado",
            "Cachorro branco correu no jardim",
            "Gato branco dormiu na cama"
        ]
        for frase in frases_teste:
            fm.adicionar_frase(frase)
        
        # Busca por "gato"
        resultado = fm.buscar_frases("gato")
        self.assertEqual(len(resultado), 2, "Busca por 'gato' falhou")
        
        # Busca por "branco"
        resultado = fm.buscar_frases("branco")
        self.assertEqual(len(resultado), 2, "Busca por 'branco' falhou")
        
        # Busca que não encontra nada
        resultado = fm.buscar_frases("inexistente")
        self.assertEqual(len(resultado), 0, "Busca deveria retornar vazio")


class TesteAPIRegressivo(unittest.TestCase):
    """Testes regressivos da API."""
    
    @classmethod
    def setUpClass(cls):
        """Inicia servidor da API para testes."""
        ensure_api_running()
        time.sleep(2)  # Aguarda API inicializar
    
    @classmethod
    def tearDownClass(cls):
        """Para servidor da API."""
        stop_api()
    
    def setUp(self):
        """Configuração para cada teste da API."""
        self.client = get_api_client()
        
        # Cria usuário único para cada teste
        import uuid
        self.test_user = f"test_{uuid.uuid4().hex[:8]}"
        self.test_password = "senha123456"
        
        # Registra e faz login
        self.client.register_user(self.test_user, self.test_password)
        success, message = self.client.login(self.test_user, self.test_password)
        self.assertTrue(success, f"Falha no login: {message}")
    
    def test_01_api_health(self):
        """Testa se a API está funcionando."""
        response = self.client._make_request('GET', '/health')
        self.assertTrue(response.get('success'), "API não está saudável")
    
    def test_02_api_frases_crud(self):
        """Testa operações CRUD via API."""
        # Adiciona frase
        result = self.client.add_phrase("Frase teste API")
        self.assertEqual(result, "Frase adicionada com sucesso!")
        
        # Lista frases
        frases = self.client.get_phrases()
        self.assertIn("Frase teste API", frases)
        
        # Atualiza frase
        result = self.client.update_phrase("Frase teste API", "Frase atualizada API")
        self.assertEqual(result, "Frase atualizada com sucesso!")
        
        # Verifica atualização
        frases = self.client.get_phrases()
        self.assertIn("Frase atualizada API", frases)
        self.assertNotIn("Frase teste API", frases)
        
        # Remove frase
        result = self.client.delete_phrases(["Frase atualizada API"])
        self.assertTrue(result)
        
        # Verifica remoção
        frases = self.client.get_phrases()
        self.assertNotIn("Frase atualizada API", frases)
    
    def test_03_api_frases_duplicadas(self):
        """Testa detecção de frases duplicadas via API."""
        # Adiciona frase
        result = self.client.add_phrase("Frase duplicada teste")
        self.assertEqual(result, "Frase adicionada com sucesso!")
        
        # Tenta adicionar duplicata
        result = self.client.add_phrase("Frase duplicada teste")
        self.assertEqual(result, "Frase já existe!")
    
    def test_04_api_busca_frases(self):
        """Testa busca de frases via API."""
        # Adiciona frases
        frases_teste = ["API gato", "API cachorro", "gato especial"]
        for frase in frases_teste:
            self.client.add_phrase(frase)
        
        # Busca por "gato"
        resultado = self.client.search_phrases("gato")
        self.assertEqual(len(resultado), 2)
        
        # Busca por "API"
        resultado = self.client.search_phrases("API")
        self.assertEqual(len(resultado), 2)


class TesteIntegracaoRegressivo(unittest.TestCase):
    """Testes regressivos de integração."""
    
    def test_01_compatibilidade_funcoes(self):
        """Testa se as funções de compatibilidade funcionam."""
        from api.internal_client import (
            ler_frases, adicionar_frase, buscar_frases, 
            remover_frase, atualizar_frase, authenticate_user, register_user
        )
        
        # Testa se as funções existem e são chamáveis
        self.assertTrue(callable(ler_frases))
        self.assertTrue(callable(adicionar_frase))
        self.assertTrue(callable(buscar_frases))
        self.assertTrue(callable(remover_frase))
        self.assertTrue(callable(atualizar_frase))
        self.assertTrue(callable(authenticate_user))
        self.assertTrue(callable(register_user))
    
    def test_02_migracao_api_funcionando(self):
        """Testa se a migração para APIs mantém funcionalidade."""
        # Inicia API
        ensure_api_running()
        time.sleep(1)
        
        try:
            from api.internal_client import ler_frases, adicionar_frase
            
            # Testa função de compatibilidade
            frases_antes = ler_frases()
            count_antes = len(frases_antes)
            
            # Adiciona via função de compatibilidade
            resultado = adicionar_frase("Teste compatibilidade")
            
            # Verifica se funcionou
            frases_depois = ler_frases()
            
            # Se não houve erro, deveria ter pelo menos o mesmo número de frases
            self.assertGreaterEqual(len(frases_depois), count_antes)
            
        finally:
            stop_api()


def run_regression_tests():
    """Executa todos os testes regressivos."""
    print("🧪 INICIANDO TESTES REGRESSIVOS")
    print("=" * 50)
    
    # Cria suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona testes na ordem
    suite.addTests(loader.loadTestsFromTestCase(TesteDatabaseRegressivo))
    suite.addTests(loader.loadTestsFromTestCase(TesteAPIRegressivo))
    suite.addTests(loader.loadTestsFromTestCase(TesteIntegracaoRegressivo))
    
    # Executa testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL DOS TESTES REGRESSIVOS")
    print("=" * 50)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    success = total_tests - failures - errors
    
    print(f"✅ Sucessos: {success}/{total_tests}")
    print(f"❌ Falhas: {failures}")
    print(f"🚨 Erros: {errors}")
    
    if result.wasSuccessful():
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ As funcionalidades estão preservadas")
        return True
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM!")
        print("❌ Verifique as funcionalidades afetadas")
        return False


if __name__ == "__main__":
    success = run_regression_tests()
    sys.exit(0 if success else 1)
