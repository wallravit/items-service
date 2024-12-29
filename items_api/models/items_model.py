"""
This module defines the data models for the Items API.

Models:
- ItemORM: The SQLAlchemy ORM model representing the `items` table.
- ItemBase: The Pydantic base model for item data validation.
- ItemCreate: A Pydantic model for item creation payloads.
- ItemResponse: A Pydantic model for item response payloads.
"""

from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from items_api.store.sqlite import Base


class ItemORM(Base):
    """SQLAlchemy ORM model for the `items` table."""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)


class ItemBase(BaseModel):
    """Base Pydantic model for item data validation."""
    name: str
    description: Optional[str]


class ItemCreate(ItemBase):
    """Pydantic model for creating a new item."""
    pass # pylint: disable=unnecessary-pass


class ItemResponse(ItemBase):
    """Pydantic model for item response payloads."""
    id: int

    class Config:
        """Additional configuration for Pydantic model."""
        from_attributes = True
        orm_mode = True # pylint: disable=too-few-public-methods
