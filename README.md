# FastAPI Multi-Database Tool Template

A flexible FastAPI application template that supports both Oracle and PostgreSQL databases with raw SQL execution.

## Features

- FastAPI framework with automatic OpenAPI documentation
- Support for both Oracle and PostgreSQL databases
- Environment variable configuration
- Raw SQL execution (no ORM abstractions)
- Async database operations with databases module
- Unit testing with pytest and mocked database
- Clean, modular structure

## Project Structure

```
python-tool-template/
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Example environment configuration
├── .gitignore            # Git ignore configuration
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── main.py               # Application entry point
├── app/
│   ├── __init__.py
│   ├── config.py         # Configuration management
│   ├── db.py             # Database connection and queries
│   └── api/
│       ├── __init__.py
│       └── items.py      # Example endpoint implementations
└── tests/
    ├── __init__.py
    └── test_endpoints.py # API tests
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Access to an Oracle or PostgreSQL database

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd python-tool-template
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file by copying the example:

```bash
cp .env.example .env
```

6. Edit the `.env` file with your database credentials and other settings.

## Configuration

The application is configured using environment variables in the `.env` file:

```
# Database Configuration
DB_TYPE=oracle  # or postgresql
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=1521  # 1521 for Oracle, 5432 for PostgreSQL
DB_NAME=your_database  # Database name for PostgreSQL or service name for Oracle
DB_SCHEMA=your_schema

# Application Settings
APP_NAME=FastAPI Database App
APP_VERSION=0.1.0
DEBUG=True
```

## Running the Application

Start the application with:

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload
```

The application will be available at http://localhost:8000

## API Documentation

Once the application is running, access the interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Adding New Endpoints

To add new endpoints:

1. Create a new file in the `app/api/` directory
2. Define your endpoint functions using FastAPI's router
3. Add your router to the main application in `main.py`

Example:

```python
# app/api/users.py
from fastapi import APIRouter, HTTPException
from app.db import database, get_query

router = APIRouter()

@router.get("/")
async def get_users():
    query = get_query("SELECT_USERS")
    users = await database.fetch_all(query)
    return [dict(user) for user in users]
```

Then in `main.py`:

```python
from app.api import users

# Add your new router
app.include_router(users.router, prefix="/api/users", tags=["users"])
```

## Working with SQL Queries

Define your SQL queries in the `app/db.py` file within the `Queries` class:

```python
class Queries:
    # Oracle specific queries
    ORACLE = {
        "SELECT_USERS": "SELECT * FROM {schema}.USERS",
        # Add more queries here
    }

    # PostgreSQL specific queries
    POSTGRESQL = {
        "SELECT_USERS": "SELECT * FROM {schema}.users",
        # Add more queries here
    }
```

Then use them in your endpoints:

```python
query = get_query("SELECT_USERS")
users = await database.fetch_all(query)
```

## Testing

Run tests with pytest:

```bash
pytest
```

To run specific tests:

```bash
pytest tests/test_endpoints.py::test_read_items
```
