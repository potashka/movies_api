LOG_FORMAT = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
LOG_DEFAULT_HANDLERS = ['console']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {'default': {'format': LOG_FORMAT}},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'root': {'handlers': LOG_DEFAULT_HANDLERS, 'level': 'INFO'},
}
