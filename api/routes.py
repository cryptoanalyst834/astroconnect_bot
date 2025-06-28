from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import UserProfile
from database import get_async_session
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["profiles"])

@router.get("/profiles")
async def get_profiles(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(UserProfile))
    profiles = result.scalars().all()
    data = [
        {
            "id": p.id,
            "name": p.name,
            "zodiac": p.zodiac,
            "ascendant": p.ascendant,
            "photo_id": p.photo_id,
        }
        for p in profiles
    ]
    return JSONResponse(content=data)

@router.get("/compatibility")
async def get_compatible(
    zodiac: str = Query(...),
    session: AsyncSession = Depends(get_async_session),
):
    # Пример — ищем любую анкету с тем же знаком зодиака (здесь можно прописать настоящую астросовместимость)
    result = await session.execute(
        select(UserProfile).where(UserProfile.zodiac == zodiac)
    )
    user = result.scalars().first()
    if user:
        data = {
            "id": user.id,
            "name": user.name,
            "zodiac": user.zodiac,
            "ascendant": user.ascendant,
            "photo_id": user.photo_id,
        }
        return JSONResponse(content=data)
    return JSONResponse(content={})
