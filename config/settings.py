"""Configuración general del proyecto Proper MKT."""

import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/proper_mkt")

# yt-dlp path
YT_DLP_PATH = os.getenv("YT_DLP_PATH", "yt-dlp")

# Flask
FLASK_PORT = int(os.getenv("PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

# Plataformas soportadas
PLATFORMS = ["tiktok", "instagram"]

# Perfiles a monitorear
MONITORED_PROFILES = [
    {"platform": "instagram", "username": "decatecainversion", "is_competitor": True},
    {"platform": "instagram", "username": "capitalizarme", "is_competitor": True},
    {"platform": "instagram", "username": "100ladrillos", "is_competitor": True},
    {"platform": "tiktok", "username": "capitalizarme.com", "is_competitor": True},
    {"platform": "instagram", "username": "proper.inversion", "is_competitor": False},
]

# Scheduler
SCHEDULER_HOUR = int(os.getenv("SCHEDULER_HOUR", 7))
SCHEDULER_MINUTE = int(os.getenv("SCHEDULER_MINUTE", 0))

# Directorios
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
