import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from database import async_main, get_all_profiles
from astro_utils import calculate_astrology_data
from models import UserProfile

# Загрузка переменных окружения
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан")

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram-бот
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# FastAPI-приложение
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Обработка /start
@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать в AstroConnect! ✨\n\n"
        "Пожалуйста, введите вашу дату рождения в формате: ДД.ММ.ГГГГ ЧЧ:ММ"
    )


# Пример обработки текстового сообщения
@dp.message(F.text.regexp(r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}"))
async def handle_birth_input(message: Message):
    try:
        astro_data = calculate_astrology_data(message.text)
        await message.answer(f"Натальная карта:\n\n{astro_data}")
    except Exception as e:
        logger.error(f"Ошибка при расчете карты: {e}")
        await message.answer("Ошибка при расчете натальной карты. Попробуйте снова.")


# FastAPI endpoint для анкет
@app.get("/profiles")
async def get_profiles():
    try:
        profiles = await get_all_profiles()
        return {"profiles": [profile.to_dict() for profile in profiles]}
    except Exception as e:
        logger.error(f"Ошибка при получении анкет: {e}")
        return {"error": str(e)}


async def main():
    logger.info("Запуск бота и инициализация БД...")
    await async_main()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
