from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String)
    birth_date = Column(String)
    birth_time = Column(String)
    birth_place = Column(String)
    photo_id = Column(String)
    sun_sign = Column(String)
    asc_sign = Column(String)

class UserCreate(BaseModel):
    telegram_id: int
    name: str
    birth_date: str
    birth_time: str
    birth_place: str
    photo_id: str
    sun_sign: str
    asc_sign: str
