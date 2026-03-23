import logging
import os
from logging.config import dictConfig


def configure_logging() -> None:
    """
    Basic structured-ish logging config suitable for local dev.

    Note: production-grade observability (tracing, JSON logs, etc.) can be added later.
    """

    log_level = os.getenv("HEALTH_LOG_LEVEL", "INFO").upper()

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                }
            },
            "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},
            "root": {"handlers": ["console"], "level": log_level},
        }
    )

    # Ensure libraries inherit the configured root level.
    logging.getLogger("uvicorn").setLevel(log_level)

