from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart

from states import ProfileStates
from aiogram.fsm.context import FSMContext

router = Router()

WELCOME_TEXT = (
    "<b>Добро пожаловать в AstroConnect!</b>\n\n"
    "Мы анализируем дату, время и место рождения, чтобы находить максимально совместимых партнёров.\n\n"
    "AstroConnect поможет:\n"
    "— Найти подходящего человека по звёздам\n"
    "— Избежать токсичных связей\n"
    "— Понять, кто вам действительно подходит\n"
    "— Раскрыть сильные стороны личности\n\n"
    "Вы в надёжных астрологических руках. Готовы начать?"
)

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="🚀 Начать регистрацию",
            callback_data="start_registration"
        )
    ]
])

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        WELCOME_TEXT,
        reply_markup=start_keyboard,
        parse_mode="HTML"
    )

@router.callback_query(F.data == "start_registration")
async def on_start_registration(
    query: CallbackQuery,
    state: FSMContext
):
    # Убираем кнопки
    await query.message.edit_reply_markup(None)
    # Запускаем FSM-диалог
    await query.message.answer("Как тебя зовут?")
    await state.set_state(ProfileStates.name)
    # Отвечаем на коллбэк, чтобы убрать "часики" на кнопке
    await query.answer()
