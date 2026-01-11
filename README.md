# Todo API (Flask)

A RESTful Todo List API with user authentication and per-user task ownership.

## Tech Stack
- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- JWT Authentication
- Passlib (bcrypt)

## Features
- User registration & login
- JWT-based authentication
- Per-user todo ownership
- Task status management (todo / inprogress / done)
- Secure password hashing

## Setup Instructions

1. Clone the repo
2. Create virtual environment
3. Install dependencies
4. Run the server

## Authentication Flow

- User logs in and receives a JWT access token
- Token is sent in `Authorization: Bearer <token>`
- Backend verifies token on every request

## API Endpoints

### Auth
```js
POST /auth/register  
POST /auth/login  
```

### Todos
```js
GET /todos  
POST /todos  
PUT /todos/<id>  
DELETE /todos/<id>
```