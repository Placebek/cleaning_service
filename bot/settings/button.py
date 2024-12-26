from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


#Кнопки меню
button1 = InlineKeyboardButton(
    text="Имя",
    callback_data='button1'
)
button2 = InlineKeyboardButton(
    text="Тип объекта",
    callback_data='button2'
)
button3 = InlineKeyboardButton(
    text="Количество комнат",
    callback_data='button3'
)
button4 = InlineKeyboardButton(
    text="Тип уборки",
    callback_data='button4'
)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[button1],
                     [button2],
                     [button3],
                     [button4]]
)

#Обьект типтері кнопкалары
button5 = InlineKeyboardButton(
    text="котедж",
    callback_data='button5'
)
button6 = InlineKeyboardButton(
    text="жер үй",
    callback_data="button6"
)
keyboard2 = InlineKeyboardMarkup(
    inline_keyboard=[[button5],
                     [button6]]
)

#Бөлме кнопкалары
button7 = InlineKeyboardButton(
    text="1 және 2 бөлмелі",
    callback_data="button7"
)
button8 = InlineKeyboardButton(
    text="3 және 4 бөлмелі",
    callback_data="button8"
)
button9 = InlineKeyboardButton(
    text="Көп",
    callback_data="button9"
)
keyboard3 = InlineKeyboardMarkup(
    inline_keyboard=[[button7],
                     [button8],
                     [button9]]
)

#Тип клининга
button10 = InlineKeyboardButton(
    text="Поверхностная чистка",
    callback_data="button10"
)
button11 = InlineKeyboardButton(
    text="Средняя чистка",
    callback_data="button11"
)
button12 = InlineKeyboardButton(
    text="Максимальная чистка",
    callback_data="button12"
)
keyboard4 = InlineKeyboardMarkup(
    inline_keyboard=[[button10],
                     [button11],
                     [button12]]
)

#Адрес
button13 = InlineKeyboardButton(
    text=""
)