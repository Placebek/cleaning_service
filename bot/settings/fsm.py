from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    select = State()
    name = State()
    object_type = State()
    room_count = State()
    cleaning_type = State()