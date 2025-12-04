# backend/models.py
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class User:
    """Modelo de Usuario"""
    id: int
    email: str
    nombre: str
    tipo: str  # 'estudiante' o 'empresa'
    carrera: Optional[str] = None
    semestre: Optional[int] = None
    habilidades: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def is_student(self) -> bool:
        return self.tipo == 'estudiante'
    
    def is_company(self) -> bool:
        return self.tipo == 'empresa'
    
    def get_skills_list(self) -> List[str]:
        """Convierte las habilidades en una lista"""
        if not self.habilidades:
            return []
        return [skill.strip() for skill in self.habilidades.split(',')]

@dataclass
class Session:
    """Modelo de Sesión"""
    id: int
    usuario_id: int
    token: str
    expires_at: datetime
    created_at: datetime

@dataclass
class Offer:
    """Modelo de Oferta Laboral"""
    id: int
    empresa_id: int
    titulo: str
    descripcion: str
    tipo: str  # 'practica', 'empleo', 'servicio_social'
    habilidades_requeridas: str
    ubicacion: str
    activa: bool = True
    created_at: Optional[datetime] = None
    empresa_nombre: Optional[str] = None
    
    def get_required_skills_list(self) -> List[str]:
        """Convierte las habilidades requeridas en una lista"""
        if not self.habilidades_requeridas:
            return []
        return [skill.strip() for skill in self.habilidades_requeridas.split(',')]
    
    def get_type_display(self) -> str:
        """Retorna el tipo de oferta en formato legible"""
        type_map = {
            'practica': 'Práctica Profesional',
            'empleo': 'Empleo',
            'servicio_social': 'Servicio Social'
        }
        return type_map.get(self.tipo, self.tipo)

@dataclass
class Match:
    """Modelo de Match entre estudiante y oferta"""
    id: int
    estudiante_id: int
    oferta_id: int
    compatibilidad: float
    estado: str = 'pendiente'  # 'pendiente', 'aceptado', 'rechazado'
    created_at: Optional[datetime] = None

class UserStats:
    """Estadísticas de usuarios"""
    
    def __init__(self, total_users: int, estudiantes: int, empresas: int, 
                 users_by_career: dict, users_by_semester: dict):
        self.total_users = total_users
        self.estudiantes = estudiantes
        self.empresas = empresas
        self.users_by_career = users_by_career
        self.users_by_semester = users_by_semester
    
    def get_career_percentage(self, carrera: str) -> float:
        """Calcula el porcentaje de usuarios por carrera"""
        if self.total_users == 0:
            return 0.0
        return (self.users_by_career.get(carrera, 0) / self.total_users) * 100
    
    def get_semester_distribution(self) -> dict:
        """Retorna la distribución por semestre"""
        return self.users_by_semester

class OfferStats:
    """Estadísticas de ofertas"""
    
    def __init__(self, total_offers: int, offers_by_type: dict, offers_by_location: dict):
        self.total_offers = total_offers
        self.offers_by_type = offers_by_type
        self.offers_by_location = offers_by_location
    
    def get_type_percentage(self, tipo: str) -> float:
        """Calcula el porcentaje de ofertas por tipo"""
        if self.total_offers == 0:
            return 0.0
        return (self.offers_by_type.get(tipo, 0) / self.total_offers) * 100

class CompatibilityCalculator:
    """Calculador de compatibilidad entre estudiantes y ofertas"""
    
    @staticmethod
    def calculate_compatibility(student_skills: List[str], required_skills: List[str]) -> float:
        """Calcula la compatibilidad entre habilidades del estudiante y requeridas"""
        if not required_skills:
            return 0.0
        
        # Normalizar habilidades (minúsculas, sin espacios extra)
        student_skills_normalized = [skill.lower().strip() for skill in student_skills]
        required_skills_normalized = [skill.lower().strip() for skill in required_skills]
        
        # Contar habilidades que coinciden
        matches = 0
        for required_skill in required_skills_normalized:
            for student_skill in student_skills_normalized:
                if required_skill in student_skill or student_skill in required_skill:
                    matches += 1
                    break
        
        # Calcular porcentaje de compatibilidad
        compatibility = (matches / len(required_skills_normalized)) * 100
        return min(compatibility, 100.0)  # Máximo 100%
    
    @staticmethod
    def get_skill_gaps(student_skills: List[str], required_skills: List[str]) -> List[str]:
        """Identifica habilidades faltantes"""
        student_skills_normalized = [skill.lower().strip() for skill in student_skills]
        required_skills_normalized = [skill.lower().strip() for skill in required_skills]
        
        gaps = []
        for required_skill in required_skills_normalized:
            found = False
            for student_skill in student_skills_normalized:
                if required_skill in student_skill or student_skill in required_skill:
                    found = True
                    break
            if not found:
                gaps.append(required_skill)
        
        return gaps
