from aiogram.fsm.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    name = State()
    birth_date = State()
    birth_time = State()
    birth_place = State()
    photo_id = State()
