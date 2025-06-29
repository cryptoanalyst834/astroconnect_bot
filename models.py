from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.dialects.postgresql import JSONB
from database import Base

class UserProfile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    gender = Column(String)
    birth_date = Column(Date)
    birth_time = Column(String)
    birth_place = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    zodiac = Column(String)
    ascendant = Column(String)
    description = Column(String)
    astro_data = Column(JSONB)
