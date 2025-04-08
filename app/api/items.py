from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.config import settings
from app.db import database, get_query

router = APIRouter()


@router.get("/")
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
            query = get_query("SELECT_ITEMS_SEARCH")
            items = await database.fetch_all(
                query, {"search": f"%{search}%", "skip": skip, "limit": limit}
            )
        else:
            query = get_query("SELECT_ITEMS")
            items = await database.fetch_all(query, {"skip": skip, "limit": limit})

        # Convert to a list of dictionaries
        result = [dict(item) for item in items]
        return result
    except Exception as e:
        return {"error": str(e)}


@router.post("/", status_code=status.HTTP_201_CREATED)
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

        if settings.DB_TYPE == "postgresql":
            # PostgreSQL can return values directly
            query = get_query("INSERT_ITEM")
            result = await database.fetch_one(query, values)
            return {**values, "id": result["id"]}
        else:
            # Oracle with oracledb driver
            query = get_query("INSERT_ITEM")

            # Add output parameter for Oracle
            values["id"] = None

            # Execute the query using oracledb's output binding
            async with database.connection() as connection:
                cursor = await connection.cursor()
                await cursor.execute(query, values)
                # Get the ID from the output binding
                item_id = await cursor.var.get("id")
                await connection.commit()

            # Return the created item with its ID
            return {**payload, "id": item_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{item_id}")
async def read_item(item_id: int):
    """
    Get an item by ID.
    """
    try:
        query = get_query("SELECT_ITEM_BY_ID")
        item = await database.fetch_one(query, {"id": item_id})

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        return dict(item)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}")
async def update_item(item_id: int, payload: Dict[str, Any]):
    """
    Update an item by ID directly from JSON payload.
    """
    try:
        # First check if the item exists
        query = get_query("SELECT_ITEM_BY_ID")
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
        update_query = get_query("UPDATE_ITEM")
        await database.execute(update_query, update_data)

        # Get the updated item
        query = get_query("SELECT_ITEM_BY_ID")
        updated_item = await database.fetch_one(query, {"id": item_id})

        return dict(updated_item)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    Delete an item by ID.
    """
    try:
        # First check if the item exists
        query = get_query("SELECT_ITEM_BY_ID")
        existing_item = await database.fetch_one(query, {"id": item_id})

        if not existing_item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Delete the item
        query = get_query("DELETE_ITEM")
        await database.execute(query, {"id": item_id})

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
