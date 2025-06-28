from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states import RegistrationStates
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import UserProfile
from astro_utils import calc_zodiac_asc
from database import AsyncSessionLocal

router = Router()

@router.callback_query(F.data == "start_registration")
async def registration_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Давайте начнём регистрацию! Как вас зовут?")
    await state.set_state(RegistrationStates.name)
    await callback.answer()

@router.message(RegistrationStates.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Спасибо! Введите вашу дату рождения (ДД.ММ.ГГГГ)")
    await state.set_state(RegistrationStates.birth_date)

@router.message(RegistrationStates.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Время рождения? (например, 14:23 или 'не знаю')")
    await state.set_state(RegistrationStates.birth_time)

@router.message(RegistrationStates.birth_time)
async def process_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Город рождения?")
    await state.set_state(RegistrationStates.birth_place)

@router.message(RegistrationStates.birth_place)
async def process_birth_place(message: Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    await message.answer("Можете отправить своё фото для профиля? (необязательно, просто отправьте изображение или напишите 'нет')")
    await state.set_state(RegistrationStates.photo_id)

@router.message(RegistrationStates.photo_id)
async def process_photo(message: Message, state: FSMContext):
    user_data = await state.get_data()
    photo_id = None
    if message.photo:
        photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)

    zodiac, ascendant = calc_zodiac_asc(
        user_data['birth_date'],
        user_data['birth_time'],
        user_data['birth_place']
    )

    # Сохраняем профиль
    async with AsyncSessionLocal() as session:
        profile = UserProfile(
            telegram_id=message.from_user.id,
            name=user_data['name'],
            birth_date=user_data['birth_date'],
            birth_time=user_data['birth_time'],
            birth_place=user_data['birth_place'],
            photo_id=photo_id,
            zodiac=zodiac,
            ascendant=ascendant,
        )
        session.add(profile)
        await session.commit()

    await message.answer(
        f"Регистрация завершена!\n\n"
        f"Имя: {user_data.get('name')}\n"
        f"Знак Зодиака: {zodiac}\n"
        f"Асцендент: {ascendant}\n"
        f"Ваша анкета сохранена! Ждите подборки совместимых партнёров."
    )
    await state.clear()
