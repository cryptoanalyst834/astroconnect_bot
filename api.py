# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_all_users  # функция уже есть у тебя
import uvicorn

app = FastAPI()

# Разрешим запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в проде лучше указать конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/profiles")
async def profiles():
    users = await get_all_users()
    return users

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)
