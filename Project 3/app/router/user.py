from fastapi import FastAPI,APIRouter
from fastapi import FastAPI,HTTPException,Response,Request,status,Depends
from sqlalchemy.orm import Session
from .. import schema,utils,models,oauth2
from ..database import get_db
from typing import List

router=APIRouter(
    prefix="/user",
    tags=['User']
)

@router.get("/",response_model=List[schema.UserResponse])
def get_all_users(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    users=db.query(models.User)
    return users


@router.post("/")
async def add_user(user:schema.UserCreate,db:Session=Depends(get_db)):
    try:
        user.password=utils.hash(user.password)
        new_user=models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        access_token=oauth2.create_access_token(data={"user_id":new_user.id})
        db.refresh(new_user)
        return {"data":new_user,"token":access_token,"type":"bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Already registered email ")
