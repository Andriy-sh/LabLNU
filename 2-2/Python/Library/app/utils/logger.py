import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logger(log_level_str: Optional[str] = "INFO") -> logging.Logger:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    logger = logging.getLogger("library_app")
    logger.setLevel(log_level)

    logger.handlers.clear()

    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(log_level)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(file_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger