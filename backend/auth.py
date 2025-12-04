# backend/auth.py
import streamlit as st
from backend.database import DatabaseManager

class AuthManager:
    """Manejador de autenticación y sesiones"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def login(self, email, password):
        """Autentica un usuario y crea una sesión"""
        user = self.db.authenticate_user(email, password)
        if user:
            token = self.db.create_session(user['id'])
            st.session_state['user_token'] = token
            st.session_state['user_data'] = user
            return True
        return False
    
    def logout(self):
        """Cierra la sesión del usuario actual"""
        token = st.session_state.get('user_token')
        if token:
            self.db.logout_user(token)
        st.session_state.clear()
    
    def get_current_user(self):
        """Obtiene el usuario actual de la sesión"""
        token = st.session_state.get('user_token')
        if token:
            user = self.db.verify_session(token)
            if user:
                st.session_state['user_data'] = user
                return user
            else:
                # Sesión expirada
                st.session_state.clear()
        return None
    
    def is_authenticated(self):
        """Verifica si el usuario está autenticado"""
        return self.get_current_user() is not None
    
    def require_auth(self):
        """Decorador para requerir autenticación"""
        if not self.is_authenticated():
            st.error("❌ Debes iniciar sesión para acceder a esta página")
            st.stop()
    
    def require_user_type(self, required_type):
        """Verifica que el usuario sea del tipo requerido"""
        user = self.get_current_user()
        if not user:
            st.error("❌ Debes iniciar sesión para acceder a esta página")
            st.stop()
        
        if user['tipo'] != required_type:
            st.error(f"❌ Esta página es solo para {required_type}s")
            st.stop()
        
        return user
    
    def register_user(self, email, password, nombre, tipo, carrera=None, semestre=None, habilidades=None):
        """Registra un nuevo usuario"""
        return self.db.create_user(email, password, nombre, tipo, carrera, semestre, habilidades)
    
    def get_user_stats(self):
        """Obtiene estadísticas de usuarios"""
        users = self.db.get_all_users()
        
        stats = {
            'total_users': len(users),
            'estudiantes': len([u for u in users if u['tipo'] == 'estudiante']),
            'empresas': len([u for u in users if u['tipo'] == 'empresa']),
            'users_by_career': {},
            'users_by_semester': {}
        }
        
        for user in users:
            if user['tipo'] == 'estudiante':
                # Estadísticas por carrera
                carrera = user['carrera'] or 'No especificada'
                stats['users_by_career'][carrera] = stats['users_by_career'].get(carrera, 0) + 1
                
                # Estadísticas por semestre
                semestre = user['semestre'] or 0
                stats['users_by_semester'][semestre] = stats['users_by_semester'].get(semestre, 0) + 1
        
        return stats
