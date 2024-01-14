import asyncio
import websockets
import geocoder
import asyncio
import json

async def connect_to_websocket():
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
       while True:
            try:
                g = geocoder.ip('me') 
                lat=str(g.latlng[0])
                long=str(g.latlng[1])
                data={"lat":lat,"long":long}
                json_string = json.dumps(data)
                await websocket.send(json_string)
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosedError as e:
                print(e)
                print("server close connection")
                break
                

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect_to_websocket())
