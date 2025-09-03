from typing import Optional
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(ge=0)
    image: Optional[str] = None
    category: Optional[str] = None

class ProductOut(ProductBase):
    id: int