import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import User, UserCreate

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_user(user_data: UserCreate):
    async with SessionLocal() as session:
        user = User(**user_data.dict())
        session.add(user)
        await session.commit()

async def get_all_users():
    async with SessionLocal() as session:
        result = await session.execute(select(User))
        return result.scalars().all()
