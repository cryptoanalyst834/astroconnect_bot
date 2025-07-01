from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_async_session
from models import UserProfile
from astro_utils import get_zodiac_and_ascendant, compatibility_score

router = APIRouter()

@router.get("/profiles")
async def get_profiles(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(UserProfile))
    profiles = result.scalars().all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "gender": p.gender,
            "birth_date": p.birth_date,
            "zodiac": p.zodiac,
            "ascendant": p.ascendant,
            "description": p.description
        }
        for p in profiles
    ]

@router.get("/find_match")
async def find_match(telegram_id: int = Query(...), session: AsyncSession = Depends(get_async_session)):
    # Находим текущего пользователя
    result = await session.execute(select(UserProfile).where(UserProfile.telegram_id == telegram_id))
    current = result.scalar_one_or_none()
    if not current:
        return {"error": "Пользователь не найден"}
    # Выбираем остальных пользователей
    result = await session.execute(select(UserProfile).where(UserProfile.telegram_id != telegram_id))
    candidates = result.scalars().all()
    if not candidates:
        return {"error": "Нет других анкет"}
    # Считаем совместимость
    current_chart = get_zodiac_and_ascendant(
        str(current.birth_date),
        current.birth_time,
        current.birth_place,
        current.latitude,
        current.longitude
    )[2]
    best = None
    best_score = -1
    for c in candidates:
        c_chart = get_zodiac_and_ascendant(
            str(c.birth_date),
            c.birth_time,
            c.birth_place,
            c.latitude,
            c.longitude
        )[2]
        score = compatibility_score(current_chart, c_chart)
        if score > best_score:
            best = c
            best_score = score
    if best:
        return {
            "id": best.id,
            "name": best.name,
            "gender": best.gender,
            "birth_date": best.birth_date,
            "zodiac": best.zodiac,
            "ascendant": best.ascendant,
            "description": best.description,
            "score": best_score
        }
    return {"error": "Пару не удалось подобрать"}
