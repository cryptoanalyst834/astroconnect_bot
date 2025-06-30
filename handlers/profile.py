from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from states import RegistrationStates
from astro_utils import get_zodiac_and_ascendant
from aiogram import types, F
from states import RegistrationStates 

router = Router()

@router.callback_query(F.data == "start_registration")
async def registration_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваше имя:")
    await state.set_state(RegistrationStates.name)

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
    await state.update_data(about=message.text if message.text != '-' else '')
    await message.answer("Пришлите ваше фото (по желанию, иначе отправьте -):")
    await state.set_state(RegistrationStates.photo)

@router.message(RegistrationStates.photo)
async def process_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_id = None
    if message.photo:
        photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    # Получаем все поля для построения карты
    name = data.get('name')
    birth_date = data.get('birth_date')
    birth_time = data.get('birth_time')
    birth_city = data.get('birth_city')
    about = data.get('about')
    sun_sign, asc_sign = get_zodiac_and_ascendant(birth_date, birth_time, birth_city)
    # Сохраняем профиль (тут твоя логика БД!)
    # await save_profile_to_db(...)
    summary = (f"Ваша анкета:\n"
               f"Имя: {name}\n"
               f"Дата рождения: {birth_date}\n"
               f"Время рождения: {birth_time}\n"
               f"Город рождения: {birth_city}\n"
               f"Знак Зодиака: {sun_sign}\n"
               f"Асцендент: {asc_sign}\n"
               f"О себе: {about or '—'}")
    await message.answer(summary)
    await message.answer("Спасибо! Ваша анкета сохранена.\n"
                        "Можете воспользоваться /discover для просмотра совместимых анкет!")
    await state.clear()
