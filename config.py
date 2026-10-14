"""Application configuration classes for development, testing, and production."""

import os
from dotenv import load_dotenv

load_dotenv()


def _database_uri():
    uri = os.getenv("DATABASE_URL", "sqlite:///swiftcourier.db")
    if uri.startswith("postgresql://"):
        return uri.replace("postgresql://", "postgresql+psycopg2://", 1)
    return uri


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    DATABASE_CONFIGURED = bool(os.getenv("DATABASE_URL"))
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 300}
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


class TestingConfig(BaseConfig):
    TESTING = True
    DATABASE_CONFIGURED = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False


CONFIG = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
