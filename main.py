import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from astro_utils import generate_natal_chart
from database import init_db
from models import UserProfile, Base

# Load environment variables
load_dotenv()

# Telegram and DB config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Validate config
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL не задан")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DB setup
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Bot setup
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# FSM states
class Form(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_place = State()
    photo = State()

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mini-app API route
@app.get("/profiles")
async def get_profiles():
    async with SessionLocal() as session:
        users = await session.execute(UserProfile.__table__.select())
        profiles = [dict(row._mapping) for row in users]
        return JSONResponse(profiles)

# Telegram handlers
@dp.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("👋 Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📅 Введи дату рождения (в формате ГГГГ-ММ-ДД):")
    await state.set_state(Form.birth_date)

@dp.message(Form.birth_date)
async def get_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("⏰ Введи время рождения (в формате ЧЧ:ММ):")
    await state.set_state(Form.birth_time)

@dp.message(Form.birth_time)
async def get_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("🌍 Укажи место рождения (город):")
    await state.set_state(Form.birth_place)

@dp.message(Form.birth_place)
async def get_birth_place(message: Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    await message.answer("📷 Пришли своё фото:")
    await state.set_state(Form.photo)

@dp.message(Form.photo)
async def get_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("❌ Пожалуйста, отправь фото.")
        return

    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()

    name = data['name']
    birth_date = data['birth_date']
    birth_time = data['birth_time']
    birth_place = data['birth_place']
    dt_str = f"{birth_date} {birth_time}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

    # Astrology data
    astrology = await generate_astrology_data(birth_place, dt)

    # Save to DB
    async with SessionLocal() as session:
        user = UserProfile(
            name=name,
            birth_date=birth_date,
            birth_time=birth_time,
            birth_place=birth_place,
            photo_file_id=photo_file_id,
            zodiac=astrology["zodiac"],
            ascendant=astrology["ascendant"]
        )
        session.add(user)
        await session.commit()

    await message.answer(f"🌟 Спасибо, {name}! Твоя натальная карта рассчитана:\n"
                         f"Знак Зодиака: {astrology['zodiac']}\n"
                         f"Асцендент: {astrology['ascendant']}")
    await state.clear()

# Main
async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("🚀 Запускаем Telegram-бота и FastAPI...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
