from fastapi import APIRouter,Response,status,Depends,HTTPException
from sqlalchemy.orm import Session
from .. import database,schema,models,utils,oauth2
from typing import List
router=APIRouter(prefix="/bus")

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_post(bus:schema.BusCreate,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    try:
        create_bus=models.Bus(owner_id=current_user.id,**bus.model_dump())
        db.add(create_bus)
        db.commit()
        db.refresh(create_bus)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{e}")
    
    return create_bus

@router.get("/",response_model=List[schema.Bus])
async def get_all_bus(db:Session=Depends(database.get_db)):
    try:
        buses=db.query(models.Bus)
        return buses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,detail=f"something went wrong {e}")
    

    