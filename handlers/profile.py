from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "start_registration")
async def registration_start(callback: CallbackQuery):
    await callback.message.answer("Давайте начнем регистрацию! Напишите, пожалуйста, ваше имя.")
    await callback.answer()
    # Далее логика FSM или простая регистрация
