from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model
from . import schemas,utils


SQL_ALCHEMY_DATABASE_URL='postgresql://postgres:11092002@localhost/fastapi'

engine=create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        con=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='11092002',cursor_factory=RealDictCursor)
        cursor=con.cursor()
        print("database connected")
        break
    except Exception as error:
        print(f"{error}")
        time.sleep(2)



