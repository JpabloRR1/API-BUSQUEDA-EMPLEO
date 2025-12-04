# config/settings.py
import os
from pathlib import Path

# Configuración de la aplicación
class Config:
    # Base de datos
    DATABASE_PATH = os.path.join(Path(__file__).parent.parent, 'streamlit_app.db')
    
    # Configuración de sesiones
    SESSION_DURATION_HOURS = 24
    
    # Configuración de la aplicación Streamlit
    PAGE_TITLE = "Plataforma de Vinculación Laboral UNRC"
    PAGE_ICON = "🎓"
    LAYOUT = "wide"
    
    # Configuración de seguridad
    PASSWORD_HASH_ALGORITHM = "sha256"
    
    # Configuración de la UI
    PRIMARY_COLOR = "#1f4e79"
    SECONDARY_COLOR = "#2d5a87"
    
    # Credenciales de prueba
    TEST_USERS = {
        'estudiantes': [
            {
                'email': 'maria.lopez@alumnos.unrc.edu.mx',
                'password': 'estudiante123',
                'nombre': 'María López',
                'carrera': 'Ciencia de Datos',
                'semestre': 8,
                'habilidades': 'Python, SQL, Machine Learning'
            },
            {
                'email': 'carlos.ramirez@alumnos.unrc.edu.mx',
                'password': 'estudiante123',
                'nombre': 'Carlos Ramírez',
                'carrera': 'Ingeniería en Sistemas',
                'semestre': 6,
                'habilidades': 'Java, JavaScript, React'
            },
            {
                'email': 'ana.martinez@alumnos.unrc.edu.mx',
                'password': 'estudiante123',
                'nombre': 'Ana Martínez',
                'carrera': 'Administración',
                'semestre': 7,
                'habilidades': 'Excel, Power BI, Marketing'
            }
        ],
        'empresas': [
            {
                'email': 'rh@tecavanzadas.mx',
                'password': 'empresa123',
                'nombre': 'Tecnologías Avanzadas'
            },
            {
                'email': 'contacto@datainsights.mx',
                'password': 'empresa123',
                'nombre': 'Data Insights'
            }
        ]
    }
    
    # Ofertas de prueba
    TEST_OFFERS = [
        {
            'empresa_id': 4,
            'titulo': 'Desarrollador Python Junior',
            'descripcion': 'Buscamos desarrollador con experiencia en Python y Django',
            'tipo': 'empleo',
            'habilidades_requeridas': 'Python, Django, SQL',
            'ubicacion': 'CDMX'
        },
        {
            'empresa_id': 4,
            'titulo': 'Práctica en Machine Learning',
            'descripcion': 'Práctica profesional en proyectos de ML',
            'tipo': 'practica',
            'habilidades_requeridas': 'Python, Scikit-learn, Pandas',
            'ubicacion': 'CDMX'
        },
        {
            'empresa_id': 5,
            'titulo': 'Analista de Datos',
            'descripcion': 'Posición para analizar datos empresariales',
            'tipo': 'empleo',
            'habilidades_requeridas': 'SQL, Power BI, Excel',
            'ubicacion': 'CDMX'
        }
    ]
