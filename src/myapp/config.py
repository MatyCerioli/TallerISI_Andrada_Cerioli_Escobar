import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'app.db'}",
    )