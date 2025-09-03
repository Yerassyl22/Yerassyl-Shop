from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# движок для подключения к PostgreSQL
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# фабрика сессий
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# зависимость для FastAPI (будем подключать в эндпоинтах)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()