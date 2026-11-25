import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "conversas.db"))
AUDIO_MAX_SEGUNDOS = int(os.getenv("AUDIO_MAX_SEGUNDOS", "300"))
# Limite de download de arquivos imposto pela API de bots do Telegram.
AUDIO_MAX_BYTES = 20 * 1024 * 1024
CBO_DATA_DIR =Path(os.getenv("CBO_DATA_DIR", str(BASE_DIR.parent / "big_data" / "data" / "processed")))
