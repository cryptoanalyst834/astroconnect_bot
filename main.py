import logging
import asyncio
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from database import init_db, add_user_profile, get_all_profiles
from astro_utils import generate_astrology_data
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

# Состояния анкеты
class Form(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_place = State()
    about = State()
    photo = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    text = (
        "✨ <b>Добро пожаловать в AstroConnect</b> — астрологический бот знакомств!\n\n"
        "🔮 Мы подбираем совместимых партнёров по натальной карте и вашей уникальной энергии.\n"
        "❤️‍🔥 Закройте боль одиночества, узнайте, кто идеально вам подойдёт по звёздам.\n\n"
        "💫 Давайте начнём! Как вас зовут?"
    )
    await message.answer(text)
    await state.set_state(Form.name)

@router.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📅 Укажите дату рождения (в формате ДД.ММ.ГГГГ):")
    await state.set_state(Form.birth_date)

@router.message(Form.birth_date)
async def get_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("⏰ Укажите время рождения (в формате ЧЧ:ММ):")
    await state.set_state(Form.birth_time)

@router.message(Form.birth_time)
async def get_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("🌍 Укажите место рождения (город):")
    await state.set_state(Form.birth_place)

@router.message(Form.birth_place)
async def get_birth_place(message: Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    await message.answer("🧘‍♀️ Расскажите немного о себе:")
    await state.set_state(Form.about)

@router.message(Form.about)
async def get_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("📸 Пришлите свою фотографию:")
    await state.set_state(Form.photo)

@router.message(Form.photo)
async def get_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фотографию.")
        return

    photo_id = message.photo[-1].file_id
    data = await state.get_data()

    astrology = await generate_astrology_data(
        data["birth_date"], data["birth_time"], data["birth_place"]
    )

    await add_user_profile(
        telegram_id=message.from_user.id,
        name=data["name"],
        birth_date=data["birth_date"],
        birth_time=data["birth_time"],
        birth_place=data["birth_place"],
        about=data["about"],
        photo_file_id=photo_id,
        astrology=astrology
    )

    await message.answer("🌟 Спасибо! Ваша анкета сохранена. Мы подберём для вас совместимых партнёров!")
    await state.clear()

# FastAPI для мини-приложения
app = FastAPI()

@app.get("/profiles")
async def profiles():
    profiles = await get_all_profiles()
    return profiles

# Запуск
async def on_startup():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(on_startup())
