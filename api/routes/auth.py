# api/routes/auth.py
# Authentication routes for user registration and login

from sqlalchemy.exc import IntegrityError
from flask import jsonify, request, Blueprint
from ..models.user import User
from ..extensions import db
from ..auth.token import generate_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    Expects JSON: { "username": str, "email": str, "password": str }
    Returns user info on success or error message on failure.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data received"}), 400

    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "username, email, and password are required"}), 400

    if len(data["password"]) < 8:
        return jsonify({"error": "password must contain at least 8 characters"}), 400

    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "email or username already registered"}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login an existing user.

    Expects JSON: { "email": str, "password": str }
    Returns JWT token and user info on success or error message on failure.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data received"}), 400

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({"error": "invalid credentials"}), 401

    token = generate_token(user.id)

    return jsonify({
        "token": token,
        "user": user.to_dict()
    })
