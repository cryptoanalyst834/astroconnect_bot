import asyncio
import os
from aiogram import Bot, Dispatcher
from handlers import router
from database import init_db
from dotenv import load_dotenv

load_dotenv()

async def main():
    await init_db()  # создаёт таблицы
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
