"""
Singleton Model Loader

Models are loaded ONCE when Flask starts, then reused for every request.
Loading a model takes ~0.5 seconds. If we loaded it per request,
the API would be unbearably slow.

Pattern: We use a module-level dictionary as a simple singleton cache.
"""

import os
import joblib
import logging

logger = logging.getLogger(__name__)

# Global cache — models live here after first load
_model_cache = {}


def get_email_model():
    """Returns the (model, tfidf_vectorizer) tuple, loading from disk if needed."""
    if "email" not in _model_cache:
        _model_cache["email"] = _load_email_model()
    return _model_cache["email"]


def get_url_model():
    """Returns the (model, feature_names) tuple, loading from disk if needed."""
    if "url" not in _model_cache:
        _model_cache["url"] = _load_url_model()
    return _model_cache["url"]


def _load_email_model():
    from flask import current_app
    models_dir = current_app.config["MODELS_DIR"]

    model_path = os.path.join(models_dir, "email_model.pkl")
    tfidf_path = os.path.join(models_dir, "email_tfidf.pkl")

    if not os.path.exists(model_path):
        logger.warning("⚠️  Email model not found. Run train_email_model.py first.")
        return None, None

    model = joblib.load(model_path)
    tfidf = joblib.load(tfidf_path)
    logger.info("✅ Email model loaded.")
    return model, tfidf


def _load_url_model():
    from flask import current_app
    models_dir = current_app.config["MODELS_DIR"]

    model_path = os.path.join(models_dir, "url_model.pkl")
    names_path = os.path.join(models_dir, "url_feature_names.pkl")

    if not os.path.exists(model_path):
        logger.warning("⚠️  URL model not found. Run train_url_model.py first.")
        return None, None

    model = joblib.load(model_path)
    feature_names = joblib.load(names_path)
    logger.info("✅ URL model loaded.")
    return model, feature_names