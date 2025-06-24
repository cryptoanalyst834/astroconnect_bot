from sqlmodel import SQLModel, create_engine, Session, select
from models import UserProfile
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

async def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

async def save_user_profile(profile: UserProfile):
    with Session(engine) as session:
        session.add(profile)
        session.commit()

async def get_all_profiles():
    with Session(engine) as session:
        return session.exec(select(UserProfile)).all()
