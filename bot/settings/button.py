from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import  aiohttp


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
button_adres = InlineKeyboardButton(
    text="Адрес",
    callback_data="button_room"
)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[button1],
                     [button2],
                     [button3],
                     [button4],
                     [button_adres]]
)

async def get_object_types_keyboard(api_url: str, access_token: str) -> InlineKeyboardMarkup:
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {access_token}"}
            async with session.get(api_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()  
                    object_types = data  

                    buttons = [
                        [InlineKeyboardButton(text=item["type_of_premises"], callback_data=f"premises_{item['id']}")]
                        for item in object_types
                    ]

                    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                    return keyboard
                else:
                    print(f"Ошибка API: {response.status}")
                    return InlineKeyboardMarkup()
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return InlineKeyboardMarkup()

#Бөлме кнопкалары
button7 = InlineKeyboardButton(
    text="1 и 2 комнаты",
    callback_data="button7"
)
button8 = InlineKeyboardButton(
    text="3 и 4 комнаты",
    callback_data="button8"
)
button9 = InlineKeyboardButton(
    text="Больше",
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
    text="Город",
    callback_data="button13"
)
button14 = InlineKeyboardButton(
    text="Улица",
    callback_data='button14'
)
button15 = InlineKeyboardButton(
    text="Дом",
    callback_data="button13"
)
button16 = InlineKeyboardButton(
    text="Квартира",
    callback_data="button16"
)
keyboard5 = InlineKeyboardMarkup(
    inline_keyboard=[[button13],
                     [button14],
                     [button15],
                     [button16]]
)