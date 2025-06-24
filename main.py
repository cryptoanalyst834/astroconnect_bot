import logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from fastapi import FastAPI
from database import async_session_maker, init_db
from models import User
from astro_utils import generate_astrology_data
from datetime import datetime
from states import RegistrationState
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()

logging.basicConfig(level=logging.INFO)

# Start
@dp.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    text = (
        "🌌 <b>Добро пожаловать в AstroConnect</b> — астрологический бот знакомств!\n\n"
        "🔮 Мы подбираем совместимые пары на основе натальной карты, времени и места рождения.\n"
        "❤️ Найди партнёра, с которым у вас настоящая космическая связь.\n\n"
        "Для начала — давай создадим твою анкету ✨\n\n"
        "Как тебя зовут?"
    )
    await state.set_state(RegistrationState.name)
    await message.answer(text)

# Имя
@dp.message(RegistrationState.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegistrationState.birth_date)
    await message.answer("📅 Введи дату рождения (ГГГГ-ММ-ДД):")

# Дата рождения
@dp.message(RegistrationState.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    try:
        birth_date = datetime.strptime(message.text, "%Y-%m-%d").date()
        await state.update_data(birth_date=birth_date.isoformat())
        await state.set_state(RegistrationState.birth_time)
        await message.answer("🕒 Введи время рождения (ЧЧ:ММ):")
    except ValueError:
        await message.answer("Неверный формат. Введи дату в формате ГГГГ-ММ-ДД.")

# Время рождения
@dp.message(RegistrationState.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    try:
        birth_time = datetime.strptime(message.text, "%H:%M").time()
        await state.update_data(birth_time=birth_time.strftime("%H:%M"))
        await state.set_state(RegistrationState.birth_place)
        await message.answer("🌍 Введи место рождения:")
    except ValueError:
        await message.answer("Неверный формат. Введи время в формате ЧЧ:ММ.")

# Место рождения
@dp.message(RegistrationState.birth_place)
async def process_birth_place(message: Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    await state.set_state(RegistrationState.photo)
    await message.answer("📸 Отправь свою фотографию для анкеты:")

# Фото и финал
@dp.message(RegistrationState.photo)
async def process_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправь именно фото.")
        return
    file_id = message.photo[-1].file_id
    data = await state.get_data()

    natal_data = generate_astrology_data(
        date_str=data["birth_date"],
        time_str=data["birth_time"],
        place=data["birth_place"]
    )

    async with async_session_maker() as session:
        user = User(
            telegram_id=message.from_user.id,
            name=data["name"],
            birth_date=data["birth_date"],
            birth_time=data["birth_time"],
            birth_place=data["birth_place"],
            zodiac=natal_data["zodiac"],
            ascendant=natal_data["ascendant"],
            photo_id=file_id
        )
        session.add(user)
        await session.commit()

    await message.answer_photo(
        photo=file_id,
        caption=(
            f"✅ <b>Анкета сохранена!</b>\n\n"
            f"Имя: {data['name']}\n"
            f"Дата рождения: {data['birth_date']} {data['birth_time']}\n"
            f"Место: {data['birth_place']}\n"
            f"Знак зодиака: {natal_data['zodiac']}\n"
            f"Асцендент: {natal_data['ascendant']}\n\n"
            f"Скоро ты сможешь просматривать совместимые анкеты 🚀"
        )
    )
    await state.clear()

@app.on_event("startup")
async def on_startup():
    await init_db()
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))
