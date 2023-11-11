from .. import model,schemas,utils
from fastapi import status,Response,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
router=APIRouter(prefix='/user')
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_usere(user:schemas.UserCreate,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=schemas.UserOut)
def get_user_by_id(id:int,db:Session=Depends(get_db)):
    user=db.query(model.User).filter(model.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with {id} is not found")
    return user