from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import product, cart
from app.models.product import Base
from app.models.cart import Cart, CartItem
from app.core.database import engine

# создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS (разрешаем все, чтобы Swagger работал)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# подключаем роутеры
app.include_router(product.router)
app.include_router(cart.router)