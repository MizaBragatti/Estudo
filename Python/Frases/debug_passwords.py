#!/usr/bin/env python3
"""
Script de debug para verificar e corrigir problemas com senhas.
"""

import frase_manager

def main():
    print("=== Script de Debug - Sistema de Senhas ===\n")
    
    # Mostra debug dos usuários existentes
    frase_manager.debug_user_passwords()
    
    print("=== Opções ===")
    print("1. Criar novo usuário de teste")
    print("2. Testar login")
    print("3. Sair")
    
    while True:
        choice = input("\nEscolha uma opção (1-3): ").strip()
        
        if choice == "1":
            username = input("Nome do usuário: ").strip()
            password = input("Senha: ").strip()
            
            if username and password:
                success, message = frase_manager.register_user(username, password)
                if success:
                    print(f"✅ Usuário '{username}' criado com sucesso!")
                else:
                    print(f"❌ Erro: {message}")
            else:
                print("❌ Nome de usuário e senha são obrigatórios.")
        
        elif choice == "2":
            username = input("Nome do usuário: ").strip()
            password = input("Senha: ").strip()
            
            if username and password:
                if frase_manager.authenticate_user(username, password):
                    print("✅ Login bem-sucedido!")
                else:
                    print("❌ Login falhou - usuário ou senha inválidos.")
            else:
                print("❌ Nome de usuário e senha são obrigatórios.")
        
        elif choice == "3":
            print("Saindo...")
            break
        
        else:
            print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
