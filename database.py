from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.future import select
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    gender = Column(String)
    birth_date = Column(String)
    birth_time = Column(String)
    birth_place = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    zodiac_sign = Column(String)
    ascendant = Column(String)
    about = Column(String)
    photo_url = Column(String)

def get_session():
    return async_session()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_user_profile(data: dict):
    async with get_session() as session:
        profile = UserProfile(**data)
        session.add(profile)
        await session.commit()

async def get_all_profiles():
    async with get_session() as session:
        result = await session.execute(select(UserProfile))
        return result.scalars().all()
