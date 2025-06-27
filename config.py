import os
from dotenv import load_dotenv

load_dotenv()

# Получаем токен Telegram-бота
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Переменная TOKEN не задана!")

RAILWAY_APP_URL = os.getenv("RAILWAY_APP_URL")
if not RAILWAY_APP_URL:
    raise RuntimeError("Переменная RAILWAY_APP_URL не задана!")

FRONTEND_URL = os.getenv("FRONTEND_URL")
if not FRONTED_URL:
    raise RuntimeError("Переменная FRONTEND_URL не задана!")
