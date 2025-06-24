import asyncio
import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN            # ← импортируем токен
from database import init_db
from api.routes import router as api_router
from handlers.start import router as start_router
from handlers.profile import router as profile_router

logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start_router)
dp.include_router(profile_router)

# Lifespan для FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()                   # ← БД тоже сразу инициализируется
    asyncio.create_task(dp.start_polling(bot))
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
