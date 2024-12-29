
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.router import route as auth_route
# from router import route as ws_route
from app.api.auth.commands.auth_user_crud import flag

app = FastAPI()

origins = [
    "http://192.168.193.31:5173",  # Разрешить фронтенд на этом домене
    "http://172.20.10.2:5173",
    "http://localhost:5173",
    "http://146.0.60.15:5173" ,
    # Разрешить фронтенд на этом домене
       
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






# @app.websocket("/ws/start")
# async def websocket_endpoint(websocket: WebSocket):
#     # flag = asyncio.Event()
#     @event.listens_for(Request, "after_insert")
#     def measurement_stream(*args, **kwargs):
#         flag.set()
#         print("event set")

#     await manager.connect(websocket)
#     await manager.broadcast({
#         "asd": "asd"
#     })
#     while True:
#         print("QWEQWEQEEWEQEEEQE")
#         await flag.wait()
#         await manager.broadcast({
#             "qwe": "qwe"
#         })
#         flag.clear()
