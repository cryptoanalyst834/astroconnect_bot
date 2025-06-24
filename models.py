from sqlmodel import SQLModel, Field
from typing import Optional

class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: int
    name: str
    birth_date: str
    birth_time: str
    birth_place: str
    photo_id: str
    zodiac: str
    ascendant: str
