# api/models/user.py
# Defines the User model representing a registered user.

from passlib.hash import bcrypt
from ..extensions import db
from .util import timelog

class User(db.Model):
    """
    User Model
    ----------
    Represents a registered user in the system.

    Attributes:
        id (int): Primary key for the user.
        username (str): Unique username for login.
        email (str): Unique email address.
        password_hash (str): Hashed password.
        created_at (str): Timestamp when the user was created. Defaults to timelog().
        todos (list[Todo]): One-to-many relationship to Todo tasks.

    Methods:
        to_dict(): Returns a dictionary representation of the user (excluding password).
        set_password(password): Hashes and stores the password.
        check_password(password): Verifies a plain password against the hash.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.String(), nullable=False, default=timelog)
    todos = db.relationship("Todo", backref="user", lazy=True)

    def to_dict(self):
        """Return a dict representation of the user (without password)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at
        }

    def set_password(self, password: str):
        """Hash and store the user's password."""
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a plain password against the stored hash."""
        return bcrypt.verify(password, self.password_hash)

    def __repr__(self):
        """Return a concise string for debugging."""
        return f"<User id={self.id} username={self.username}>"
