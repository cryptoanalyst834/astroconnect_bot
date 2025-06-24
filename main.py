import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from astro_utils import generate_natal_chart
from models import Base, UserProfile
from database import get_session, add_user_profile, get_all_profiles

import uvicorn

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# FastAPI app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bot
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())


# States
class Form(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_city = State()
    about = State()
    photo = State()


@dp.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("👋 Привет! Давай построим твою натальную карту и создадим анкету. Как тебя зовут?")
    await state.set_state(Form.name)


@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📅 Введи дату рождения (дд.мм.гггг):")
    await state.set_state(Form.birth_date)


@dp.message(Form.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("⏰ Введи время рождения (чч:мм):")
    await state.set_state(Form.birth_time)


@dp.message(Form.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("🏙️ В каком городе ты родился(ась)?")
    await state.set_state(Form.birth_city)


@dp.message(Form.birth_city)
async def process_birth_city(message: Message, state: FSMContext):
    await state.update_data(birth_city=message.text)
    await message.answer("💬 Расскажи немного о себе:")
    await state.set_state(Form.about)


@dp.message(Form.about)
async def process_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("📸 Отправь своё фото:")
    await state.set_state(Form.photo)


@dp.message(Form.photo)
async def process_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    photo_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    chart = await generate_natal_chart(
        date_str=data["birth_date"],
        time_str=data["birth_time"],
        city_name=data["birth_city"]
    )

    profile_data = {
        "telegram_id": message.from_user.id,
        "name": data["name"],
        "birth_date": data["birth_date"],
        "birth_time": data["birth_time"],
        "birth_city": data["birth_city"],
        "about": data["about"],
        "photo_url": photo_url,
        "zodiac": chart["zodiac"],
        "ascendant": chart["ascendant"],
    }

    async with async_session() as session:
        await add_user_profile(session, profile_data)

    await message.answer("✅ Анкета сохранена! Теперь ты можешь перейти к поиску.")
    await state.clear()


# FastAPI route
@app.get("/profiles")
async def get_profiles():
    async with async_session() as session:
        profiles = await get_all_profiles(session)
        return profiles


# Run
if __name__ == "__main__":
    import asyncio

    async def on_startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Бот и API запущены")

    asyncio.run(on_startup())
    dp.start_polling(bot)
    # uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
