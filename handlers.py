from aiogram import Router, F
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove, InlineKeyboardMarkup,
    InlineKeyboardButton, WebAppInfo
)
from aiogram.fsm.context import FSMContext
from states import RegisterState
from database import save_user, get_user

router = Router()

@router.message(F.text == "/start")
async def start_cmd(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🌠 Открыть анкеты",
            web_app=WebAppInfo(url="https://preeminent-kelpie-cd4c81.netlify.app/")
        )]
    ])
    await message.answer(
        "Добро пожаловать в AstroConnect! ✨\nНажми /register, чтобы создать анкету или открой анкеты ниже.",
        reply_markup=markup
    )

@router.message(F.text == "/register")
async def register_start(message: Message, state: FSMContext):
    await message.answer("Как тебя зовут?")
    await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def register_gender(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Твой пол? (М / Ж)")
    await state.set_state(RegisterState.gender)

@router.message(RegisterState.gender)
async def register_birth_date(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Дата рождения? (дд.мм.гггг)")
    await state.set_state(RegisterState.birth_date)

@router.message(RegisterState.birth_date)
async def register_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Время рождения? (чч:мм, если не знаешь — укажи 12:00)")
    await state.set_state(RegisterState.birth_time)

@router.message(RegisterState.birth_time)
async def register_birth_city(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Город рождения?")
    await state.set_state(RegisterState.birth_city)

@router.message(RegisterState.birth_city)
async def register_location_city(message: Message, state: FSMContext):
    await state.update_data(birth_city=message.text)
    await message.answer("Где ты сейчас живешь?")
    await state.set_state(RegisterState.location_city)

@router.message(RegisterState.location_city)
async def register_looking_for(message: Message, state: FSMContext):
    await state.update_data(location_city=message.text)
    await message.answer("Кого ты ищешь? (М / Ж)")
    await state.set_state(RegisterState.looking_for)

@router.message(RegisterState.looking_for)
async def register_about(message: Message, state: FSMContext):
    await state.update_data(looking_for=message.text)
    await message.answer("Расскажи немного о себе (2-3 предложения):")
    await state.set_state(RegisterState.about)

@router.message(RegisterState.about)
async def register_photo(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("Пришли свою фотографию (1 шт):")
    await state.set_state(RegisterState.photo)

@router.message(RegisterState.photo, F.photo)
async def register_complete(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    data = await state.get_data()
    data["telegram_id"] = message.from_user.id
    save_user(data)
    await state.clear()
    await message.answer("Твоя анкета сохранена! 🎉", reply_markup=ReplyKeyboardRemove())

@router.message(F.text == "/profile")
async def profile(message: Message):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer("Ты ещё не зарегистрирован. Нажми /register.")
    else:
        name, gender, birth_date, _, _, location, _, about, _, _ = user[1:10]
        await message.answer(f"👤 {name} ({gender})\n📍 {location}\n📅 {birth_date}\n💬 {about}")
