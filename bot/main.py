import asyncio
import requests
from decouple import config
from aiogram.filters import Command, CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from api import FastAPIUser
from aiogram.fsm.context import FSMContext
from settings.button import *
from aiogram import F
from settings.fsm import Form


TOKEN=config('TOKEN')
bot = Bot(token=TOKEN)
dp=Dispatcher()
URL='...'#api/token
URL2='...'
URL3='...'#api/send/username
URL4=''#api/city
fastapi_client = FastAPIUser(url=URL)


#Старт
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Form.select)
    await message.answer(text="Привет! Это клининговый сервис TAZA!",
                         reply_markup=keyboard)

    telegram_id = message.from_user.id
    username = message.from_user.username

    response = (
        f"telegram_id: {telegram_id}"
        f"username: {username}"
    )
    print(response)

    tokens = fastapi_client.get_jwt_token(username=username, telegram_id=telegram_id)

    if tokens:
        access_token = tokens.get("access")
    else:
        print("не удалось получить токен")
        return
    
    result = fastapi_client.send_user_data(
        username=username,
        telegram_id=telegram_id,
        access_token=access_token
    )

    if result:
        print("Данные отправлены")
    else:
        print("Произошла ошибка при отправке данных")


#кнопки
@dp.callback_query()
async def username_callback(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "button1":
        await state.set_state(Form.name)
        await callback_query.message.answer("Напишите свое имя:")

    elif callback_query.data == "button2":
        user_data = await state.get_data()
        access_token = user_data.get("access_token")
        keyboard = await get_object_types_keyboard(URL3, access_token)

        await state.set_state(Form.object_type)
        await callback_query.message.answer("Выберите тип объекта:", reply_markup=keyboard)
        
    elif callback_query.data == "button3":
        await state.set_state(Form.room_count)
        await callback_query.message.answer(text="Выберите количество комнат:",
                                            reply_markup=keyboard3)
        
    elif callback_query.data == "button4":
        await state.set_state(Form.cleaning_type)
        await callback_query.message.answer(text="Выберите тип уборки:",
                                            reply_markup=keyboard4)
        
    elif callback_query.data == "button_address":
        await state.set_state(Form.address)
        await callback_query.message.answer(text="Напишите полный адрес, выбрав команды ниже:",
                                            reply_markup=keyboard5)
    

# Обработчик ввода имени
@dp.message(Form.name)
async def sand_name_user(message: Message, state: FSMContext):
    try:
        name_user = message.text.strip()
        user_name = name_user.split()

        response = requests.post(URL2, json={"first_name": user_name[0],
                                             "last_name": user_name[1]})
        
        await state.update_data(name=name_user)
        await state.set_state(Form.object_type)

        if response.status_code == 200:
            print(f"Данные успешно отправлены")
        else:
            print(f"Ошибка при отправке данных: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке данных: {str(e)}")
    

#Обработчик выбора типа объекта
@dp.message(Form.object_type)
async def process_boject_type(message: Message, state: FSMContext):
    user_data = await state.get_data()
    access_token = user_data.get("access_token")

    keyboard = await get_object_types_keyboard(URL3, access_token)

    await message.answer("Выберите тип помещения:", reply_markup=keyboard)


#Обработчик выбора количества комнат
async def process_room_count(callback_query: CallbackQuery, state: FSMContext):
    room_count = callback_query.data

    await state.update_data(room_count=room_count)
    await state.set_state(Form.cleaning_type)
    await callback_query.message.answer("Теперь выберите тип уборки:", reply_markup=keyboard4)


#Обработчик выбора типа уборки
@dp.callback_query(Form.cleaning_type)
async def process_cleaning_type(callback_query: CallbackQuery, state: FSMContext):
    cleaning_type = callback_query.data

    user_data = await state.get_data()
    user_data['cleaning_type'] = cleaning_type

    await state.clear()
    await callback_query.message.answer(
        f"Спасибо за ваш заказ!\n\n"
        f"Имя: {user_data['name']}\n"
        f"Тип объекта: {user_data['object_type']}\n"
        f"Количество комнат: {user_data['room_count']}\n"
        f"Тип уборки: {user_data['cleaning_type']}"
    )


@dp.callback_query(Form.address)
async def address_calback(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "button13":
        await state.set_state(Form.address_city)
        await callback_query.message.answer("Напишите свой город:")

    
    # try:
    #     city_name = message.text.strip()

    #     response = requests.post(URL4, json={"city_name": city_name})

    #     await state.update_data(city_name=city_name)
    #     await state.set_state(Form.address_street)

    #     if response.status_code == 200:
    #         print(f"Данные успешно отправлены")
    #     else:
    #         print(f"Ошибка при отправке данных: {response.status_code}")
    # except requests.exceptions.RequestException as e:
    #     print(f"Ошибка при отправке данных: {str(e)}")




#Меню
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Доступные команды: "
                         "\n/start - Старт"
                         "\n/help - Помощь"
                         "\n/info - Инфориация")
    

#Инфо
@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer("Мы очень хорошо помоем и уберем ваш дом!")


async def main():
    await dp.start_polling(bot)

asyncio.run(main())
