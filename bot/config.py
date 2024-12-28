from decouple import config

TOKEN = config('TOKEN')
API_URL = 'http://localhost:8000/auth/register'
API_URL_REQUEST = 'http://localhost:8000/auth/request'

