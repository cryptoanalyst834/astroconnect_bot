import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import init_db, async_session
from models import UserProfile
from astro_utils import generate_natal_chart
from sqlalchemy.future import select

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

bot: Bot = None
dp: Dispatcher = None

class Form(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_place = State()
    photo = State()

def register_handlers(dp: Dispatcher):
    @dp.message(F.text == "/start")
    async def cmd_start(message: Message, state: FSMContext):
        logger.info(f"/start от {message.from_user.id}")
        await message.answer("Привет! Давай создадим твою анкету. Как тебя зовут?")
        await state.set_state(Form.name)

    @dp.message(Form.name)
    async def process_name(message: Message, state: FSMContext):
        logger.info(f"Имя от {message.from_user.id}: {message.text}")
        await state.update_data(name=message.text)
        await message.answer("Укажи дату рождения (ДД.ММ.ГГГГ):")
        await state.set_state(Form.birth_date)

    @dp.message(Form.birth_date)
    async def process_birth_date(message: Message, state: FSMContext):
        logger.info(f"Дата рождения от {message.from_user.id}: {message.text}")
        await state.update_data(birth_date=message.text)
        await message.answer("Время рождения (например 14:30):")
        await state.set_state(Form.birth_time)

    @dp.message(Form.birth_time)
    async def process_birth_time(message: Message, state: FSMContext):
        logger.info(f"Время рождения от {message.from_user.id}: {message.text}")
        await state.update_data(birth_time=message.text)
        await message.answer("Город рождения:")
        await state.set_state(Form.birth_place)

    @dp.message(Form.birth_place)
    async def process_birth_place(message: Message, state: FSMContext):
        logger.info(f"Город от {message.from_user.id}: {message.text}")
        await state.update_data(birth_place=message.text)
        await message.answer("Отправь свою фотографию:")
        await state.set_state(Form.photo)

    @dp.message(Form.photo, F.photo)
    async def process_photo(message: Message, state: FSMContext):
        logger.info(f"Фото получено от {message.from_user.id}")
        photo = message.photo[-1]
        file_id = photo.file_id
        data = await state.get_data()

        try:
            natal_data = await generate_natal_chart(
                data["birth_date"], data["birth_time"], data["birth_place"]
            )
            logger.info(f"Натальная карта: {natal_data}")
        except Exception as e:
            logger.error(f"Ошибка генерации карты: {e}")
            await message.answer("Ошибка при расчёте натальной карты. Попробуй позже.")
            return

        try:
            file_info = await bot.get_file(file_id)
            photo_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        except Exception as e:
            logger.error(f"Ошибка получения photo_url: {e}")
            photo_url = ""

        try:
            async with async_session() as session:
                profile = UserProfile(
                    telegram_id=message.from_user.id,
                    name=data["name"],
                    birth_date=data["birth_date"],
                    birth_time=data["birth_time"],
                    birth_place=data["birth_place"],
                    photo_id=file_id,
                    photo_url=photo_url,
                    zodiac=natal_data["zodiac"],
                    ascendant=natal_data["ascendant"]
                )
                session.add(profile)
                await session.commit()
                logger.info(f"Анкета {profile.name} сохранена")
        except Exception as e:
            logger.error(f"Ошибка при сохранении анкеты: {e}")
            await message.answer("Ошибка при сохранении анкеты.")
            return

        await message.answer(
            f"Анкета сохранена! Ты — {natal_data['zodiac']}, асцендент {natal_data['ascendant']}."
        )
        await state.clear()

@app.get("/profiles")
async def get_profiles():
    logger.info("GET /profiles")
    try:
        async with async_session() as session:
            result = await session.execute(select(UserProfile))
            profiles = result.scalars().all()
            logger.info(f"Отдано анкет: {len(profiles)}")
            return JSONResponse(content=[profile.to_dict() for profile in profiles])
    except Exception as e:
        logger.error(f"Ошибка API /profiles: {e}")
        return JSONResponse(content={"error": "Ошибка на сервере"}, status_code=500)

async def main():
    global bot, dp
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN не задан")

    bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    register_handlers(dp)
    await init_db()
    logger.info("База данных инициализирована")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
