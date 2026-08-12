import os

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


class Config:
    # ============================================================
    # Flask Security
    # ============================================================

    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY environment variable is not configured."
        )

    # ============================================================
    # Session Security
    # ============================================================

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"

    # ============================================================
    # Application
    # ============================================================

    TESTING = False
