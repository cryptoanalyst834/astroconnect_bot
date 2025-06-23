import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from fastapi import FastAPI
from astro_utils import generate_natal_chart
from database import create_db_and_tables, save_user
from models import User

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Проверка переменной окружения
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в .env файле")

# Инициализация FastAPI и Aiogram
app = FastAPI()
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Состояния FSM
class Form(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_place = State()

# Обработка команды /start
@dp.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажи дату рождения (дд.мм.гггг):")
    await state.set_state(Form.birth_date)

@dp.message(Form.birth_date)
async def get_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Укажи время рождения (чч:мм):")
    await state.set_state(Form.birth_time)

@dp.message(Form.birth_time)
async def get_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Где ты родился?")
    await state.set_state(Form.birth_place)

@dp.message(Form.birth_place)
async def get_place(message: Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    data = await state.get_data()

    try:
        sun, asc = generate_natal_chart(
            data['birth_date'], data['birth_time'], data['birth_place']
        )
    except Exception as e:
        await message.answer("Произошла ошибка при расчёте натальной карты. Проверь введённые данные.")
        return

    new_user = User(
        telegram_id=str(message.from_user.id),
        name=data['name'],
        birth_date=data['birth_date'],
        birth_time=data['birth_time'],
        birth_place=data['birth_place'],
        sun_sign=sun,
        asc_sign=asc
    )

    await save_user(new_user)
    await message.answer(f"Готово! 🌞 Солнце в знаке: {sun}, Асцендент: {asc}")
    await state.clear()

# Запуск при старте FastAPI
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    asyncio.create_task(dp.start_polling(bot))
