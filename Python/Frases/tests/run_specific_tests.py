# tests/run_specific_tests.py
"""
Script para executar testes específicos de funcionalidades.
"""

import sys
import os
import unittest
import importlib

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_config import setup_test_environment, cleanup_test_files

class TestRunner:
    """Executor de testes específicos."""
    
    def __init__(self):
        self.available_tests = {
            'database': 'Testes do banco de dados',
            'api': 'Testes da API',
            'ui': 'Testes da interface',
            'integration': 'Testes de integração',
            'all': 'Todos os testes',
            'quick': 'Teste rápido (essenciais)',
        }
    
    def list_available_tests(self):
        """Lista testes disponíveis."""
        print("📋 TESTES DISPONÍVEIS:")
        print("=" * 30)
        for key, description in self.available_tests.items():
            print(f"  {key}: {description}")
        print()
    
    def run_database_tests(self):
        """Executa apenas testes de banco de dados."""
        print("🗄️ EXECUTANDO TESTES DE BANCO DE DADOS")
        print("=" * 40)
        
        from test_regression import TesteDatabaseRegressivo
        
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TesteDatabaseRegressivo)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
    
    def run_api_tests(self):
        """Executa apenas testes de API."""
        print("🌐 EXECUTANDO TESTES DE API")
        print("=" * 25)
        
        from test_regression import TesteAPIRegressivo
        
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TesteAPIRegressivo)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
    
    def run_ui_tests(self):
        """Executa apenas testes de UI."""
        print("🖥️ EXECUTANDO TESTES DE INTERFACE")
        print("=" * 35)
        
        from test_ui_regression import run_ui_regression_tests
        return run_ui_regression_tests()
    
    def run_integration_tests(self):
        """Executa apenas testes de integração."""
        print("🔗 EXECUTANDO TESTES DE INTEGRAÇÃO")
        print("=" * 35)
        
        from test_regression import TesteIntegracaoRegressivo
        
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TesteIntegracaoRegressivo)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
    
    def run_quick_tests(self):
        """Executa testes essenciais rápidos."""
        print("⚡ EXECUTANDO TESTES RÁPIDOS")
        print("=" * 30)
        
        # Testa importações básicas
        try:
            import frase_manager
            print("✅ frase_manager")
            
            from api.internal_client import get_api_client
            print("✅ API client")
            
            from ui.phrase_manager_app import PhraseManagerApp
            print("✅ Interface principal")
            
            from components.phrase_list import PhraseListManager
            print("✅ Componente de lista")
            
            from components.dialogs import DialogManager
            print("✅ Componente de diálogos")
            
            print("\n✅ Todos os módulos principais carregaram corretamente")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar módulos: {e}")
            return False
    
    def run_all_tests(self):
        """Executa todos os testes."""
        print("🧪 EXECUTANDO TODOS OS TESTES")
        print("=" * 30)
        
        from test_regression import run_regression_tests
        return run_regression_tests()
    
    def run_test(self, test_type):
        """Executa teste específico."""
        test_methods = {
            'database': self.run_database_tests,
            'api': self.run_api_tests,
            'ui': self.run_ui_tests,
            'integration': self.run_integration_tests,
            'quick': self.run_quick_tests,
            'all': self.run_all_tests,
        }
        
        if test_type not in test_methods:
            print(f"❌ Tipo de teste inválido: {test_type}")
            self.list_available_tests()
            return False
        
        # Configura ambiente
        setup_test_environment()
        
        try:
            success = test_methods[test_type]()
            
            if success:
                print(f"\n✅ TESTE '{test_type}' PASSOU!")
            else:
                print(f"\n❌ TESTE '{test_type}' FALHOU!")
            
            return success
            
        except Exception as e:
            print(f"\n🚨 ERRO DURANTE TESTE '{test_type}': {e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            # Limpa ambiente de teste
            cleanup_test_files()


def main():
    """Função principal."""
    runner = TestRunner()
    
    print("🧪 EXECUTOR DE TESTES ESPECÍFICOS")
    print("Gerenciador de Frases")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        # Executa teste especificado na linha de comando
        test_type = sys.argv[1].lower()
        success = runner.run_test(test_type)
        sys.exit(0 if success else 1)
    else:
        # Modo interativo
        runner.list_available_tests()
        
        try:
            test_type = input("Digite o tipo de teste para executar: ").strip().lower()
            
            if test_type == '':
                test_type = 'quick'
                print("Executando teste rápido (padrão)...")
            
            success = runner.run_test(test_type)
            
            if success:
                print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
            else:
                print("\n⚠️ TESTE FALHOU!")
            
            sys.exit(0 if success else 1)
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Teste interrompido pelo usuário")
            sys.exit(1)


if __name__ == "__main__":
    main()
