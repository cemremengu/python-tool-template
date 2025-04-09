from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.config import settings
from app.db import database

router = APIRouter()


@router.get("/items", operation_id="get_items")
async def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str = None,
):
    """
    Retrieve items with optional search capability.
    """
    try:
        if search:
            query = f"SELECT * FROM {settings.DB_SCHEMA}.items WHERE name ILIKE :search ORDER BY id OFFSET :skip LIMIT :limit"
            items = await database.fetch_all(
                query, {"search": f"%{search}%", "skip": skip, "limit": limit}
            )
        else:
            query = f"SELECT * FROM {settings.DB_SCHEMA}.items ORDER BY id OFFSET :skip LIMIT :limit"
            items = await database.fetch_all(query, {"skip": skip, "limit": limit})

        # Convert to a list of dictionaries
        result = [dict(item) for item in items]
        return result
    except Exception as e:
        return {"error": str(e)}


@router.post(
    "/items",
    status_code=status.HTTP_201_CREATED,
    operation_id="create_items",
)
async def create_item(payload: Dict[str, Any]):
    """
    Create a new item directly from JSON payload.
    """
    try:
        values = {
            "name": payload.get("name"),
            "description": payload.get("description"),
            "price": payload.get("price"),
            "is_active": payload.get("is_active", 1),
        }

        query = f"INSERT INTO {settings.DB_SCHEMA}.items (name, description, price, is_active) VALUES (:name, :description, :price, :is_active) RETURNING id"
        result = await database.fetch_one(query, values)
        return {**values, "id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/items/{item_id}", operation_id="get_one_item")
async def read_item(item_id: int):
    """
    Get an item by ID.
    """
    try:
        query = f"SELECT * FROM {settings.DB_SCHEMA}.items WHERE id = :id"
        item = await database.fetch_one(query, {"id": item_id})

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        return dict(item)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/items/{item_id}", operation_id="update_items")
async def update_item(item_id: int, payload: Dict[str, Any]):
    """
    Update an item by ID directly from JSON payload.
    """
    try:
        # First check if the item exists
        query = f"SELECT * FROM {settings.DB_SCHEMA}.items WHERE id = :id"
        existing_item = await database.fetch_one(query, {"id": item_id})

        if not existing_item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Convert to dict for merging
        current_item = dict(existing_item)

        # Build the update data, preserving existing values if not provided
        update_data = {
            "name": payload.get("name", current_item["name"]),
            "description": payload.get("description", current_item["description"]),
            "price": payload.get("price", current_item["price"]),
            "is_active": payload.get("is_active", current_item["is_active"]),
            "id": item_id,
        }

        # Update the item
        update_query = f"UPDATE {settings.DB_SCHEMA}.items SET name = :name, description = :description, price = :price, is_active = :is_active WHERE id = :id"
        await database.execute(update_query, update_data)

        # Get the updated item
        query = f"SELECT * FROM {settings.DB_SCHEMA}.items WHERE id = :id"
        updated_item = await database.fetch_one(query, {"id": item_id})

        return dict(updated_item)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_items",
)
async def delete_item(item_id: int):
    """
    Delete an item by ID.
    """
    try:
        # First check if the item exists
        query = f"SELECT * FROM {settings.DB_SCHEMA}.items WHERE id = :id"
        existing_item = await database.fetch_one(query, {"id": item_id})

        if not existing_item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Delete the item
        query = f"DELETE FROM {settings.DB_SCHEMA}.items WHERE id = :id"
        await database.execute(query, {"id": item_id})

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
