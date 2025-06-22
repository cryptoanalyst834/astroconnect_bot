import os
import json
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
import asyncpg
import asyncio

# Загружаем переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Инициализация
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# Состояния
class Form(StatesGroup):
    birth_date = State()
    birth_time = State()
    birth_city = State()
    photo = State()

# Подключение к БД
async def get_db():
    return await asyncpg.connect(DATABASE_URL)

# Расчёт натальной карты
def generate_chart(birth_date: str, birth_time: str):
    dt = Datetime(f"{birth_date}", f"{birth_time}", '+03:00')
    pos = GeoPos('55n45', '37e34')  # Москва по умолчанию
    chart = Chart(dt, pos)
    return {obj.id: obj.sign for obj in chart.objects}

# Команда /start
@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Введи свою дату рождения (ГГГГ-ММ-ДД):")
    await state.set_state(Form.birth_date)

# Получение даты
@router.message(Form.birth_date)
async def process_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Теперь время рождения (ЧЧ:ММ):")
    await state.set_state(Form.birth_time)

# Получение времени
@router.message(Form.birth_time)
async def process_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Город рождения?")
    await state.set_state(Form.birth_city)

# Город
@router.message(Form.birth_city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(birth_city=message.text)
    await message.answer("Пришли своё фото:")
    await state.set_state(Form.photo)

# Фото
@router.message(Form.photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()
    
    chart = generate_chart(data['birth_date'], data['birth_time'])

    # Сохраняем в БД
    conn = await get_db()
    await conn.execute('''
        INSERT INTO users (telegram_id, birth_date, birth_time, birth_city, photo, natal_chart)
        VALUES ($1, $2, $3, $4, $5, $6)
    ''', str(message.from_user.id), data['birth_date'], data['birth_time'],
         data['birth_city'], photo_file_id, json.dumps(chart))
    await conn.close()

    await message.answer("Спасибо! Данные и натальная карта сохранены.")
    await state.clear()

# FastAPI
app = FastAPI()

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.get("/profiles")
async def get_profiles():
    conn = await get_db()
    rows = await conn.fetch("SELECT telegram_id, birth_date, birth_time, birth_city, natal_chart FROM users")
    await conn.close()
    return JSONResponse([dict(row) for row in rows])

# Запуск
async def main():
    tg_task = asyncio.create_task(dp.start_polling(bot))
    api_task = asyncio.create_task(uvicorn.run(app, host="0.0.0.0", port=8000))
    await asyncio.gather(tg_task, api_task)

if __name__ == "__main__":
    asyncio.run(main())
