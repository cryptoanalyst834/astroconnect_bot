import os
from dotenv import load_dotenv

# Один вызов load_dotenv для всего проекта
load_dotenv()

# Теперь эти переменные можно импортировать в любой модуль
TOKEN        = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://685798b95e51acca36207efb--astroconnectminiapp.netlify.app/")

if not TOKEN or not DATABASE_URL:
    raise RuntimeError("Не установлены обязательные переменные окружения: TOKEN и DATABASE_URL")
