"""
Google Safe Browsing API

Checks if a URL is in Google's database of known phishing/malware sites.
Updated constantly by Google's security team — very reliable.

Docs: https://developers.google.com/safe-browsing/v4/lookup-api
Free tier: 10,000 requests/day
"""

import requests
import logging
from flask import current_app

logger = logging.getLogger(__name__)

GSB_ENDPOINT = "https://safebrowsing.googleapis.com/v4/threatMatches:find"


def check_url(url: str) -> dict:
    """
    Check a URL against Google Safe Browsing.

    Returns:
        { "flagged": bool, "threat_type": str or None }
    """
    api_key = current_app.config.get("GOOGLE_SAFE_BROWSING_API_KEY", "")

    if not api_key:
        logger.warning("Google Safe Browsing API key not set — skipping check.")
        return {"flagged": False, "threat_type": None, "source": "google_safe_browsing", "skipped": True}

    payload = {
        "client": {"clientId": "phishing-detector", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    try:
        response = requests.post(
            f"{GSB_ENDPOINT}?key={api_key}",
            json=payload,
            timeout=5
        )
        data = response.json()

        if "matches" in data and data["matches"]:
            threat_type = data["matches"][0].get("threatType", "UNKNOWN")
            return {"flagged": True, "threat_type": threat_type, "source": "google_safe_browsing"}

        return {"flagged": False, "threat_type": None, "source": "google_safe_browsing"}

    except requests.Timeout:
        logger.warning("Google Safe Browsing API timed out.")
        return {"flagged": False, "threat_type": None, "source": "google_safe_browsing", "error": "timeout"}
    except Exception as e:
        logger.error(f"GSB API error: {e}")
        return {"flagged": False, "threat_type": None, "source": "google_safe_browsing", "error": str(e)}