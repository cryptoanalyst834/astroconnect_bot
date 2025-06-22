import os
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from database import create_users_table, save_user, get_all_users
from astro_utils import generate_natal_chart
from states import Form

TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# --- FastAPI ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.get("/profiles")
async def get_profiles():
    users = get_all_users()
    return JSONResponse(content=users)

# --- Telegram Bot ---
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Привет! Как тебя зовут?")

@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.gender)
    await message.answer("Укажи пол (м/ж):")

@dp.message(Form.gender)
async def process_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Form.birth_date)
    await message.answer("Дата рождения (ГГГГ-ММ-ДД):")

@dp.message(Form.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await state.set_state(Form.birth_time)
    await message.answer("Время рождения (чч:мм):")

@dp.message(Form.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await state.set_state(Form.birth_city)
    await message.answer("Город рождения:")

@dp.message(Form.birth_city)
async def process_birth_city(message: Message, state: FSMContext):
    await state.update_data(birth_city=message.text)
    await state.set_state(Form.location_city)
    await message.answer("Где ты сейчас живёшь?")

@dp.message(Form.location_city)
async def process_location_city(message: Message, state: FSMContext):
    await state.update_data(location_city=message.text)
    await state.set_state(Form.looking_for)
    await message.answer("Кого ты ищешь?")

@dp.message(Form.looking_for)
async def process_looking_for(message: Message, state: FSMContext):
    await state.update_data(looking_for=message.text)
    await state.set_state(Form.about)
    await message.answer("Расскажи о себе:")

@dp.message(Form.about)
async def process_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await state.set_state(Form.photo)
    await message.answer("Пришли свою фотографию:")

@dp.message(Form.photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()

    natal_chart = generate_natal_chart(
        birth_date=data["birth_date"],
        birth_time=data["birth_time"],
        city=data["birth_city"]
    )

    save_user({
        "telegram_id": message.from_user.id,
        "name": data["name"],
        "gender": data["gender"],
        "birth_date": data["birth_date"],
        "birth_time": data["birth_time"],
        "birth_city": data["birth_city"],
        "location_city": data["location_city"],
        "looking_for": data["looking_for"],
        "about": data["about"],
        "photo": photo_file_id,
        "natal_chart": natal_chart
    })

    await message.answer("Спасибо! Твоя анкета сохранена.")
    await state.clear()

# Запуск бота и FastAPI
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_users_table()
    asyncio.create_task(dp.start_polling(bot))
    yield

app.router.lifespan_context = lifespan
