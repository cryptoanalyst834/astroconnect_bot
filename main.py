import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart

TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
DOMAIN = os.getenv("RAILWAY_PUBLIC_DOMAIN")
WEBHOOK_URL = f"https://{DOMAIN}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()

WELCOME_TEXT = """
<b>Добро пожаловать в AstroConnect!</b>

Мы анализируем дату, время и место рождения, чтобы находить максимально совместимых партнёров.

AstroConnect поможет:
— Найти подходящего человека по звёздам
— Избежать токсичных связей
— Понять, кто вам действительно подходит
— Раскрыть сильные стороны личности

Вы в надёжных астрологических руках. Готовы начать?
"""

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Начать регистрацию", callback_data="start_registration")]
    ]
)

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=start_keyboard, parse_mode="HTML")

@app.on_event("startup")
async def on_startup():
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
