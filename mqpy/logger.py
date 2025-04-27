"""Logging configuration for the MqPy application.

This module provides a centralized logging configuration for the entire application.
Import this module instead of directly importing the logging module to ensure consistent
logging behavior across the application.
"""

from __future__ import annotations

import logging
import sys


def get_logger(name: str, level: int | None = None) -> logging.Logger:
    """Get a logger with the specified name and level.

    Args:
        name (str): The name of the logger, typically __name__.
        level (int | None): The logging level. Defaults to INFO if None.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)

    # Only configure the logger if it doesn't already have handlers
    if not logger.handlers:
        # Set default level if not specified
        if level is None:
            level = logging.INFO

        logger.setLevel(level)

        # Create console handler with a specific format
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


# Configure the root logger
root_logger = logging.getLogger()
if not root_logger.handlers:
    root_logger.setLevel(logging.WARNING)
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
