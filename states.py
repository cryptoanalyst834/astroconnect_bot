from aiogram.fsm.state import StatesGroup, State

class RegisterState(StatesGroup):
    name = State()
    gender = State()
    birth_date = State()
    birth_time = State()
    birth_city = State()
    location_city = State()
    looking_for = State()
    about = State()
    photo = State()