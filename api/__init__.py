# api/__init__.py
# Flask app factory and initial configuration

import os
from flask import Flask
from .extensions import db
from dotenv import load_dotenv

load_dotenv()
def create_app():
    """
    Create and configure the Flask app instance.
    Initializes database, registers blueprints, and sets JWT config.
    """
    app = Flask(__name__)

    # App configuration
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("Fatal Error! Secret Key is missing.")
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = os.getenv("DEBUG", "False").lower() == "true"

    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("Fatal Error! Database URL is missing.")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Security / JWT configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        raise RuntimeError("Fatal Error! JWT Secret Key is missing.")
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ALGORITHM'] = os.getenv("JWT_ALGORITHM", "HS256")
    app.config['JWT_EXP_SECONDS'] = int(os.getenv("JWT_EXP_SECONDS", "3600"))  # 1 hour token expiry

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from .routes.todos import todo_bp
    app.register_blueprint(todo_bp, url_prefix='/todos')

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
