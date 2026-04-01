import os
from pathlib import Path

# Project Roots
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DB_DIR = BASE_DIR / "data"
DB_FILE = DB_DIR / "terminal_data.db"

# Logs configuration
LOGS_DIR = BASE_DIR / "logs"
ENABLE_LOGGING = True

# Serial Defaults
DEFAULT_BAUDRATE = 115200

def ensure_directories():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    if ENABLE_LOGGING:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
