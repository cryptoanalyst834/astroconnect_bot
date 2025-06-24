from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    name = Column(String)
    birth_date = Column(String)
    birth_time = Column(String)
    birth_place = Column(String)
    zodiac_sign = Column(String)
    ascendant = Column(String)
    description = Column(String)
    photo_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
