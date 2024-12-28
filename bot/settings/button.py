from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import  aiohttp

#заявка
button1 = InlineKeyboardButton(
    text="Создать заявку",
    callback_data="button1"
)
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[button1],]
)

#Тип объекта
OBJECT_TYPES = {
    "object_house": "Частный дом",
    "object_cottage": "Коттедж",
    "object_office": "Офис"
}
button2 = InlineKeyboardButton(text="Коттедж", callback_data="object_cottage")
button3 = InlineKeyboardButton(text="Частный дом", callback_data="object_house")
button9 = InlineKeyboardButton(text="Офис", callback_data="object_office")
keyboard2 = InlineKeyboardMarkup(inline_keyboard=[[button2], [button3], [button9]])

#Число комнат
ROOM_COUNTS = {
    "room_1": "1 комнатный",
    "room_2": "2 комнатный",
    "room_3_plus": "3+ комнатный"
}
button3 = InlineKeyboardButton(text="1 комнатный", callback_data="room_1")
button4 = InlineKeyboardButton(text="2 комнатный", callback_data="room_2")
button5 = InlineKeyboardButton(text="3+ комнатный", callback_data="room_3_plus")
keyboard3 = InlineKeyboardMarkup(inline_keyboard=[[button3], [button4], [button5]])

#Тип уборки
CLEANING_TYPES = {
    "cleaning_surface": "Поверхностная чистка",
    "cleaning_average": "Средняя чистка",
    "cleaning_max": "Максимальная чистка"
}
button6 = InlineKeyboardButton(text="Поверхностная чистка", callback_data="cleaning_surface")
button7 = InlineKeyboardButton(text="Средняя чистка", callback_data="cleaning_average")
button8 = InlineKeyboardButton(text="Максимальная чистка", callback_data="cleaning_max")
keyboard4 = InlineKeyboardMarkup(inline_keyboard=[[button6], [button7], [button8]])

#Подтверждение заявки
confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_request")],
        [InlineKeyboardButton(text="🔄 Заполнить заново", callback_data="retry_request")]
    ]
)

#Выбрать дату
MONTH = {
    "1": "Январь",
    "2": "Февраль",
    "3": "Март",
    "4": "Апрель",
    "5": "Май",
    "6": "Июнь",
    "7": "Июль",
    "8": "Август",
    "9": "Сентябрь",
    "10": "Октябрь",
    "11": "Ноябрь",
    "12": "Декябрь"
}

button10 = InlineKeyboardButton(text="Январь", callback_data="button10")
button11 = InlineKeyboardButton(text="Февраль", callback_data="button11")
keyboard5 = InlineKeyboardMarkup(inline_keyboard=[[button10], [button11]])

days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]