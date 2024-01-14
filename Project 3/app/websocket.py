from fastapi import FastAPI,WebSocket
import websockets

app=FastAPI()

@app.websocket("/ws")
async def websocket(websocket:WebSocket):
    await websocket.accept()
    while True:
        data=await websocket.receive.text()
        await websocket._send(f"Message text was  {data")
