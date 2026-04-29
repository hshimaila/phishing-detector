"""
Email Classifier — Inference

This is the "prediction" side. Training is done offline.
Here we just load the trained model and use it.

Input:  Raw email string
Output: { score: float, signals: list }
"""

import scipy.sparse as sp
import numpy as np
import logging

logger = logging.getLogger(__name__)


def classify_email(text: str) -> dict:
    """
    Run the email through the NLP pipeline and return a phishing score.

    Returns:
        {
            "score": 0.87,           # 0.0 (safe) to 1.0 (phishing)
            "signals": [             # Human-readable reasons
                "Urgency language detected",
                "Credential harvesting attempt",
            ]
        }
    """
    try:
        from .model_loader import get_email_model
        from ..utils.text_cleaner import clean_text, extract_phishing_signals

        model, tfidf = get_email_model()

        # Model not available — fallback to rule-based only
        if model is None:
            return _rule_based_fallback(text)

        # Step 1: Clean and vectorize
        cleaned = clean_text(text)
        tfidf_features = tfidf.transform([cleaned])

        # Step 2: Extract phishing signals
        raw_signals = extract_phishing_signals(text)
        signals_array = sp.csr_matrix(
            np.array(list(raw_signals.values())).reshape(1, -1)
        )

        # Step 3: Combine features
        features = sp.hstack([tfidf_features, signals_array])

        # Step 4: Predict
        score = float(model.predict_proba(features)[0][1])

        # Step 5: Convert raw signal flags to human-readable strings
        readable_signals = _signals_to_text(raw_signals)

        return {"score": score, "signals": readable_signals}

    except Exception as e:
        logger.error(f"Email classification error: {e}")
        return {"score": 0.5, "signals": ["Classification error — manual review recommended"]}


def _signals_to_text(signals: dict) -> list:
    """Convert the binary signal dict into plain-English warnings."""
    messages = []
    if signals.get("has_urgency"):
        messages.append("⚡ Urgency language detected (e.g. 'act now', 'expires')")
    if signals.get("has_threat"):
        messages.append("⚠️ Threatening language detected (e.g. 'account suspended')")
    if signals.get("has_money_bait"):
        messages.append("💰 Prize or money bait detected")
    if signals.get("has_credential_ask"):
        messages.append("🔑 Credential harvesting attempt (asking for password/SSN)")
    if signals.get("has_impersonation"):
        messages.append("🎭 Possible brand impersonation (PayPal, Amazon, etc.)")
    if signals.get("has_url"):
        messages.append("🔗 Suspicious link or 'click here' detected")
    if signals.get("exclamation_count", 0) >= 3:
        messages.append("❗ Excessive punctuation (common in phishing)")
    if signals.get("caps_ratio", 0) > 0.3:
        messages.append("🔠 Excessive capitalization")
    return messages


def _rule_based_fallback(text: str) -> dict:
    """
    If the ML model isn't loaded, use pure rules.
    Less accurate, but better than nothing.
    """
    from ..utils.text_cleaner import extract_phishing_signals
    signals = extract_phishing_signals(text)
    signal_count = sum([
        signals["has_urgency"],
        signals["has_threat"],
        signals["has_money_bait"],
        signals["has_credential_ask"],
        signals["has_impersonation"],
    ])
    score = min(signal_count / 5.0, 1.0)
    return {"score": score, "signals": _signals_to_text(signals)}