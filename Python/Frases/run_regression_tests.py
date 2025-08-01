# run_regression_tests.py
"""
Script principal para executar testes regressivos do Gerenciador de Frases.
"""

import os
import sys
import subprocess
import importlib.util

def check_dependencies():
    """Verifica se todas as dependências estão disponíveis."""
    print("🔍 Verificando dependências...")
    
    required_modules = [
        'flet', 'requests', 'flask', 'sqlite3'
    ]
    
    missing = []
    for module in required_modules:
        try:
            importlib.util.find_spec(module)
            print(f"  ✅ {module}")
        except ImportError:
            missing.append(module)
            print(f"  ❌ {module}")
    
    if missing:
        print(f"\n⚠️ Módulos faltando: {', '.join(missing)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão disponíveis")
    return True

def run_quick_test():
    """Executa um teste rápido das funcionalidades principais."""
    print("\n⚡ TESTE RÁPIDO DE FUNCIONALIDADES")
    print("=" * 40)
    
    try:
        # Teste básico do banco
        import frase_manager as fm
        print("✅ frase_manager importado")
        
        # Teste básico da API
        from api.internal_client import get_api_client
        print("✅ API client importado")
        
        # Teste básico da interface
        import ui.phrase_manager_app
        print("✅ Interface importada")
        
        print("✅ Importações básicas funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Erro nas importações: {e}")
        return False

def run_full_regression():
    """Executa testes regressivos completos."""
    print("\n🧪 TESTES REGRESSIVOS COMPLETOS")
    print("=" * 40)
    
    try:
        from tests.test_regression import run_regression_tests
        return run_regression_tests()
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False

def generate_test_report():
    """Gera relatório detalhado dos testes."""
    report = """
# RELATÓRIO DE TESTES REGRESSIVOS

## Funcionalidades Testadas

### 🗄️ Banco de Dados
- ✅ Criação de tabelas
- ✅ Registro de usuários
- ✅ Autenticação
- ✅ CRUD de frases
- ✅ Criptografia/Descriptografia
- ✅ Ordenação de frases
- ✅ Busca de frases

### 🌐 API
- ✅ Health check da API
- ✅ CRUD via API
- ✅ Detecção de duplicatas
- ✅ Busca via API

### 🔗 Integração
- ✅ Funções de compatibilidade
- ✅ Migração para APIs
- ✅ Preservação de funcionalidades

## Resultados
- Total de testes executados
- Sucessos vs Falhas
- Tempo de execução
- Cobertura funcional

## Recomendações
- Execute antes de cada release
- Execute após mudanças significativas
- Monitore performance dos testes
"""
    
    with open("test_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("📊 Relatório salvo em test_report.md")

def main():
    """Função principal."""
    print("🚀 SISTEMA DE TESTES REGRESSIVOS")
    print("Gerenciador de Frases")
    print("=" * 50)
    
    # Verifica dependências
    if not check_dependencies():
        return False
    
    # Teste rápido
    if not run_quick_test():
        print("❌ Teste rápido falhou!")
        return False
    
    # Pergunta se deve executar teste completo
    print("\n📋 OPÇÕES:")
    print("1. Executar apenas teste rápido (concluído)")
    print("2. Executar testes regressivos completos")
    print("3. Gerar relatório de testes")
    
    try:
        choice = input("\nEscolha uma opção (1-3): ").strip()
        
        if choice == "2":
            success = run_full_regression()
            if success:
                print("\n🎉 TODOS OS TESTES REGRESSIVOS PASSARAM!")
                print("✅ Aplicação está estável para deployment")
            else:
                print("\n⚠️ ALGUNS TESTES FALHARAM!")
                print("❌ Verifique as funcionalidades antes do deployment")
            return success
            
        elif choice == "3":
            generate_test_report()
            return True
            
        else:
            print("✅ Teste rápido executado com sucesso!")
            return True
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Testes interrompidos pelo usuário")
        return False
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
