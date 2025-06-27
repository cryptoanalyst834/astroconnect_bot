import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import CommandStart

TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
# Пример: "astroconnectbot-production.up.railway.app"
DOMAIN = os.getenv("RAILWAY_PUBLIC_DOMAIN")
WEBHOOK_URL = f"https://{DOMAIN}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

app = FastAPI()

# --- aiogram handlers ---
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Бот работает через webhook на Railway 🚀")

# --- Webhook endpoints ---
@app.on_event("startup")
async def on_startup():
    # Важно: выставляем webhook только когда Railway поднимает сервер
    await bot.set_webhook(WEBHOOK_URL)
    print("Webhook установлен:", WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    print("Webhook удалён!")

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    update = types.Update(**await request.json())
    await dp.feed_update(bot, update)
    return {"ok": True}
