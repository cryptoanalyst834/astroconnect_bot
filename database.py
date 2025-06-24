from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import UserProfile
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Это и есть get_session — генератор сессии
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Добавление анкеты в базу
async def add_user_profile(session: AsyncSession, data: dict):
    profile = UserProfile(**data)
    session.add(profile)
    await session.commit()

# Получение всех анкет
async def get_all_profiles(session: AsyncSession):
    result = await session.execute(select(UserProfile))
    return result.scalars().all()
