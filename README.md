# Smart ToDo API

Smart ToDo API is a secure RESTful backend application that allows users to manage personal tasks using JWT-based authentication.

---

## Features

- User Registration
- User Login with JWT Token
- Secure Password Hashing (Argon2)
- JWT Authentication & Authorization
- Task CRUD Operations (Create, Read, Update, Delete)
- User-Specific Task Access
- MongoDB Integration

---

## Tech Stack

- Python 3.11
- FastAPI
- MongoDB
- JWT (JSON Web Tokens)
- Argon2 Password Hashing

---

## Project Structure

<pre>
smart-todo-api/
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── schemas.py
│   ├── config.py
│   └── __init__.py
├── requirements.txt
├── .env
└── README.md
</pre>


## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```
### 2. Install Dependencies
pip install -r requirements.txt

### 3. Configure Environment Variables
Create .env file:

### 4. Run MongoDB (Local)
mongodb://localhost:27017

### 5. Run the Application
- uvicorn app.main:app --reload
- Open Swagger UI:
- http://127.0.0.1:8000/docs

### 6. Authentication Flow
- Register user
- Login to receive JWT token
- Send token in header:

### 7. Testing Protected Routes 
curl -X POST http://127.0.0.1:8000/tasks \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <token>" \
-d '{"title":"My Task","description":"Test"}'
