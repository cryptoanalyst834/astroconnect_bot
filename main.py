import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import setup_application

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import create_db_and_tables, save_user_profile, get_all_profiles
from astro_utils import generate_natal_chart
from models import UserProfile

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Form(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_place = State()
    photo = State()

@dp.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Давай создадим твою анкету. Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажи дату рождения (в формате ДД.ММ.ГГГГ):")
    await state.set_state(Form.birth_date)

@dp.message(Form.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Время рождения (например 14:30):")
    await state.set_state(Form.birth_time)

@dp.message(Form.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Город рождения:")
    await state.set_state(Form.birth_place)

@dp.message(Form.birth_place)
async def process_birth_place(message: Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    await message.answer("Отправь свою фотографию:")
    await state.set_state(Form.photo)

@dp.message(Form.photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    data = await state.get_data()

    natal_data = generate_natal_chart(
        data["birth_date"], data["birth_time"], data["birth_place"]
    )

    profile = UserProfile(
        telegram_id=message.from_user.id,
        name=data["name"],
        birth_date=data["birth_date"],
        birth_time=data["birth_time"],
        birth_place=data["birth_place"],
        photo_id=file_id,
        zodiac=natal_data["zodiac"],
        ascendant=natal_data["ascendant"]
    )
    await save_user_profile(profile)
    await message.answer(f"Анкета сохранена! Ты — {natal_data['zodiac']}, асцендент {natal_data['ascendant']}.")
    await state.clear()

@app.get("/profiles")
async def get_profiles():
    profiles = await get_all_profiles()
    return JSONResponse(content=[profile.model_dump() for profile in profiles])

async def main():
    await create_db_and_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
