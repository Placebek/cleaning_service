import aiohttp
from config import API_URL
from aiogram.fsm.context import FSMContext


async def get_and_send_user_data(username: str, telegram_id: int, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        payload = {
            "tg_username": username,
            "tg_id": telegram_id,
        }
        
        async with session.post(API_URL, json=payload) as response:
            if response.status == 200:
                tokens = await response.json()
                access_token = tokens.get("access_token")
                access_token_expire_time = tokens.get("access_token_expire_time")
                
                if access_token:
                    await state.update_data(access_token=access_token, access_token_expire_time=access_token_expire_time)
                    
                    headers = {"Authorization": f"Bearer {access_token}"}
                    payload = {
                        "tg_username": username,
                        "tg_id": telegram_id,
                    }
                    
                    async with session.post(API_URL, json=payload, headers=headers) as send_response:
                        if send_response.status == 200:
                            print("Данные успешно отправлены на сервер")
                            return True
                        else:
                            print(f"Ошибка при отправке данных: {send_response.status}")
                            return False
                else:
                    print("Не удалось получить access_token")
                    return False
            else:
                print(f"Ошибка при получении токена: {response.status}")
                return False
