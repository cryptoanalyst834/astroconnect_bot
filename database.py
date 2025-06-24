from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import Base, UserProfile
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_user_profile(
    telegram_id: int,
    name: str,
    birth_date: str,
    birth_time: str,
    birth_place: str,
    photo_id: str,
    zodiac_sign: str,
    ascendant: str
):
    async with async_session() as session:
        profile = UserProfile(
            telegram_id=telegram_id,
            name=name,
            birth_date=birth_date,
            birth_time=birth_time,
            birth_place=birth_place,
            photo_id=photo_id,
            zodiac_sign=zodiac_sign,
            ascendant=ascendant
        )
        session.add(profile)
        await session.commit()

async def get_all_profiles():
    async with async_session() as session:
        result = await session.execute(select(UserProfile))
        return [row[0].as_dict() for row in result.all()]
