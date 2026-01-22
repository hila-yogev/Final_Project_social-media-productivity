"""
logger_config.py

Creates one standardized logger for the whole project.
- Logs to console (stdout)
- Logs to a file under outputs/logs/pipeline.log
- Avoids adding duplicate handlers when imported in multiple modules
"""

import logging                  # Built-in logging framework
import sys                      # Gives access to sys.stdout
from pathlib import Path         # OS-independent path handling

from src.social_media_productivity.constants import LOGS_DIR  # Centralized logs directory path

# Default location of the log file: outputs/logs/pipeline.log
DEFAULT_LOG_FILE: Path = LOGS_DIR / "pipeline.log"


def setup_logger(
    name: str = "social_media_productivity",   # Logger name (same name -> same logger shared across modules)
    log_file: Path = DEFAULT_LOG_FILE,         # Where to save logs on disk
) -> logging.Logger:
    """
    Create (or retrieve) a configured logger.

    Returns a logger that writes:
    1) to the console, and
    2) to a file (log_file)

    If this logger was already configured earlier (handlers exist),
    it returns the existing logger to prevent duplicated output.
    """

    # Get the logger object by name (same name returns the same logger instance)
    logger = logging.getLogger(name)

    # Set the minimum log level that will be handled (INFO and above)
    logger.setLevel(logging.INFO)

    # Prevent the message from being sent to ancestor loggers (avoids duplicates in some setups)
    logger.propagate = False

    # If handlers already exist, this logger was configured before -> return it as-is
    if logger.handlers:
        return logger

    # Format of each log line
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    # --- Console handler: print logs to stdout ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # --- File handler: write logs to a file ---
    try:
        # Ensure the directory (outputs/logs) exists
        log_file.parent.mkdir(parents=True, exist_ok=True)

        # Create a handler that overwrites the file each run (mode="w")
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    except Exception as e:
        # If file logging fails, we still want the program to run (console logging still works)
        logger.warning(f"Could not create log file at {log_file}. Error: {e}")

    return logger
