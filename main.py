import asyncio
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers.start import router as start_router
from handlers.profile import router as profile_router
from api.router import api_router

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start_router)
dp.include_router(profile_router)

app = FastAPI()
app.include_router(api_router)

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(dp.start_polling(bot))
