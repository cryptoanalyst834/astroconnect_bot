import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import uvicorn

from handlers import router
from datetime import datetime

# Telegram bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

# FastAPI backend
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # укажи конкретный frontend-домен для безопасности
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")

@app.on_event("startup")
async def on_startup():
    app.state.db = await asyncpg.connect(DATABASE_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await app.state.db.close()

@app.get("/profiles")
async def get_profiles():
    rows = await app.state.db.fetch("SELECT * FROM users ORDER BY RANDOM() LIMIT 20")
    profiles = []
    for row in rows:
        profiles.append({
            "name": row["name"],
            "about": row["about"],
            "photo": row["photo"],
            "location_city": row["location_city"],
            "sun": row.get("sun", ""),
            "ascendant": row.get("ascendant", ""),
            "age": calculate_age(row["birth_date"])
        })
    return profiles

def calculate_age(birth_date_str):
    try:
        birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y")
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except:
        return None

# Объединённый запуск Telegram-бота и FastAPI
async def start_all():
    api = uvicorn.Server(
        uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    )
    await asyncio.gather(
        api.serve(),
        dp.start_polling(bot),
    )

if __name__ == "__main__":
    asyncio.run(start_all())
