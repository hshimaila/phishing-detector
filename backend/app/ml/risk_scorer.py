"""
Risk Scorer — The Final Judge

This combines:
  - ML model score (0.0 to 1.0)
  - Threat intelligence results (binary: flagged or not)
  - Rule-based signals (count of red flags)

Into a single weighted risk score and a plain-English verdict.

Why not just use the ML score alone?
Because a new phishing URL might not be in training data,
but IS in PhishTank. Combining sources = fewer misses.

Weight breakdown:
  ML Score:          50%  ← Most reliable for unknown patterns
  Threat Intel:      35%  ← Authoritative for known threats
  Rule-based bonus:  15%  ← Extra signal boost
"""


# Weights must sum to 1.0
WEIGHT_ML           = 0.50
WEIGHT_THREAT_INTEL = 0.35
WEIGHT_RULES        = 0.15


def compute_risk_score(
    ml_score: float,
    threat_intel_results: list,
    signal_count: int,
    max_signals: int = 8
) -> dict:
    """
    Compute a final weighted risk score.

    Args:
        ml_score:             Raw ML model probability (0.0 to 1.0)
        threat_intel_results: List of dicts from GSB/PhishTank checks
        signal_count:         Number of rule-based signals triggered
        max_signals:          Maximum possible signals (for normalization)

    Returns:
        {
            "risk_score": 0.84,
            "verdict": "phishing",
            "confidence": "high",
            "threat_intel_flagged": True,
            "explanation": "⚠️ This looks like a phishing attempt!"
        }
    """

    # --- Component 1: ML Score ---
    ml_component = ml_score * WEIGHT_ML

    # --- Component 2: Threat Intelligence ---
    # If ANY threat intel source flags it, that's a strong signal
    threat_flagged = any(r.get("flagged") for r in threat_intel_results)
    threat_score = 1.0 if threat_flagged else 0.0
    threat_component = threat_score * WEIGHT_THREAT_INTEL

    # --- Component 3: Rule-based signals ---
    rule_score = min(signal_count / max(max_signals, 1), 1.0)
    rule_component = rule_score * WEIGHT_RULES

    # --- Final Score ---
    final_score = ml_component + threat_component + rule_component
    final_score = round(min(final_score, 1.0), 4)

    # --- Verdict ---
    verdict, confidence, explanation = _get_verdict(final_score, threat_flagged)

    return {
        "risk_score":           final_score,
        "verdict":              verdict,
        "confidence":           confidence,
        "threat_intel_flagged": threat_flagged,
        "explanation":          explanation,
        "score_breakdown": {
            "ml_contribution":           round(ml_component, 3),
            "threat_intel_contribution": round(threat_component, 3),
            "rules_contribution":        round(rule_component, 3),
        }
    }


def _get_verdict(score: float, threat_flagged: bool) -> tuple:
    """
    Convert a numeric score into a verdict, confidence level, and user message.

    Thresholds:
        0.0 – 0.3  → Safe (low risk)
        0.3 – 0.6  → Suspicious (medium risk)
        0.6 – 1.0  → Phishing (high risk)

    If threat intel flagged it, always verdict = phishing regardless of score.
    """

    if threat_flagged:
        return (
            "phishing",
            "high",
            "🚨 This URL is in a known phishing database. Do NOT proceed!"
        )

    if score >= 0.6:
        return (
            "phishing",
            "high" if score >= 0.8 else "medium",
            "⚠️ This looks like a phishing attempt! Treat with extreme caution."
        )
    elif score >= 0.3:
        return (
            "suspicious",
            "medium",
            "🟡 This looks suspicious. Proceed with caution and verify the source."
        )
    else:
        return (
            "safe",
            "high" if score <= 0.1 else "medium",
            "✅ This appears to be safe. No major threats detected."
        )