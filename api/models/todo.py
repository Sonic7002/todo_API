# api/models/todo.py
# Defines the Todo model representing a single task in the todo-list.

from ..extensions import db
from .util import timelog  # function returning current timestamp as string

class Todo(db.Model):
    """
    Todo Model
    ----------
    Represents a single task in the Todo list system.

    Attributes:
        id (int): Primary key for the task.
        user_id (int): Foreign key linking the task to a specific user.
        title (str): Task title. Cannot be null.
        description (str, optional): Additional details about the task.
        status (str): Current state of the task ('todo' by default).
        created_at (str): Timestamp when the task was created. Defaults to timelog().
        updated_at (str): Timestamp when the task was last updated. Defaults to timelog().

    Methods:
        to_dict(): Returns a dictionary representation of the task.
        __repr__(): Developer-friendly string representation showing the task ID.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(255), default = None )
    description = db.Column(db.String())
    status = db.Column(db.String(), nullable=False, default='todo')
    created_at = db.Column(db.String(), nullable=False, default=timelog)
    updated_at = db.Column(db.String(), nullable=False, default=timelog)

    def to_dict(self):
        """Return a dict representation of the Todo instance."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        """Return a concise string for debugging."""
        return f"<Todo id={self.id} title={self.title}>"
