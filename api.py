from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

# Разрешаем доступ с фронтенда (например, Netlify)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # укажи конкретный домен при проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/profiles")
async def get_profiles():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("SELECT * FROM users")
    await conn.close()
    return [dict(row) for row in rows]
