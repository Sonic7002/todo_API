# api/auth/token.py
"""
JWT token utilities.

Provides methods to generate and decode JWT tokens using
the app's secret key and algorithm.
"""

import jwt
from datetime import datetime, timedelta
from flask import current_app


def generate_token(user_id: int) -> str:
    """
    Create a JWT token with user_id and expiry time.

    Expires after `JWT_EXP_SECONDS` defined in app config.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=current_app.config["JWT_EXP_SECONDS"])
    }
    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"]
    )


def decode_token(token: str):
    """
    Decode a JWT token and return its payload.

    Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError
    if the token is invalid or expired.
    """
    return jwt.decode(
        token,
        current_app.config["SECRET_KEY"],
        algorithms=[current_app.config["JWT_ALGORITHM"]]
    )
