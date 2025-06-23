from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    name = Column(String)
    birth_date = Column(String)
    birth_time = Column(String)
    birth_place = Column(String)
    sun_sign = Column(String)
    asc_sign = Column(String)
