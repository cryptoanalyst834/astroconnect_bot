
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import APIRouter
import os
from db import add_user_to_db
from astro_utils import generate_natal_chart

router = APIRouter()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_gender = State()
    waiting_for_birth_date = State()
    waiting_for_birth_time = State()
    waiting_for_birth_city = State()
    waiting_for_location_city = State()
    waiting_for_looking_for = State()
    waiting_for_about = State()
    waiting_for_photo = State()

@dp.message(F.text, commands=["start"])
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Привет! Давай начнём регистрацию. Как тебя зовут?")
    await state.set_state(Registration.waiting_for_name)

@dp.message(Registration.waiting_for_name)
async def name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажи свой пол (м/ж):")
    await state.set_state(Registration.waiting_for_gender)

@dp.message(Registration.waiting_for_gender)
async def gender_handler(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Дата рождения (в формате ГГГГ-ММ-ДД):")
    await state.set_state(Registration.waiting_for_birth_date)

@dp.message(Registration.waiting_for_birth_date)
async def birth_date_handler(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Время рождения (часы:минуты, например 14:30):")
    await state.set_state(Registration.waiting_for_birth_time)

@dp.message(Registration.waiting_for_birth_time)
async def birth_time_handler(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Город рождения:")
    await state.set_state(Registration.waiting_for_birth_city)

@dp.message(Registration.waiting_for_birth_city)
async def birth_city_handler(message: Message, state: FSMContext):
    await state.update_data(birth_city=message.text)
    await message.answer("Где ты сейчас живешь?")
    await state.set_state(Registration.waiting_for_location_city)

@dp.message(Registration.waiting_for_location_city)
async def location_city_handler(message: Message, state: FSMContext):
    await state.update_data(location_city=message.text)
    await message.answer("Кого ты ищешь? (например, парня, девушку, друга):")
    await state.set_state(Registration.waiting_for_looking_for)

@dp.message(Registration.waiting_for_looking_for)
async def looking_for_handler(message: Message, state: FSMContext):
    await state.update_data(looking_for=message.text)
    await message.answer("Расскажи немного о себе:")
    await state.set_state(Registration.waiting_for_about)

@dp.message(Registration.waiting_for_about)
async def about_handler(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("Отправь свою фотографию:")
    await state.set_state(Registration.waiting_for_photo)

@dp.message(Registration.waiting_for_photo, F.photo)
async def photo_handler(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    data = await state.get_data()
    await message.answer("Спасибо! Обрабатываем анкету...")

    chart = generate_natal_chart(data["birth_date"], data["birth_time"], data["birth_city"])

    await add_user_to_db(
        telegram_id=message.from_user.id,
        name=data["name"],
        gender=data["gender"],
        birth_date=data["birth_date"],
        birth_time=data["birth_time"],
        birth_city=data["birth_city"],
        location_city=data["location_city"],
        looking_for=data["looking_for"],
        about=data["about"],
        photo=photo_id,
        chart=chart
    )

    await message.answer("Готово! Анкета добавлена 🎉")
    await state.clear()
