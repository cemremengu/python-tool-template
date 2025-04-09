# FastAPI PostgreSQL Tool Template

A flexible FastAPI application template that supports PostgreSQL database with raw SQL execution.

## Features

- FastAPI framework with automatic OpenAPI documentation
- Support for PostgreSQL database
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
│   ├── db.py             # Database connection
│   └── api.py            # API endpoints with direct SQL
└── tests/
    ├── __init__.py
    └── test_endpoints.py # API tests
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Access to a PostgreSQL database

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
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=5432  # Default PostgreSQL port
DB_NAME=your_database  # Database name for PostgreSQL
DB_SCHEMA=your_schema

# Application Settings
APP_NAME=FastAPI Database App
APP_VERSION=0.1.0
DEBUG=True
```

## Running the Application

Start the application with:

```bash
fastapi dev main.py
```

The application will be available at http://localhost:8000

## API Documentation

Once the application is running, access the interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Adding New Endpoints

To add new endpoints, simply add them to the `app/api.py` file:

```python
# In app/api.py
@router.get("/users")
async def get_users():
    query = f"SELECT * FROM {settings.DB_SCHEMA}.users"
    users = await database.fetch_all(query)
    return [dict(user) for user in users]
```

## Working with SQL Queries

SQL queries are executed directly in the API handlers:

```python
@router.get("/users")
async def get_users():
    query = f"SELECT * FROM {settings.DB_SCHEMA}.users"
    users = await database.fetch_all(query)
    return [dict(user) for user in users]
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
