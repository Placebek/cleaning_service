import asyncio
import websockets


WEBSOCKET_URL="ws://http://172.20.10.8:8000/ws"

async def websocket_listener():
    async with websockets.connect(WEBSOCKET_URL) as websocket: 
        print("Websocket подключен")
        while True:
            try:
                message = await websocket.recv()
                print(f"Message from WebSocket: {message}")

            except Exception as e:
                print(f"Webscoket error {e}")
                await asyncio.sleep(5)
