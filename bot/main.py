from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from settings.fsm import Form
from api import *
from config import *
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from settings.button import *
from aiogram import F
from config import TOKEN 
import asyncio
import re
from datetime import datetime


bot = Bot(token=TOKEN)
dp = Dispatcher()

# Старт
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Form.select)
    await message.answer(text="Привет! Это клининговый сервис TAZA! Узнать больше - /info",
                         reply_markup=keyboard)

    telegram_id = message.from_user.id
    username = message.from_user.username

    response = (
        f"tg_id: {telegram_id}\n"
        f"tg_username: {username}"
    )
    print(response)

    result = await get_and_send_user_data(username=username, telegram_id=telegram_id, state=state)

    if result:
        print("Данные успешно отправлены")
    else:
        print("Ошибка при обработке данных")

@dp.callback_query(F.data == "button1") 
async def create_request(callback_query: CallbackQuery, state: FSMContext):
    print("Кнопка нажата: button1")
    await state.set_state(Form.request_name) 
    await callback_query.message.answer("Напишите свое имя:")

@dp.message(Form.request_name)
async def send_name(message: Message, state: FSMContext):
    name_user = message.text.strip()
    user_name = name_user.split()
    if len(user_name) < 2:
        await message.answer("Пожалуйста, введите и имя, и фамилию.")
        return
    await state.update_data({"first_name": user_name[0], "last_name": user_name[1]})
    await state.set_state(Form.phone_number)
    await message.answer("Напишите номер телефона:")

@dp.message(Form.phone_number)
async def send_phone_number(message: Message, state: FSMContext):
    number = message.text.strip()

    phone_pattern = re.compile(r"^\+?\d{10,15}$")
    
    if not phone_pattern.match(number):
        await message.answer(
            "Пожалуйста, введите корректный номер телефона. "
            "Пример: +77769814746 или 87058880457"
        )
        return
    
    await state.update_data(phone_number=number)  
    await state.set_state(Form.object_type)  
    await message.answer("Теперь выберите свой тип объекта", reply_markup=keyboard2)

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

    state_data = await state.get_data()
    access_token = state_data.get("access_token")
    
    if not access_token:
        print("Ошибка: токен отсутствует. Попробуйте снова позже.")
        return

    url = "http://localhost:8000/auth/cities/"
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                city_list = await response.json()
                if city_list:
                    city_buttons = [
                        [KeyboardButton(text=city['city_name'])] for city in city_list
                    ]
                    city_keyboard = ReplyKeyboardMarkup(keyboard=city_buttons, resize_keyboard=True)
                    await callback_query.message.answer("Выберите город из списка:", reply_markup=city_keyboard)
                    await state.set_state(Form.city)
                else:
                    await callback_query.message.answer("Города не найдены. Попробуйте позже.")
            else:
                await callback_query.message.answer("Ошибка при получении списка городов. Попробуйте позже.")

@dp.message(Form.city) 
async def select_city(message: Message, state: FSMContext):
    selected_city = message.text.strip()
    if not selected_city:
        await message.answer("Пожалуйста, выберите или введите город.")
        return

    await state.update_data(name_city=selected_city)
    await state.set_state(Form.street)
    await message.answer(f"Вы выбрали город {selected_city}.\nТеперь напишите вашу улицу.")

@dp.message(Form.street)
async def send_city(message: Message, state: FSMContext):
    name_street = message.text.strip()

    street_pattern = re.compile(r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-\.]+$")

    if not street_pattern.match(name_street) or len(name_street) < 2:
        await message.answer(
            "Пожалуйста, введите корректное название улицы. "
            "Название должно содержать только буквы, цифры, пробелы или дефисы."
        )
        return
    
    await state.update_data(name_street=name_street)
    await state.set_state(Form.home)
    await message.answer("Напишите свой номер дома")

@dp.message(Form.home)
async def send_street(message: Message, state: FSMContext):
    name_home = message.text.strip()

    home_pattern = re.compile(r"^[0-9a-zA-Zа-яА-ЯёЁ\-\/]+$")

    if not home_pattern.match(name_home) or len(name_home) < 1:
        await message.answer(
            "Пожалуйста, введите корректный номер дома. "
            "Пример: 25, 25А, 25/1."
        )
        return
    
    await state.update_data(name_home=name_home)
    await state.set_state(Form.apartment)
    await message.answer("Напишите номер своей квартиры:")

@dp.message(Form.apartment)
async def send_apartment(message: Message, state: FSMContext):
    number_apartment = message.text.strip()

    apartment_pattern = re.compile(r"^[0-9a-zA-Zа-яА-Я\-]+$")

    if not apartment_pattern.match(number_apartment) or len(number_apartment) < 1:
        await message.answer(
            "Пожалуйста, введите корректный номер квартиры. "
            "Пример: 45, 45А, 101-2."
        )
        return
    
    await state.update_data(number_apartment=number_apartment)
    await state.set_state(Form.date_request)
    await message.answer("Напишите дату, в формате гг.мм.дд")

