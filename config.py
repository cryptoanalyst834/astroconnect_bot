import os
from dotenv import load_dotenv

# Один вызов для всего проекта
load_dotenv()

# Токен бота
TOKEN = os.getenv("BOT_TOKEN")
# Строка подключения к БД
DATABASE_URL = os.getenv("DATABASE_URL")
# URL вашего приложения Railway (без https://)
RAILWAY_APP_URL = os.getenv("RAILWAY_APP_URL")
# URL мини-приложения (Netlify)
FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "https://685798b95e51acca36207efb--astroconnectminiapp.netlify.app"
)

# Проверка
missing = [name for name in ("TOKEN", "DATABASE_URL", "RAILWAY_APP_URL") if not globals().get(name)]
if missing:
    raise RuntimeError(f"❌ Не заданы переменные окружения: {', '.join(missing)}")
