"""
This module provides CRUD operations for items using SQLAlchemy with async support.

Functions:
- list_items: Retrieves a list of all items.
- get_item_by_id: Fetches a single item by its ID.
- create_item: Adds a new item to the database.
- update_item: Updates an existing item's details.
- delete_item: Deletes an item from the database.
"""

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from items_api.models.items_model import ItemORM, ItemCreate, ItemResponse


async def list_items(db: AsyncSession):
    """Retrieve a list of all items."""
    result = await db.execute(select(ItemORM))
    items = result.scalars().all()
    return [ItemResponse.from_orm(item) for item in items]


async def get_item_by_id(db: AsyncSession, item_id: int):
    """Fetch a single item by its ID."""
    result = await db.execute(select(ItemORM).where(ItemORM.id == item_id))
    item = result.scalar()
    return ItemResponse.from_orm(item) if item else None


async def create_item(db: AsyncSession, item_data: ItemCreate):
    """Add a new item to the database."""
    new_item = ItemORM(name=item_data.name, description=item_data.description)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return ItemResponse.from_orm(new_item)


async def update_item(db: AsyncSession, item_id: int, item_data: ItemCreate):
    """Update an existing item's details."""
    result = await db.execute(select(ItemORM).where(ItemORM.id == item_id))
    item = result.scalar()
    if item:
        item.name = item_data.name
        item.description = item_data.description
        await db.commit()
        await db.refresh(item)
        return ItemResponse.from_orm(item)
    return None


async def delete_item(db: AsyncSession, item_id: int):
    """Delete an item from the database."""
    result = await db.execute(select(ItemORM).where(ItemORM.id == item_id))
    item = result.scalar()
    if item:
        await db.delete(item)
        await db.commit()
        return True
    return False
