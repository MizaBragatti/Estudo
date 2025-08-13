# utils/language_manager.py
"""
Gerenciador de idiomas da aplicação (i18n).
"""

import json
import os
import flet as ft

class LanguageManager:
    """Gerenciador de idiomas da aplicação."""
    
    LANGUAGE_FILE = "language_config.json"
    
    # Idiomas suportados
    SUPPORTED_LANGUAGES = {
        "pt": "Português",
        "en": "English", 
        "es": "Español"
    }
    
    # Traduções
    TRANSLATIONS = {
        "pt": {
            # Tela de Login
            "login_title": "Login de Usuário",
            "app_title": "Gerenciador e Lembretes de Frases",
            "welcome": "Bem-vindo!",
            "username": "Usuário",
            "password": "Senha",
            "login": "Entrar",
            "register": "Registrar Novo Usuário",
            "settings": "Configurações",
            "login_success": "Login bem-sucedido!",
            "login_error": "Usuário ou senha inválidos.",
            "login_required": "Por favor, insira usuário e senha.",
            "register_required": "Por favor, insira usuário e senha para registrar.",
            "register_success": "Usuário '{}' registrado com sucesso! Agora você pode fazer login.",
            "user_not_logged": "❌ Usuário não está logado.",
            
            # Tela Principal
            "phrase_manager": "Gerenciador e Lembretes de Frases",
            "phrase_management": "Gerenciamento de Frases",
            "phrase": "Frase",
            "search_phrases": "🔍 Buscar frases...",
            "search_placeholder": "Digite para buscar frases",
            "sort_by": "Ordenar por:",
            "add_phrase": "Adicionar Frase",
            "update_phrase": "Atualizar Frase",
            "delete_phrase": "Excluir Frase",
            "select_all": "Selecionar Tudo",
            "deselect_all": "Desselecionar Tudo",
            "import_phrases": "Importar Frases",
            "export_phrases": "Exportar Frases",
            "logout": "Sair/Logout",
            "total_phrases": "Total de Frases: {}",
            "phrase": "Frase",
            "search_phrases": "🔍 Buscar frases...",
            "search_placeholder": "Digite para buscar frases",
            "sort_by": "Ordenar por:",
            "add_phrase": "Adicionar Frase",
            "update_phrase": "Atualizar Frase",
            "delete_phrase": "Excluir Frase",
            "select_all": "Selecionar Tudo",
            "deselect_all": "Desselecionar Tudo",
            "import_phrases": "Importar Frases",
            "export_phrases": "Exportar Frases",
            "logout": "Sair/Logout",
            "total_phrases": "Total de frases: {}",
            
            # API Status
            "waiting_api": "Aguardando API...",
            "api_connecting": "🔄 Conectando com a API...",
            "api_ready": "✅ API conectada! Você pode fazer login.",
            "api_error": "❌ Erro na API. Verifique a conexão.",
            
            # Lembretes
            "start_reminders": "Iniciar Lembretes",
            "stop_reminders": "Parar Lembretes",
            "click_start_reminders": "Clique em 'Iniciar Lembretes' para começar.",
            "interval_seconds": "Intervalo (segundos)",
            "timeout_minutes": "Tempo Limite (minutos)",
            
            # Interface - Textos adicionais
            "multiple_selection_info": "💡 Use o checkbox abaixo para ativar seleção múltipla",
            "multiple_selection_mode": "Modo Seleção Múltipla",
            
            # Tela de Configurações
            "settings_title": "⚙️ Configurações",
            "window_position": "📍 Posição da Janela",
            "save_position": "💾 Salvar Posição Atual",
            "reset_position": "🔄 Resetar Posição",
            "monitor_title": "🖥️ Monitor",
            "monitor": "🖥️ Monitor",
            "current_monitor": "Monitor Atual: {}",
            "theme_title": "🎨 Tema",
            "theme": "🎨 Tema",
            "light_theme": "☀️ Tema Claro",
            "dark_theme": "🌙 Tema Escuro",
            "language_title": "🌍 Idioma",
            "language": "🌍 Idioma",
            "language_pt": "🇧🇷 Português",
            "language_en": "🇺🇸 Inglês", 
            "language_es": "🇪🇸 Espanhol",
            "back": "← Voltar",
            "position_saved": "✅ Posição salva com sucesso!",
            "position_save_error": "❌ Erro ao salvar posição",
            "position_reset": "✅ Posição resetada com sucesso! Reinicie a aplicação para aplicar.",
            "position_reset_error": "❌ Erro ao resetar posição",
            "position_info_format": "X: {} | Y: {} | Largura: {} | Altura: {}",
            "current_monitor": "Monitor Atual: {}",
            "theme_changed": "✅ Tema alterado com sucesso!",
            "theme_already_active": "✅ Este tema já está ativo!",
            "theme_change_error": "❌ Erro ao alterar tema",
            "language_changed": "✅ Idioma alterado com sucesso!",
            "language_already_active": "✅ Este idioma já está ativo!",
            "language_change_error": "❌ Erro ao alterar idioma",
            "width": "Largura",
            "height": "Altura",
            "error": "❌ Erro: {}",
            "ok": "OK",
            
            # Ordenação
            "sort_creation_old": "Ordem de Criação (Antiga para Nova)",
            "sort_creation_new": "Ordem de Criação Inversa (Nova para Antiga)", 
            "sort_alphabetical": "Ordem Alfabética (A-Z)",
            "sort_alphabetical_reverse": "Ordem Alfabética Inversa (Z-A)",
            
            # Mensagens da UI
            "delete_multiple_phrases": "Excluir {} Frases",
            "delete_single_phrase": "Excluir Frase",
            "phrase_added_success": "Frase adicionada com sucesso!",
            "phrase_already_exists": "Frase já existe!",
            "phrase_added_success_detail": "✅ Frase '{}' adicionada com sucesso!",
            "please_enter_phrase": "Por favor, digite uma frase para adicionar.",
            "invalid_interval_number": "Por favor, digite um número válido para o intervalo.",
            "invalid_timeout_number": "Por favor, digite um número válido para o tempo limite.",
            "timeout_must_be_positive": "O tempo limite deve ser um número positivo ou zero para sem limite.",
            "duplicate_phrase_title": "Frase Duplicada",
            "duplicate_phrase_message": "A frase abaixo já existe na sua lista:\n\n'{}'\n\n🔍 Veja a frase destacada em laranja na lista ao lado.\nDigite uma frase diferente ou edite a existente.",
            "ok_understood": "OK, ENTENDI",
            "phrases_selected": "✅ {} frases selecionadas",
            "no_changes_made": "✅ Nenhuma alteração realizada - frase mantida!",
            "phrase_updated": "Frase atualizada para:\n'{}'",
            "update_error": "❌ Erro ao atualizar: {}",
            "reminders_already_active": "Lembretes já estão ativos.",
            "interval_must_be_positive": "O intervalo deve ser um número positivo.",
            "empty_phrase_update": "O campo de frase para atualização não pode estar vazio.",
            "error_generic": "❌ Erro: {}",
            "no_phrases_to_select": "Não há frases para selecionar.",
            "please_select_phrases": "Por favor, selecione uma ou mais frases para excluir.",
            "confirm_deletion": "Confirmar Exclusão",
            "confirm_multiple_deletion": "Confirmar Exclusão Múltipla",
            "confirm_delete_single": "Tem certeza que deseja excluir a frase:\n'{}'?",
            "confirm_delete_multiple": "Tem certeza que deseja excluir {} frases?\n\n{}",
            "and_more_phrases": "... e mais {} frases",
            "phrase_deleted_success": "Frase '{}' excluída com sucesso!",
            "phrase_delete_error": "Erro ao excluir a frase '{}'.",
            "phrases_deleted_success": "{} frases excluídas com sucesso!",
            "phrases_delete_error": "Erro ao excluir as frases selecionadas.",
            "all_phrases_deleted": "Todas as frases foram excluídas. Lembretes parados."
        },
        
        "en": {
            # Login Screen
            "login_title": "User Login",
            "app_title": "Phrase Manager and Reminders",
            "welcome": "Welcome!",
            "username": "Username",
            "password": "Password",
            "login": "Login",
            "register": "Register New User",
            "settings": "Settings",
            "login_success": "Login successful!",
            "login_error": "Invalid user or password.",
            "login_required": "Please enter user and password.",
            "register_required": "Please enter user and password to register.",
            "register_success": "User '{}' registered successfully! You can now login.",
            "user_not_logged": "❌ User is not logged in.",
            
            # Main Screen
            "phrase_manager": "Phrase Manager and Reminders",
            "phrase_management": "Phrase Management",
            "phrase": "Phrase",
            "search_phrases": "🔍 Search phrases...",
            "search_placeholder": "Type to search phrases",
            "sort_by": "Sort by:",
            "add_phrase": "Add Phrase",
            "update_phrase": "Update Phrase",
            "delete_phrase": "Delete Phrase",
            "select_all": "Select All",
            "deselect_all": "Deselect All",
            "import_phrases": "Import Phrases",
            "export_phrases": "Export Phrases",
            "logout": "Exit/Logout",
            "total_phrases": "Total phrases: {}",
            "phrase": "Phrase",
            "search_phrases": "🔍 Search phrases...",
            "search_placeholder": "Type to search phrases",
            "sort_by": "Sort by:",
            "add_phrase": "Add Phrase",
            "update_phrase": "Update Phrase",
            "delete_phrase": "Delete Phrase",
            "select_all": "Select All",
            "deselect_all": "Deselect All",
            "import_phrases": "Import Phrases",
            "export_phrases": "Export Phrases",
            "logout": "Logout",
            "total_phrases": "Total phrases: {}",
            
            # API Status
            "waiting_api": "Waiting for API...",
            "api_connecting": "🔄 Connecting to API...",
            "api_ready": "✅ API connected! You can login.",
            "api_error": "❌ API error. Check connection.",
            
            # Reminders
            "start_reminders": "Start Reminders",
            "stop_reminders": "Stop Reminders",
            "click_start_reminders": "Click 'Start Reminders' to begin.",
            "interval_seconds": "Interval (seconds)",
            "timeout_minutes": "Timeout (minutes)",
            
            # Interface - Additional texts
            "multiple_selection_info": "💡 Use the checkbox below to enable multiple selection",
            "multiple_selection_mode": "Multiple Selection Mode",
            
            # Settings Screen
            "settings_title": "⚙️ Settings",
            "window_position": "📍 Window Position",
            "save_position": "💾 Save Current Position",
            "reset_position": "🔄 Reset Position",
            "monitor_title": "🖥️ Monitor",
            "monitor": "🖥️ Monitor",
            "current_monitor": "Current Monitor: {}",
            "theme_title": "🎨 Theme",
            "theme": "🎨 Theme",
            "light_theme": "☀️ Light Theme",
            "dark_theme": "🌙 Dark Theme",
            "language_title": "🌍 Language",
            "language": "🌍 Language",
            "language_pt": "🇧🇷 Portuguese",
            "language_en": "🇺🇸 English",
            "language_es": "🇪🇸 Spanish",
            "back": "← Back",
            "position_saved": "✅ Position saved successfully!",
            "position_save_error": "❌ Error saving position",
            "position_reset": "✅ Position reset successfully! Restart application to apply.",
            "position_reset_error": "❌ Error resetting position",
            "position_info_format": "X: {} | Y: {} | Width: {} | Height: {}",
            "current_monitor": "Current Monitor: {}",
            "theme_changed": "✅ Theme changed successfully!",
            "theme_already_active": "✅ This theme is already active!",
            "theme_change_error": "❌ Error changing theme",
            "language_changed": "✅ Language changed successfully!",
            "language_already_active": "✅ This language is already active!",
            "language_change_error": "❌ Error changing language",
            "width": "Width",
            "height": "Height",
            "error": "❌ Error: {}",
            "ok": "OK",
            
            # Sorting
            "sort_creation_old": "Creation Order (Old to New)",
            "sort_creation_new": "Reverse Creation Order (New to Old)",
            "sort_alphabetical": "Alphabetical Order (A-Z)",
            "sort_alphabetical_reverse": "Reverse Alphabetical Order (Z-A)",
            
            # UI Messages
            "delete_multiple_phrases": "Delete {} Phrases",
            "delete_single_phrase": "Delete Phrase",
            "phrase_added_success": "Phrase added successfully!",
            "phrase_already_exists": "Phrase already exists!",
            "phrase_added_success_detail": "✅ Phrase '{}' added successfully!",
            "please_enter_phrase": "Please enter a phrase to add.",
            "invalid_interval_number": "Please enter a valid number for the interval.",
            "invalid_timeout_number": "Please enter a valid number for the timeout.",
            "timeout_must_be_positive": "The timeout must be a positive number or zero for no limit.",
            "duplicate_phrase_title": "Duplicate Phrase",
            "duplicate_phrase_message": "The phrase below already exists in your list:\n\n'{}'\n\n🔍 See the phrase highlighted in orange in the list on the side.\nEnter a different phrase or edit the existing one.",
            "ok_understood": "OK, GOT IT",
            "phrases_selected": "✅ {} phrases selected",
            "no_changes_made": "✅ No changes made - phrase kept!",
            "phrase_updated": "Phrase updated to:\n'{}'",
            "update_error": "❌ Update error: {}",
            "reminders_already_active": "Reminders are already active.",
            "interval_must_be_positive": "The interval must be a positive number.",
            "empty_phrase_update": "The phrase field for update cannot be empty.",
            "error_generic": "❌ Error: {}",
            "no_phrases_to_select": "No phrases to select.",
            "please_select_phrases": "Please select one or more phrases to delete.",
            "confirm_deletion": "Confirm Deletion",
            "confirm_multiple_deletion": "Confirm Multiple Deletion",
            "confirm_delete_single": "Are you sure you want to delete the phrase:\n'{}'?",
            "confirm_delete_multiple": "Are you sure you want to delete {} phrases?\n\n{}",
            "and_more_phrases": "... and {} more phrases",
            "phrase_deleted_success": "Phrase '{}' deleted successfully!",
            "phrase_delete_error": "Error deleting phrase '{}'.",
            "phrases_deleted_success": "{} phrases deleted successfully!",
            "phrases_delete_error": "Error deleting selected phrases.",
            "all_phrases_deleted": "All phrases have been deleted. Reminders stopped."
        },
        
        "es": {
            # Pantalla de Login
            "login_title": "Inicio de Sesión de Usuario",
            "app_title": "Gestor de Frases y Recordatorios",
            "welcome": "¡Bienvenido!",
            "username": "Usuario", 
            "password": "Contraseña",
            "login": "Iniciar Sesión",
            "register": "Registrar Nuevo Usuario",
            "settings": "Configuración",
            "login_success": "¡Inicio de sesión exitoso!",
            "login_error": "Usuario o contraseña inválidos.",
            "login_required": "Por favor, ingrese usuario y contraseña.",
            "register_required": "Por favor, ingrese usuario y contraseña para registrarse.",
            "register_success": "¡Usuario '{}' registrado exitosamente! Ahora puede iniciar sesión.",
            "user_not_logged": "❌ El usuario no está conectado.",
            
            # Pantalla Principal
            "phrase_manager": "Gestor de Frases y Recordatorios",
            "phrase_management": "Gestión de Frases",
            "phrase": "Frase",
            "search_phrases": "🔍 Buscar frases...",
            "search_placeholder": "Escriba para buscar frases",
            "sort_by": "Ordenar por:",
            "add_phrase": "Agregar Frase",
            "update_phrase": "Actualizar Frase",
            "delete_phrase": "Eliminar Frase",
            "select_all": "Seleccionar Todo",
            "import_phrases": "Importar Frases",
            "export_phrases": "Exportar Frases",
            "logout": "Salir/Cerrar Sesión",
            "total_phrases": "Total de frases: {}",
            "phrase": "Frase",
            "search_phrases": "🔍 Buscar frases...",
            "search_placeholder": "Escriba para buscar frases",
            "sort_by": "Ordenar por:",
            "add_phrase": "Agregar Frase",
            "update_phrase": "Actualizar Frase",
            "delete_phrase": "Eliminar Frase",
            "select_all": "Seleccionar Todo",
            "deselect_all": "Deseleccionar Todo",
            "import_phrases": "Importar Frases",
            "export_phrases": "Exportar Frases",
            "logout": "Cerrar Sesión",
            "total_phrases": "Total de frases: {}",
            
            # Estado de API
            "waiting_api": "Esperando API...",
            "api_connecting": "🔄 Conectando con la API...",
            "api_ready": "✅ API conectada! Puede iniciar sesión.",
            "api_error": "❌ Error en API. Verifique conexión.",
            
            # Recordatorios
            "start_reminders": "Iniciar Recordatorios",
            "stop_reminders": "Detener Recordatorios",
            "click_start_reminders": "Haga clic en 'Iniciar Recordatorios' para comenzar.",
            "interval_seconds": "Intervalo (segundos)",
            "timeout_minutes": "Tiempo Límite (minutos)",
            
            # Interfaz - Textos adicionales
            "multiple_selection_info": "💡 Use la casilla de verificación a continuación para habilitar selección múltiple",
            "multiple_selection_mode": "Modo Selección Múltiple",
            
            # Pantalla de Configuración
            "settings_title": "⚙️ Configuración",
            "window_position": "📍 Posición de Ventana",
            "save_position": "💾 Guardar Posición Actual",
            "reset_position": "🔄 Restablecer Posición",
            "monitor_title": "🖥️ Monitor",
            "monitor": "🖥️ Monitor",
            "current_monitor": "Monitor Actual: {}",
            "theme_title": "🎨 Tema",
            "theme": "🎨 Tema",
            "light_theme": "☀️ Tema Claro",
            "dark_theme": "🌙 Tema Oscuro",
            "language_title": "🌍 Idioma",
            "language": "🌍 Idioma",
            "language_pt": "🇧🇷 Portugués",
            "language_en": "🇺🇸 Inglés",
            "language_es": "🇪🇸 Español",
            "back": "← Volver",
            "position_saved": "✅ ¡Posición guardada exitosamente!",
            "position_save_error": "❌ Error al guardar posición",
            "position_reset": "✅ ¡Posición restablecida exitosamente! Reinicie la aplicación para aplicar.",
            "position_reset_error": "❌ Error al restablecer posición",
            "position_info_format": "X: {} | Y: {} | Ancho: {} | Alto: {}",
            "current_monitor": "Monitor Actual: {}",
            "theme_changed": "✅ ¡Tema cambiado exitosamente!",
            "theme_already_active": "✅ ¡Este tema ya está activo!",
            "theme_change_error": "❌ Error al cambiar tema",
            "language_changed": "✅ ¡Idioma cambiado exitosamente!",
            "language_already_active": "✅ ¡Este idioma ya está activo!",
            "language_change_error": "❌ Error al cambiar idioma",
            "width": "Ancho",
            "height": "Alto",
            "error": "❌ Error: {}",
            "ok": "OK",
            
            # Ordenación
            "sort_creation_old": "Orden de Creación (Antigua a Nueva)",
            "sort_creation_new": "Orden de Creación Inverso (Nueva a Antigua)",
            "sort_alphabetical": "Orden Alfabético (A-Z)",
            "sort_alphabetical_reverse": "Orden Alfabético Inverso (Z-A)",
            
            # Mensajes de UI
            "delete_multiple_phrases": "Eliminar {} Frases",
            "delete_single_phrase": "Eliminar Frase",
            "phrase_added_success": "¡Frase agregada exitosamente!",
            "phrase_already_exists": "¡La frase ya existe!",
            "phrase_added_success_detail": "✅ Frase '{}' agregada exitosamente!",
            "please_enter_phrase": "Por favor, ingrese una frase para agregar.",
            "invalid_interval_number": "Por favor, ingrese un número válido para el intervalo.",
            "invalid_timeout_number": "Por favor, ingrese un número válido para el tiempo límite.",
            "timeout_must_be_positive": "El tiempo límite debe ser un número positivo o cero para sin límite.",
            "duplicate_phrase_title": "Frase Duplicada",
            "duplicate_phrase_message": "La frase siguiente ya existe en su lista:\n\n'{}'\n\n🔍 Vea la frase resaltada en naranja en la lista al lado.\nIngrese una frase diferente o edite la existente.",
            "ok_understood": "OK, ENTENDIDO",
            "phrases_selected": "✅ {} frases seleccionadas",
            "no_changes_made": "✅ No se realizaron cambios - ¡frase mantenida!",
            "phrase_updated": "Frase actualizada a:\n'{}'",
            "update_error": "❌ Error de actualización: {}",
            "reminders_already_active": "Los recordatorios ya están activos.",
            "interval_must_be_positive": "El intervalo debe ser un número positivo.",
            "empty_phrase_update": "El campo de frase para actualización no puede estar vacío.",
            "error_generic": "❌ Error: {}",
            "no_phrases_to_select": "No hay frases para seleccionar.",
            "please_select_phrases": "Por favor, seleccione una o más frases para eliminar.",
            "confirm_deletion": "Confirmar Eliminación",
            "confirm_multiple_deletion": "Confirmar Eliminación Múltiple",
            "confirm_delete_single": "¿Está seguro de que desea eliminar la frase:\n'{}'?",
            "confirm_delete_multiple": "¿Está seguro de que desea eliminar {} frases?\n\n{}",
            "and_more_phrases": "... y {} frases más",
            "phrase_deleted_success": "Frase '{}' eliminada exitosamente!",
            "phrase_delete_error": "Error al eliminar la frase '{}'.",
            "phrases_deleted_success": "¡{} frases eliminadas exitosamente!",
            "phrases_delete_error": "Error al eliminar las frases seleccionadas.",
            "all_phrases_deleted": "Todas las frases han sido eliminadas. Recordatorios detenidos."
        }
    }
    
    def __init__(self):
        self.current_language = self.load_language()
    
    def load_language(self):
        """Carrega o idioma salvo ou retorna o padrão."""
        try:
            if os.path.exists(self.LANGUAGE_FILE):
                with open(self.LANGUAGE_FILE, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    language = saved_config.get('language', 'pt')
                    if language in self.SUPPORTED_LANGUAGES:
                        return language
            return 'pt'  # Padrão português
        except Exception as e:
            print(f"Erro ao carregar idioma: {e}")
            return 'pt'
    
    def save_language(self, language_code):
        """Salva o idioma escolhido."""
        try:
            if language_code not in self.SUPPORTED_LANGUAGES:
                return False
                
            config = {"language": language_code}
            with open(self.LANGUAGE_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.current_language = language_code
            return True
        except Exception as e:
            print(f"Erro ao salvar idioma: {e}")
            return False
    
    def get_current_language(self):
        """Retorna o código do idioma atual."""
        return self.current_language
    
    def get_current_language_name(self):
        """Retorna o nome do idioma atual."""
        return self.SUPPORTED_LANGUAGES.get(self.current_language, "Português")
    
    def get_supported_languages(self):
        """Retorna os idiomas suportados."""
        return self.SUPPORTED_LANGUAGES
    
    def translate(self, key, *args):
        """Traduz uma chave para o idioma atual."""
        try:
            translation = self.TRANSLATIONS[self.current_language].get(key, key)
            if args:
                return translation.format(*args)
            return translation
        except Exception as e:
            print(f"Erro na tradução da chave '{key}': {e}")
            return key
    
    def t(self, key, *args):
        """Atalho para translate."""
        return self.translate(key, *args)
