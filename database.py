from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy.orm import declarative_base
from models import UserProfile
from typing import List

DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # (это будет заменено через .env)

Base = declarative_base()


# ✅ ВАЖНО: init_db должен быть здесь
async def init_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_user_profile(session: AsyncSession, name, birthdate, birthtime, city, zodiac, ascendant, photo_path):
    profile = UserProfile(
        name=name,
        birthdate=birthdate,
        birthtime=birthtime,
        city=city,
        zodiac=zodiac,
        ascendant=ascendant,
        photo_path=photo_path
    )
    session.add(profile)
    await session.commit()


async def get_all_profiles(session: AsyncSession) -> List[dict]:
    result = await session.execute(
        UserProfile.__table__.select()
    )
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]
