import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
APP_URL = os.getenv("astroconnectbot-production.up.railway.app/")  # Это Railway APP URL для webhooks
FRONTEND_URL = os.getenv("685798b95e51acca36207efb--astroconnectminiapp.netlify.app")
