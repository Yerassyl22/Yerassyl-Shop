from typing import Optional
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Numeric

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text())
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    image: Mapped[Optional[str]] = mapped_column(String(500))
    category: Mapped[Optional[str]] = mapped_column(String(120), index=True)