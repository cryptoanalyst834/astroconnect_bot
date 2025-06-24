from sqlalchemy import Column, Integer, String
from db_base import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    username = Column(String)
    about = Column(String)
    photo_path = Column(String)
    zodiac = Column(String)
    ascendant = Column(String)
