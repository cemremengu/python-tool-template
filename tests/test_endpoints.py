from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def test_app():
    """
    Create a test client for our FastAPI app with mocked database
    """
    # Mock the database connection
    with patch("app.db.database.connect", return_value=MagicMock()):
        with patch("app.db.database.disconnect", return_value=MagicMock()):
            client = TestClient(app)
            yield client


@pytest.fixture
def mock_db():
    """
    Create a mock for database operations
    """
    with (
        patch("app.db.database.fetch_all") as mock_fetch_all,
        patch("app.db.database.fetch_one") as mock_fetch_one,
        patch("app.db.database.execute") as mock_execute,
        patch("app.db.database.connection") as mock_connection,
    ):
        # Setup the connection mock to handle cursor operations
        mock_cursor = MagicMock()
        mock_connection.return_value.__aenter__.return_value.cursor.return_value = (
            mock_cursor
        )
        mock_cursor.execute = MagicMock()
        mock_cursor.var = MagicMock()
        mock_cursor.var.get = MagicMock(return_value=1)  # Mock ID return value

        yield {
            "fetch_all": mock_fetch_all,
            "fetch_one": mock_fetch_one,
            "execute": mock_execute,
            "connection": mock_connection,
            "cursor": mock_cursor,
        }


def test_read_main(test_app):
    """
    Test the root endpoint
    """
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI Oracle application"}


def test_read_items(test_app, mock_db):
    """
    Test getting the list of items
    """
    # Mock the fetch_all to return a list of items
    mock_items = [
        {
            "id": 1,
            "name": "Test Item",
            "description": "Test Description",
            "price": 10.99,
            "is_active": 1,
        },
        {
            "id": 2,
            "name": "Another Item",
            "description": "Another Description",
            "price": 20.99,
            "is_active": 1,
        },
    ]

    # Create Row-like objects that mimic database response
    class Row(dict):
        def __getitem__(self, key):
            return self.get(key)

    mock_db["fetch_all"].return_value = [Row(item) for item in mock_items]

    response = test_app.get("/api/items/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Test Item"


def test_read_item(test_app, mock_db):
    """
    Test getting an item by ID
    """

    # Mock fetch_one to return a single item
    class Row(dict):
        def __getitem__(self, key):
            return self.get(key)

    mock_db["fetch_one"].return_value = Row(
        {
            "id": 1,
            "name": "Test Item",
            "description": "Test Description",
            "price": 10.99,
            "is_active": 1,
        }
    )

    response = test_app.get("/api/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Test Item"


def test_create_item(test_app, mock_db):
    """
    Test creating a new item
    """
    # The cursor and connection mocks are already set up in the mock_db fixture

    # Define test data
    test_item = {
        "name": "New Item",
        "description": "New Description",
        "price": 15.99,
        "is_active": 1,
    }

    # Post to create the item
    response = test_app.post("/api/items/", json=test_item)
    assert response.status_code == 201
    assert response.json()["id"] == 1  # The mock returns 1 as ID
    assert response.json()["name"] == "New Item"


# Add more tests for update and delete operations as needed
