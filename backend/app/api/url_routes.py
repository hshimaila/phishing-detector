"""
URL Scan API Endpoint

POST /api/scan/url
Body: { "url": "https://suspicious-site.tk/login" }
"""

from flask import Blueprint, request, jsonify
from ..ml.url_classifier import classify_url
from ..ml.risk_scorer import compute_risk_score
from ..threat_intel import google_safebrowsing, phishtank
from ..models import db
from ..models.scan_result import ScanResult
import json
import re

url_bp = Blueprint("url", __name__)

# Simple URL format validator
URL_PATTERN = re.compile(
    r'^(https?://)'          # must start with http:// or https://
    r'(\S+)'                 # followed by non-whitespace
    r'(\.[a-zA-Z]{2,})'     # must have a TLD
    , re.IGNORECASE
)


@url_bp.route("/scan/url", methods=["POST"])
def scan_url():
    # --- Input Validation ---
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' field in request body"}), 400

    url = data["url"].strip()

    # Auto-add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    if not URL_PATTERN.match(url):
        return jsonify({"error": "Invalid URL format"}), 400

    # --- ML Classification ---
    ml_result = classify_url(url)
    ml_score  = ml_result["score"]
    signals   = ml_result["signals"]

    # --- Threat Intelligence Checks (run in parallel ideally, sequential for simplicity) ---
    gsb_result      = google_safebrowsing.check_url(url)
    phishtank_result = phishtank.check_url(url)
    threat_results  = [gsb_result, phishtank_result]

    # Add threat intel source to signals if flagged
    if gsb_result.get("flagged"):
        signals.insert(0, f"🔴 Flagged by Google Safe Browsing ({gsb_result.get('threat_type', 'threat')})")
    if phishtank_result.get("flagged"):
        signals.insert(0, "🔴 Confirmed phishing URL in PhishTank database")

    # --- Risk Scoring ---
    result = compute_risk_score(
        ml_score=ml_score,
        threat_intel_results=threat_results,
        signal_count=len(signals),
        max_signals=10
    )

    # --- Save to Database ---
    scan = ScanResult(
        scan_type="url",
        input_content=url,
        verdict=result["verdict"],
        risk_score=result["risk_score"],
        ml_score=ml_score,
        threat_intel_flagged=result["threat_intel_flagged"],
        signals=json.dumps(signals)
    )
    db.session.add(scan)
    db.session.commit()

    return jsonify({
        **result,
        "ml_score":      round(ml_score, 3),
        "signals":       signals,
        "scan_id":       scan.id,
        "scan_type":     "url",
        "scanned_url":   url
    }), 200