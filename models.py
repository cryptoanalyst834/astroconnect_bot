from sqlalchemy import Column, Integer, String
from db_base import Base  # импортируем из нового файла

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    birth_date = Column(String)
    birth_time = Column(String)
    birth_place = Column(String)
    sun_sign = Column(String)
    asc_sign = Column(String)
    photo_id = Column(String)
