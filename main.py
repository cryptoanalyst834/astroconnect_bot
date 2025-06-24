import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from config import TOKEN
from database import init_db
from handlers.start import router as start_router
from handlers.profile import router as profile_router
from api import api_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание экземпляра бота и диспетчера
bot = Bot(token=TOKEN, default=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start_router)
dp.include_router(profile_router)

# Lifespan (инициализация БД при старте FastAPI)
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

# FastAPI-приложение
app = FastAPI(lifespan=lifespan)

# Настройка CORS (для мини-приложения)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Заменить на домен фронтенда в проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутер API
app.include_router(api_router)

# Команды бота (при старте)
async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="🚀 Начать работу"),
        BotCommand(command="/edit", description="✏️ Редактировать анкету"),
    ]
    await bot.set_my_commands(commands)

# Фоновая задача запуска бота
async def start_bot():
    await set_default_commands(bot)
    await dp.start_polling(bot)

# Запуск бота в фоне при запуске FastAPI
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())
