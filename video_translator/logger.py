"""Logging configuration for Video Translator application.

This module sets up structured logging with appropriate formatting and handlers
for both console and file output.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "video_translator",
    level: str = "INFO",
    log_file: Optional[Path] = None,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """Configure and return a logger instance.

    This function creates a logger with console output and optional file output.
    The logger uses a structured format with timestamps, log levels, and messages.

    Args:
        name: Logger name (typically the module name)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to a log file for persistent logging
        log_format: Optional custom log format string

    Returns:
        Configured Logger instance

    Example:
        >>> logger = setup_logger("my_module", "DEBUG")
        >>> logger.info("Application started")
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Default log format
    if log_format is None:
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(message)s"
        )

    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)  # Always log DEBUG level to file
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Create default logger instance
logger = setup_logger()


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module.

    This is a convenience function to get loggers with consistent configuration
    throughout the application.

    Args:
        name: Name for the logger (typically __name__ from the calling module)

    Returns:
        Logger instance

    Example:
        >>> from video_translator.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Module loaded")
    """
    return logging.getLogger(name)
