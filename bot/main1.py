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


@dp.callback_query(F.data == "button1") 
async def create_request(callback_query: CallbackQuery, state: FSMContext):
    # if callback_query.data == "button1":
        await state.set_state(Form.request_name)
        await callback_query.message.answer("Напишите свое имя:")

@dp.message(Form.request_name)
async def send_user( message: Message, state: FSMContext):
    name_user = message.text.strip()
    await state.update_data(name_user=name_user)
    await state.set_state(Form.object_type)
    await message.answer("Теперь выберите свой тип обьекта", reply_markup=keyboard2)

@dp.callback_query(Form.object_type)
async def send_object_type(callback_query: CallbackQuery, state: FSMContext):
    object_type = callback_query.data
    human_readable_object_type = OBJECT_TYPES.get(object_type, "Неизвестный тип объекта")
    await state.update_data(object_type=human_readable_object_type)
    await state.set_state(Form.number_room)
    await callback_query.message.answer("Теперь выберите число комнат", reply_markup=keyboard3)

@dp.callback_query(Form.number_room)
async def send_number_room(callback_query: CallbackQuery, state: FSMContext):
    number_room = callback_query.data
    human_readable_room_count = ROOM_COUNTS.get(number_room, "Неизвестное количество комнат")
    await state.update_data(number_room=human_readable_room_count)
    await state.set_state(Form.cleaning_type)
    await callback_query.message.answer('Теперь выберите тип уборки',reply_markup=keyboard4)

@dp.callback_query(Form.cleaning_type)
async def send_cleaning_type(callback_query: CallbackQuery, state: FSMContext):
    cleaning_type = callback_query.data
    human_readable_cleaning_type = CLEANING_TYPES.get(cleaning_type, "Неизвестный тип уборки")
    await state.update_data(cleaning_type=human_readable_cleaning_type)
    await state.set_state(Form.city)
    await callback_query.message.answer('Теперь напишите ваш город')

@dp.message(Form.city)
async def sand_city(message: Message, state: FSMContext):
    name_city = message.text.strip()
    await state.update_data(name_city=name_city)
    await state.set_state(Form.street)
    await message.answer("Напишите свою улицу")

@dp.message(Form.street)
async def send_city(message: Message, state: FSMContext):
    name_street = message.text.strip()
    await state.update_data(name_street=name_street)
    await state.set_state(Form.home)
    await message.answer("Напишите свой номер дома")

@dp.message(Form.home)
async def send_street(message: Message, state: FSMContext):
    name_home = message.text.strip()
    await state.update_data(name_home=name_home)
    await state.set_state(Form.apartment)
    await message.answer("Напишите номер своей квартиры:")

@dp.message(Form.apartment)
async def send_home(message: Message, state: FSMContext):
    number_apartment = message.text.strip()
    await state.update_data(number_apartment=number_apartment)
    await state.set_state(Form.date_request)
    await message.answer("А теперь напишите дату для прихода чистки на ваш обьект. В формате (12.12.2004)")

@dp.message(Form.date_request)
async def send_date_request(message: Message, state: FSMContext):
    date_request = message.text.strip()
    await state.update_data(date_request=date_request)
    data = await state.get_data()

    await message.answer(
        f"Ваши данные:\n"
        f"Имя: {data.get('name_user')}\n"
        f"Тип объекта: {data.get('object_type')}\n"
        f"Число комнат: {data.get('number_room')}\n"
        f"Тип уборки: {data.get('cleaning_type')}\n"
        f"Город: {data.get('name_city')}\n"
        f"Улица: {data.get('name_street')}\n"
        f"Дом: {data.get('name_home')}\n"
        f"Квартира: {data.get('number_apartment')}\n"
        f"Дата заявки: {data.get('data_request')}\n\n"
        f"Проверьте правильность данных. Если всё верно, подтвердите заявку.",
        reply_markup=confirm_keyboard
    )
    await state.set_state(Form.confirmation)
        
@dp.callback_query(Form.confirmation, lambda callback: callback.data == "confirm_request")
async def confirm_request(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payload = {
        "name": data.get("name_user"),
        "object_type": data.get("object_type"),
        "room_count": data.get("number_room"),
        "cleaning_type": data.get("cleaning_type"),
        "city": data.get("name_city"),
        "street": data.get("name_street"),
        "home": data.get("name_home"),
        "apartment": data.get("number_apartment"),
        "date": data.get("date_request")
    }

    api_url = "..."  
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(api_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    await callback_query.message.edit_text(
                        f"Заявка успешно отправлена!\n\nОтвет сервера: {result}"
                    )
                else:
                    await callback_query.message.edit_text("Произошла ошибка при отправке данных на сервер.")
        except Exception as e:
            await callback_query.message.edit_text(f"Ошибка при подключении к API: {e}")
    await state.clear()

@dp.callback_query(Form.confirmation, lambda callback: callback.data == "retry_request")
async def retry_request(callback_query: CallbackQuery, state: FSMContext):
    await state.clear() 
    await callback_query.message.edit_text("Начнём заново. Напишите своё имя:")
    await state.set_state(Form.request_name)

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