# Yerassyl Shop — тестовое API (FastAPI + PostgreSQL)

Небольшое API интернет-магазина: каталог товаров с поиском/фильтрами/сортировкой/пагинацией и корзина, привязанная к заголовку `X-Session-Id`. Документация — Swagger.

## Стек
- Python 3.9
- FastAPI, Uvicorn
- SQLAlchemy 2.0, PostgreSQL (psycopg)
- Pydantic v2, pydantic-settings

### 1) Установка
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

```
### 2) База данных (локально)
```bash
createuser user --pwprompt    # пароль: 0000
createdb taskdb -O user
```

### 3) Запуск
```bash
python -m uvicorn app.main:app --reload
# Swagger: http://127.0.0.1:8000/docs

```
### 4) Тестовые данные
```bash
python -m scripts.seed_products
```


### В Swagger нажми “Try it out” и добавь заголовок `X-Session-Id`, например `test`.

### API
# Products
GET /api/products/               # search, category, price_min, price_max, sort=name|price, order=asc|desc, limit, offset
GET /api/products/{product_id}/

# Cart (нужен заголовок: X-Session-Id: <любая_строка>)
GET    /api/cart/
POST   /api/cart/            # body: {"product_id": 1, "quantity": 2}
PUT    /api/cart/{item_id}/  # body как в POST
DELETE /api/cart/{item_id}/




### Структура проекта
app/
  core/        # config.py, database.py
  models/      # cart.py, product.py
  schemas/     # cart.py, product.py
  routers/     # product.py, cart.py
  main.py
scripts/
  seed_products.py
.env
.env.example
README.md
requirements.txt