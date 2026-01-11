# run.py
# Entry point to run the Flask Todo API

from api import create_app
from api.extensions import db

app = create_app()

# Ensure database tables are created before the first request
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # For development only; disable debug in production
    app.run(debug=True)
