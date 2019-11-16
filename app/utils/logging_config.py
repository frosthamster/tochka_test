import logging.config
import os

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
