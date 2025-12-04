# 🎓 API Vinculación Laboral UNRC

Sistema inteligente de vinculación entre estudiantes de la Universidad Nacional Rosario Castellanos y oportunidades laborales del sector público y privado.

## 🚀 Características

- ✅ **Sistema de Login Seguro**: Autenticación con hash de contraseñas
- ✅ **Registro de Usuarios**: Para estudiantes y empresas
- ✅ **Dashboard Interactivo**: Con métricas y visualizaciones
- ✅ **Base de Datos SQLite**: Gestión de usuarios y sesiones
- ✅ **Interfaz Responsive**: Diseño moderno y adaptable
- ✅ **Arquitectura Modular**: Backend y frontend separados

## 📦 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Crear entorno virtual** (recomendado)
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

La aplicación estará disponible en: `http://localhost:8501`

## 📁 Estructura del Proyecto

```
api-Integracion/
│
├── app.py                    # Aplicación principal
├── requirements.txt          # Dependencias Python
├── streamlit_app.db         # Base de datos SQLite (generada)
│
├── backend/                  # Módulos del backend
│   ├── __init__.py
│   ├── database.py          # Gestión de base de datos
│   ├── auth.py              # Autenticación y sesiones
│   └── models.py            # Modelos de datos
│
├── frontend/                 # Módulos del frontend
│   ├── __init__.py
│   ├── pages.py             # Páginas de la aplicación
│   └── styles.py            # Estilos CSS personalizados
│
└── config/                   # Configuración
    ├── __init__.py
    └── settings.py          # Configuración de la aplicación
```

## 🔑 Credenciales de Prueba

### Estudiantes
- **Email**: `maria.lopez@alumnos.unrc.edu.mx`
- **Password**: `estudiante123`

Otros estudiantes disponibles:
- `carlos.ramirez@alumnos.unrc.edu.mx`
- `ana.martinez@alumnos.unrc.edu.mx`

### Empresas
- **Email**: `rh@tecavanzadas.mx`
- **Password**: `empresa123`

Otras empresas disponibles:
- `contacto@datainsights.mx`

## 🎯 Funcionalidades

### Sistema de Autenticación
- Login seguro con hash de contraseñas
- Gestión de sesiones con tokens
- Registro de nuevos usuarios
- Cierre de sesión automático

### Dashboard de Estudiante
- Visualización de ofertas recomendadas
- Análisis de habilidades vs demanda del mercado
- Progreso del perfil personal
- Métricas de compatibilidad

### Dashboard de Empresa
- Gestión de ofertas laborales
- Estadísticas de candidatos
- Distribución de tipos de ofertas
- Métricas de contratación

## 🏗️ Arquitectura

### Backend (`backend/`)
- **`database.py`**: Gestión completa de la base de datos SQLite
- **`auth.py`**: Sistema de autenticación y gestión de sesiones
- **`models.py`**: Modelos de datos y clases de negocio

### Frontend (`frontend/`)
- **`pages.py`**: Páginas de login, registro y dashboard
- **`styles.py`**: Estilos CSS personalizados y componentes UI

### Configuración (`config/`)
- **`settings.py`**: Configuración centralizada de la aplicación

## 🛠️ Desarrollo

### Agregar Nueva Funcionalidad

1. **Backend**: Agregar métodos en `backend/database.py` o `backend/auth.py`
2. **Frontend**: Crear nueva página en `frontend/pages.py`
3. **Configuración**: Agregar configuraciones en `config/settings.py`

### Ejemplo: Agregar Nueva Página

```python
# frontend/pages.py
class NewPage:
    def __init__(self):
        self.auth = AuthManager()
    
    def render(self):
        st.markdown("### Nueva Página")
        # Tu código aquí
```

## 🚀 Próximas Funcionalidades

- [ ] Sistema de matching con IA
- [ ] Chat entre estudiantes y empresas
- [ ] Notificaciones en tiempo real
- [ ] Exportación de reportes
- [ ] Integración con APIs externas

## 📞 Contacto

- **Universidad**: Universidad Nacional Rosario Castellanos
- **Carrera**: Licenciatura en Ciencia de Datos para Negocios
- **Semestre**: 2025-2

---

**Nota**: Esta aplicación está en desarrollo activo. Las funcionalidades pueden expandirse conforme avanza el proyecto.
