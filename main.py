import os
import asyncio
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import asyncpg
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Настройка Telegram бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# Состояния
class Form(StatesGroup):
    name = State()
    gender = State()
    birth_date = State()
    birth_time = State()
    birth_city = State()
    location_city = State()
    looking_for = State()
    about = State()
    photo = State()

# PostgreSQL соединение
async def connect_db():
    return await asyncpg.connect(DATABASE_URL)

# Маршруты Telegram-бота
@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Давай начнём. Как тебя зовут?")
    await state.set_state(Form.name)

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажи свой пол (м/ж):")
    await state.set_state(Form.gender)

@router.message(Form.gender)
async def process_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Дата рождения (ГГГГ-ММ-ДД):")
    await state.set_state(Form.birth_date)

@router.message(Form.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Время рождения (например, 14:30):")
    await state.set_state(Form.birth_time)

@router.message(Form.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Город рождения:")
    await state.set_state(Form.birth_city)

@router.message(Form.birth_city)
async def process_birth_city(message: Message, state: FSMContext):
    await state.update_data(birth_city=message.text)
    await message.answer("Текущий город проживания:")
    await state.set_state(Form.location_city)

@router.message(Form.location_city)
async def process_location_city(message: Message, state: FSMContext):
    await state.update_data(location_city=message.text)
    await message.answer("Кого ты ищешь (м/ж/любой):")
    await state.set_state(Form.looking_for)

@router.message(Form.looking_for)
async def process_looking_for(message: Message, state: FSMContext):
    await state.update_data(looking_for=message.text)
    await message.answer("Расскажи о себе в двух словах:")
    await state.set_state(Form.about)

@router.message(Form.about)
async def process_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("Пришли свою фотографию:")
    await state.set_state(Form.photo)

@router.message(Form.photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    user_data = await state.get_data()

    conn = await connect_db()
    await conn.execute('''
        INSERT INTO users (
            telegram_id, name, gender, birth_date, birth_time, birth_city, location_city, looking_for, about, photo
        ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
        ON CONFLICT (telegram_id) DO NOTHING
    ''',
        message.from_user.id,
        user_data["name"],
        user_data["gender"],
        user_data["birth_date"],
        user_data["birth_time"],
        user_data["birth_city"],
        user_data["location_city"],
        user_data["looking_for"],
        user_data["about"],
        user_data["photo"]
    )
    await conn.close()

    await message.answer("Спасибо! Анкета сохранена. Скоро ты увидишь совместимых пользователей.")
    await state.clear()

# FastAPI часть
app = FastAPI()

# CORS, чтобы фронт мог обращаться
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель анкеты
class Profile(BaseModel):
    telegram_id: int
    name: str
    gender: str
    birth_date: str
    birth_time: str
    birth_city: str
    location_city: str
    looking_for: str
    about: str
    photo: str

# API для мини-приложения
@app.get("/profiles", response_model=list[Profile])
async def get_profiles():
    conn = await connect_db()
    rows = await conn.fetch("SELECT * FROM users LIMIT 20")
    await conn.close()
    return [dict(row) for row in rows]

# Запуск бота
@app.on_event("startup")
async def startup():
    asyncio.create_task(dp.start_polling(bot))
