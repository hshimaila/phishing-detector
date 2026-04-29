"""
Scan History Endpoint

GET /api/history           → Last 50 scans
GET /api/history?type=url  → Filter by type
GET /api/history/<id>      → Single scan detail
"""

from flask import Blueprint, request, jsonify
from ..models.scan_result import ScanResult

history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
def get_history():
    scan_type = request.args.get("type")  # optional filter: "email" or "url"
    limit = min(int(request.args.get("limit", 50)), 100)

    query = ScanResult.query.order_by(ScanResult.created_at.desc())
    if scan_type in ("email", "url"):
        query = query.filter_by(scan_type=scan_type)

    scans = query.limit(limit).all()
    return jsonify({
        "scans": [s.to_dict() for s in scans],
        "count": len(scans)
    }), 200


@history_bp.route("/history/<int:scan_id>", methods=["GET"])
def get_scan(scan_id):
    scan = ScanResult.query.get_or_404(scan_id)
    return jsonify(scan.to_dict()), 200


@history_bp.route("/history/<int:scan_id>", methods=["DELETE"])
def delete_scan(scan_id):
    scan = ScanResult.query.get_or_404(scan_id)
    from ..models import db
    db.session.delete(scan)
    db.session.commit()
    return jsonify({"message": f"Scan {scan_id} deleted."}), 200