# models/user.py
from sqlalchemy import Column, Integer, String
from database import Base

class UserProfile(Base):
    __tablename__ = "profiles"
    id           = Column(Integer, primary_key=True, index=True)
    telegram_id  = Column(Integer, unique=True, index=True)
    name         = Column(String)
    birth_date   = Column(String)
    birth_time   = Column(String)
    birth_place  = Column(String)
    zodiac       = Column(String)
    ascendant    = Column(String)
    photo_id     = Column(String)
