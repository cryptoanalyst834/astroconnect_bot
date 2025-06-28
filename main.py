import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from config import TOKEN, RAILWAY_APP_URL, FRONTEND_URL
from database import init_db
from api import api_router
from handlers.profile import router as profile_router

logging.basicConfig(level=logging.INFO)

# --- FastAPI app setup ---
app = FastAPI()

# --- CORS для miniapp ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "https://astroconnectminiapp.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(api_router)
# (можно добавить дополнительные api-роутеры если нужно)
# app.include_router(other_router)

# --- Telegram Bot ---
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(profile_router)

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
async def start_handler(message: types.Message):
    await message.answer(WELCOME_TEXT, reply_markup=start_keyboard, parse_mode="HTML")

@dp.callback_query(F.data == "start_registration")
async def registration_callback(callback: CallbackQuery):
    await callback.message.answer("Давай начнём регистрацию!\n\nКак тебя зовут?")
    await callback.answer()

# --- FastAPI startup/shutdown ---
@app.on_event("startup")
async def on_startup():
    await init_db()
    webhook_url = f"{RAILWAY_APP_URL}/webhook"
    await bot.set_webhook(webhook_url)
    logging.info(f"Webhook установлен на {webhook_url}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    logging.info("Webhook удалён")

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = types.Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}
