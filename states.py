from aiogram.fsm.state import StatesGroup, State

class ProfileStates(StatesGroup):
    waiting_for_birthdate = State()
    waiting_for_birthtime = State()
    waiting_for_location = State()
