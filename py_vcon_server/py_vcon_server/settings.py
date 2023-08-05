import os
from pathlib import Path

VCON_STORAGE_TYPE = os.getenv("VCON_STORAGE_TYPE", "redis")
VCON_STORAGE_URL = os.getenv("STORAGE_URL", "redis://localhost")
STATE_DB_URL = os.getenv("STATE_DB_URL", "redis://localhost")
REST_URL = os.getenv("REST_URL", "http://localhost:8000")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOGGING_CONFIG_FILE = os.getenv("LOGGING_CONFIG_FILE", Path(__file__).parent / 'logging.conf')
LAUNCH_VCON_API = os.getenv("LAUNCH_VCON_API", True)
LAUNCH_ADMIN_API = os.getenv("LAUNCH_ADMIN_API", True)
NUM_WORKERS = os.getenv("NUM_WORKERS", os. cpu_count())

