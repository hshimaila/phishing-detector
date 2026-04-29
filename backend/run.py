"""
Flask App Entry Point

Run with: python run.py
"""

from app import create_app

app = create_app()


@app.route("/api/health", methods=["GET"])
def health():
    """Health check — useful for Docker and deployment monitoring."""
    from app.ml.model_loader import get_email_model, get_url_model
    email_model, _ = get_email_model()
    url_model, _   = get_url_model()

    return {
        "status": "ok",
        "models": {
            "email_model_loaded": email_model is not None,
            "url_model_loaded":   url_model is not None,
        }
    }, 200


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)