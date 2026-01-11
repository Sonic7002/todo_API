# api/routes/todos.py
# Todo routes: create, update, delete, and retrieve tasks

from flask import jsonify, request, Blueprint
from ..models.todo import Todo
from ..models.util import timelog
from ..extensions import db
from ..auth.decorators import jwt_required

todo_bp = Blueprint('todos', __name__, url_prefix='/todos')

ALLOWED_STATUSES = {"todo", "inprogress", "done"}

# utility (for internal use)
def get_authenticated_user():
    """Helper to get authenticated user or return 401 response."""
    user = request.user
    if not user:
        return None, jsonify({"error": "unauthorized"}), 401
    return user, None, None

# POST: Add a new task
@todo_bp.route('/', methods=['POST'])
@jwt_required
def add_task():
    """
    Create a new todo task for the authenticated user.
    Expects JSON: { "title": str, "description": str (optional) }
    """
    user, resp, code = get_authenticated_user()
    if resp:
        return resp, code

    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    todo = Todo(
        title=data['title'],
        description=data.get('description', ''),
        user_id=user.id
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

# PUT: Update an existing task
@todo_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required
def update_task(task_id):
    """
    Update fields of a task: title, description, status.
    Status must be one of ALLOWED_STATUSES.
    """
    user, resp, code = get_authenticated_user()
    if resp:
        return resp, code

    data = request.get_json()
    if not data:
        return jsonify({"error": "no data provided"}), 400

    task = Todo.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        return jsonify({"error": "task not found"}), 404

    updated = False
    if "status" in data:
        if data["status"] not in ALLOWED_STATUSES:
            return jsonify({"error": "invalid status"}), 400
        task.status = data["status"]
        updated = True

    if "title" in data:
        task.title = data["title"]
        updated = True

    if "description" in data:
        task.description = data["description"]
        updated = True

    if not updated:
        return jsonify({"error": "no valid fields to update"}), 400

    task.updated_at = timelog()
    db.session.commit()
    return jsonify(task.to_dict()), 200

# DELETE: Delete a task
@todo_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required
def delete_task(task_id):
    """
    Delete a task belonging to the authenticated user.
    """
    user, resp, code = get_authenticated_user()
    if resp:
        return resp, code

    task = Todo.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        return jsonify({"error": "task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify(task.to_dict()), 200

# GET: Retrieve all tasks
@todo_bp.route('/', methods=['GET'])
@jwt_required
def get_all_tasks():
    """
    Retrieve all tasks of the authenticated user.
    """
    user, resp, code = get_authenticated_user()
    if resp:
        return resp, code

    tasks = Todo.query.filter_by(user_id=user.id).all()
    return jsonify([task.to_dict() for task in tasks]), 200

# GET: Retrieve tasks by status
@todo_bp.route('/<status>', methods=['GET'])
@jwt_required
def get_tasks_by_status(status):
    """
    Retrieve tasks of the authenticated user filtered by status.
    Status must be one of ALLOWED_STATUSES.
    """
    user, resp, code = get_authenticated_user()
    if resp:
        return resp, code

    if status not in ALLOWED_STATUSES:
        return jsonify({"error": "invalid status"}), 400

    tasks = Todo.query.filter_by(user_id=user.id, status=status).all()
    return jsonify([task.to_dict() for task in tasks]), 200
