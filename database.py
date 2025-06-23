from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_user(user_data):
    async with AsyncSessionLocal() as session:
        session.add(user_data)
        await session.commit()

async def get_all_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT * FROM users")
        return result.fetchall()
