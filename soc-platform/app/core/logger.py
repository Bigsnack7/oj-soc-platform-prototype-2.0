import logging
from .config import settings


def setup_logging() -> logging.Logger:
    """Configure a simple application logger for console output."""

    logger = logging.getLogger("soc-platform")
    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level.upper())
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setLevel(settings.log_level.upper())
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = setup_logging()
