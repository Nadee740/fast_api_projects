from fastapi import APIRouter,Response,status,Depends,HTTPException
from sqlalchemy.orm import Session
from .. import database,schema,models,utils,oauth2
from typing import List
router=APIRouter(prefix="/stops")

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_stop(stop:schema.StopCreate,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    try:
        create_stop=models.Stop(created_user_id=current_user.id,**stop.model_dump())
        db.add(create_stop)
        db.commit()
        db.refresh(create_stop)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{e}")
    
    return create_stop

@router.get("/",response_model=List[schema.Stop])
async def get_all_stops(db:Session=Depends(database.get_db)):
    try:
        stops= db.query(models.Stop).all()
        print(stops[0].dumps())
        return stops 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,detail=f"something went wrong")
    