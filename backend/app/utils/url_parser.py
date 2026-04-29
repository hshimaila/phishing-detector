"""
URL Feature Extractor

Instead of treating a URL as raw text, we extract structured features from it.
The ML model then learns which combinations of features indicate phishing.

Why features instead of raw text?
Because "paypa1.suspicious-login.tk/verify?user=john" and
"paypa1.evil-site.ml/account/confirm" share structural patterns,
not just words.
"""

import re
from urllib.parse import urlparse


# Known legitimate TLDs vs suspicious ones
SUSPICIOUS_TLDS = {'.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click'}
TRUSTED_DOMAINS = {'google.com', 'microsoft.com', 'apple.com', 'amazon.com', 'paypal.com'}


def extract_url_features(url: str) -> dict:
    """
    Extracts a feature vector from a URL.
    
    Each feature is a numerical value the ML model can learn from.
    
    Example:
        Input:  "http://paypa1.verify-account.tk/login?redirect=http://evil.com"
        Output: {url_length: 58, num_dots: 3, has_ip: 0, ...}
    """
    features = {}

    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        query = parsed.query
    except Exception:
        # Return all-zero features for unparseable URLs
        return {k: 0 for k in _get_feature_names()}

    # --- Length-based features ---
    # Phishing URLs tend to be longer to hide the real domain
    features["url_length"] = len(url)
    features["domain_length"] = len(domain)
    features["path_length"] = len(path)

    # --- Dot count ---
    # Many subdomains = suspicious (e.g., login.verify.paypal.fake.tk)
    features["num_dots"] = url.count(".")
    features["num_subdomains"] = max(len(domain.split(".")) - 2, 0)

    # --- Special character counts ---
    # Phishing URLs often use @, -, _ to disguise domains
    features["num_hyphens"] = url.count("-")
    features["num_underscores"] = url.count("_")
    features["num_at_signs"] = url.count("@")  # @ redirects to different domain
    features["num_slashes"] = url.count("/")
    features["num_query_params"] = len(query.split("&")) if query else 0

    # --- Suspicious patterns ---
    features["has_ip_address"] = int(bool(re.match(
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain
    )))  # IPs instead of domain names are suspicious

    features["has_https"] = int(parsed.scheme == "https")  # No HTTPS = risky

    features["has_suspicious_tld"] = int(any(
        domain.endswith(tld) for tld in SUSPICIOUS_TLDS
    ))

    # --- Keyword signals ---
    url_lower = url.lower()
    features["has_login_keyword"] = int(any(
        w in url_lower for w in ["login", "signin", "verify", "account", "secure", "update", "confirm"]
    ))
    features["has_brand_in_subdomain"] = int(any(
        brand in domain.lower() and not domain.lower().endswith(f".{brand}.com")
        for brand in ["paypal", "google", "amazon", "apple", "microsoft", "netflix"]
    ))

    # --- Encoding tricks ---
    features["has_hex_encoding"] = int("%" in url)
    features["has_double_slash"] = int("//" in path)

    # --- Redirect signals ---
    features["has_redirect"] = int(
        "redirect" in url_lower or "url=" in url_lower or "return=" in url_lower
    )

    return features


def _get_feature_names():
    """Returns list of all feature names (used for fallback empty dict)."""
    return [
        "url_length", "domain_length", "path_length", "num_dots",
        "num_subdomains", "num_hyphens", "num_underscores", "num_at_signs",
        "num_slashes", "num_query_params", "has_ip_address", "has_https",
        "has_suspicious_tld", "has_login_keyword", "has_brand_in_subdomain",
        "has_hex_encoding", "has_double_slash", "has_redirect"
    ]