from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import os
from contextlib import asynccontextmanager
from bot import bot, dp
import asyncio

DATABASE_URL = os.getenv("DATABASE_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await asyncpg.connect(DATABASE_URL)
    yield
    await app.state.db.close()

app = FastAPI(lifespan=lifespan)

# CORS для фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Лучше указать Netlify-домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def calculate_age(birth_date_str):
    from datetime import datetime
    try:
        birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y")
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except:
        return None

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

# 🚀 Telegram бот запускается в фоне
@app.on_event("startup")
async def start_bot():
    asyncio.create_task(dp.start_polling(bot))
