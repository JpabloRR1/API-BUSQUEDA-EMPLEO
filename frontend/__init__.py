# frontend/__init__.py
from .pages import LoginPage, RegisterPage, DashboardPage
from .styles import get_css_styles

__all__ = [
    'LoginPage',
    'RegisterPage', 
    'DashboardPage',
    'get_css_styles'
]
