"""Konfigurasi aplikasi. Nilai rahasia dibaca dari environment (.env), bukan ditulis di kode."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-ganti-di-produksi")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'portlink.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PRODUCTS_PER_PAGE = 9
    LOG_DIR = BASE_DIR / "logs"
    UPLOAD_DIR = BASE_DIR / "instance" / "uploads"            # bukti pembayaran (di luar folder static)
    MAX_PROOF_BYTES = 10 * 1024 * 1024                         # batas bukti pembayaran: 10 MB
    MAX_CONTENT_LENGTH = MAX_PROOF_BYTES + 1024 * 1024         # batas keras ukuran request


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
