import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
import uvicorn
from database import init_db
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# Инициализация FastAPI и бота
app = FastAPI()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@app.on_event("startup")
async def on_startup():
    logging.info("Starting bot and initializing DB")
    await init_db()
    asyncio.create_task(dp.start_polling(bot))

@app.get("/")
async def read_root():
    return {"message": "AstroConnect API is working!"}
