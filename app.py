# app.py - Aplicación principal refactorizada
import streamlit as st
from backend import DatabaseManager, AuthManager
from frontend import LoginPage, RegisterPage, DashboardPage, get_css_styles
from config import Config

def main():
    """Función principal de la aplicación"""
    # Configuración de la página
    st.set_page_config(
        page_title=Config.PAGE_TITLE,
        page_icon=Config.PAGE_ICON,
        layout=Config.LAYOUT,
        initial_sidebar_state="collapsed"
    )
    
    # Aplicar estilos CSS
    st.markdown(get_css_styles(), unsafe_allow_html=True)
    
    # Inicializar componentes
    db = DatabaseManager()
    auth = AuthManager()
    
    # Inicializar base de datos
    if not db.init_database():
        st.error("❌ Error inicializando la base de datos")
        st.stop()
    
    # Poblar datos de prueba
    db.populate_test_data()
    
    # Verificar si hay una sesión activa
    user_data = auth.get_current_user()
    
    if user_data:
        # Usuario autenticado - mostrar dashboard
        dashboard = DashboardPage()
        dashboard.render()
    else:
        # Usuario no autenticado - mostrar login o registro
        if st.session_state.get('show_register'):
            register = RegisterPage()
            register.render()
        else:
            login = LoginPage()
            login.render()

if __name__ == "__main__":
    main()
