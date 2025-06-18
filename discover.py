from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database import connect
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
import datetime

router = Router()

# Helper: calculate compatibility (заглушка на основе знаков)
def calculate_compatibility(user1, user2):
    return 70  # TODO: Реализовать астросинастрию

def get_users_for_discover(current_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id != %s ORDER BY created_at DESC LIMIT 10", (current_id,))
    users = cur.fetchall()
    conn.close()
    return users

@router.message(F.text == "/discover")
async def discover_users(message: Message):
    users = get_users_for_discover(message.from_user.id)
    if not users:
        await message.answer("Нет новых анкет для просмотра.")
        return

    for user in users:
        name, gender, birth_date, _, _, city, _, about, photo_id, _ = user[1:]
        percent = calculate_compatibility(message.from_user.id, user[0])
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💘 Лайк", callback_data=f"like:{user[0]}"),
             InlineKeyboardButton(text="⏭ Пропустить", callback_data=f"skip:{user[0]}")]
        ])
        text = f"👤 {name}, {gender}\n📍 {city}\n📅 {birth_date}\n💬 {about}\n❤️ Совместимость: {percent}%"
        if photo_id:
            await message.bot.send_photo(chat_id=message.chat.id, photo=photo_id, caption=text, reply_markup=kb)
        else:
            await message.answer(text, reply_markup=kb)
        break  # Показать только одного за раз

@router.callback_query(F.data.startswith("like"))
async def like_user(callback: CallbackQuery):
    await callback.message.answer("Ты поставил лайк! ❤️ (система матчей в разработке)")
    await callback.answer()

@router.callback_query(F.data.startswith("skip"))
async def skip_user(callback: CallbackQuery):
    await callback.message.answer("Анкета пропущена. Используй /discover чтобы продолжить.")
    await callback.answer()