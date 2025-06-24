import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api import api_router
from database import init_db
from handlers.start import router as start_router
from handlers.profile import router as profile_router

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ Переменная окружения TOKEN не установлена.")

# Инициализация бота
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(profile_router)

# Lifespan вместо устаревшего on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

# FastAPI app
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

# Запуск Telegram-бота
@app.on_event("startup")
async def start_bot():
    import asyncio
    asyncio.create_task(dp.start_polling(bot))
