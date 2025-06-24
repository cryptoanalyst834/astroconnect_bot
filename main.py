import os
from dotenv import load_dotenv
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from contextlib import asynccontextmanager

from api.routes import router as api_router
from handlers.start import router as start_router
from handlers.profile import router as profile_router
from database import init_db
from states import storage

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN not set in environment variables")

# Создание бота и диспетчера
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=storage)

# Регистрация роутеров
dp.include_router(start_router)
dp.include_router(profile_router)

# Lifespan вместо on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan startup initiated.")
    await init_db()
    await dp.start_polling(bot)
    yield
    print("Lifespan shutdown initiated.")

# FastAPI instance
app = FastAPI(lifespan=lifespan)

# Подключение API роутов
app.include_router(api_router)
