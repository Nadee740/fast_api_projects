from fastapi import FastAPI
from . import model
from .database import engine  
from .routers import users,posts,auth

model.Base.metadata.create_all(bind=engine)
app=FastAPI() 

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)









                                                                                                                                                 