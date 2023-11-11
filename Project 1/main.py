from fastapi import FastAPI,Body,Depends
import schemas
import models
from database import Base,engine,SessionLocal
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
Base.metadata.create_all(engine)

def get_session():
    session=SessionLocal()
    try:
        yield session
    finally:
        session.close()

app=FastAPI()

try:
    con=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='11092002',cursor_factory=RealDictCursor)
    cursor=con.cursor()
    print("database connected")
except Exception as error:
    print(f"{error}")
    

fakeDatabase={
    1:{'task':"Clean a"},
    2:{'task':"Clean b"},
    3:{'task':"Clean c"},
}

@app.get("/")
def getItems(session:Session=Depends(get_session)):
    items=session.query(models.Item).all()
    return items
@app.get("/{id}")
def getItem(id:int,session:Session=Depends(get_session)):
    item=session.query(models.Item).get(id)
    return item

@app.post("/")
def addItem(item:schemas.Item,session:Session=Depends(get_session)):
    item=models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


# @app.post("/")
# def addItem(body=Body()):
#     newId=len(fakeDatabase.keys())+1
#     fakeDatabase[newId]={"task":body['task']}
#     return fakeDatabase

@app.put("/{id}")
def updateItem(id:int,item:schemas.Item,session:Session=Depends(get_session)):
    itemobject=session.query(models.Item).get(id)
    itemobject.task=item.task
    session.commit()
    return itemobject
@app.delete("/{id}")
def deleteItem(id:int,session:Session=Depends(get_session)):
    itemObject=session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item Deleted'

