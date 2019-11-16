import os


def get_pg_uri():
    user = os.getenv('DB_USER')
    pwd = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    name = os.getenv('DB_NAME', 'postgres')

    return f'postgresql+psycopg2://{user}:{pwd}@{host}/{name}'


class Config:
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    SECRET_KEY = os.getenv('APP_SECRET_KEY', 'fa692e9c9fe0a1e22322ef87bb19f26b129d8c9b44b98')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', get_pg_uri())
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
