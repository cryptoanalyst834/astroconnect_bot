from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_async_session
from models import UserProfile
from astro_utils import geocode_place, get_zodiac_and_ascendant
from datetime import datetime

router = Router()

class Registration(StatesGroup):
    waiting_name = State()
    waiting_gender = State()
    waiting_birth_date = State()
    waiting_birth_time = State()
    waiting_birth_place = State()
    waiting_description = State()

@router.callback_query(F.data == "start_registration")
async def start_registration(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваше имя:")
    await state.set_state(Registration.waiting_name)
    await callback.answer()

@router.message(Registration.waiting_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажите ваш пол (м/ж):")
    await state.set_state(Registration.waiting_gender)

@router.message(Registration.waiting_gender)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Введите дату рождения (ГГГГ-ММ-ДД):")
    await state.set_state(Registration.waiting_birth_date)

@router.message(Registration.waiting_birth_date)
async def process_birth_date(message: types.Message, state: FSMContext):
    try:
        birth_date = datetime.strptime(message.text, "%Y-%m-%d").date()
    except ValueError:
        await message.answer("Некорректная дата. Попробуйте снова (ГГГГ-ММ-ДД):")
        return
    await state.update_data(birth_date=birth_date)
    await message.answer("Введите время рождения (ЧЧ:ММ, 24ч):")
    await state.set_state(Registration.waiting_birth_time)

@router.message(Registration.waiting_birth_time)
async def process_birth_time(message: types.Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Где вы родились? (Город, страна):")
    await state.set_state(Registration.waiting_birth_place)

@router.message(Registration.waiting_birth_place)
async def process_birth_place(message: types.Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    await message.answer("Опишите себя (по желанию):")
    await state.set_state(Registration.waiting_description)

@router.message(Registration.waiting_description)
async def process_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    gender = data["gender"]
    birth_date = data["birth_date"]
    birth_time = data["birth_time"]
    birth_place = data["birth_place"]
    description = message.text

    # Определяем координаты по месту рождения
    lat, lon = geocode_place(birth_place)
    zodiac, ascendant, chart = get_zodiac_and_ascendant(
        str(birth_date), birth_time, birth_place, lat, lon
    )

    # Сохраняем профиль
    async with get_async_session() as session:
        user = UserProfile(
            tg_id=message.from_user.id,
            name=name,
            gender=gender,
            birth_date=birth_date,
            birth_time=birth_time,
            birth_place=birth_place,
            latitude=lat,
            longitude=lon,
            zodiac=zodiac,
            ascendant=ascendant,
            description=description,
            astro_data={"chart": chart.toJSON()}
        )
        session.add(user)
        await session.commit()
    await message.answer(f"Анкета сохранена!\nВаш знак: {zodiac}, Асцендент: {ascendant}")
    await state.clear()
