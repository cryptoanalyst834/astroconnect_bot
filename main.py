from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import asyncpg
import os
from datetime import datetime

app = FastAPI()

# Разрешаем CORS (для Netlify и др. фронтов)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://astroconnectminiapp.netlify.app/"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Читаем токен из переменной окружения

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.connect(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.get("/profiles")
async def get_profiles():
    rows = await app.state.db.fetch("SELECT * FROM users ORDER BY RANDOM() LIMIT 20")
    profiles = []
    for row in rows:
        profiles.append({
            "name": row["name"],
            "about": row["about"],
            "photo": row["photo"],  # file_id от Telegram
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

@app.get("/photo/{file_id}")
async def get_photo(file_id: str):
    bot_token = os.getenv("BOT_TOKEN")
    tg_url = f"https://api.telegram.org/file/bot{bot_token}/{file_id}"
    return RedirectResponse(tg_url)
