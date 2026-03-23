import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
    DEBUG   = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        "title":       "ApiRestFlask – Blog API",
        "version":     "1.0.0",
        "description": "API REST pour gérer des articles de blog – DK-dorinal",
        "uiversion":   3,
    }


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'blog.db')}",
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///blog.db")


config_map = {
    "development": DevelopmentConfig,
    "testing":     TestingConfig,
    "production":  ProductionConfig,
}

active_config = config_map.get(os.environ.get("APP_ENV", "development"), DevelopmentConfig)
