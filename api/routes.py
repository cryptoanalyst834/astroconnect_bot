from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import UserProfile
from sqlalchemy import select

router = APIRouter(prefix="/api")

@router.get("/profiles")
async def read_profiles(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(UserProfile))
    profiles = result.scalars().all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "birth_date": p.birth_date,
            "birth_time": p.birth_time,
            "birth_place": p.birth_place,
            "zodiac": p.zodiac,
            "ascendant": p.ascendant,
            "photo_id": p.photo_id,
        }
        for p in profiles
    ]
