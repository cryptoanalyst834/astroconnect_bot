from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False)
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, index=True)
    name = Column(String)
    birth_date = Column(String)
    birth_time = Column(String)
    birth_place = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    zodiac_sign = Column(String)
    ascendant = Column(String)
    description = Column(String)
    photo_url = Column(String)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_user_profile(profile_data: dict):
    async with async_session() as session:
        new_profile = UserProfile(**profile_data)
        session.add(new_profile)
        await session.commit()

async def get_all_profiles():
    async with async_session() as session:
        result = await session.execute(select(UserProfile))
        return result.scalars().all()
