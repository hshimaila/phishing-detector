"""
Flask App Factory Pattern

Why factory pattern?
Instead of creating the app globally (common in tutorials),
we use a function that CREATES the app. This makes testing
easier — you can create separate app instances for tests.
"""

from flask import Flask
from flask_cors import CORS
from .config import Config
from .models import db


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Enable CORS so React (running on port 3000) can talk to Flask (port 5000)
    # Without this, the browser will block all API requests
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize database
    db.init_app(app)

    # Register all route blueprints
    from .api.email_routes import email_bp
    from .api.url_routes import url_bp
    from .api.history_routes import history_bp

    app.register_blueprint(email_bp, url_prefix="/api")
    app.register_blueprint(url_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")

    # Create DB tables if they don't exist
    with app.app_context():
        db.create_all()

    return app