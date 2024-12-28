import asyncio

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import event

from app.router import route as auth_route
from model.model import Request
# from router import route as ws_route


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

@app.websocket("/ws/start")
async def websocket_endpoint(websocket: WebSocket):
    flag = asyncio.Event()
    @event.listens_for(Request, "after_insert")
    def measurement_stream(*args, **kwargs):
        flag.set()
        print("event set")

    await websocket.accept()
    await websocket.send_json({
        "asd": "asd"
    })
    while True:
        print("QWEQWEQEEWEQEEEQE")
        await flag.wait()
        # data = await websocket.receive_text()
        # print(data)
        await websocket.send_json({
            "qwe": "qwe"
        })
        flag.clear()
