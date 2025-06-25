from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()

class ProfileStates(StatesGroup):
    name        = State()
    birth_date  = State()
    birth_time  = State()
    birth_place = State()
    photo       = State()
