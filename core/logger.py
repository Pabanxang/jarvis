import logging
import sys
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Create a custom logger
logger = logging.getLogger("Jarvis")
logger.setLevel(logging.DEBUG)

# Format for log messages
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

# File handler (logs to file)
file_handler = logging.FileHandler(LOG_DIR / "jarvis.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Console handler (logs to console)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Add handlers to the logger
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)