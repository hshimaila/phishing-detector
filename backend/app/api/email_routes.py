"""
Email Scan API Endpoint

POST /api/scan/email
Body: { "text": "email content here" }

Response:
{
    "verdict": "phishing",
    "risk_score": 0.87,
    "confidence": "high",
    "explanation": "⚠️ This looks like a phishing attempt!",
    "signals": ["Urgency language detected", "..."],
    "scan_id": 42
}
"""

from flask import Blueprint, request, jsonify
from ..ml.email_classifier import classify_email
from ..ml.risk_scorer import compute_risk_score
from ..models import db
from ..models.scan_result import ScanResult
import json

email_bp = Blueprint("email", __name__)


@email_bp.route("/scan/email", methods=["POST"])
def scan_email():
    # --- Input Validation ---
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field in request body"}), 400

    text = data["text"].strip()
    if len(text) < 10:
        return jsonify({"error": "Email text too short to analyze"}), 400
    if len(text) > 50000:
        return jsonify({"error": "Email text too long (max 50,000 chars)"}), 400

    # --- ML Classification ---
    ml_result = classify_email(text)
    ml_score = ml_result["score"]
    signals = ml_result["signals"]

    # --- Risk Scoring (no threat intel for emails — just ML + rules) ---
    result = compute_risk_score(
        ml_score=ml_score,
        threat_intel_results=[],    # Email threat intel not implemented yet
        signal_count=len(signals),
        max_signals=8
    )

    # --- Save to Database ---
    scan = ScanResult(
        scan_type="email",
        input_content=text[:500],
        verdict=result["verdict"],
        risk_score=result["risk_score"],
        ml_score=ml_score,
        threat_intel_flagged=False,
        signals=json.dumps(signals)
    )
    db.session.add(scan)
    db.session.commit()

    return jsonify({
        **result,
        "ml_score":  round(ml_score, 3),
        "signals":   signals,
        "scan_id":   scan.id,
        "scan_type": "email"
    }), 200