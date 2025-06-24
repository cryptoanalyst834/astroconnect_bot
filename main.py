import os
import logging
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", "PLACEHOLDER_TOKEN")

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация FastAPI
app = FastAPI(title="AstroConnect API")

# Инициализация Telegram-бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

# Роутинг FastAPI
from api.router import api_router
app.include_router(api_router)

# Хэндлеры Telegram-бота
@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот AstroConnect 🚀")

# Фоновый запуск бота при старте FastAPI
@app.on_event("startup")
async def on_startup():
    import asyncio
    asyncio.create_task(dp.start_polling(bot))
