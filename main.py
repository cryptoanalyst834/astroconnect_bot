import os
import logging

from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.start import router as start_router
from handlers.profile import router as profile_router
from api.routes import router as api_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получаем токен из переменных окружения
TOKEN = os.getenv("TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# FastAPI
app = FastAPI()
app.include_router(api_router)

# Регистрация роутеров aiogram
dp.include_router(start_router)
dp.include_router(profile_router)

@app.on_event("startup")
async def on_startup():
    logging.info("Starting bot polling")
    # Стартуем aiogram в отдельном таске
    import asyncio
    asyncio.create_task(dp.start_polling(bot))

@app.get("/")
async def root():
    return {"status": "AstroConnect bot & API are running!"}
