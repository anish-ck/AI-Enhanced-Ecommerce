from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    title: str
    description: str
    category_id: int
    price: Decimal
    stock: int


class ProductCreate(ProductBase):
    ai_title: Optional[str] = None
    ai_description: Optional[str] = None
    ai_category: Optional[str] = None
    ai_tags: Optional[list[str]] = None
    ai_generated: Optional[bool] = None


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    ai_title: Optional[str] = None
    ai_description: Optional[str] = None
    ai_category: Optional[str] = None
    ai_tags: Optional[list[str]] = None
    ai_generated: Optional[bool] = None


class ProductOut(ProductBase):
    id: int
    created_at: datetime
    ai_title: Optional[str] = None
    ai_description: Optional[str] = None
    ai_category: Optional[str] = None
    ai_tags: Optional[list[str]] = None
    ai_generated: bool

    model_config = ConfigDict(from_attributes=True)
