import os
import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, DATABASE_URL
from database import init_db
from api.routes import router as api_router
from handlers.start import router as start_router
from handlers.profile import router as profile_router

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
# Регистрируем все routers
dp.include_router(start_router)
dp.include_router(profile_router)

# Lifespan для FastAPI — инициализируем БД и запускаем polling в фоне
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Инициализируем базу
    logger.info("Инициализация БД...")
    await init_db()
    # 2. Запускаем polling в фоне
    logger.info("Старт polling Telegram-бота...")
    asyncio.create_task(dp.start_polling(bot))
    yield
    # 3. Опционально: здесь можно очищать ресурсы
    logger.info("Завершение lifespan.")

# Создаём FastAPI с кастомным lifespan
app = FastAPI(lifespan=lifespan)
# Подключаем ваш API-router (ping, профили и т.д.)
app.include_router(api_router, prefix="/api")

# Дополнительный «корневой» эндпоинт
@app.get("/")
async def root():
    return {"status": "ok", "service": "AstroConnect"}
