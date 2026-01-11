# api/__init__.py
# Flask app factory and initial configuration

import os
from flask import Flask
from api.extensions import db

def create_app():
    """
    Create and configure the Flask app instance.
    Initializes database, registers blueprints, and sets JWT config.
    """
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Security / JWT configuration
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret-change-this")
    app.config['JWT_ALGORITHM'] = "HS256"
    app.config['JWT_EXP_SECONDS'] = 3600  # 1 hour token expiry

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from api.routes.todos import todo_bp
    app.register_blueprint(todo_bp, url_prefix='/todos')

    from api.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
