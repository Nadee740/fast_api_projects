from fastapi import FastAPI,HTTPException,Response,Request,status
from . import schema,utils
from  .router import user,auth,stops,bus
app=FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(stops.router)
app.include_router(bus.router)

@app.get("/")
def index():
    return {"msg":"App is live"}





