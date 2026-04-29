"""
Configuration for different environments.

Development  → SQLite (no setup needed, file-based)
Production   → PostgreSQL (set DATABASE_URL env variable)
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env file

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Secret key for Flask sessions
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

    # SQLite database stored in backend/
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, '..', 'phishing_detector.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # External API keys (set in .env file)
    GOOGLE_SAFE_BROWSING_API_KEY = os.environ.get("GOOGLE_SAFE_BROWSING_API_KEY", "")
    PHISHTANK_API_KEY = os.environ.get("PHISHTANK_API_KEY", "")

    # Path to saved ML models
    MODELS_DIR = os.path.join(BASE_DIR, "..", "saved_models")

    # Risk score threshold: above this = phishing
    PHISHING_THRESHOLD = 0.5