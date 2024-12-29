from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from items_api.store.sqlite import Base


class ItemORM(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)


class ItemBase(BaseModel):
    name: str
    description: Optional[str]


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
