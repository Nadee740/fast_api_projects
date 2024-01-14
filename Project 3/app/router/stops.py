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
@router.get("/stop-by-id")
async def get_stop_id(db:Session=Depends(database.get_db)):
    stop=db.query(models.Stop).filter(models.Stop.stop_id==5).first()
    associated_bus_routes = stop.bus_routes

# Print or use the associated bus routes
    for bus_route in associated_bus_routes:
        print(f"Bus ID: {bus_route.bus_id}, Time: {bus_route.time}")
        print(stop)
    return stop
@router.get("/",response_model=List[schema.Stop])
async def get_all_stops(db:Session=Depends(database.get_db)):
    try:
        stops= db.query(models.Stop).all()
        return stops 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,detail=f"something went wrong")
    