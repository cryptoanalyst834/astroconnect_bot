from sqlalchemy import Column, Integer, String, Date, Text
from database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    birth_date = Column(Date, nullable=False)
    birth_time = Column(String, nullable=False)
    birth_place = Column(String, nullable=False)
    zodiac = Column(String, nullable=False)
    ascendant = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    photo = Column(String, nullable=True)
