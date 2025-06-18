import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router as handlers_router
from discover import router as discover_router
from database import init_db  # init_db() будет вызван при запуске
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Инициализация БД
    await init_db()

    # Регистрация роутеров
    dp.include_router(handlers_router)
    dp.include_router(discover_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
