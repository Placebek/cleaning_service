from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    select = State()
    request_name = State()
    phone_number = State()
    object_type = State()
    number_room = State()
    cleaning_type = State()
    city = State()
    street = State()
    home = State()
    apartment = State()
    date_request = State()
    confirmation = State()
