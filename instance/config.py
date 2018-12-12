"""
Api configurations
"""
import os


class Config:
    """
    Base configuration class.
    """
    DEBUG = False
    CSRF_ENABLED = True
    TESTING = False
    DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_URL_TEST = os.getenv('DATABASE_URL_TEST')


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """
    Testing Configurations, with a separate test database
    """
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    """
    Staging configuartions
    """
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    TESTING = False


APP_CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
