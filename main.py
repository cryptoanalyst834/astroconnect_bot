import os
import logging
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация Telegram-бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот AstroConnect 🚀")

# Lifespan context (вместо @app.on_event("startup"))
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запускаем бота в фоне
    import asyncio
    asyncio.create_task(dp.start_polling(bot))
    yield

# Инициализация FastAPI
app = FastAPI(title="AstroConnect API", lifespan=lifespan)

# FastAPI API роутер
from api.router import api_router
app.include_router(api_router)
