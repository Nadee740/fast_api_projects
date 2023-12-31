from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,database,model
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

oauth2_schema=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556uc818166b7a9563b93f70978384384aa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    jwt_token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return jwt_token

def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data=schemas.TokenData(id=id)
    
    except JWTError:
        raise credential_exception
    
    return token_data

def get_current_user(token:str=Depends(oauth2_schema),db:Session=Depends(database.get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credential",headers={"WWW-Authenticate":"Bearer"})

    token= verify_access_token(token,credential_exception)
    user=db.query(model.User).filter(model.User.id==token.id).first()
    return user

