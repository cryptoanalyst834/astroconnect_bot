from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart

router = Router()

# Приветственное сообщение
WELCOME_TEXT = """
Добро пожаловать в AstroConnect — сервис знакомств по натальной карте!

Мы анализируем дату, время и место рождения, чтобы находить максимально совместимых партнёров.

AstroConnect поможет:
— Найти подходящего человека по звёздам
— Избежать токсичных связей
— Понять, кто вам действительно подходит
— Раскрыть сильные стороны личности

Вы в надёжных астрологических руках. Готовы начать?
"""

# Кнопка "Начать регистрацию"
start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚀 Начать регистрацию", callback_data="start_registration")]
])

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=start_keyboard)