@dp.message(Form.date_request)
async def process_calendar(message: Message, state: FSMContext):
    selected_date = message.text.strip()
    try:
        date_object = datetime.strptime(selected_date, "%Y.%m.%d") 
        current_date = datetime.now()

        if date_object < current_date:
            await message.answer("Дата не может быть в прошлом. Пожалуйста, введите корректную дату.")
            return

    except ValueError:
        await message.answer("Пожалуйста, введите дату в правильном формате: гг.мм.дд. Пример: 2024.12.31")
        return

    await state.update_data(date_request=selected_date)
    data = await state.get_data()

    await message.answer(
        f"Ваши данные:\n"
        f"Фамилия: {data.get('first_name')}\n"
        f"Имя: {data.get('last_name')}\n"
        f"Номер телефона: {data.get('phone_number')}\n"
        f"Тип объекта: {data.get('object_type')}\n"
        f"Число комнат: {data.get('number_room')}\n"
        f"Тип уборки: {data.get('cleaning_type')}\n"
        f"Город: {data.get('name_city')}\n"
        f"Улица: {data.get('name_street')}\n"
        f"Дом: {data.get('name_home')}\n"
        f"Квартира: {data.get('number_apartment')}\n"
        f"Дата заявки: {data.get('date_request')}\n\n"
        f"Проверьте правильность данных. Если всё верно, подтвердите заявку.",
        reply_markup=confirm_keyboard
    )
    await state.set_state(Form.confirmation)

@dp.callback_query(Form.confirmation, lambda callback: callback.data == "confirm_request")
async def confirm_request(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    raw_date = data.get("date_request")  
    try:
        formatted_date = datetime.strptime(raw_date, "%Y.%m.%d").strftime("%Y-%m-%d")
    except ValueError:
        await callback_query.message.answer("Ошибка: дата указана в неверном формате. Используйте формат гггг.мм.дд.")
        return
    
    payload = {
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "number": data.get("phone_number"),
        "object_type": data.get("object_type"),
        "room_count": data.get("number_room"),
        "cleaning_type": data.get("cleaning_type"),
        "city": data.get("name_city"),
        "street": data.get("name_street"),
        "home": int(data.get("name_home")),
        "apartment": int(data.get("number_apartment")),
        "date": formatted_date 
    }

    access_token = data.get("access_token")
    if not access_token:
        await callback_query.message.answer("Ошибка: отсутствует токен. Попробуйте заново.")
        return

    async with aiohttp.ClientSession() as session:
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",  
                "Content-Type": "application/json" 
            }
            async with session.post(API_URL_REQUEST, json=payload, headers=headers) as response:
                if response.status == 200:  
                    result = await response.json()
                    print(f"Заявка успешно отправлена!\n\nОтвет сервера: {result}")
                    await callback_query.message.edit_text(f"Спасибо! Ваша заявка успешно отправлена. "
                                                           f"Ожидайте нашу команду для дальнейших инструкций."
                                                           f"Скорее всего вам придет Жандарбек👽 или Диляра👻")
                else:  
                    error_text = await response.text()
                    print(f"Произошла ошибка при отправке данных на сервер. {response.status}: {error_text}")
        except Exception as e:
            print(f"Ошибка при подключении к API: {e}")

    await state.clear()

@dp.callback_query(Form.confirmation, lambda callback: callback.data == "retry_request")
async def retry_request(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text("Начнём заново. Напишите своё имя:")
    await state.set_state(Form.request_name)

@dp.message(Command("info"))
async def info_command(message: Message):
    await message.answer(
        "🧹   Клининговый сервис TAZA\n\n"
        "Мы предлагаем профессиональные услуги уборки для вашего дома, офиса и других помещений.\n\n"
        "🎯 Наши преимущества:\n"
        "✔️ Профессиональная команда с опытом.\n"
        "✔️ Генеральная уборка, химчистка, уборка после ремонта.\n"
        "✔️ Индивидуальный подход к каждому клиенту.\n"
        "✔️ Только безопасные и экологичные моющие средства.\n"
        "✔️ Удобный выбор даты и времени уборки.\n\n"
        "📋    Как заказать услугу:\n"
        "1️⃣ Нажмите /start для начала работы с ботом.\n"
        "2️⃣ Заполните короткую анкету.\n"
        "3️⃣ Подтвердите заявку и ожидайте уборку в удобное для вас время!\n\n"
        "💡   TAZA — это ваш надежный помощник в чистоте! 😊\n"
        "🧼   Типы уборки:\n"
        "🔹 Поверхностная чистка — уборка поверхностей, включая вытирание пыли с мебели, столов, полок, уборка пола и общая поддержка чистоты.\n"
        "🔹 Средняя чистка — включает поверхностную чистку плюс более тщательная уборка санузлов, кухни, подоконников и других труднодоступных мест.\n"
        "🔹 Максимальная чистка — полный спектр уборочных услуг, включая генеральную уборку, очистку всех поверхностей, окон, углов и т.д. Обработка всех участков вашего помещения для достижения максимальной чистоты."
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())