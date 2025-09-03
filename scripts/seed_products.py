from app.core.database import SessionLocal, engine
from app.models.product import Base, Product

Base.metadata.create_all(bind=engine)

data = [
    {"name": "iPhone 14", "description": "Смартфон Apple", "price": 490000, "image": None, "category": "Электроника"},
    {"name": "MacBook Pro M1", "description": "Лёгкий ноутбук", "price": 890000, "image": None, "category": "Электроника"},
    {"name": "Кроссовки Nike", "description": "Модель Air", "price": 59990, "image": None, "category": "Одежда"},
    {"name": "Футболка Adidas", "description": "100% хлопок", "price": 6900, "image": None, "category": "Одежда"},
    {"name": "Чайник электрический", "description": "1.7L", "price": 12990, "image": None, "category": "Бытовая техника"},
    {"name": "Наушники Sony", "description": "Беспроводные", "price": 79990, "image": None, "category": "Электроника"},
    {"name": "Книга", "description": "Учебник", "price": 8990, "image": None, "category": "Книги"},
    {"name": "Стул офисный", "description": "Эргономичный", "price": 45990, "image": None, "category": "Мебель"},
    {"name": "Мышь Logitech", "description": "Беспроводная", "price": 24990, "image": None, "category": "Электроника"},
    {"name": "Рюкзак", "description": "25L", "price": 15990, "image": None, "category": "Аксессуары"},
]

db = SessionLocal()
try:
    # чтобы не плодить дублей — вставим только если в таблице пусто
    if db.query(Product).count() == 0:
        for d in data:
            db.add(Product(**d))
        db.commit()
        print("✅ Seed: добавлены тестовые товары.")
    else:
        print("ℹ️ Seed: товары уже существуют, пропускаю.")
finally:
    db.close()