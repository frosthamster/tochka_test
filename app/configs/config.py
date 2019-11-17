import os
import logging.config


def get_pg_uri(prefix=''):
    pwd = os.getenv(f'{prefix}DB_PASSWORD')
    user = os.getenv(f'{prefix}DB_USER', 'postgres')
    host = os.getenv(f'{prefix}DB_HOST', 'postgres')
    name = os.getenv(f'{prefix}DB_NAME', 'postgres')

    return f'postgresql+psycopg2://{user}:{pwd}@{host}/{name}'


class Config:
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    SECRET_KEY = os.getenv('APP_SECRET_KEY', 'fa692e9c9fe0a1e22322ef87bb19f26b129d8c9b44b98')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', get_pg_uri())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', '0') == '1'


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', get_pg_uri('TEST_'))


LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {'format': '{levelname} {asctime} {module} {message}', 'style': '{'},
            'simple': {'format': '{levelname} {message}', 'style': '{'},
            'only_msg': {'format': '{message}', 'style': '{'},
        },
        'filters': {'exc_filter': {'()': 'app.utils.exceptions.ExceptionsLoggingFilter'}},
        'handlers': {'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'}},
        'loggers': {
            '': {'level': 'WARNING', 'handlers': ['console']},
            'app': {'level': LOG_LEVEL, 'handlers': ['console'], 'propagate': False},
            'app.utils.exceptions': {
                'level': LOG_LEVEL,
                'handlers': ['console'],
                'filters': ['exc_filter'],
                'propagate': False,
            },
            'huey.consumer': {'level': 'INFO', 'handlers': ['console'], 'propagate': False},
        },
    }
)
