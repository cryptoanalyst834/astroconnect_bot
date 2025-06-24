import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from fastapi import FastAPI
from database import init_db, add_user_profile, get_all_profiles
from astro_utils import generate_astrology_data
from dotenv import load_dotenv
from models import UserProfile

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

app = FastAPI()

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_birthdate = State()
    waiting_for_birthtime = State()
    waiting_for_birthplace = State()

@dp.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    text = (
        "<b>Добро пожаловать в AstroConnect \u2728</b>\n\n"
        "Это AI-сервис знакомств на основе астрологической совместимости.\n\n"
        "\ud83d\udcc5 Мы рассчитываем натальную карту\n"
        "\ud83d\ude0d Подбираем совместимых партнёров\n"
        "\ud83e\udeaa Помогаем понять себя и свои сильные стороны\n\n"
        "Чтобы начать, напишите своё <b>имя</b>."
    )
    await message.answer(text, parse_mode="HTML")
    await state.set_state(Registration.waiting_for_name)

@dp.message(Registration.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Укажи дату рождения в формате ГГГГ-ММ-ДД")
    await state.set_state(Registration.waiting_for_birthdate)

@dp.message(Registration.waiting_for_birthdate)
async def get_birthdate(message: Message, state: FSMContext):
    await state.update_data(birthdate=message.text.strip())
    await message.answer("Укажи точное время рождения (например, 14:30)")
    await state.set_state(Registration.waiting_for_birthtime)

@dp.message(Registration.waiting_for_birthtime)
async def get_birthtime(message: Message, state: FSMContext):
    await state.update_data(birthtime=message.text.strip())
    await message.answer("И последнее — напиши город рождения")
    await state.set_state(Registration.waiting_for_birthplace)

@dp.message(Registration.waiting_for_birthplace)
async def get_birthplace(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    birthdate = data['birthdate']
    birthtime = data['birthtime']
    birthplace = message.text.strip()

    astro_data = await generate_astrology_data(birthdate, birthtime, birthplace)

    user = await add_user_profile(
        name=name,
        birth_date=birthdate,
        birth_time=birthtime,
        birth_place=birthplace,
        sun_sign=astro_data['sun_sign'],
        ascendant=astro_data['ascendant']
    )

    await message.answer(
        f"Спасибо, {name}!\n"
        f"\n<code>\u2609 Солнце в: {astro_data['sun_sign']}\n"
        f"\u2191 Асцендент: {astro_data['ascendant']}</code>\n\n"
        "Ты успешно зарегистрирован в системе \U0001F973",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()

@app.get("/profiles")
async def profiles():
    return await get_all_profiles()

async def on_startup():
    await init_db()
    print("Bot is ready.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))
    loop.run_until_complete(on_startup())
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
