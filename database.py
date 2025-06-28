import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager

# Загружаем переменные окружения из .env (или Railway variables)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не задана в окружении!")

# Создаём асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Поставь True для отладки SQL
    pool_pre_ping=True
)

# Фабрика асинхронных сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Базовый класс для моделей
Base = declarative_base()

async def init_db():
    """
    Инициализация базы данных (создание таблиц).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_async_session() -> AsyncSession:
    """
    Асинхронный генератор сессии для Depends (FastAPI).
    """
    async with AsyncSessionLocal() as session:
        yield session
