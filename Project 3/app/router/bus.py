from fastapi import APIRouter,Response,status,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from .. import database,schema,models,utils,oauth2
from typing import List
router=APIRouter(prefix="/bus")

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_bus(bus:schema.BusCreate,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    try:
        create_bus=models.Bus(owner_id=current_user.id,**bus.model_dump())
        db.add(create_bus)
        db.commit()
        db.refresh(create_bus)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{e}")
    
    return create_bus

@router.get("/")
async def get_all_bus(db:Session=Depends(database.get_db)):
    try:
        response=[]
        results = db.query(models.Bus).outerjoin(models.User, models.Bus.owner_id == models.User.id).all()
        # print(user)
        print(**results[0].model_dump())
        # return results
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,detail=f"something went wrong {e}")
    
@router.post("/add-bus-route")
def add_bus_route(busroute:schema.BusRoute,db:Session=Depends(database.get_db)):
    try:
        bus_route=models.BusRoute(**busroute.model_dump())
        db.add(bus_route)
        db.commit()
        db.refresh(bus_route)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Something went wrong {e}")
    
    return bus_route
@router.get("/get-bus-id")
async def get_bus_by_id(db:Session=Depends(database.get_db)):
    try:
         bus_routes=db.query(models.Stop).filter(models.Stop.stop_id==5).first()
         return bus_routes
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
@router.get("/get-bus-routes",response_model=List[schema.BusRoute])
async def get_all_bus_routes(db:Session=Depends(database.get_db)):
    try:
        bus_routes=db.query(models.BusRoute)
        return bus_routes
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,detail=f"something went wrong {e}")
    

@router.get("/find-bus",response_model=List[schema.BusRoute])
async def get_all_bus_routes(start:int,end:int,db:Session=Depends(database.get_db)):
    try:
        query=text("select s.bus_id,s.stop_id,s.time from bus_routes s join bus_routes d on s.bus_id=d.bus_id where s.stop_id=:start and d.stop_id=:end and s.time <d.time order by d.time")
        params={"start":start,"end":end}
        results=db.execute(query,params).all()
        if len(results) is 0:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"No bus found")
        # for bus in results:
        #     res.append({"bus":bus})
        return results
        # results=db.query(models.BusRoute,models.Bus).join(models.Bus,models.Bus.bus_id==models.BusRoute.bus_id).all()
        # res=[]
        # for route,bus in results:
        #     res.append({"route":route,"bus":bus})
        # return res
        # return bus_routes
        # bus_routes=db.query(models.BusRoute).filter()
    except HTTPException as e:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No bus found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,detail=f"something went wrong {e}")
    


    

    