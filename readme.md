
# TaskGuard

A secure, full-stack Task Management System built with FastAPI, featuring dual authentication (session-based for web users and JWT-based for API users).

## Objective

TaskGuard allows users to register, log in, and manage personal tasks securely. It supports:

- **Web Interface**: Session-based authentication for browser access.
- **API Interface**: JWT-based authentication for programmatic access (e.g., mobile apps).

## Features

### User Authentication:
- Register and log in with email and password (hashed using bcrypt).
- Session-based login for web users with cookie storage.
- JWT token authentication for API users.

### Task Management:
- Create, view, edit, and delete tasks.
- Users can only access their own tasks.

### Web Routes:
- `/register`
- `/login`
- `/logout`
- `/dashboard`
- `/tasks/add`
- `/tasks/edit/{id}`
- `/tasks/delete/{id}`

### API Endpoints:
- `POST /api/login`: Get JWT token.
- `GET /api/tasks`, `POST /api/tasks`, `PUT /api/tasks/{id}`, `DELETE /api/tasks/{id}` (all JWT-protected).

## Technical Stack:
- **Backend**: FastAPI, SQLAlchemy (SQLite), Jinja2 templates.
- **Security**: Password hashing with passlib, JWT with python-jose.

## Setup Instructions

### Clone the Repository:
```bash
git clone https://github.com/rehmanmani/FastAPI-based-task-management-app.git
cd FastAPI-based-task-management-app
```



### Install Dependencies:
```bash
pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt] python-jose[cryptography] jinja2 itsdangerous
```

### Run the Application:
```bash
uvicorn main:app --reload
```

### Access the App:
- Web Interface: [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)
- API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
