"""
Centralized logging configuration for the Google ADK Multi-Agent system.

This module provides a standardized logging setup that configures both
file and console logging based on environment variables.
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import datetime

# Default values
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_PATH = "logs"

def get_logger(name, log_level=None, log_path=None):
    """
    Get a configured logger instance.
    
    Args:
        name (str): Name of the logger, typically __name__ of the calling module
        log_level (str, optional): Override the LOG_LEVEL environment variable
        log_path (str, optional): Override the LOG_PATH environment variable
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Read from environment or use provided values, falling back to defaults
    log_level = log_level or os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)
    log_path = log_path or os.environ.get("LOG_PATH", DEFAULT_LOG_PATH)
    
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        print(f"Invalid log level: {log_level}. Defaulting to INFO.")
        numeric_level = logging.INFO

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    
    # Clear existing handlers if any
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    try:
        # Ensure log directory exists
        log_dir = Path(log_path)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create timestamped log filename
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"{current_date}.log"
        
        # Set up rotating file handler (10MB max size, 5 backup files)
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.error(f"Failed to set up file logging: {e}")
        # Continue with just console logging
    
    return logger 