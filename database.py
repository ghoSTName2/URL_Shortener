import os
from pathlib import Path
from dotenv import load_dotenv


from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Отримуємо URL (наприклад: postgresql+asyncpg://user:pass@localhost:5432/dbname
# або sqlite+aiosqlite:///./sql_app.db)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

# 1. Асинхронний двигун
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 2. Асинхронна фабрика сесій
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# 3. Базовий клас моделей (SQLAlchemy 2.0+)
class Base(DeclarativeBase):
    pass


# 4. Асинхронна залежність для отримання сесії у FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session