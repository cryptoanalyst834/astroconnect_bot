from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import UserProfile
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

async def add_user_profile(profile_data):
    async with AsyncSessionLocal() as session:
        session.add(profile_data)
        await session.commit()

async def get_all_profiles():
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT * FROM user_profiles")
        return result.fetchall()
