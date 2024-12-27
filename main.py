from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import route as auth_route

app = FastAPI()

origins = [
    "http://172.20.10.2:5173",  # Разрешить фронтенд на этом домене
    # "https://your-production-frontend.com",  # Разрешить продакшен-домен
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)


app.include_router(auth_route, prefix="/auth")
