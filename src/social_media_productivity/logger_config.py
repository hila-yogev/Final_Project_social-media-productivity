"""
logger_config.py

Provides a single standardized logger for the whole project.
- Logs to console AND to a file under outputs/logs/
- Avoids duplicate handlers when imported by multiple modules
"""

import logging
import sys
from pathlib import Path

from src.social_media_productivity.constants import LOGS_DIR

DEFAULT_LOG_FILE: Path = LOGS_DIR / "pipeline.log"


def setup_logger(
    name: str = "social_media_productivity",
    log_file: Path = DEFAULT_LOG_FILE,
) -> logging.Logger:
    """
    Create (or retrieve) a configured logger.

    Parameters
    ----------
    name:
        Logger name. Using a stable name helps all modules share the same logger.
    log_file:
        Full path to the log file. Default: outputs/logs/pipeline.log

    Returns
    -------
    logging.Logger
        Configured logger with console + file handlers.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False  # prevents duplicate logs in some environments

    if logger.handlers:
        return logger  # already configured

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not create log file at {log_file}. Error: {e}")

    return logger
