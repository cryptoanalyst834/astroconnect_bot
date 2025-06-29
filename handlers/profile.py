from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from config import FRONTEND_URL

router = Router()

@router.callback_query(F.data == "start_registration")
async def registration_callback(callback: CallbackQuery):
    url = f"{FRONTEND_URL}/register?tg_id={callback.from_user.id}"
    await callback.message.answer(
        "Перейдите по ссылке для заполнения анкеты: " + url,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[
                types.InlineKeyboardButton(text="Заполнить анкету", url=url)
            ]]
        ),
    )
    await callback.answer()
