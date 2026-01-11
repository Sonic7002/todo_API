# api/auth/decorators.py
"""
JWT authentication decorator.

Verifies Bearer token from Authorization header,
decodes it, fetches the user, and attaches the user
object to the request.
"""

from functools import wraps
from flask import request, jsonify
from jwt import ExpiredSignatureError, InvalidTokenError

from .token import decode_token
from ..models.user import User


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")

        # Expect: Authorization: Bearer <token>
        if not auth or not auth.startswith("Bearer "):
            return jsonify({"error": "missing or invalid token"}), 401

        token = auth.split()[1]

        try:
            payload = decode_token(token)
        except ExpiredSignatureError:
            return jsonify({"error": "token expired"}), 401
        except InvalidTokenError:
            return jsonify({"error": "invalid token"}), 401

        user = User.query.get(payload.get("user_id"))
        if not user:
            return jsonify({"error": "user not found"}), 401

        # Attach authenticated user to request context
        request.user = user

        return fn(*args, **kwargs)

    return wrapper
