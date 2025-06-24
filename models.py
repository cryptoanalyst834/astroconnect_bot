from sqlalchemy import Column, Integer, String
from database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer)
    name = Column(String)
    birth_date = Column(String)
    birth_time = Column(String)
    birth_place = Column(String)
    photo_id = Column(String)
    photo_url = Column(String)
    zodiac = Column(String)
    ascendant = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "name": self.name,
            "birth_date": self.birth_date,
            "birth_time": self.birth_time,
            "birth_place": self.birth_place,
            "photo_id": self.photo_id,
            "photo_url": self.photo_url,
            "zodiac": self.zodiac,
            "ascendant": self.ascendant,
        }
