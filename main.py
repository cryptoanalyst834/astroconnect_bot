import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from database import init_db, add_user_profile, get_all_profiles
from astro_utils import generate_astrology_data

load_dotenv()

# Telegram bot setup
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# FastAPI
app = FastAPI()

# Database
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


# FSM для регистрации анкеты
class ProfileState(StatesGroup):
    name = State()
    birthdate = State()
    birthtime = State()
    birthcity = State()
    photo = State()


@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Давай создадим твою астрологическую анкету.\nКак тебя зовут?")
    await state.set_state(ProfileState.name)


@dp.message(ProfileState.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажи дату рождения (в формате ДД.ММ.ГГГГ):")
    await state.set_state(ProfileState.birthdate)


@dp.message(ProfileState.birthdate)
async def get_birthdate(message: Message, state: FSMContext):
    await state.update_data(birthdate=message.text)
    await message.answer("Укажи время рождения (в формате ЧЧ:ММ):")
    await state.set_state(ProfileState.birthtime)


@dp.message(ProfileState.birthtime)
async def get_birthtime(message: Message, state: FSMContext):
    await state.update_data(birthtime=message.text)
    await message.answer("Укажи город рождения:")
    await state.set_state(ProfileState.birthcity)


@dp.message(ProfileState.birthcity)
async def get_birthcity(message: Message, state: FSMContext):
    await state.update_data(birthcity=message.text)
    await message.answer("Отправь свою фотографию:")
    await state.set_state(ProfileState.photo)


@dp.message(ProfileState.photo)
async def get_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, пришли фотографию.")
        return

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = f"photos/{photo.file_id}.jpg"
    await bot.download_file(file.file_path, file_path)

    data = await state.get_data()
    astrology = generate_astrology_data(
        birthdate=data["birthdate"],
        birthtime=data["birthtime"],
        city=data["birthcity"]
    )

    async with async_session() as session:
        await add_user_profile(
            session=session,
            name=data["name"],
            birthdate=data["birthdate"],
            birthtime=data["birthtime"],
            city=data["birthcity"],
            zodiac=astrology["zodiac_sign"],
            ascendant=astrology["ascendant"],
            photo_path=file_path
        )

    await message.answer(
        f"Анкета создана!\n\n"
        f"<b>Имя:</b> {data['name']}\n"
        f"<b>Знак Зодиака:</b> {astrology['zodiac_sign']}\n"
        f"<b>Асцендент:</b> {astrology['ascendant']}"
    )
    await state.clear()


# FastAPI endpoint для отдачи анкет фронтенду
@app.get("/profiles")
async def get_profiles():
    async with async_session() as session:
        profiles = await get_all_profiles(session)
        return profiles


# Запуск Telegram-бота
async def main():
    await init_db(engine)
    await dp.start_polling(bot)

# Запуск FastAPI и Telegram
if __name__ == "__main__":
    import uvicorn

    async def on_startup():
        await init_db(engine)

    asyncio.run(on_startup())
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
