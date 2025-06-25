# main.py

import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.client.default import DefaultBotProperties

load_dotenv()
TOKEN = os.getenv("TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_APP_URL")  # например: astroconnectbot-production.up.railway.app
if not TOKEN or not RAILWAY_URL:
    raise RuntimeError("Не заданы TOKEN или RAILWAY_APP_URL")

WEBHOOK_PATH = f"/telegram/{TOKEN}"
WEBHOOK_URL = f"https://{RAILWAY_URL}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# подключаем роутеры хэндлеров
from handlers.start    import router as start_router
from handlers.profile  import router as profile_router
dp.include_router(start_router)
dp.include_router(profile_router)

# FastAPI
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # удалить старый webhook (на всякий случай)
    await bot.delete_webhook(drop_pending_updates=True)
    # установить новый webhook
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook установлено на {WEBHOOK_URL}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    """
    Точка входа для Telegram Webhook.
    Telegram будет шлать POST запросы сюда.
    """
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}

# Роутер для проверки
@app.get("/ping")
async def ping():
    return {"message": "pong"}

# Для локальной отладки можно запускать long-polling:
if __name__ == "__main__":
    import uvicorn
    # удобный запуск локально:
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
