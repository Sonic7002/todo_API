# api/extensions.py
# Initialize Flask extensions

from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy database instance to be initialized in the app factory
db = SQLAlchemy()
