from aiogram import Bot, Dispatcher
import os

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router  # импортируем маршруты

# Инициализация бота
bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Подключаем маршрутизатор
dp.include_router(router)
