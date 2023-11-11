from jose import jwt,JWTError
from datetime import datetime,timedelta
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from . import schema,database,models
from sqlalchemy.orm import Session
oauth2_schema=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d2bus5e094faarouting6ca2556uc818166b7a9563b93f70978384384aa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get('user_id')
        if id is None:
            raise credential_exception
        token_data=schema.TokenData(id=str(id))
    except JWTError:
        raise credential_exception
    return token_data

def get_current_user(token:str=Depends(oauth2_schema),db:Session=Depends(database.get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token=verify_access_token(token,credential_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    return user