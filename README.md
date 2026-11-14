# Notes API

A simple notes application built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

The main goal of this project is to provide a small, understandable example of building a REST API with FastAPI, demonstrating authentication, database integration, CRUD operations, and a basic separation of concerns between API endpoints and application services.
> [!CAUTION]
> **This is not a production-ready application.** It is a small educational project and should not be used as-is in production environments.

## Features

- User registration with username and password.
- JWT-based authentication.
- Password hashing.
- Create, read, update, and delete notes.
- Each user can only access their own notes.
- SQLite database with SQLAlchemy ORM.
- Interactive API documentation using Swagger UI.
- Simple AI-generated frontend for interacting with the API.

## Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Authentication:** JWT
- **Frontend:** HTML, CSS, JavaScript (AI-generated)

## Project Structure

text

```text
.
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── auth.py
│       │   └── notes.py
│       ├── dependencies.py
│       └── router.py
│
├── core/
│   ├── config.py
│   └── security.py
│
├── services/
│   ├── auth_service.py
│   ├── exceptions.py
│   └── note_service.py
│
├── static/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── .env
├── db.py
├── main.py
├── models.py
├── schemas.py
└── requirements.txt
```

### Architecture Overview

The project follows a simple layered architecture:

- **api/**: Contains the API routes and endpoints. Handles HTTP requests, responses, status codes, and authentication dependencies.
- **services/**: Contains the application logic and database CRUD operations. Services are independent of HTTP and FastAPI.
- **core/**: Contains application configuration and security utilities, including JWT generation and password hashing.
- **models.py**: Defines the SQLAlchemy database models.
- **schemas.py**: Defines Pydantic schemas for request validation and response serialization.
- **db.py**: Handles the SQLite database connection and SQLAlchemy sessions.
- **static/**: Contains the frontend files.

The frontend was generated with the assistance of AI. It is a simple interface intended to demonstrate interaction with the backend API, rather than a polished or production-ready frontend.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/FrancescoValentini/NotesAPI
cd NotesAPI
```

### 2. Configure environment variables

Create a `.env` file in the project root directory with the following content:

```env
JWT_SECRET_KEY=long-secret-key
DATABASE_URL=sqlite:///./notes_database.db
```

> [!WARNING]
> **Note:** The `JWT_SECRET_KEY` above is an example. Generate your own secure secret key before using the application:
> ```bash
> python -c "import secrets; print(secrets.token_urlsafe(32))"
> ```

Replace the example key in your `.env` file with the generated value.

### 3. Run the application

**Linux / macOS**

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
```

**Windows (PowerShell)**

```pwsh
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
```

**Windows (cmd)**
```bat
:: Create a virtual environment
python -m venv venv

:: Activate the virtual environment
venv\Scripts\activate.bat

:: Install dependencies
pip install -r requirements.txt

:: Run the application
uvicorn main:app --reload
```

**Docker**

```bash
# Build the container image
docker compose build

# Run the container
docker compose up
```

### 4. Access the application

Once the application is running, it will be available at:

- **Frontend:** http://127.0.0.1:8000/webui
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

All API endpoints are prefixed with `/api/v1`.

| Method | Endpoint | Description | Authentication |
| --- | --- | --- | --- |
| POST | `/auth/register` | Register a user | No |
| POST | `/auth/login` | Authenticate and obtain a JWT | No |
| POST | `/notes/` | Create a note | Yes |
| GET | `/notes/` | List user's notes | Yes |
| GET | `/notes/{note_id}` | Retrieve a note | Yes |
| PUT | `/notes/{note_id}` | Update a note | Yes |
| DELETE | `/notes/{note_id}` | Delete a note | Yes |

