from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, Field

class CartAddItem(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    name: str
    price: float
    image: Optional[str] = None
    category: Optional[str] = None

class CartOut(BaseModel):
    items: List['CartItemOut']
    total: float