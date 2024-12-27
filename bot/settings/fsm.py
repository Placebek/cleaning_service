from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    select = State()
    name = State()
    object_type = State()
    room_count = State()
    cleaning_type = State()
    address = State()
    address_city = State()
    address_street = State()
    address_home = State()
    address_appartment = State() 
