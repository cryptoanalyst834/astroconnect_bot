from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import ProfileStates

router = Router()

@router.message(ProfileStates.name)
async def process_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("📅 Введи дату рождения (ДД.ММ.ГГГГ):")
    await state.set_state(ProfileStates.birth_date)

# Аналогично для birth_date, birth_time, birth_place, фото и т.д.
