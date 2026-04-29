"""
URL Classifier — Inference

Input:  Raw URL string
Output: { score: float, signals: list }
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def classify_url(url: str) -> dict:
    """
    Extract URL features and predict phishing probability.

    Returns:
        {
            "score": 0.92,
            "signals": ["Suspicious TLD (.tk)", "IP address used as domain"]
        }
    """
    try:
        from .model_loader import get_url_model
        from ..utils.url_parser import extract_url_features

        model, feature_names = get_url_model()
        features = extract_url_features(url)

        if model is None:
            return _rule_based_url_fallback(features)

        # Build feature DataFrame (must match training column order)
        X = pd.DataFrame([features])
        for col in feature_names:
            if col not in X.columns:
                X[col] = 0
        X = X[feature_names].fillna(0)

        # Predict
        score = float(model.predict_proba(X)[0][1])
        signals = _features_to_signals(features)

        return {"score": score, "signals": signals}

    except Exception as e:
        logger.error(f"URL classification error: {e}")
        return {"score": 0.5, "signals": ["URL classification error"]}


def _features_to_signals(features: dict) -> list:
    """Convert URL feature dict into human-readable warnings."""
    signals = []
    if features.get("has_ip_address"):
        signals.append("🔢 IP address used instead of domain name")
    if features.get("has_suspicious_tld"):
        signals.append("🌐 Suspicious top-level domain (.tk, .ml, .xyz, etc.)")
    if features.get("has_brand_in_subdomain"):
        signals.append("🎭 Trusted brand name in subdomain (possible impersonation)")
    if features.get("num_subdomains", 0) >= 3:
        signals.append("🔗 Excessive subdomains (common in phishing)")
    if not features.get("has_https"):
        signals.append("🔓 No HTTPS — connection is not encrypted")
    if features.get("has_login_keyword"):
        signals.append("🔑 Login/verify keyword in URL")
    if features.get("url_length", 0) > 75:
        signals.append("📏 Unusually long URL (often used to hide true destination)")
    if features.get("has_redirect"):
        signals.append("↩️  URL contains redirect parameter")
    if features.get("num_hyphens", 0) >= 3:
        signals.append("➖ Multiple hyphens (common in lookalike domains)")
    if features.get("has_hex_encoding"):
        signals.append("🔒 Hex-encoded characters detected")
    return signals


def _rule_based_url_fallback(features: dict) -> dict:
    """Pure rule-based scoring if model isn't loaded."""
    score = 0.0
    if features.get("has_ip_address"):       score += 0.3
    if features.get("has_suspicious_tld"):   score += 0.25
    if not features.get("has_https"):        score += 0.15
    if features.get("has_brand_in_subdomain"): score += 0.2
    if features.get("has_login_keyword"):    score += 0.1
    score = min(score, 1.0)
    return {"score": score, "signals": _features_to_signals(features)}