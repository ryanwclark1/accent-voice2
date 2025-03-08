# accent_auth/logging_config.py
import logging.config

from .config.app import settings  # Import app settings


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": settings.log_level,  # Use setting here
        },
        "file": {  # Add a file handler
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "level": settings.log_level,  # Use setting here
            "filename": settings.log_filename,  # Use setting
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,  # Keep 5 backup files
        },
    },
    "root": {
        "handlers": ["console", "file"],  # Log to console AND file
        "level": settings.log_level,  # Use setting here
    },
    "loggers": {
        "sqlalchemy": {"level": "WARN"},
        "alembic": {"level": "INFO"},
        "accent": {"level": "DEBUG"},  # Added to debug
    },
}


def configure_logging():
    """Load logging configuration"""
    logging.config.dictConfig(LOGGING_CONFIG)
