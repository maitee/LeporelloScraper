'''
Created on Mar 7, 2012

@author: simon
'''

LOGGING_CONFIG = {
    'version': 1, 
    'disable_existing_loggers': True, 
    
    'formatters': {
        'verbose': {
            'format': '%(levelname)s - (%(asctime)s) %(module)s [%(process)d %(thread)d]: %(message)s'
        }, 
        'simple': {
            'format': '%(levelname)s - %(module)s %(lineno)s: %(message)s'
        }
    }, 
           
    'handlers': {
        'console': {
            'level': 'DEBUG', 
            'class': 'logging.StreamHandler', 
            'formatter': 'simple'
        }, 
        'file': {
            'level': 'DEBUG', 
            'class': 'logging.FileHandler', 
            'filename': 'leporello.log', 
            'formatter': 'verbose'
        }, 
    }, 
           
    'loggers': {
        'leporello': {
            'handlers': ['console', 'file'], 
            'propagate': True, 
            'level': 'INFO'
        }, 
        'leporello.custom': {
            'handlers': ['console'], 
            'propagate': True, 
            'level': 'INFO'
        }
    }
}
        