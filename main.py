from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
import asyncpg
import asyncio
import os
from contextlib import asynccontextmanager
from datetime import datetime

# Получение переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Настройка бота
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Обработка команды /start
@dp.message(lambda message: message.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Привет! 👋 Добро пожаловать в AstroConnect!")

# FastAPI + Lifespan для подключения к БД
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await asyncpg.connect(DATABASE_URL)
    asyncio.create_task(dp.start_polling(bot))
    yield
    await app.state.db.close()

app = FastAPI(lifespan=lifespan)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или укажи Netlify-домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Эндпоинт для фронта
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
        return today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
    except:
        return None
