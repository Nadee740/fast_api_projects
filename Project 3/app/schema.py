from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None

class BusCreate(BaseModel):
    bus_name:str

class Bus(BaseModel):
    bus_id:int
    bus_name:str
    owner_id:int

class StopCreate(BaseModel):
    stop_name:str

class Stop(BaseModel):
    stop_id:int
    stop_name:str
    is_active:bool
    created_at:datetime
    created_user_id:int


class BusRoute(BaseModel):
    bus_id:int
    stop_id:int
    time:datetime

    
