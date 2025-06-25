from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from states import ProfileStates
from database import async_session_maker
from models import UserProfile

router = Router()

# После нажатия «Начать регистрацию» мы уже в состоянии name
@router.message(ProfileStates.name)
async def cmd_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📅 Введите дату рождения (ДД.MM.ГГГГ):")
    await state.set_state(ProfileStates.birth_date)

@router.message(ProfileStates.birth_date)
async def cmd_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("⏰ Введите время рождения (ЧЧ:ММ):")
    await state.set_state(ProfileStates.birth_time)

@router.message(ProfileStates.birth_time)
async def cmd_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("🌍 Введите город рождения:")
    await state.set_state(ProfileStates.birth_place)

@router.message(ProfileStates.birth_place)
async def cmd_birth_place(message: Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    await message.answer("📸 Пришлите фотографию для анкеты:")
    await state.set_state(ProfileStates.photo)

@router.message(ProfileStates.photo)
async def cmd_photo(message: Message, state: FSMContext):
    if not message.photo:
        return await message.answer("Пожалуйста, отправьте фотографию.")
    file_id = message.photo[-1].file_id

    data = await state.get_data()
    # Генерация астроданных
    from astro_utils import generate_astrology_data
    astro = await generate_astrology_data(
        data["birth_date"], data["birth_time"], data["birth_place"]
    )

    # Сохранение в БД
    async with async_session_maker() as session:
        profile = UserProfile(
            telegram_id=message.from_user.id,
            name=data["name"],
            birth_date=data["birth_date"],
            birth_time=data["birth_time"],
            birth_place=data["birth_place"],
            zodiac=astro["zodiac"],
            ascendant=astro["ascendant"],
            photo_id=file_id,
        )
        session.add(profile)
        await session.commit()

    # Вывод результата
    await message.answer_photo(
        photo=file_id,
        caption=(
            f"✅ Ваш профиль сохранён!\n\n"
            f"Имя: {data['name']}\n"
            f"Дата рождения: {data['birth_date']} {data['birth_time']}\n"
            f"Место: {data['birth_place']}\n"
            f"Знак: {astro['zodiac']}\n"
            f"Асцендент: {astro['ascendant']}\n\n"
            "Теперь вы можете открыть мини-приложение и смотреть совместимые анкеты."
        )
    )
    await state.clear()
