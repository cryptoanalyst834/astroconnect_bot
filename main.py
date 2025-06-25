# main.py

import os
import logging
from api.routes import router as api_router
app.include_router(api_router)
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.client.default import DefaultBotProperties

# Загрузка .env
load_dotenv()
TOKEN        = os.getenv("TOKEN")
RAILWAY_APP  = os.getenv("RAILWAY_APP_URL")  # без https://
if not TOKEN or not RAILWAY_APP:
    raise RuntimeError("❌ Нужно задать TOKEN и RAILWAY_APP_URL в окружении")

# Путь для webhook и его публичный URL
WEBHOOK_PATH = f"/telegram/{TOKEN}"
WEBHOOK_URL  = f"https://{RAILWAY_APP}{WEBHOOK_PATH}"

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp  = Dispatcher()

# Подключаем ваши роутеры хэндлеров
from handlers.start   import router as start_router
from handlers.profile import router as profile_router
dp.include_router(start_router)
dp.include_router(profile_router)

# FastAPI-приложение
app = FastAPI(title="AstroConnect Webhook")

@app.on_event("startup")
async def on_startup():
    # Удаляем старый webhook и все ожидающие обновления
    await bot.delete_webhook(drop_pending_updates=True)
    # Устанавливаем новый webhook на Railway URL
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook установлен: {WEBHOOK_URL}")

@app.on_event("shutdown")
async def on_shutdown():
    # Удаляем webhook при остановке
    await bot.delete_webhook()

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    # Принимем JSON от Telegram, прокинем его в Aiogram
    data = await request.json()
    try:
        update = Update.model_validate(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid update: {e}")
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/ping")
async def ping():
    return {"status": "ok"}
