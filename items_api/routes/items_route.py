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
    async with AsyncSessionLocal() as db:
        yield db

@router.get("/items", response_model=List[ItemResponse])  # Use typing.List for Python 3.8
async def fetch_items(db: AsyncSession = Depends(get_db)):
    return await list_items(db)

@router.get("/items/{item_id}", response_model=ItemResponse)
async def fetch_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_new_item(item_data: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_item(db, item_data)

@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_existing_item(item_id: int, item_data: ItemCreate, db: AsyncSession = Depends(get_db)):
    updated_item = await update_item(db, item_id, item_data)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}")
async def delete_existing_item(item_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
