from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String)
    birth_date = Column(String)
    birth_time = Column(String)
    birth_place = Column(String)
    photo_id = Column(String)
    zodiac_sign = Column(String)
    ascendant = Column(String)

    def as_dict(self):
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "name": self.name,
            "birth_date": self.birth_date,
            "birth_time": self.birth_time,
            "birth_place": self.birth_place,
            "photo_id": self.photo_id,
            "zodiac_sign": self.zodiac_sign,
            "ascendant": self.ascendant,
        }
