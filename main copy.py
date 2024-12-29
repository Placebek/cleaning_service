


from fastapi import FastAPI, WebSocket

app = FastAPI()


# @app.get("/")
# def root():
#     return {"msg":"welcome"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:

        data = await websocket.receive_text()
        await websocket.send_text(f"{data}")