"""
PhishTank API

Community-verified phishing URL database.
Anyone can submit and verify phishing URLs.
Very comprehensive for known phishing campaigns.

Free API — just register at phishtank.com for a key.
"""

import requests
import logging

logger = logging.getLogger(__name__)

PHISHTANK_ENDPOINT = "https://checkurl.phishtank.com/checkurl/"


def check_url(url: str) -> dict:
    """
    Check if a URL is in PhishTank's verified phishing database.

    Returns:
        { "flagged": bool, "verified": bool, "source": "phishtank" }
    """
    try:
        from flask import current_app
        api_key = current_app.config.get("PHISHTANK_API_KEY", "")
    except RuntimeError:
        api_key = ""

    headers = {"User-Agent": "phishing-detector/1.0"}
    payload = {"url": url, "format": "json"}
    if api_key:
        payload["app_key"] = api_key

    try:
        response = requests.post(
            PHISHTANK_ENDPOINT,
            data=payload,
            headers=headers,
            timeout=5
        )
        data = response.json()

        results = data.get("results", {})
        in_database = results.get("in_database", False)
        verified = results.get("verified", False)

        return {
            "flagged":  in_database and verified,
            "verified": verified,
            "source":   "phishtank"
        }

    except requests.Timeout:
        logger.warning("PhishTank API timed out.")
        return {"flagged": False, "verified": False, "source": "phishtank", "error": "timeout"}
    except Exception as e:
        logger.error(f"PhishTank API error: {e}")
        return {"flagged": False, "verified": False, "source": "phishtank", "error": str(e)}