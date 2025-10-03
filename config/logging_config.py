# config/logging_config.py
import logging.config
from datetime import datetime
import os

# Crear directorio de logs si no existe
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(logs_dir, exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d - %(message)s'
        },
        'test': {
            'format': '%(asctime)s [%(levelname)s] TEST-%(name)s: %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(logs_dir, f"test_execution_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"),
            'formatter': 'detailed',
            'mode': 'w'  # Sobrescribir archivo en cada ejecución
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'test'
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'selenium': {  # Logger específico para selenium
            'handlers': ['file', 'console'],
            'level': 'WARNING',  # Solo mostrar warnings y errores de selenium
            'propagate': False
        },
        'urllib3': {  # Reducir ruido de requests HTTP
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}

def setup_logging():
    """Configura el sistema de logging global"""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized for MyBees Testing")
    return logger

def get_logger(name: str = None):
    """Obtiene un logger configurado para usar en los tests"""
    if name is None:
        name = __name__
    return logging.getLogger(name)