import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
OUTPUT_DIR = BASE_DIR / "static" / "outputs"

APP_SECRET = os.getenv("MC_DTF_SECRET", "mc-dtf-pro-local-secret")
MAX_UPLOAD_MB = int(os.getenv("MC_DTF_MAX_UPLOAD_MB", "60"))
MAX_PIXELS = int(os.getenv("MC_DTF_MAX_PIXELS", str(9000 * 9000)))
AI_MAX_SIDE = int(os.getenv("MC_DTF_AI_MAX_SIDE", "1800"))
