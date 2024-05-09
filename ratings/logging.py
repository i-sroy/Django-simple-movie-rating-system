LOGGING = {
    'version': 1,
    'disable_exising_loggers': False,
    'formatters':{
        'standard': {
            'format':'%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level':'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'filters': [],

        }
    },
    'loggers' : {
        logger_name: {
            'level' : 'WARNING',
            'propagate' : True,
        } for logger_name in ('django', 'django.requests', 'django.db.backends', 'django.templates','core')
    },
    'root' : {
        'level' : 'DEBUG',
        'handlers' : ['console']

    }
}