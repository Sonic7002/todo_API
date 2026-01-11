# 📘 Todo API – Endpoint Documentation
## Base Information

**Base URL:** `/api`

**Authentication:** JWT (Bearer token)

**Content-Type:** `application/json`

**Authentication Header (Required for protected routes)**
`Authorization: Bearer <JWT_TOKEN>`

If this header is missing, malformed, expired, or invalid, the API will return:
```json
{
  "error": "unauthorized"
}
```

with status **401 Unauthorized.**

**⚠️ All errors are accompanied by a error message of the format:**
```json
{
  "error": "error message"
}
```

## 🔐 Authentication Endpoints
### Register User

POST `/auth/register`

Creates a new user account.

**Request Body**
{
  "username": "sonic",
  "email": "sonic@example.com",
  "password": "strongpassword"
}

Validation Rules

- **username**, **email**, **password** are required

- **password** must be at least 8 characters

- **email** and **username** must be unique

### Success Response

`201 Created`
```json
{
  "id": 1,
  "username": "sonic",
  "email": "sonic@example.com",
  "created_at": "14:21:10 10-01-2026"
}
```
### Error Responses

|Status|Reason|
|:---|:---|
|`400`|	Missing fields / weak password|
|`409`|	Email or username already registered|

### Login User

POST `/auth/login`

Authenticates a user and issues a JWT.

### Request Body
```json
{
  "email": "sonic@example.com",
  "password": "strongpassword"
}
```

### Success Response
`200 OK`
```json
{
  "token": "<jwt_token>",
  "user": {
    "id": 1,
    "username": "sonic",
    "email": "sonic@example.com"
  }
}
```

### Error Responses
|Status|	Reason|
|:---|:--|
|`400`|	Missing email or password|
|`401`|	Incorrect password|
|`404`|	User does not exist|

**⚠️ Token must be stored client-side (localStorage / memory / cookie depending on frontend strategy).**

## 📝 Todo Endpoints (Protected)

### All todo routes:

- Require valid JWT
- Operate only on the authenticated user’s data
- Will never return another user’s todos
---

### Create Todo

POST `/todos/`

Creates a new todo.

### Request Body
```json
{
  "title": "Study Flask",
  "description": "Finish JWT section"
}
```
### Success Response

`201 Created`
```json
{
  "id": 5,
  "title": "Study Flask",
  "description": "Finish JWT section",
  "status": "todo",
  "created_at": "14:30:00 10-01-2026",
  "updated_at": "14:30:00 10-01-2026"
}
```
### Error Responses
|Status|	Reason|
|:---|:---|
|`400`|	Missing title or description
|`401`|	Unauthorized
### Get All Todos

GET `/todos/`

Returns all todos belonging to the logged-in user.

### Success Response

`200 OK`
```json
[
  {
    "id": 1,
    "title": "Study Flask",
    "description": "Finish JWT section",
    "status": "todo"
  },
  {
    "id": 2,
    "title": "Push to GitHub",
    "status": "done"
  }
]
```

If user has no todos:
```json
[]
```

### Get Todos by Status
|Endpoint|	Description|
|:---|:---|
|GET `/todos/todo`|	Todos with status todo|
|GET `/todos/in-progress`|	Todos in progress|
|GET `/todos/done`|	Completed todos|

### Success Response

`200 OK`
```json
[
  {
    "id": 3,
    "title": "Write docs",
    "status": "inprogress"
  }
]
```
### Update Todo

PUT `/todos/<task_id>`

Updates one or more fields of a todo.

**Request Body (Partial updates allowed)**
```json
{
  "status": "done",
  "title": "Write API docs"
}
```

### Allowed Status Values
```
todo | inprogress | done
```

### Success Response

`200 OK`
```json
{
  "id": 3,
  "title": "Write API docs",
  "status": "done",
  "updated_at": "15:01:22 10-01-2026"
}
```

### Error Responses

|Status|	Reason|
|:---|:---|
|400|	Invalid status / no valid fields|
|404	|Todo not found or not owned by user|
|401	|Unauthorized|

### Delete Todo

DELETE `/todos/<task_id>`

Deletes a todo owned by the authenticated user.

### Success Response

`200 OK`
```json
{
  "message": "task deleted"
}
```

### Error Responses
|Status|	Reason|
|:---|:---|
|404|	Todo not found|
|401	|Unauthorized|

## 🔑 Authentication Behavior Summary

- JWT is validated on every protected request

- Token expiration automatically invalidates access

- No server-side session storage

- Logout is handled client-side by deleting the token

## 🧠 Notes for Frontend Developers

- Always send Authorization header for protected routes

- Expect 401 when token expires → trigger re-login

- Empty lists ([]) are valid responses, not errors

- API never leaks data across users