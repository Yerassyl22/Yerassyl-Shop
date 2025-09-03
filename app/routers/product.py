from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, and_, asc, desc
from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductOut

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=dict)
def list_products(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    price_min: Optional[float] = Query(None, ge=0),
    price_max: Optional[float] = Query(None, ge=0),
    search: Optional[str] = None,
    sort: str = Query("name", pattern="^(name|price)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    stmt = select(Product)

    conditions = []
    if category:
        conditions.append(Product.category == category)
    if price_min is not None:
        conditions.append(Product.price >= price_min)
    if price_max is not None:
        conditions.append(Product.price <= price_max)
    if search:
        q = f"%{search.lower()}%"
        conditions.append(or_(func.lower(Product.name).like(q),
                              func.lower(Product.description).like(q)))
    if conditions:
        stmt = stmt.where(and_(*conditions))

    # сортировка
    order_fn = asc if order == "asc" else desc
    if sort == "price":
        stmt = stmt.order_by(order_fn(Product.price))
    else:
        stmt = stmt.order_by(order_fn(Product.name))

    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    items = db.execute(stmt.limit(limit).offset(offset)).scalars().all()

    def make_url(off):
        base = f"/api/products/?limit={limit}&offset={off}"
        if category: base += f"&category={category}"
        if price_min is not None: base += f"&price_min={price_min}"
        if price_max is not None: base += f"&price_max={price_max}"
        if search: base += f"&search={search}"
        base += f"&sort={sort}&order={order}"
        return base

    return {
        "count": int(total or 0),
        "next": make_url(offset + limit) if (offset + limit) < (total or 0) else None,
        "previous": make_url(offset - limit) if offset - limit >= 0 else None,
        "results": [ProductOut.model_validate(p, from_attributes=True).model_dump() for p in items],
    }

@router.get("/{product_id}/", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut.model_validate(product, from_attributes=True)
