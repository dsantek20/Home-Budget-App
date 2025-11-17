import logging
from logging.config import dictConfig
from pathlib import Path
from app_config import AppConfiguration
from common.middleware import crid_context


class CRIDFilter(logging.Filter):
    def filter(self, record):
        record.crid = crid_context.get('-')
        return True


def initialize_logging(config: AppConfiguration):
    log_file_path = Path(config.log_file_path) / config.log_file_name

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - [CRID: %(crid)s] - %(message)s"
            },
        },
        "filters": {
            "crid_filter": {
                "()": CRIDFilter,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "filters": ["crid_filter"],
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filters": ["crid_filter"],
                "filename": str(log_file_path),
                "mode": "a",
                "maxBytes": 10 * 1024 * 1024, 
                "backupCount": 5,  
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "fastapi": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "gunicorn.error": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "gunicorn.access": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
    }

    dictConfig(LOGGING_CONFIG)
