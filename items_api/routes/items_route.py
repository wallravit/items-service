"""
This module defines API endpoints for managing items using FastAPI.
It includes routes to list, retrieve, create, update, and delete items,
and leverages asynchronous database sessions with SQLAlchemy.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from items_api.store.sqlite import AsyncSessionLocal
from items_api.controllers.items_controller import (
    list_items,
    get_item_by_id,
    create_item,
    update_item,
    delete_item,
)
from items_api.models.items_model import ItemCreate, ItemResponse

router = APIRouter()

async def get_db():
    """
    Dependency function to provide a database session for request handling.

    Yields:
        AsyncSession: An instance of the asynchronous database session.
    """
    async with AsyncSessionLocal() as db:
        yield db

@router.get(
    "/items", response_model=List[ItemResponse]
)
async def fetch_items(db: AsyncSession = Depends(get_db)):
    """
    Fetch a list of all items.

    Args:
        db (AsyncSession): Database session dependency.

    Returns:
        List[ItemResponse]: A list of item details.
    """
    return await list_items(db)

@router.get("/items/{item_id}", response_model=ItemResponse)
async def fetch_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Fetch a single item by its ID.

    Args:
        item_id (int): The ID of the item to retrieve.
        db (AsyncSession): Database session dependency.

    Raises:
        HTTPException: If the item is not found.

    Returns:
        ItemResponse: The details of the requested item.
    """
    item = await get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_new_item(item_data: ItemCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new item.

    Args:
        item_data (ItemCreate): Data for the item to create.
        db (AsyncSession): Database session dependency.

    Returns:
        ItemResponse: The details of the newly created item.
    """
    return await create_item(db, item_data)

@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_existing_item(
    item_id: int, item_data: ItemCreate, db: AsyncSession = Depends(get_db)
):
    """
    Update an existing item by its ID.

    Args:
        item_id (int): The ID of the item to update.
        item_data (ItemCreate): Updated data for the item.
        db (AsyncSession): Database session dependency.

    Raises:
        HTTPException: If the item is not found.

    Returns:
        ItemResponse: The updated details of the item.
    """
    updated_item = await update_item(db, item_id, item_data)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}")
async def delete_existing_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete an existing item by its ID.

    Args:
        item_id (int): The ID of the item to delete.
        db (AsyncSession): Database session dependency.

    Raises:
        HTTPException: If the item is not found.

    Returns:
        dict: A message confirming the successful deletion.
    """
    success = await delete_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
