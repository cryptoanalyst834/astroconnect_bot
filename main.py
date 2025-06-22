import os
import asyncio
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

# === CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# === FASTAPI APP ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    app.state.db = await asyncpg.connect(DATABASE_URL)
    asyncio.create_task(start_bot())  # Запуск бота в фоне

@app.on_event("shutdown")
async def on_shutdown():
    await app.state.db.close()

@app.get("/profiles")
async def get_profiles():
    rows = await app.state.db.fetch("SELECT * FROM users ORDER BY RANDOM() LIMIT 20")
    return [{
        "name": row["name"],
        "about": row["about"],
        "photo": row["photo"],
        "location_city": row["location_city"],
        "sun": row.get("sun", ""),
        "ascendant": row.get("ascendant", ""),
        "age": calculate_age(row["birth_date"])
    } for row in rows]

def calculate_age(birth_date_str):
    try:
        birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y")
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except:
        return None

# === TELEGRAM BOT ===
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    about = State()
    city = State()
    photo = State()

@dp.message(commands=["start"])
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Привет! Давай создадим твою анкету.\nКак тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Когда ты родился? (в формате ДД.ММ.ГГГГ)")
    await state.set_state(Form.birth_date)

@dp.message(Form.birth_date)
async def set_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Во сколько ты родился? (часы:минуты, например 14:30)")
    await state.set_state(Form.birth_time)

@dp.message(Form.birth_time)
async def set_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Расскажи немного о себе.")
    await state.set_state(Form.about)

@dp.message(Form.about)
async def set_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("Из какого ты города?")
    await state.set_state(Form.city)

@dp.message(Form.city)
async def set_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Отправь свою фотографию.")
    await state.set_state(Form.photo)

@dp.message(Form.photo)
async def set_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправь именно фото.")
        return
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)

    data = await state.get_data()
    sun, asc = generate_astrology_info(data)

    await app.state.db.execute("""
        INSERT INTO users (name, birth_date, birth_time, about, location_city, photo, sun, ascendant)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """, data["name"], data["birth_date"], data["birth_time"], data["about"],
         data["city"], data["photo"], sun, asc)

    await message.answer(f"Анкета создана! ☀️ Солнце: {sun}, 🌅 Асцендент: {asc}")
    await state.clear()

def generate_astrology_info(data):
    date_parts = data["birth_date"].split(".")
    time_parts = data["birth_time"].split(":")
    dt = Datetime(f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}",
                  f"{time_parts[0]}:{time_parts[1]}", '+03:00')
    pos = GeoPos("55.7558", "37.6173")  # Москва
    chart = Chart(dt, pos)
    return chart.get(const.SUN).sign, chart.get(const.ASC).sign

# === BOT STARTUP TASK ===
async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
