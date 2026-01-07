import logging
import logging.handlers
import os
import sys
from pathlib import Path

def setup_logging():
    """Configure structured logging for the application"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Define log format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Console Handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    
    # Rotating File Handler
    # maxBytes=10MB, backupCount=5
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "agroai.log",
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    
    # Specific loggers for our modules to ensure they propagate
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    
    logging.info("📝 Logging initialized successfully")

# Get specific loggers
def get_logger(name: str):
    return logging.getLogger(name)
