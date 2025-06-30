from sqlalchemy import Column, Integer, String, Date, Time, Float
from sqlalchemy.dialects.postgresql import JSONB
from database import Base

class UserProfile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    birth_date = Column(Date)
    birth_time = Column(Time)
    birth_place = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    gender = Column(String)
    description = Column(String)
    photo_id = Column(String)
    zodiac = Column(String)
    ascendant = Column(String)
    natal_chart = Column(JSONB)
