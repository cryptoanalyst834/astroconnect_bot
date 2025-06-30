from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_async_session
from models import UserProfile
from astro_utils import get_zodiac_and_ascendant
from sqlalchemy import select
from datetime import datetime
from config import FRONTEND_URL

router = Router()

class ProfileFSM(StatesGroup):
    waiting_for_name = State()
    waiting_for_birth_date = State()
    waiting_for_birth_time = State()
    waiting_for_birth_place = State()
    waiting_for_gender = State()
    waiting_for_description = State()
    waiting_for_photo = State()
    completed = State()

@router.callback_query(F.data == "start_registration")
async def start_reg(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите ваше имя:")
    await state.set_state(ProfileFSM.waiting_for_name)

@router.message(ProfileFSM.waiting_for_name)
async def ask_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажите дату рождения (ГГГГ-ММ-ДД):")
    await state.set_state(ProfileFSM.waiting_for_birth_date)

@router.message(ProfileFSM.waiting_for_birth_date)
async def ask_birth_time(message: types.Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Укажите время рождения (ЧЧ:ММ):")
    await state.set_state(ProfileFSM.waiting_for_birth_time)

@router.message(ProfileFSM.waiting_for_birth_time)
async def ask_birth_place(message: types.Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Введите место рождения (город):")
    await state.set_state(ProfileFSM.waiting_for_birth_place)

@router.message(ProfileFSM.waiting_for_birth_place)
async def ask_gender(message: types.Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Мужской", callback_data="gender_male"),
             InlineKeyboardButton(text="Женский", callback_data="gender_female")]
        ]
    )
    await message.answer("Ваш пол:", reply_markup=kb)
    await state.set_state(ProfileFSM.waiting_for_gender)

@router.callback_query(ProfileFSM.waiting_for_gender)
async def ask_description(call: types.CallbackQuery, state: FSMContext):
    gender = "Мужской" if call.data == "gender_male" else "Женский"
    await state.update_data(gender=gender)
    await call.message.answer("Опишите себя:")
    await state.set_state(ProfileFSM.waiting_for_description)

@router.message(ProfileFSM.waiting_for_description)
async def ask_photo(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Загрузите своё фото:")
    await state.set_state(ProfileFSM.waiting_for_photo)

@router.message(ProfileFSM.waiting_for_photo)
async def complete_registration(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, загрузите фотографию.")
        return
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    data = await state.get_data()

    # Преобразуем к нужным типам
    birth_date = datetime.strptime(data['birth_date'], "%Y-%m-%d").date()
    birth_time = datetime.strptime(data['birth_time'], "%H:%M").time()
    try:
        zodiac, asc, aspects = get_zodiac_and_ascendant(birth_date, birth_time, data['birth_place'])
    except Exception as e:
        await message.answer(f"Ошибка геокодинга: {e}")
        return

    async with get_async_session() as session:
        profile = UserProfile(
            telegram_id=str(message.from_user.id),
            name=data['name'],
            birth_date=birth_date,
            birth_time=birth_time,
            birth_place=data['birth_place'],
            latitude=0,  # Для простоты, но лучше извлечь координаты
            longitude=0,
            gender=data['gender'],
            description=data['description'],
            photo_id=photo_id,
            zodiac=zodiac,
            ascendant=asc,
            natal_chart={"aspects": str(aspects)},
        )
        session.add(profile)
        await session.commit()

    await message.answer(
        f"Спасибо, ваша анкета сохранена!\n\n"
        f"Знак: {zodiac}\nАсцендент: {asc}\n\n"
        f"Ваш профиль доступен в мини-приложении: {FRONTEND_URL}/profile/{message.from_user.id}"
    )
    await state.clear()
