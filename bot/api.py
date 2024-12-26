import requests

URL='...'

class FastAPIUser:
    def __init__(self, url):
        self.url = url

    def get_jwt_token(self, username, telegram_id):
        api = f'{self.url}/api/'
        data = {
            'username': username,
            'telegram_id': telegram_id
        }

        try:
            response = requests.post(api, json=data)
            response.raise_for_status()
            return response.json().get('tokens')
        except requests.exceptions.RequestException as e:
            print(f"Токенді ала алмадық: {e}")
            return None
        
    def send_user_data(self, username, telegram_id, access_token):
        api = f'{self.url}/api/'
        data = {
            'username': username,
            'telegram_id': telegram_id
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        