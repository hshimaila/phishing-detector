"""
Database model for storing every scan result.

Why store scans?
1. Users can view their scan history
2. We can use flagged results to retrain the model later
3. Useful for analytics — what phishing patterns are most common?
"""

from datetime import datetime
from . import db


class ScanResult(db.Model):
    __tablename__ = "scan_results"

    id            = db.Column(db.Integer, primary_key=True)
    scan_type     = db.Column(db.String(10), nullable=False)   # "email" or "url"
    input_content = db.Column(db.Text, nullable=False)         # The scanned text/URL
    verdict       = db.Column(db.String(20), nullable=False)   # "phishing" or "safe"
    risk_score    = db.Column(db.Float, nullable=False)        # 0.0 to 1.0
    ml_score      = db.Column(db.Float)                        # Raw ML model score
    threat_intel_flagged = db.Column(db.Boolean, default=False) # Was it in PhishTank/GSB?
    signals       = db.Column(db.Text)                         # JSON string of detected signals
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for JSON responses."""
        import json
        return {
            "id":                   self.id,
            "scan_type":            self.scan_type,
            "input_content":        self.input_content[:200],  # Truncate for safety
            "verdict":              self.verdict,
            "risk_score":           round(self.risk_score, 3),
            "ml_score":             round(self.ml_score or 0, 3),
            "threat_intel_flagged": self.threat_intel_flagged,
            "signals":              json.loads(self.signals) if self.signals else [],
            "created_at":           self.created_at.isoformat(),
        }