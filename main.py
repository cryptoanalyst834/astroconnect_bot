# main.py

import os
import logging
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update

from config import TOKEN, RAILWAY_APP_URL
from database import init_db
from handlers.start   import router as start_router
from handlers.profile import router as profile_router
from api.routes       import router as api_router

# Загрузка .env (для локальной отладки)
load_dotenv()

if not TOKEN or not RAILWAY_APP_URL:
    raise RuntimeError("❌ Нужны TOKEN и RAILWAY_APP_URL в окружении")

WEBHOOK_PATH = f"/telegram/{TOKEN}"
WEBHOOK_URL  = f"https://{RAILWAY_APP_URL}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаём экземпляры Bot и Dispatcher
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# Регистрируем роутеры aiogram
dp.include_router(start_router)
dp.include_router(profile_router)

# Lifespan — инициализация БД и установка web-hook’а
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1) Инициализация БД
    logger.info("Инициализация базы данных...")
    await init_db()

    # 2) Установка webhook в Telegram
    logger.info(f"Установка webhook: {WEBHOOK_URL}")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)

    # 3) Запуск polling в фоне (на всякий случай, если понадобится)
    asyncio.create_task(dp.start_polling(bot))

    yield

    # 4) Очистка при shutdown
    logger.info("Удаление webhook...")
    await bot.delete_webhook()

# --- ЗДЕСЬ определяем FastAPI и регистрируем всё! ---
app = FastAPI(lifespan=lifespan, title="AstroConnect Webhook API")

# Подключаем HTTP-роуты вашего API
app.include_router(api_router, prefix="/api", tags=["profiles"])

# Точка входа для Telegram Webhook
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    try:
        update = Update.model_validate(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid update: {e}")
    await dp.feed_update(bot, update)
    return {"ok": True}

# Health-check
@app.get("/ping")
async def ping():
    return {"status": "ok"}
