# database.py

import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager

# Поддержка переменных окружения (для локального запуска)
load_dotenv()

# Получаем DATABASE_URL (например: postgresql+asyncpg://user:pass@host:5432/dbname)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не задана в окружении!")

# Создаём асинхронный движок с asyncpg
engine = create_async_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# Сессии для работы с БД
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Базовый класс моделей
Base = declarative_base()

async def init_db():
    """
    Создаёт таблицы (вызывать при старте приложения, например, через FastAPI startup event).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_async_session():
    """
    Используйте в Depends(FastAPI) для получения асинхронной сессии.
    """
    async with AsyncSessionLocal() as session:
        yield session
