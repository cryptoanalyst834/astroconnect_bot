import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, add_user_to_db, get_all_users
from telegram_bot import router as telegram_router

app = FastAPI()

# Разрешаем CORS для фронтенда
origins = [
    "https://astroconnect.netlify.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

@app.get("/profiles")
async def get_profiles():
    return await get_all_users()

app.include_router(telegram_router)
