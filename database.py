# database.py

import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager

# Загружаем переменные окружения из .env (либо из Railway Variables)
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не задана в окружении")

# Создаём асинхронный движок без пула соединений (NullPool)
engine = create_async_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# Сессия для AsyncSession
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей
Base = declarative_base()

async def init_db():
    """Создаёт все таблицы (вызывать при старте приложения)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_async_session() -> AsyncSession:
    """
    Генератор сессии для FastAPI Depends.
    Пример использования:

        async def read_profiles(session: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session
