import os
import logging
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = os.getenv("TOKEN")
RAILWAY_APP_URL = os.getenv("RAILWAY_APP_URL")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

app = FastAPI()

WELCOME_TEXT = "<b>Добро пожаловать...</b>"

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Начать регистрацию", callback_data="start_registration")]
    ]
)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(WELCOME_TEXT, reply_markup=start_keyboard, parse_mode="HTML")

@dp.callback_query(F.data == "start_registration")
async def registration_callback(callback: types.CallbackQuery):
    await callback.message.answer("Давай начнём регистрацию!\n\nКак тебя зовут?")
    await callback.answer()

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(f"{RAILWAY_APP_URL}/webhook")

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = types.Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}
