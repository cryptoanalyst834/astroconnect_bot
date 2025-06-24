from aiogram.fsm.state import StatesGroup, State

class RegistrationState(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_place = State()
    photo = State()
