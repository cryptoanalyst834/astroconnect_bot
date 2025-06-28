from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

class Registration(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_place = State()

@router.callback_query(F.data == "start_registration")
async def registration_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Давайте начнем регистрацию! Введите ваше имя:")
    await state.set_state(Registration.name)
    await callback.answer()

@router.message(Registration.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажите дату рождения (в формате ГГГГ-ММ-ДД):")
    await state.set_state(Registration.birth_date)

@router.message(Registration.birth_date)
async def reg_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Введите время рождения (например, 14:30):")
    await state.set_state(Registration.birth_time)

@router.message(Registration.birth_time)
async def reg_birth_time(message: Message, state: FSMContext):
    await state.update_data(birth_time=message.text)
    await message.answer("Введите город рождения:")
    await state.set_state(Registration.birth_place)

@router.message(Registration.birth_place)
async def reg_birth_place(message: Message, state: FSMContext):
    user_data = await state.update_data(birth_place=message.text)
    # Тут вставь вычисление координат и расчёт карты, запись в базу и пр.
    await message.answer("Спасибо! Ваша анкета принята.")
    await state.clear()
