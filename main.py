import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, save_user, get_all_users
from models import UserCreate
from astro_utils import generate_natal_chart

# Инициализация
bot = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()

# CORS для фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# Состояния
class Form(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_place = State()
    photo = State()

# Старт
@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Как тебя зовут?")

@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.birth_date)
    await message.answer("Укажи дату рождения (дд.мм.гггг):")

@dp.message(Form.birth_date)
async def get_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await state.set_state(Form.birth_time)
    await message.answer("Время рождения (чч:мм):")

@dp.message(Form.birth_time)
async def get_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await state.set_state(Form.birth_place)
    await message.answer("Город рождения:")

@dp.message(Form.birth_place)
async def get_birth_place(message: Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    await state.set_state(Form.photo)
    await message.answer("Пришли своё фото:")

@dp.message(Form.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()

    # Расчёт натальной карты
    sun_sign, asc_sign = generate_natal_chart(data['birth_date'], data['birth_time'], data['birth_place'])

    # Сохранение в БД
    user = UserCreate(
        telegram_id=message.from_user.id,
        name=data['name'],
        birth_date=data['birth_date'],
        birth_time=data['birth_time'],
        birth_place=data['birth_place'],
        photo_id=photo_id,
        sun_sign=sun_sign,
        asc_sign=asc_sign
    )
    await save_user(user)
    await message.answer(f"Спасибо, {user.name}! 🌟\nСолнце в {sun_sign}, Асцендент в {asc_sign}.\nАнкета сохранена!")
    await state.clear()

# FastAPI: получить анкеты
@app.get("/profiles")
async def get_profiles():
    return await get_all_users()

# Старт апи и бота
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    import asyncio
    asyncio.create_task(dp.start_polling(bot))
