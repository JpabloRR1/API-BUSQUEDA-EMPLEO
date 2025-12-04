# backend/database.py
import sqlite3
import hashlib
from datetime import datetime, timedelta
from config.settings import Config

class DatabaseManager:
    """Manejador de la base de datos SQLite"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or Config.DATABASE_PATH
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    tipo TEXT NOT NULL CHECK (tipo IN ('estudiante', 'empresa')),
                    carrera TEXT,
                    semestre INTEGER,
                    habilidades TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de sesiones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sesiones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER,
                    token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            ''')
            
            # Tabla de ofertas laborales
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ofertas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    empresa_id INTEGER,
                    titulo TEXT NOT NULL,
                    descripcion TEXT,
                    tipo TEXT NOT NULL CHECK (tipo IN ('practica', 'empleo', 'servicio_social')),
                    habilidades_requeridas TEXT,
                    ubicacion TEXT,
                    activa BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (empresa_id) REFERENCES usuarios (id)
                )
            ''')
            
            # Tabla de matches
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    estudiante_id INTEGER,
                    oferta_id INTEGER,
                    compatibilidad REAL,
                    estado TEXT DEFAULT 'pendiente',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (estudiante_id) REFERENCES usuarios (id),
                    FOREIGN KEY (oferta_id) REFERENCES ofertas (id)
                )
            ''')
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error inicializando base de datos: {e}")
            return False
        finally:
            conn.close()
    
    def hash_password(self, password):
        """Hashea una contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, password_hash):
        """Verifica si una contraseña coincide con su hash"""
        return self.hash_password(password) == password_hash
    
    def create_user(self, email, password, nombre, tipo, carrera=None, semestre=None, habilidades=None):
        """Crea un nuevo usuario en la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO usuarios (email, password_hash, nombre, tipo, carrera, semestre, habilidades)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (email, password_hash, nombre, tipo, carrera, semestre, habilidades))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user_by_email(self, email):
        """Obtiene un usuario por su email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, password_hash, nombre, tipo, carrera, semestre, habilidades
            FROM usuarios WHERE email = ?
        ''', (email,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'email': user[1],
                'password_hash': user[2],
                'nombre': user[3],
                'tipo': user[4],
                'carrera': user[5],
                'semestre': user[6],
                'habilidades': user[7]
            }
        return None
    
    def authenticate_user(self, email, password):
        """Autentica un usuario y retorna sus datos"""
        user = self.get_user_by_email(email)
        if user and self.verify_password(password, user['password_hash']):
            # Remover el hash de la contraseña del retorno
            user.pop('password_hash')
            return user
        return None
    
    def create_session(self, user_id):
        """Crea una nueva sesión para el usuario"""
        import secrets
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=Config.SESSION_DURATION_HOURS)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sesiones (usuario_id, token, expires_at)
            VALUES (?, ?, ?)
        ''', (user_id, token, expires_at))
        
        conn.commit()
        conn.close()
        
        return token
    
    def verify_session(self, token):
        """Verifica si una sesión es válida"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.usuario_id, u.email, u.nombre, u.tipo, u.carrera, u.semestre, u.habilidades
            FROM sesiones s
            JOIN usuarios u ON s.usuario_id = u.id
            WHERE s.token = ? AND s.expires_at > ?
        ''', (token, datetime.now()))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'email': user[1],
                'nombre': user[2],
                'tipo': user[3],
                'carrera': user[4],
                'semestre': user[5],
                'habilidades': user[6]
            }
        return None
    
    def logout_user(self, token):
        """Cierra la sesión del usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sesiones WHERE token = ?', (token,))
        conn.commit()
        conn.close()
    
    def get_all_users(self):
        """Obtiene todos los usuarios"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, nombre, tipo, carrera, semestre, habilidades, created_at
            FROM usuarios
        ''')
        
        users = cursor.fetchall()
        conn.close()
        
        return [{
            'id': user[0],
            'email': user[1],
            'nombre': user[2],
            'tipo': user[3],
            'carrera': user[4],
            'semestre': user[5],
            'habilidades': user[6],
            'created_at': user[7]
        } for user in users]
    
    def get_offers_by_company(self, empresa_id):
        """Obtiene las ofertas de una empresa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, titulo, descripcion, tipo, habilidades_requeridas, ubicacion, activa, created_at
            FROM ofertas WHERE empresa_id = ?
        ''', (empresa_id,))
        
        offers = cursor.fetchall()
        conn.close()
        
        return [{
            'id': offer[0],
            'titulo': offer[1],
            'descripcion': offer[2],
            'tipo': offer[3],
            'habilidades_requeridas': offer[4],
            'ubicacion': offer[5],
            'activa': offer[6],
            'created_at': offer[7]
        } for offer in offers]
    
    def get_all_offers(self):
        """Obtiene todas las ofertas activas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT o.id, o.titulo, o.descripcion, o.tipo, o.habilidades_requeridas, 
                   o.ubicacion, u.nombre as empresa_nombre
            FROM ofertas o
            JOIN usuarios u ON o.empresa_id = u.id
            WHERE o.activa = 1
        ''')
        
        offers = cursor.fetchall()
        conn.close()
        
        return [{
            'id': offer[0],
            'titulo': offer[1],
            'descripcion': offer[2],
            'tipo': offer[3],
            'habilidades_requeridas': offer[4],
            'ubicacion': offer[5],
            'empresa_nombre': offer[6]
        } for offer in offers]
    
    def populate_test_data(self):
        """Pobla la base de datos con datos de prueba"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar si ya existen datos
            cursor.execute('SELECT COUNT(*) FROM usuarios')
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Crear usuarios de prueba
                for user_type, users in Config.TEST_USERS.items():
                    for user in users:
                        password_hash = self.hash_password(user['password'])
                        cursor.execute('''
                            INSERT INTO usuarios (email, password_hash, nombre, tipo, carrera, semestre, habilidades)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            user['email'], 
                            password_hash, 
                            user['nombre'], 
                            user_type[:-1],  # Remove 's' from 'estudiantes'/'empresas'
                            user.get('carrera'),
                            user.get('semestre'),
                            user.get('habilidades')
                        ))
                
                # Crear ofertas de prueba
                for offer in Config.TEST_OFFERS:
                    cursor.execute('''
                        INSERT INTO ofertas (empresa_id, titulo, descripcion, tipo, habilidades_requeridas, ubicacion)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        offer['empresa_id'],
                        offer['titulo'],
                        offer['descripcion'],
                        offer['tipo'],
                        offer['habilidades_requeridas'],
                        offer['ubicacion']
                    ))
                
                conn.commit()
                return True
            return False
            
        except Exception as e:
            print(f"Error poblando datos de prueba: {e}")
            return False
        finally:
            conn.close()
