from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import RegistrationStates
from astro_utils import get_zodiac_and_ascendant

router = Router()

@router.callback_query(F.data == "start_registration")
async def registration_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваше имя:")
    await state.set_state(RegistrationStates.name)
    await callback.answer()

@router.message(RegistrationStates.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите дату рождения (ГГГГ-ММ-ДД):")
    await state.set_state(RegistrationStates.birth_date)

@router.message(RegistrationStates.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Введите время рождения (ЧЧ:ММ):")
    await state.set_state(RegistrationStates.birth_time)

@router.message(RegistrationStates.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Введите город рождения:")
    await state.set_state(RegistrationStates.birth_city)

@router.message(RegistrationStates.birth_city)
async def process_birth_city(message: Message, state: FSMContext):
    await state.update_data(birth_city=message.text)
    await message.answer("Кратко расскажите о себе (по желанию, иначе отправьте -):")
    await state.set_state(RegistrationStates.about)

@router.message(RegistrationStates.about)
async def process_about(message: Message, state: FSMContext):
    about_text = message.text if message.text != '-' else ''
    await state.update_data(about=about_text)
    await message.answer("Пришлите ваше фото (по желанию, иначе отправьте -):")
    await state.set_state(RegistrationStates.photo)

@router.message(RegistrationStates.photo)
async def process_photo(message: Message, state: FSMContext):
    photo_id = None
    if message.photo:
        photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    data = await state.get_data()
    # Расчет карты:
    sun_sign, asc_sign = get_zodiac_and_ascendant(
        data["birth_date"], data["birth_time"], data["birth_city"]
    )
    # Здесь вставить сохранение в БД!
    summary = (
        f"<b>Ваша анкета:</b>\n"
        f"Имя: {data.get('name')}\n"
        f"Дата рождения: {data.get('birth_date')}\n"
        f"Время рождения: {data.get('birth_time')}\n"
        f"Город рождения: {data.get('birth_city')}\n"
        f"Знак Зодиака: {sun_sign}\n"
        f"Асцендент: {asc_sign}\n"
        f"О себе: {data.get('about') or '—'}"
    )
    await message.answer(summary, parse_mode="HTML")
    await message.answer("Спасибо! Ваша анкета сохранена.\nМожете воспользоваться /discover для поиска совместимых анкет!")
    await state.clear()
