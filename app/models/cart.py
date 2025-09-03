from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from app.models.product import Base

class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[str] = mapped_column(String(200), index=True, unique=True)

    items: Mapped[List["CartItem"]] = relationship(
    "CartItem", back_populates="cart", cascade="all, delete-orphan"
)


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"), index=True)

    cart = relationship("Cart", back_populates="items")

    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),
    )