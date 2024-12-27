from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    select = State()
    request_name = State()
    city = State()
    street = State()
    home = State()
    apartment = State()
    object_type = State()
    number_room = State()
    cleaning_type = State()
    date_request = State()
    confirmation = State()
