# frontend/pages.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend.auth import AuthManager
from backend.database import DatabaseManager
from backend.models import CompatibilityCalculator
from config.settings import Config

class LoginPage:
    """Página de login"""
    
    def __init__(self):
        self.auth = AuthManager()
    
    def render(self):
        """Renderiza la página de login"""
        st.markdown("""
        <div class="encabezado">
            <h1>🎓 Plataforma de Vinculación Laboral UNRC </h1>
            <p>Sistema inteligente de vinculación entre estudiantes y oportunidades laborales</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            
            st.markdown("### 🔐 Iniciar Sesión")
            
            with st.form("login_form"):
                email = st.text_input("📧 Email", placeholder="tu.email@alumnos.unrc.edu.mx")
                password = st.text_input("🔒 Contraseña", type="password")
                
                col_login, col_register = st.columns(2)
                
                with col_login:
                    login_submitted = st.form_submit_button("🚀 Iniciar Sesión", use_container_width=True)
                
                with col_register:
                    register_submitted = st.form_submit_button("📝 Registrarse", use_container_width=True)
            
            if login_submitted:
                if email and password:
                    if self.auth.login(email, password):
                        st.success(f"¡Bienvenido!")
                        st.rerun()
                    else:
                        st.error("❌ Credenciales incorrectas")
                else:
                    st.error("❌ Por favor completa todos los campos")
            
            if register_submitted:
                st.session_state['show_register'] = True
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Mostrar credenciales de prueba
            with st.expander("🔑 Credenciales de Prueba"):
                st.markdown("""
                **Estudiantes:**
                - Email: `maria.lopez@alumnos.unrc.edu.mx`
                - Password: `estudiante123`
                
                **Empresas:**
                - Email: `rh@tecavanzadas.mx`
                - Password: `empresa123`
                """)

class RegisterPage:
    """Página de registro"""
    
    def __init__(self):
        self.auth = AuthManager()
    
    def render(self):
        """Renderiza la página de registro"""
        st.markdown("""
        <div class="encabezado">
            <h1>📝 Registro de Usuario</h1>
            <p>Únete a nuestra plataforma de vinculación laboral</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            
            with st.form("register_form"):
                tipo_usuario = st.selectbox("👤 Tipo de Usuario", ["estudiante", "empresa"])
                
                nombre = st.text_input("👤 Nombre Completo")
                email = st.text_input("📧 Email")
                password = st.text_input("🔒 Contraseña", type="password")
                confirm_password = st.text_input("🔒 Confirmar Contraseña", type="password")
                
                if tipo_usuario == "estudiante":
                    carrera = st.text_input("🎓 Carrera")
                    semestre = st.number_input("📚 Semestre", min_value=1, max_value=12, value=1)
                    habilidades = st.text_area("🛠️ Habilidades (separadas por comas)")
                else:
                    carrera = None
                    semestre = None
                    habilidades = None
                
                col_submit, col_back = st.columns(2)
                
                with col_submit:
                    register_submitted = st.form_submit_button("✅ Registrarse", use_container_width=True)
                
                with col_back:
                    back_submitted = st.form_submit_button("⬅️ Volver al Login", use_container_width=True)
            
            if register_submitted:
                if password != confirm_password:
                    st.error("❌ Las contraseñas no coinciden")
                elif not all([nombre, email, password]):
                    st.error("❌ Por favor completa todos los campos obligatorios")
                else:
                    success = self.auth.register_user(email, password, nombre, tipo_usuario, carrera, semestre, habilidades)
                    if success:
                        st.success("✅ Usuario registrado exitosamente")
                        st.session_state['show_register'] = False
                        st.rerun()
                    else:
                        st.error("❌ El email ya está registrado")
            
            if back_submitted:
                st.session_state['show_register'] = False
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

class DashboardPage:
    """Página principal del dashboard"""
    
    def __init__(self):
        self.auth = AuthManager()
        self.db = DatabaseManager()
        self.compatibility_calc = CompatibilityCalculator()
    
    def render(self):
        """Renderiza el dashboard principal"""
        user_data = self.auth.get_current_user()
        
        if not user_data:
            st.error("❌ Sesión no válida")
            return
        
        # Sidebar con información del usuario
        with st.sidebar:
            st.markdown(f"""
            ### 👋 Hola, {user_data['nombre']}
            
            **Tipo:** {user_data['tipo'].title()}
            **Email:** {user_data['email']}
            """)
            
            if user_data['tipo'] == 'estudiante':
                st.markdown(f"""
                **Carrera:** {user_data['carrera']}
                **Semestre:** {user_data['semestre']}
                **Habilidades:** {user_data['habilidades']}
                """)
            
            if st.button("🚪 Cerrar Sesión"):
                self.auth.logout()
                st.rerun()
        
        # Contenido principal
        st.markdown(f"""
        <div class="encabezado">
            <h1>📊 Dashboard - {user_data['nombre']}</h1>
            <p>Bienvenido al sistema de vinculación laboral</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas principales
        self._render_metrics()
        
        # Contenido específico según el tipo de usuario
        if user_data['tipo'] == 'estudiante':
            self._render_student_dashboard(user_data)
        else:
            self._render_company_dashboard(user_data)
    
    def _render_metrics(self):
        """Renderiza las métricas principales"""
        col1, col2, col3, col4 = st.columns(4)
        
        # Obtener estadísticas reales
        offers = self.db.get_all_offers()
        users = self.db.get_all_users()
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📈</h3>
                <h2>{len(offers)}</h2>
                <p>Ofertas Activas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            estudiantes = len([u for u in users if u['tipo'] == 'estudiante'])
            st.markdown(f"""
            <div class="metric-card">
                <h3>👥</h3>
                <h2>{estudiantes}</h2>
                <p>Estudiantes Registrados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            empresas = len([u for u in users if u['tipo'] == 'empresa'])
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏢</h3>
                <h2>{empresas}</h2>
                <p>Empresas Participantes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯</h3>
                <h2>89%</h2>
                <p>Match Rate</p>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_student_dashboard(self, user_data):
        """Renderiza el dashboard específico para estudiantes"""
        st.markdown("### 🎓 Panel del Estudiante")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown("#### 🔍 Ofertas Recomendadas")
            
            # Obtener ofertas y calcular compatibilidad
            offers = self.db.get_all_offers()
            user_skills = user_data['habilidades'].split(',') if user_data['habilidades'] else []
            
            recommendations = []
            for offer in offers:
                required_skills = offer['habilidades_requeridas'].split(',') if offer['habilidades_requeridas'] else []
                compatibility = self.compatibility_calc.calculate_compatibility(user_skills, required_skills)
                
                recommendations.append({
                    'Empresa': offer['empresa_nombre'],
                    'Posición': offer['titulo'],
                    'Tipo': offer['tipo'].title(),
                    'Compatibilidad': f"{compatibility:.0f}%"
                })
            
            # Ordenar por compatibilidad
            recommendations.sort(key=lambda x: float(x['Compatibilidad'].replace('%', '')), reverse=True)
            
            df_recommendations = pd.DataFrame(recommendations[:5])  # Top 5
            st.dataframe(df_recommendations, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown("#### 📊 Mi Progreso")
            
            # Calcular progreso del perfil
            progress = 0
            if user_data['carrera']:
                progress += 25
            if user_data['semestre']:
                progress += 25
            if user_data['habilidades']:
                progress += 25
            if user_data['email']:
                progress += 25
            
            # Gráfico de progreso
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=progress,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Perfil Completo"},
                delta={'reference': 60},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráfico de habilidades
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown("#### 🛠️ Análisis de Habilidades")
        
        if user_data['habilidades']:
            habilidades_data = {
                'Habilidad': [skill.strip() for skill in user_data['habilidades'].split(',')],
                'Mi Nivel': [85, 70, 60, 90, 75][:len(user_data['habilidades'].split(','))],
                'Demanda': [95, 88, 92, 65, 80][:len(user_data['habilidades'].split(','))]
            }
            
            df_habilidades = pd.DataFrame(habilidades_data)
            
            fig = px.bar(df_habilidades, x='Habilidad', y=['Mi Nivel', 'Demanda'], 
                         title="Mi Nivel vs Demanda del Mercado",
                         barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Completa tu perfil agregando tus habilidades para ver el análisis")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_company_dashboard(self, user_data):
        """Renderiza el dashboard específico para empresas"""
        st.markdown("### 🏢 Panel de la Empresa")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown("#### 📋 Mis Ofertas")
            
            # Botón para crear nueva oferta
            if st.button("➕ Crear Nueva Oferta"):
                st.session_state['show_create_offer'] = True
            
            # Obtener ofertas de la empresa
            offers = self.db.get_offers_by_company(user_data['id'])
            
            if offers:
                offers_data = {
                    'Título': [offer['titulo'] for offer in offers],
                    'Estado': ['Activa' if offer['activa'] else 'Cerrada' for offer in offers],
                    'Tipo': [offer['tipo'].title() for offer in offers],
                    'Ubicación': [offer['ubicacion'] for offer in offers]
                }
                
                df_ofertas = pd.DataFrame(offers_data)
                st.dataframe(df_ofertas, use_container_width=True)
            else:
                st.info("No tienes ofertas publicadas aún")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown("#### 📈 Estadísticas")
            
            # Gráfico de ofertas por tipo
            if offers:
                tipos_ofertas = {}
                for offer in offers:
                    tipo = offer['tipo']
                    tipos_ofertas[tipo] = tipos_ofertas.get(tipo, 0) + 1
                
                fig = px.pie(values=list(tipos_ofertas.values()), 
                             names=list(tipos_ofertas.keys()), 
                             title="Distribución de Mis Ofertas")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Publica ofertas para ver estadísticas")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráfico de ubicaciones
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown("#### 📍 Ofertas por Ubicación")
        
        if offers:
            ubicaciones = {}
            for offer in offers:
                ubicacion = offer['ubicacion']
                ubicaciones[ubicacion] = ubicaciones.get(ubicacion, 0) + 1
            
            fig = px.bar(x=list(ubicaciones.keys()), 
                         y=list(ubicaciones.values()),
                         title="Ofertas por Ubicación")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Publica ofertas para ver el análisis por ubicación")
        
        st.markdown('</div>', unsafe_allow_html=True)
