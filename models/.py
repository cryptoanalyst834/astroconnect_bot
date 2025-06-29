from sqlalchemy import Column, Integer, String, Date, Time
from database import Base

class UserProfile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(String, unique=True, index=True)
    name = Column(String)
    birth_date = Column(Date)
    birth_time = Column(Time)
    birth_place = Column(String)
    zodiac = Column(String)
    ascendant = Column(String)
    photo_id = Column(String, nullable=True)
    from sqlalchemy import Column, Integer, String, DateTime

