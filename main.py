import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
from database import init_db, add_user_profile, get_all_profiles
from models import UserProfile
from astro_utils import generate_astrology_data
from aiogram.types import FSInputFile
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from starlette.responses import JSONResponse
import os
from dotenv import load_dotenv
from states import RegistrationState

load_dotenv()

# --- Logging ---
logging.basicConfig(level=logging.INFO)

# --- Bot Setup ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher(storage=MemoryStorage())

# --- FastAPI Setup ---
app = FastAPI()

@app.get("/profiles")
async def read_profiles():
    profiles = await get_all_profiles()
    return profiles

# --- Bot Handlers ---

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    WELCOME_TEXT = (
        "✨ *Добро пожаловать в AstroConnect!* ✨\n\n"
        "🔮 Здесь ты сможешь найти совместимого партнёра по звёздам — с помощью астрологии и натальной карты.\n\n"
        "🪐 *Что умеет бот:*\n"
        "— Построить твою натальную карту\n"
        "— Сохранить анкету\n"
        "— Найти подходящих партнёров по совместимости\n\n"
        "🚀 *Готов(а) начать?* Жми /profile, чтобы заполнить анкету!"
    )
    await message.answer(WELCOME_TEXT)

@dp.message(Command("profile"))
async def create_profile(message: types.Message, state: FSMContext):
    await message.answer("Как тебя зовут?")
    await state.set_state(RegistrationState.name)

@dp.message(RegistrationState.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Когда ты родился? (в формате ДД.ММ.ГГГГ)")
    await state.set_state(RegistrationState.birth_date)

@dp.message(RegistrationState.birth_date)
async def process_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("В какое время ты родился? (например, 14:30)")
    await state.set_state(RegistrationState.birth_time)

@dp.message(RegistrationState.birth_time)
async def process_birth_time(message: types.Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Где ты родился? (город, страна)")
    await state.set_state(RegistrationState.birth_place)

@dp.message(RegistrationState.birth_place)
async def process_birth_place(message: types.Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    await message.answer("Отправь свою фотографию")
    await state.set_state(RegistrationState.photo)

@dp.message(RegistrationState.photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    await state.update_data(photo_id=file_id)

    data = await state.get_data()

    astro_data = await generate_astrology_data(
        birth_date=data["birth_date"],
        birth_time=data["birth_time"],
        birth_place=data["birth_place"]
    )

    await add_user_profile(
        telegram_id=message.from_user.id,
        name=data["name"],
        birth_date=data["birth_date"],
        birth_time=data["birth_time"],
        birth_place=data["birth_place"],
        photo_id=file_id,
        zodiac_sign=astro_data["zodiac_sign"],
        ascendant=astro_data["ascendant"]
    )

    await message.answer("✅ Анкета сохранена! Теперь ты можешь открыть мини-приложение и смотреть совместимость.")
    await state.clear()

# --- Startup ---

async def on_startup():
    await init_db()
    logging.info("Bot and DB initialized")

if __name__ == "__main__":
    asyncio.run(on_startup())
    dp.run_polling(bot)
