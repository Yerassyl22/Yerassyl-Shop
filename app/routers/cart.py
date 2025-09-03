from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.cart import CartAddItem, CartOut, CartItemOut

router = APIRouter(prefix="/api/cart", tags=["cart"])

# хелпер для получения корзины по session_id
def get_cart(db: Session, session_id: str) -> Cart:
    cart = db.scalar(select(Cart).where(Cart.session_id == session_id))
    if not cart:
        cart = Cart(session_id=session_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.get("/", response_model=CartOut)
def get_cart_items(x_session_id: str = Header(...), db: Session = Depends(get_db)):
    cart = get_cart(db, x_session_id)
    items_out = []
    total = 0
    for item in cart.items:
        product = db.get(Product, item.product_id)
        if not product:
            continue
        total += product.price * item.quantity
        items_out.append(CartItemOut(
            id=item.id,
            product_id=product.id,
            quantity=item.quantity,
            name=product.name,
            price=float(product.price),
            image=product.image,
            category=product.category,
        ))
    return {"items": items_out, "total": total}

@router.post("/", response_model=CartOut)
def add_to_cart(payload: CartAddItem, x_session_id: str = Header(...), db: Session = Depends(get_db)):
    cart = get_cart(db, x_session_id)
    product = db.get(Product, payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    item = db.scalar(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product.id))
    if item:
        item.quantity += payload.quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product.id, quantity=payload.quantity)
        db.add(item)
    db.commit()
    return get_cart_items(x_session_id, db)

@router.put("/{item_id}/", response_model=CartOut)
def update_cart_item(item_id: int, payload: CartAddItem, x_session_id: str = Header(...), db: Session = Depends(get_db)):
    cart = get_cart(db, x_session_id)
    item = db.get(CartItem, item_id)
    if not item or item.cart_id != cart.id:
        raise HTTPException(status_code=404, detail="Item not found")
    item.quantity = payload.quantity
    db.commit()
    return get_cart_items(x_session_id, db)

@router.delete("/{item_id}/", response_model=CartOut)
def remove_cart_item(item_id: int, x_session_id: str = Header(...), db: Session = Depends(get_db)):
    cart = get_cart(db, x_session_id)
    item = db.get(CartItem, item_id)
    if not item or item.cart_id != cart.id:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return get_cart_items(x_session_id, db)