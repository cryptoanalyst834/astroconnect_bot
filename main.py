import os
import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from astro_utils import generate_natal_chart
from database import create_db_and_tables, save_user
from models import User

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Инициализация компонентов
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()

# Настройки CORS (если frontend подключается отдельно)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Состояния формы
class Form(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_place = State()

# Обработчики Telegram-бота
@dp.message(F.text, Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажи дату рождения (дд.мм.гггг):")
    await state.set_state(Form.birth_date)

@dp.message(Form.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Во сколько ты родился? (чч:мм):")
    await state.set_state(Form.birth_time)

@dp.message(Form.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Где ты родился?")
    await state.set_state(Form.birth_place)

@dp.message(Form.birth_place)
async def process_birth_place(message: Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    data = await state.get_data()

    try:
        sun_sign, asc_sign = generate_natal_chart(
            data['birth_date'], data['birth_time'], data['birth_place']
        )

        user = User(
            telegram_id=str(message.from_user.id),
            name=data['name'],
            birth_date=data['birth_date'],
            birth_time=data['birth_time'],
            birth_place=data['birth_place'],
            sun_sign=sun_sign,
            asc_sign=asc_sign
        )
        await save_user(user)

        await message.answer(f"🌞 Солнце: {sun_sign}\n🔭 Асцендент: {asc_sign}")
    except Exception as e:
        await message.answer("Ошибка при расчёте натальной карты. Попробуй ещё раз.")
        print(e)

    await state.clear()

# Запуск FastAPI + Telegram polling
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    asyncio.create_task(dp.start_polling(bot))
