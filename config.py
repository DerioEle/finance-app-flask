import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuração padrão da aplicação"""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'finance.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de segurança
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    TESTING = False
    # Em desenvolvimento, permitir cookies não-seguros
    REMEMBER_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# Seleciona a configuração baseada no ambiente
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
