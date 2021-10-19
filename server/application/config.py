import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    hostname = os.environ["POSTGRES_HOSTNAME"]
    port = os.environ["POSTGRES_PORT"]
    database = os.environ["POSTGRES_DB"]
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{database}"
    )


class ProductionConfig(Config):
    """Production configuration"""
    PRODUCTION = True


class DevelopmentConfig(Config):
    """Development configuration"""
    DEVELOPMENT = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
