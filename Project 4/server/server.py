from fastapi import FastAPI,WebSocket
import geocoder
import asyncio
from geopy.geocoders import Nominatim
app=FastAPI()

@app.get("/get-location")
def get_current_location():
    # Create a geolocator object
    try:
        print('hy')
        g = geocoder.ip('me') 
        lat=str(g.latlng[0])
        long=str(g.latlng[1])
        # geolocator = Nominatim(user_agent="geoapiExercises")
        
        # location = geolocator.reverse(lat+","+long)
        # print(location)
    except Exception as e:
        print(e)
 
# # Display
#     print(location)
   
    # print(g.latlng)
      

@app.websocket("/ws")
async def websocket(websocket:WebSocket):
    data=0
    await websocket.accept()
    while True:
        try:
            data=data+5
            data=await websocket.receive_json()
            print(data)
        except Exception as e:
            print(e)
            break

