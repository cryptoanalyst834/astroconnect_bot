import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import asyncpg
from datetime import datetime
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()
dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)

# CORS для фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Лучше указать конкретный Netlify-домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Состояния анкеты
class Form(StatesGroup):
    name = State()
    about = State()
    birth_date = State()
    birth_time = State()
    photo = State()

@app.on_event("startup")
async def on_startup():
    app.state.db = await asyncpg.connect(DATABASE_URL)
    asyncio.create_task(dp.start_polling(bot))

@app.on_event("shutdown")
async def on_shutdown():
    await app.state.db.close()
    await bot.session.close()

# API: Отдаём анкеты
@app.get("/profiles")
async def get_profiles():
    rows = await app.state.db.fetch("SELECT * FROM users ORDER BY RANDOM() LIMIT 20")
    profiles = []
    for row in rows:
        profiles.append({
            "name": row["name"],
            "about": row["about"],
            "photo": row["photo"],
            "location_city": row["location_city"],
            "sun": row.get("sun", ""),
            "ascendant": row.get("ascendant", ""),
            "age": calculate_age(row["birth_date"])
        })
    return profiles

def calculate_age(birth_date_str):
    try:
        birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y")
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except:
        return None

def generate_astrology_info(data):
    birth_date = data['birth_date']  # формат дд.мм.гггг
    birth_time = data['birth_time']  # формат чч:мм
    date_parts = birth_date.split(".")
    time_parts = birth_time.split(":")
    dt = Datetime(f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}", f"{time_parts[0]}:{time_parts[1]}", '+03:00')
    pos = GeoPos("55.7558", "37.6173")
    chart = Chart(dt, pos)
    sun_sign = chart.get(const.SUN).sign
    asc = chart.get(const.ASC).sign
    return sun_sign, asc

# ==== Telegram bot handlers ====

@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Давай создадим твою анкету.\nКак тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Расскажи немного о себе")
    await state.set_state(Form.about)

@dp.message(Form.about)
async def process_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("Введи дату рождения (дд.мм.гггг):")
    await state.set_state(Form.birth_date)

@dp.message(Form.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Введи время рождения (чч:мм):")
    await state.set_state(Form.birth_time)

@dp.message(Form.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Теперь отправь своё фото:")
    await state.set_state(Form.photo)

@dp.message(Form.photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)

    data = await state.get_data()
    sun, asc = generate_astrology_info(data)

    await app.state.db.execute("""
        INSERT INTO users (name, about, birth_date, birth_time, photo, sun, ascendant, location_city)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """, data["name"], data["about"], data["birth_date"], data["birth_time"], photo_id, sun, asc, "Москва")

    await message.answer("Анкета сохранена! 🎉 Ты можешь перейти в мини-приложение для поиска пары.")
    await state.clear()
