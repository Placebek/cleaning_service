import asyncio
import requests
from decouple import config
from aiogram.filters import Command, CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import aiohttp
from api import FastAPIUser


TOKEN=config('TOKEN')
bot = Bot(token=TOKEN)
dp=Dispatcher()
URL='...'
fastapi_client = FastAPIUser(url=URL)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Сәлем! Бұл JAKEBEKOV клининг сервисі.")

    telegram_id = message.from_user.id
    username = message.from_user.username

    response = (
        f"telegram_id: {telegram_id}"
        f"username: {username}"
    )
    await message.answer(response)

    tokens = fastapi_client.get_jwt_token(username=username, telegram_id=telegram_id)

    if tokens:
        access_token = tokens.get("access")
    else:
        await message.answer("Токенді ала алмадық")
        return
    
    result = fastapi_client.send_user_data(
        username=username,
        telegram_id=telegram_id,
        access_token=access_token
    )

    if result:
        await message.answer("Деректер кетті")
    else:
        await message.answer("деректерде жіберуде қате кетті")

    
async def main():
    await dp.start_polling(bot)

asyncio.run(main())
