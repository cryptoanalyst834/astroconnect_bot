# api/routes.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from database import get_async_session
from models import UserProfile

router = APIRouter()

class ProfileSchema(BaseModel):
    id: int
    name: str
    birth_date: str
    birth_time: str
    birth_place: str
    zodiac: str
    ascendant: str
    photo_id: str

    model_config = {
        "from_attributes": True
    }

@router.get("/profiles", response_model=List[ProfileSchema])
async def read_profiles(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(UserProfile))
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
