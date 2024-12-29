from fastapi import  WebSocket
from typing import List


class WebsocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, data):
        print('waaiiiittt', self.active_connections)
        for connection in self.active_connections:
            try:
                list_data = [dict(i) for i in data]
                print('www', list_data,)
                await connection.send_json(list_data)
            except Exception as e:
                print(f"Broadcast failed for {connection}: {e}")
                self.disconnect(connection)
            
manager = WebsocketManager()

        
        