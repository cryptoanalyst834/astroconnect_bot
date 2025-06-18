from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

origins = [
    "*",  # Упростим на время тестов, потом заменить
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель анкеты
class Profile(BaseModel):
    name: str
    age: int
    city: str
    zodiac: str
    about: str
    photo: str

@app.get("/profiles", response_model=List[Profile])
def get_profiles():
    # Заглушка: возвращает 3 анкеты
    return [
        Profile(
            name="Анна",
            age=25,
            city="Москва",
            zodiac="Скорпион",
            about="Люблю звёзды и кофе ☕",
            photo="https://placehold.co/300x300"
        ),
        Profile(
            name="Ирина",
            age=29,
            city="Минск",
            zodiac="Рак",
            about="Вяжу свитеры и слушаю джаз 🎷",
            photo="https://placehold.co/300x300"
        ),
        Profile(
            name="Мария",
            age=31,
            city="Сочи",
            zodiac="Лев",
            about="Обожаю закаты и морской воздух 🌅",
            photo="https://placehold.co/300x300"
        ),
    ]