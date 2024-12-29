from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from items_api.models.items_model import ItemORM, ItemCreate, ItemResponse


async def list_items(db: AsyncSession):
    result = await db.execute(select(ItemORM))
    items = result.scalars().all()
    return [ItemResponse.from_orm(item) for item in items]


async def get_item_by_id(db: AsyncSession, item_id: int):
    result = await db.execute(select(ItemORM).where(ItemORM.id == item_id))
    item = result.scalar()
    return ItemResponse.from_orm(item) if item else None


async def create_item(db: AsyncSession, item_data: ItemCreate):
    new_item = ItemORM(name=item_data.name, description=item_data.description)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return ItemResponse.from_orm(new_item)


async def update_item(db: AsyncSession, item_id: int, item_data: ItemCreate):
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
    result = await db.execute(select(ItemORM).where(ItemORM.id == item_id))
    item = result.scalar()
    if item:
        await db.delete(item)
        await db.commit()
        return True
    return False
