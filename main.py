import os
import logging
import asyncio
from typing import List

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold
from aiogram.types import FSInputFile
from aiogram import Router

from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models import Base, UserProfile
from database import add_user_profile, get_all_profiles
from astro_utils import generate_astrology_data

load_dotenv()

# === Логгер ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Telegram bot ===
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# === FastAPI ===
app = FastAPI()

# === Database ===
DATABASE_URL = os.getenv("DATABASE_URL")
async_engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# === Handlers ===
@router.message(F.text == "/start")
async def cmd_start(message: Message):
    welcome_text = (
        f"\U0001F4AB <b>Добро пожаловать в AstroConnect</b>!\n\n"
        "Это астрологический сервис знакомств,\n"
        "где вы можете найти свою идеальную пару по звёздам.\n\n"
        "Что умеет бот:\n"
        "\u2022 Рассчитывает натальную карту\n"
        "\u2022 Анализирует астрологическую совместимость\n"
        "\u2022 Помогает найти подходящего партнёра по дате рождения\n\n"
        "Отправьте свою дату рождения, время и город — и мы начнём!"
    )
    await message.answer(welcome_text)

@router.message()
async def handle_profile(message: Message):
    try:
        # Предполагаем, что пользователь присылает дату, время и город
        user_input = message.text.strip()
        birth_date, birth_time, city = [x.strip() for x in user_input.split(",")]

        # Генерация астрологических данных
        astro_data = await generate_astrology_data(birth_date, birth_time, city)

        # Сохранение в БД
        async with async_session() as session:
            profile = UserProfile(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                birth_date=birth_date,
                birth_time=birth_time,
                city=city,
                sun_sign=astro_data["sun_sign"],
                ascendant=astro_data["ascendant"]
            )
            await add_user_profile(session, profile)

        response = (
            f"<b>Ваша натальная карта:</b>\n"
            f"Знак Солнца: {astro_data['sun_sign']}\n"
            f"Асцендент: {astro_data['ascendant']}\n\n"
            "Вы успешно добавлены в AstroConnect! \U0001F48D"
        )
        await message.answer(response)

    except Exception as e:
        logger.exception("Ошибка при обработке профиля")
        await message.answer("Пожалуйста, отправьте данные в формате: \n<дата рождения>, <время>, <город>")

# === FastAPI routes ===
@app.get("/profiles", response_model=List[dict])
async def get_profiles():
    async with async_session() as session:
        result = await get_all_profiles(session)
        return result

@app.post("/profile")
async def create_profile(profile: dict):
    async with async_session() as session:
        await add_user_profile(session, profile)
        return {"status": "ok"}

# === DB init ===
async def on_startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("База данных инициализирована.")

# === Run bot and API ===
async def main():
    await on_startup()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import uvicorn
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # запуск бота
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
